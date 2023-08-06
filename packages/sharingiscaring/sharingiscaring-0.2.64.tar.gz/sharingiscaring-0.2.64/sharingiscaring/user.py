import json
import os
from dateutil.relativedelta import relativedelta

from .GRPCClient import GRPCClient
from .mongodb import MongoDB, Collections, MongoTypeInvolvedAccount
from enum import Enum
import datetime as dt
import dateutil.parser
from datetime import timezone
from rich.console import Console

console = Console()


class UserReminderStatus(Enum):
    NO_NEED = -1  # there is no need to remind. The bot has plenty of credits
    RUNNING_OUT_IN_2_DAYS = 0  #
    OUT_OF_CREDITS_1 = 1
    OUT_OF_CREDITS_2 = 2
    OUT_OF_CREDITS_3 = 3
    NOT_RESPONDING = 4


class SubscriptionDetails(Enum):
    EXPLORER_CCD = os.environ.get(
        "EXPLORER_CCD", "3cunMsEt2M3o9Rwgs2pNdsCWZKB5MkhcVbQheFHrvjjcRLSoGP"
    )
    BAKER_ID = int(os.environ.get("BAKER_ID", 72723))

    SUBSCRIPTION_ONE_TIME_FEE = int(os.environ.get("SUBSCRIPTION_ONE_TIME_FEE", 1000))
    SUBSCRIPTION_DELEGATION_FEE = int(os.environ.get("SUBSCRIPTION_DELEGATION_FEE", 1))
    SUBSCRIPTION_MESSAGE_CREDITS_IN_FEE = int(
        os.environ.get("SUBSCRIPTION_MESSAGE_CREDITS_IN_FEE", 50)
    )
    SUBSCRIPTION_WARN_HOURS_BEFORE = int(
        os.environ.get("SUBSCRIPTION_WARN_HOURS_BEFORE", 48)
    )
    SUBSCRIPTION_MESSAGE_FEE = int(os.environ.get("SUBSCRIPTION_MESSAGE_FEE", 1))
    SUBSCRIPTION_UNLIMITED = int(os.environ.get("SUBSCRIPTION_UNLIMITED", 5000))
    SUBSCRIPTION_DELEGATOR_STAKE_LIMIT = int(
        os.environ.get("SUBSCRIPTION_DELEGATOR_STAKE_LIMIT", 100_000)
    )
    SUBSCRIPTION_PLAN_START_DATE = dateutil.parser.parse(
        os.environ.get("SUBSCRIPTION_PLAN_START_DATE", "2022-12-01 01:00:00")
    ).astimezone(timezone.utc)


class SubscriptionPlans(Enum):
    PLUS = "Plus"
    DELEGATION = "Delegation"
    UNLIMITED = "Unlimited"
    NO_PLAN = "No Plan"


class Subscription:
    def __init__(self):
        self.start_date = None
        self.payment_transactions = []
        self.subscription_active = (
            False  # If True, the user has paid enough to pay for one-time fee
        )
        self.delegator_active = False  # If True, the user has paid any amount from an account that is an active delegator
        self.site_active = False  # This is the indicator that a user can use the site
        self.bot_active = False  # If True, the user has paid enough to cover the one-time fee and sent messages

        self.unlimited = (
            False  # If True, the user has paid enough for subscription_unlimited
        )
        # unlimited credits
        self.unlimited_end_date = None
        self.remaining_message_credits = 0
        self.count_messages = 0
        self.paid_amount = 0
        self.messages_per_hour = 0
        self.plan = SubscriptionPlans.NO_PLAN


