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

class DepositListSerializer(serializers.ModelSerializer):
    class DepositListOptionsSerializer(serializers.ModelSerializer):
        class Meta :
            model = DepositOptions
            exclude = ("fin_prdt_cd",)
    options = DepositListOptionsSerializer(source='deposit_options', many=True, read_only=True)
    class Meta:
        model = Deposit
        fields = '__all__'

class InstallmentSavingsListSerializer(serializers.ModelSerializer):
    class InstallmentSavingsListOptionsSerializer(serializers.ModelSerializer):
        class Meta :
            model = InstallmentSavingsOptions
            exclude = ("fin_prdt_cd",)
    options = InstallmentSavingsListOptionsSerializer(source='installment_savings_options', many=True, read_only=True)
    class Meta:
        model = InstallmentSavings
        fields = '__all__'