from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import User
import uuid as generateUUID
from uuid import uuid4
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import MinLengthValidator

from polaris.models import Transaction


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """User model."""
    USER_TYPES = (
        ('admin', 'Admin'),
        ('member', 'Member'),
        ('participant', 'Participant'),
    )
    username = None
    is_active = models.BooleanField(_('active'), default=True)
    is_subscribed = models.BooleanField(default=False)
    email = models.EmailField(_('email address'), unique=True)
    nickname = models.CharField(max_length=60, blank=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    user_type = models.CharField(_('user type'), max_length=60, choices=USER_TYPES, default="participant")

    avatar = models.ImageField(
        upload_to='avatars/', null=True, blank=True)
    unique_id = models.UUIDField(
        unique=True, default=generateUUID.uuid4, editable=False)
    locale = models.CharField(_('locale'), max_length=3, blank=True)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        return self.first_name

    def get_nickname(self):
        '''
        Returns the short name for the user.
        '''
        return self.email.split('@')[0]

    def email_user(self, subject, message, from_email=None, **kwargs):
        '''
        Sends an email to this User.
        '''
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def save(self, *args, **kwargs):
        self.nickname = self.email.split('@')[0]
        super(User, self).save(*args, **kwargs)


class UserProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="profile")

    websiteUrl = models.URLField(blank=True, null=True)
    facebookUrl = models.URLField(blank=True, null=True)
    twitterUrl = models.URLField(blank=True, null=True)
    telegramUrl = models.URLField(blank=True, null=True)
    linkedinUrl = models.URLField(blank=True, null=True)
    youtubeUrl = models.URLField(blank=True, null=True)

    date_joined = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        try:
            return self.user.email
        except:
            return None


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
        print('Profile for user {} has been created.'.format(instance.nickname))


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    print('Profile for user {} has been saved.'.format(instance.nickname))
    instance.profile.save()


def get_new_token():
    return str(uuid4())


class PolarisUser(models.Model):
    tontine_user = models.OneToOneField(User, on_delete=models.CASCADE)

    bank_account_number = models.CharField(max_length=254, null=True)
    bank_number = models.CharField(max_length=254, null=True)

    objects = models.Manager()

    @property
    def name(self):
        return " ".join([str(self.tontine_user.first_name), str(self.tontine_user.last_name)])

    def __str__(self):
        return f"{self.name} ({self.id})"


class PolarisStellarAccount(models.Model):
    user = models.ForeignKey(PolarisUser, on_delete=models.CASCADE)
    memo = models.TextField(null=True, blank=True)
    memo_type = models.TextField(null=True, blank=True)
    account = models.CharField(max_length=56, validators=[MinLengthValidator(56)])
    confirmed = models.BooleanField(default=False)
    confirmation_token = models.CharField(max_length=36, default=get_new_token)

    objects = models.Manager()

    class Meta:
        unique_together = ["memo", "account"]

    def __str__(self):
        return f"{str(self.user)}: {str(self.account)} - {str(self.memo)}"


class PolarisUserTransaction(models.Model):
    """
    Since we cannot add a PolarisStellarAccount foreign key to :class:`Transaction`,
    this table serves to join the two entities.
    """

    transaction_id = models.TextField(db_index=True)
    user = models.ForeignKey(PolarisUser, on_delete=models.CASCADE, null=True)
    account = models.ForeignKey(
        PolarisStellarAccount, on_delete=models.CASCADE, null=True
    )

    @property
    def transaction(self):
        return Transaction.objects.filter(id=self.transaction_id).first()

    objects = models.Manager()

    def __str__(self):
        return f"{str(self.account)}: {str(self.transaction)}"
