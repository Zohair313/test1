from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from configs.models import ModelBase

# Contacts model to save each contact details.
class Contact(ModelBase):
    class Gender(models.TextChoices):
        MALE = 'male', 'Male'
        FEMALE = 'female', 'Female'

    class Title(models.TextChoices):
        SYED = 'syed', 'Syed'
        SYEDA = 'syeda', 'Syeda'
        MIRZA = 'mirza', 'Mirza'

    title = models.CharField(max_length=10, choices=Title.choices)
    gender = models.CharField(max_length=10, choices=Gender.choices)
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50, null=True, blank=True)
    cnic = models.CharField(max_length=15, unique=True, verbose_name="CNIC")
    date_of_birth_gregorian = models.DateField(verbose_name='Date of Birth (Solar)')
    date_of_birth_hijri = models.CharField(max_length=20, verbose_name="Date of Birth (Lunar)")
    reference = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, default=None, related_name='ref')

    def __str__(self):
        return f"{self.title} {self.name}"

    @property
    def prefix(self):
        pass


class PhoneNumber(ModelBase):
    contact = models.ForeignKey(Contact, on_delete=models.PROTECT)
    number = PhoneNumberField()
    is_whatsapp = models.BooleanField(default=True)
    is_primary = models.BooleanField(default=False)


class Address(ModelBase):
    contact = models.ForeignKey(Contact, on_delete=models.PROTECT)
    country = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    line_1 = models.CharField(max_length=500)
    line_2 = models.CharField(max_length=500, blank=True, default='')
    landmark = models.CharField(max_length=500, blank=True, default='')
