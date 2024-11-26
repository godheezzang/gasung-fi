from rest_framework import serializers
from .models import Deposit, DepositOptions, InstallmentSavings, InstallmentSavingsOptions, UserProducts

class DepositSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deposit
        fields = '__all__'

class DepositOptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepositOptions
        exclude = ("fin_prdt_cd",)
        read_only_fields = ("fin_prdt_cd",)

class DepositOptionsUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepositOptions
        exclude = ("fin_prdt_cd", )
        read_only_fields = ('fin_prdt_cd', 'intr_rate_type', 'intr_rate_type_nm', 'save_trm', )

class InstallmentSavingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstallmentSavings
        fields = '__all__'

class InstallmentSavingsOptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstallmentSavingsOptions
        exclude = ("fin_prdt_cd",)
        read_only_fields = ("fin_prdt_cd",)
class InstallmentSavingsOptionsUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstallmentSavingsOptions
        exclude = ("fin_prdt_cd", )
        read_only_fields = ('fin_prdt_cd', 'intr_rate_type', 'intr_rate_type_nm', 'save_trm', 'rsrv_type', 'rsrv_type_nm')

class DepositListSerializer(serializers.ModelSerializer):
    class DepositListOptionsSerializer(serializers.ModelSerializer):
        class Meta :
            model = DepositOptions
            exclude = ("fin_prdt_cd",)
    options = DepositListOptionsSerializer(source='deposit_options', many=True, read_only=True)
    class Meta:
        model = Deposit
        fields = "__all__"

class InstallmentSavingsListSerializer(serializers.ModelSerializer):
    class InstallmentSavingsListOptionsSerializer(serializers.ModelSerializer):
        class Meta :
            model = InstallmentSavingsOptions
            exclude = ("fin_prdt_cd", )
    options = InstallmentSavingsListOptionsSerializer(source='installment_savings_options', many=True, read_only=True)
    class Meta:
        model = InstallmentSavings
        fields = '__all__'

class UserProductsSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    class Meta:
        model = UserProducts
        fields = '__all__'
        read_only_fields = ("user",)

    def get_user(self, obj):
        return obj.user.username