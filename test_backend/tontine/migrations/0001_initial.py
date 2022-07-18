# Generated by Django 3.2.13 on 2022-07-08 18:22

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import tontine.utils.utils


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomFrequency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('custom_duration', models.IntegerField(default=1, validators=[tontine.utils.utils.validate_frequency_duration], verbose_name='Custom Number')),
                ('type_frequency', models.IntegerField(choices=[(0, 'DAILY'), (1, 'WEEKLY'), (2, 'MONTHLY'), (3, 'YEAR')], verbose_name='Type Frequency')),
            ],
        ),
        migrations.CreateModel(
            name='Package',
            fields=[
                ('name', models.CharField(choices=[('bronze', 'BRONZE'), ('silver', 'SILVER'), ('gold', 'GOLD')], default='bronze', max_length=255, primary_key=True, serialize=False)),
                ('point_accorded', models.IntegerField(verbose_name='Point accorded')),
                ('description', models.TextField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Price of the package')),
            ],
            options={
                'verbose_name': 'Package',
                'db_table': 'Package',
                'order_with_respect_to': 'point_accorded',
                'unique_together': {('name', 'point_accorded')},
            },
        ),
        migrations.CreateModel(
            name='Penalty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('warning', 'WARNING'), ('punishment', 'PUNISHMENT'), ('ban', 'BAN')], max_length=255, verbose_name='Penalty type')),
                ('amount_to_pay', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Amount to pay')),
            ],
            options={
                'db_table': 'Penalty',
            },
        ),
        migrations.CreateModel(
            name='Rule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('penalty', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='tontine.penalty')),
            ],
            options={
                'db_table': 'Rule',
            },
        ),
        migrations.CreateModel(
            name='Tontine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='tontine-bcf23faacb1b76699535e39d78e521dcd44bba32', max_length=255, verbose_name='Name of Tontine')),
                ('is_active', models.BooleanField(default=False)),
                ('is_closed', models.BooleanField(default=False)),
                ('description', models.TextField(blank=True, null=True)),
                ('required_point', models.IntegerField(verbose_name='Required user point to access')),
                ('max_allowed_member', models.IntegerField(verbose_name='Maximum Allowed Member')),
                ('amount', models.IntegerField(verbose_name='Amount to pay each round')),
                ('number_of_round', models.IntegerField(verbose_name='Number of rounds')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('default_frequency', models.IntegerField(choices=[(0, 'DAILY'), (1, 'WEEKLY'), (2, 'MONTHLY'), (3, 'YEAR')], default=2)),
                ('creator', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('custom_frequency', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tontine.customfrequency')),
            ],
            options={
                'verbose_name': 'Tontine',
                'db_table': 'Tontine',
                'order_with_respect_to': 'created_at',
            },
        ),
        migrations.CreateModel(
            name='TontineWallet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('wallet_pk', models.CharField(max_length=56, validators=[django.core.validators.MinLengthValidator(56)], verbose_name='Stellar wallet of tontine')),
                ('wallet_sk', models.CharField(max_length=56, validators=[django.core.validators.MinLengthValidator(56)], verbose_name='Stellar wallet of tontine')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=20, verbose_name='Total amount')),
                ('tontine', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='tontine.tontine')),
            ],
            options={
                'db_table': 'TontineWallet',
            },
        ),
        migrations.CreateModel(
            name='TontineRules',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rules', models.ManyToManyField(to='tontine.Rule')),
                ('tontine', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='tontine.tontine')),
            ],
            options={
                'db_table': 'TontineRules',
            },
        ),
        migrations.CreateModel(
            name='TontineRound',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('amount_out', models.DecimalField(decimal_places=2, max_digits=20)),
                ('is_tx_successful', models.BooleanField(default=False)),
                ('round_number', models.IntegerField(default=1)),
                ('recipient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('tontine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tontine.tontine')),
            ],
            options={
                'verbose_name': 'Tontine Round',
                'db_table': 'TontineRound',
                'order_with_respect_to': 'created_at',
                'unique_together': {('created_at', 'recipient', 'tontine')},
            },
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('package', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tontine.package')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Subscription',
                'db_table': 'Subscription',
                'unique_together': {('user', 'package')},
            },
        ),
    ]