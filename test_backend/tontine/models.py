from django.core.validators import MinLengthValidator
from django.db import models
from accounts.models import User
from tontine.utils.utils import generate_tontine_name, validate_frequency_duration
from django.utils.translation import ugettext_lazy as _


class Package(models.Model):
    PACKAGE_TYPES = (
        ('bronze', 'BRONZE'),
        ('silver', 'SILVER'),
        ('gold', 'GOLD'),
    )
    name = models.CharField(max_length=255, choices=PACKAGE_TYPES, default='bronze', primary_key=True)
    point_accorded = models.IntegerField('Point accorded')
    description = models.TextField()
    price = models.DecimalField('Price of the package', max_digits=12, decimal_places=2)

    def __str__(self):
        return str(self.name) + " point: " + str(self.point_accorded)

    class Meta:
        db_table = "Package"
        verbose_name = _('Package')
        unique_together = [('name', 'point_accorded')]
        order_with_respect_to = 'point_accorded'


class Subscription(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=False, null=False)
    package = models.ForeignKey(Package, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user) + " is is subscribed to " + str(self.package)

    class Meta:
        db_table = "Subscription"
        verbose_name = _('Subscription')
        unique_together = [('user', 'package')]


FREQUENCIES = [
    (0, "DAILY"),
    (1, "WEEKLY"),
    (2, "MONTHLY"),
    (3, "YEAR")
]


class CustomFrequency(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
    custom_duration = models.IntegerField('Custom Number', validators=[validate_frequency_duration], default=1)
    type_frequency = models.IntegerField('Type Frequency', choices=FREQUENCIES)


class Tontine(models.Model):
    name = models.CharField('Name of Tontine', max_length=255, null=False,
                            default="tontine-" + generate_tontine_name())
    creator = models.OneToOneField(User, on_delete=models.CASCADE, null=False, blank=False)
    is_active = models.BooleanField(default=False)
    is_closed = models.BooleanField(default=False)
    description = models.TextField(null=True, blank=True)
    required_point = models.IntegerField("Required user point to access")
    max_allowed_member = models.IntegerField('Maximum Allowed Member')
    amount = models.IntegerField('Amount to pay each round')
    number_of_round = models.IntegerField('Number of rounds')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    default_frequency = models.IntegerField(choices=FREQUENCIES, default=2)
    custom_frequency = models.ForeignKey(CustomFrequency, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "Tontine"
        verbose_name = _('Tontine')
        order_with_respect_to = 'created_at'


class TontineWallet(models.Model):
    tontine = models.OneToOneField(Tontine, on_delete=models.CASCADE)
    wallet_pk = models.CharField('Stellar wallet of tontine public key', null=False, blank=False, max_length=56,
                                 validators=[MinLengthValidator(56)])
    wallet_sk = models.CharField('Stellar wallet of tontine secret key', null=False, blank=False, max_length=56,
                                 validators=[MinLengthValidator(56)])
    amount = models.DecimalField("Total amount", max_digits=20, decimal_places=2)

    def __str__(self):
        return "Wallet: " + str(self.wallet_pk)

    class Meta:
        db_table = "TontineWallet"


class Penalty(models.Model):
    PENALTIES_TYPE = (
        ('warning', 'WARNING'),
        ('punishment', "PUNISHMENT"),
        ('ban', 'BAN')
    )
    type = models.CharField('Penalty type', max_length=255, choices=PENALTIES_TYPE)
    amount_to_pay = models.DecimalField('Amount to pay', max_digits=10, decimal_places=2)

    def __str__(self):
        return "PENALTY: " + self.type

    class Meta:
        db_table = "Penalty"


class Rule(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    penalty = models.OneToOneField(Penalty, on_delete=models.CASCADE)

    def __str__(self):
        return "Rule:  L" + self.name

    class Meta:
        db_table = "Rule"


class TontineRules(models.Model):
    tontine = models.OneToOneField(Tontine, on_delete=models.CASCADE)
    rules = models.ManyToManyField(Rule)

    def __str__(self):
        return str(self.rules) + "are applied to " + str(self.tontine)

    class Meta:
        db_table = "TontineRules"


class TontineRound(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    recipient = models.ForeignKey(User, on_delete=models.CASCADE)
    tontine = models.ForeignKey(Tontine, on_delete=models.CASCADE)
    amount_out = models.DecimalField(max_digits=20, decimal_places=2)
    is_tx_successful = models.BooleanField(default=False)
    round_number = models.IntegerField(default=1)

    class Meta:
        db_table = "TontineRound"
        verbose_name = _("Tontine Round")
        unique_together = ('created_at', 'recipient', 'tontine')
        order_with_respect_to = 'created_at'
