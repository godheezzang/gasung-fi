from django.db import models

# Create your models here.
class Deposit(models.Model):
    fin_prdt_cd = models.CharField(max_length=255, unique=True)
    kor_co_nm = models.TextField()
    mtrt_int = models.TextField()
    join_way = models.TextField()
    spcl_cnd = models.TextField()
    join_deny = models.TextField()
    join_member = models.TextField()

class DepositOptions(models.Model):
    fin_prdt_cd = models.ForeignKey("Deposit", to_field="fin_prdt_cd" , on_delete=models.CASCADE, related_name="deposit_options")
    intr_rate_type = models.TextField()
    intr_rate_type_nm = models.TextField()
    save_trm = models.TextField()
    intr_rate = models.FloatField()
    intr_rate2 = models.FloatField()

class InstallmentSavings(models.Model):
    fin_prdt_cd = models.CharField(max_length=255, unique=True)
    kor_co_nm = models.TextField()
    mtrt_int = models.TextField()
    join_way = models.TextField()
    spcl_cnd = models.TextField()
    join_deny = models.TextField()
    join_member = models.TextField()

class InstallmentSavingsOptions(models.Model):
    fin_prdt_cd = models.ForeignKey("InstallmentSavings", to_field="fin_prdt_cd", on_delete=models.CASCADE, related_name="installment_savings_options")
    intr_rate_type = models.TextField()
    intr_rate_type_nm = models.TextField()
    save_trm = models.TextField()
    intr_rate = models.FloatField()
    intr_rate2 = models.FloatField()
    rsrv_type = models.TextField()
    rsrv_type_nm = models.TextField()