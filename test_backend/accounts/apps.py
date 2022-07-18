from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

    def ready(self):
        from polaris.integrations import register_integrations
        from .integrations import (
            MyDepositIntegration,
            MyWithdrawalIntegration,
            MyCustomerIntegration,
            MySEP31ReceiverIntegration,
            MyRailsIntegration,
            toml_integration,
            scripts_integration,
            fee_integration,
            info_integration,
        )

        register_integrations(
            deposit=MyDepositIntegration(),
            withdrawal=MyWithdrawalIntegration(),
            toml=toml_integration,
            fee=fee_integration,
            sep6_info=info_integration,
            customer=MyCustomerIntegration(),
            sep31_receiver=MySEP31ReceiverIntegration(),
            rails=MyRailsIntegration(),
        )
