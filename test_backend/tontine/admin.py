from django.apps import apps
from django.contrib import admin

from accounts.models import User, PolarisUser, PolarisStellarAccount, PolarisUserTransaction
from .models import Tontine, TontineWallet, TontineRound, TontineRules, Penalty, Package, Subscription, CustomFrequency, \
    Rule


class ListAdminMixin(object):
    def __init__(self, model, admin_site):
        self.list_display = [field.name for field in model._meta.fields]
        super(ListAdminMixin, self).__init__(model, admin_site)


models = apps.get_models()
for model in models:
    admin_class = type('AdminClass', (ListAdminMixin, admin.ModelAdmin), {})
    try:
        if model not in [User, PolarisUser, PolarisStellarAccount, PolarisUserTransaction]:
            admin.site.register(model, admin_class)
    except admin.sites.AlreadyRegistered:
        pass