class User:
    def __init__(self):
        self.bakers_to_follow = []
        self.tags = {}
        self.explorer_ccd_transactions = []
        self.explorer_ccd_delegators = []
        self.token = "x" * 10
        self.subscription = Subscription()
        self.last_refreshed_for_user = None

    def add_user_from_telegram(self, user):
        self.first_name = user.first_name
        self.username = user.username
        self.chat_id = user.id
        self.language_code = user.language_code
        return self

    def read_user_from_git(self, user):
        # Testing is enabled through a parameters in pytest tests
        self.testing = user.get("testing", False)
        self.bakers_to_follow = user.get("bakers_to_follow", [])
        self.chat_id = user.get("chat_id", None)
        self.token = user.get("token", None)
        self.first_name = user.get("first_name", None)
        self.username = user.get("username", None)
        self.accounts_to_follow = user.get("accounts_to_follow", [])
        self.labels = user.get("labels", None)
        self.transactions_downloaded = user.get("transactions_downloaded", {})
        self.transaction_limit_notifier = user.get("transaction_limit_notifier", -1)
        self.transaction_limit_notifier_to_exchange_only = user.get(
            "transaction_limit_notifier_to_exchange_only", False
        )
        self.unstake_limit_notifier = user.get("unstake_limit_notifier", -1)
        self.smart_init = user.get("smart_init", False)
        self.smart_update = user.get("smart_update", False)
        self.cns_domain = user.get("cns_domain", False)
        self.nodes = user.get("nodes", {})
        # self.subscription                   = Subscription()
        return self

    def prepare_for_subscription_logic(
        self,
        mongodb: MongoDB,
        grpcclient: GRPCClient,
        txs_as_receiver: list[MongoTypeInvolvedAccount] = None,
        explorer_ccd_delegators: dict = None,
    ):
        grpcclient.switch_to_net("mainnet")
        if not txs_as_receiver:
            console.log("Need to get explorer transactions...")
            self.get_explorer_transactions(mongodb, grpcclient)
        else:
            self.explorer_ccd_transactions = txs_as_receiver

        if not explorer_ccd_delegators:
            console.log("Need to get explorer delegators...")
            self.get_explorer_delegators(grpcclient)
        else:
            self.explorer_ccd_delegators = explorer_ccd_delegators
        self.last_refreshed_for_user = dt.datetime.utcnow()

    def get_explorer_transactions(self, mongodb: MongoDB, grpcclient: GRPCClient):
        try:
            pipeline = mongodb.search_txs_hashes_for_account_as_receiver_with_params(
                SubscriptionDetails.EXPLORER_CCD.value, 0, 1_000_000_000
            )
            txs_as_receiver = [
                MongoTypeInvolvedAccount(**x)
                for x in mongodb.mainnet[
                    Collections.involved_accounts_transfer
                ].aggregate(pipeline)
            ]

            self.explorer_ccd_transactions = txs_as_receiver
        except:
            self.explorer_ccd_transactions = []

    def get_explorer_delegators(self, grpcclient: GRPCClient):
        try:
            explorer_ccd_delegators = grpcclient.get_delegators_for_pool(
                SubscriptionDetails.BAKER_ID.value, "last_final"
            )

            # keyed on accountAddress
            self.explorer_ccd_delegators = {
                x.account: x for x in explorer_ccd_delegators
            }
        except:
            self.explorer_ccd_delegators = []

    def set_count_messages(self, mongodb: MongoDB, ENVIRONMENT: str):
        # get count of messages sent to this user
        # only count from subscription.start_date
        if self.subscription.start_date:
            try:
                pipeline = mongodb.get_bot_messages_for_user(
                    self, ENVIRONMENT, self.subscription.start_date
                )
                result = list(
                    mongodb.mainnet[Collections.bot_messages].aggregate(pipeline)
                )

                self.subscription.count_messages = 0
                if len(result) > 0:
                    if "count_messages" in result[0]:
                        self.subscription.count_messages = result[0]["count_messages"]

            except:
                pass

    def perform_subscription_logic(self, grpcclient: GRPCClient):
        grpcclient.switch_to_net("mainnet")
        payment_memo = self.token[:6]

        # check if the right memo is set, if so, count towards user.
        payment_txs = []
        paid_amount = 0
        SUBSCRIPTION_ONE_TIME_FEE_set = False
        ACTIVE_DELEGATOR_set = False

        for concordium_tx in self.explorer_ccd_transactions:
            if concordium_tx.memo:
                if payment_memo in concordium_tx.memo:
                    slot_time = grpcclient.get_finalized_block_at_height(
                        concordium_tx.block_height
                    ).slot_time

                    paid_amount += concordium_tx.amount / 1_000_000

                    # Is this sender a current active delegator?
                    if not ACTIVE_DELEGATOR_set:
                        if concordium_tx.sender in self.explorer_ccd_delegators:
                            sender_delegated_stake = (
                                self.explorer_ccd_delegators[concordium_tx.sender].stake
                                / 1_000_000
                            )
                            self.subscription.delegator_active = (
                                sender_delegated_stake
                                >= SubscriptionDetails.SUBSCRIPTION_DELEGATOR_STAKE_LIMIT.value
                            )

                            # Make sure that multiple transactions to not UNset this if later transactions make this invalid.
                            if self.subscription.delegator_active:
                                ACTIVE_DELEGATOR_set = True
                                self.subscription.plan = SubscriptionPlans.DELEGATION

                                # some users have purchased before the official start date.
                                self.subscription.start_date = max(
                                    SubscriptionDetails.SUBSCRIPTION_PLAN_START_DATE.value,
                                    slot_time,
                                )

                    # Has the user paid the one time fee? If so, record the subscription start date
                    if not SUBSCRIPTION_ONE_TIME_FEE_set:
                        self.subscription.subscription_active = (
                            paid_amount
                            >= SubscriptionDetails.SUBSCRIPTION_ONE_TIME_FEE.value
                        )

                        # Make sure that multiple transactions to not UNset this if later transactions make this invalid.
                        if self.subscription.subscription_active:
                            SUBSCRIPTION_ONE_TIME_FEE_set = True
                            self.subscription.plan = SubscriptionPlans.PLUS

                            # some users have purchased before the official start date.
                            self.subscription.start_date = max(
                                SubscriptionDetails.SUBSCRIPTION_PLAN_START_DATE.value,
                                slot_time,
                            )

                    # Has the user paid enough for unlimited? If so, record the unlimited end date
                    self.subscription.unlimited = (
                        paid_amount >= SubscriptionDetails.SUBSCRIPTION_UNLIMITED.value
                    )
                    if self.subscription.unlimited:
                        self.subscription.plan = SubscriptionPlans.UNLIMITED
                        self.subscription.unlimited_end_date = (
                            slot_time + relativedelta(years=1)
                        )
                        # if isinstance(
                        #     concordium_tx.block["blockSlotTime"], dt.datetime
                        # ):
                        #     self.subscription.unlimited_end_date = concordium_tx.block[
                        #         "blockSlotTime"
                        #     ] + relativedelta(years=1)
                        # else:
                        #     self.subscription.unlimited_end_date = (
                        #         dateutil.parser.parse(
                        #             concordium_tx.block["blockSlotTime"]
                        #         )
                        #         + relativedelta(years=1)
                        #     )
                    payment_txs.append(concordium_tx)

        self.subscription.payment_transactions = payment_txs
        self.subscription.paid_amount = paid_amount

        # This is the indicator that a user can use the site.
        self.subscription.site_active = (
            self.subscription.delegator_active or self.subscription.subscription_active
        )

        # exclude me
        if self.token == "e2410784-fde1-11ec-a3b9-de5c44736176":
            self.subscription.bot_active = True
            self.subscription.site_active = True
            self.subscription.subscription_active = True
            self.subscription.unlimited = True
            self.subscription.unlimited_end_date = dt.datetime(
                2040, 4, 16, 23, 59, 59
            ).astimezone(timezone.utc)
            self.subscription.plan = SubscriptionPlans.UNLIMITED

    def determine_bot_status(self):
        # update remaining message credits
        FEE_TO_USE = (
            SubscriptionDetails.SUBSCRIPTION_DELEGATION_FEE
            if self.subscription.plan == SubscriptionPlans.DELEGATION
            else SubscriptionDetails.SUBSCRIPTION_ONE_TIME_FEE
        )
        self.subscription.remaining_message_credits = max(
            0,
            (self.subscription.paid_amount - FEE_TO_USE.value)
            / SubscriptionDetails.SUBSCRIPTION_MESSAGE_FEE.value
            - self.subscription.count_messages
            + SubscriptionDetails.SUBSCRIPTION_MESSAGE_CREDITS_IN_FEE.value,
        )

        # finally, determine if the bot is active
        if self.subscription.site_active:
            if self.subscription.remaining_message_credits > 0:
                self.subscription.bot_active = True
            else:
                self.subscription.bot_active = False

        if self.subscription.unlimited:
            self.subscription.bot_active = True

        if self.subscription.start_date:
            hours_plan_active = (
                dt.datetime.now().astimezone(timezone.utc)
                - self.subscription.start_date
            ).total_seconds() / (60 * 60)
            self.subscription.messages_per_hour = (
                self.subscription.count_messages / hours_plan_active
            )

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True)
