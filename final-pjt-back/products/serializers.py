from rest_framework import serializers
from .models import Deposit, DepositOptions, InstallmentSavings, InstallmentSavingsOptions

class DepositSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deposit
        fields = '__all__'

class DepositOptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepositOptions
        exclude = ("fin_prdt_cd",)
        read_only_fields = ("fin_prdt_cd",)

class InstallmentSavingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstallmentSavings
        fields = '__all__'

class InstallmentSavingsOptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstallmentSavingsOptions
        exclude = ("fin_prdt_cd",)
        read_only_fields = ("fin_prdt_cd",)