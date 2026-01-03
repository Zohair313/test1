
from django.contrib.auth.models import User
from django.db import models
from configs.models import ModelBase, Currency
from contacts.models import Contact

class Mujtahid(ModelBase):
    name = models.CharField(max_length=100, verbose_name='Name')

    def __str__(self):
        return self.name


class MujtahidRepresentative(ModelBase):
    name = models.CharField(max_length=100, verbose_name='Name')
    mujtahid_for = models.ForeignKey(Mujtahid, on_delete=models.CASCADE)

    def __str__(self):
        return self.name + ' -> ' + self.mujtahid_for.name


class ObligationType(ModelBase):
    designated_choice = [
        ('syed', 'Only Syed'),
        ('non_syed', 'Only Non-Syed'),
        ('both', 'Both(Syed & Non-Syed)'),
        ('none', 'None'),
    ]

    name = models.CharField(max_length=50, verbose_name='Name')
    quantity = models.BooleanField()
    designate_for = models.CharField(max_length=50, choices=designated_choice)

    def __str__(self):
        return self.name


class WakalaType(ModelBase):
    mujtahid_representative = models.ForeignKey(MujtahidRepresentative, on_delete=models.CASCADE, verbose_name='Mujtahid Representative')
    obligation_type = models.ForeignKey(ObligationType, on_delete=models.CASCADE)
    mujtahid_liability_percentage = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Mujtahid Liability %')
    sadaat_liability_percentage = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Saddat Liability %')
    non_sadaat_liability_percentage = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Non-Saddat Liability %')
    income_percentage = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Income %')

    def __str__(self):
        return self.mujtahid_representative.name + ' -> ' + self.mujtahid_representative.mujtahid_for.name + ': ' + self.obligation_type.name


class ObligationDistribution(ModelBase):
    income_liability_choice = [
        ('liability', 'Liability'),
        ('income', 'Income'),
    ]

    name = models.CharField(max_length=100)
    percentage = models.DecimalField(max_digits=5, decimal_places=2)
    wakala_type = models.ForeignKey(WakalaType, on_delete=models.CASCADE)
    liability_income = models.CharField(max_length=50, choices=income_liability_choice, verbose_name='Liability/Income')


class Obligation(ModelBase):
    payment_choices = [
        ('cash', 'Cash'),
        ('online', 'Online'),
    ]

    receipt_no = models.CharField(max_length=15)
    received_date = models.DateField(auto_now=False)
    sender = models.ForeignKey(Contact, on_delete=models.CASCADE, verbose_name='From', related_name='%(class)s_sender')
    reference = models.ForeignKey(Contact, null=True, blank=True, on_delete=models.CASCADE, related_name='%(class)s_reference')
    amount = models.DecimalField(decimal_places=2, max_digits=10)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    payment_mode = models.CharField(max_length=10, choices=payment_choices)
    type = models.ForeignKey(ObligationType, on_delete=models.CASCADE, verbose_name='Obligation Type')
    mujtahid_repr = models.ForeignKey(MujtahidRepresentative, on_delete=models.CASCADE, verbose_name="Mujtahid Representative")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Received By')

    def __str__(self):
        return self.type.name + ': ' + str(self.amount)


class Payment(ModelBase):
    obligation = models.ForeignKey(Obligation, on_delete=models.CASCADE)


class PaymentDetail(ModelBase):
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)
    is_income = models.BooleanField()
    income_liability_percentage = models.DecimalField(max_digits=5, decimal_places=2)

