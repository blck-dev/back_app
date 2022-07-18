from rest_framework import serializers
from .models import Tontine, TontineWallet, TontineRound, TontineRules, Penalty, Package, Subscription, CustomFrequency, \
    Rule
from djoser.serializers import UserSerializer


class PackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Package
        fields = '__all__'


class CreateSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'


class SubscriptionSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only=True)
    package = PackageSerializer(many=False, read_only=True)

    class Meta:
        model = Subscription
        fields = '__all__'
