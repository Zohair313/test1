from django.contrib.auth.models import User
from django.db import models

# Create your models here.
# Base Class
class ModelBase(models.Model):
    created_at = models.DateTimeField(auto_created=True, auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(class)s_created_by', editable=False, null=True)
    updated_at = models.DateTimeField(auto_created=True, auto_now=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(class)s_updated_by', editable=False, null=True)

    class Meta:
        abstract = True


class Organization(ModelBase):
    name = models.CharField(max_length=100, verbose_name='Name')
    description = models.CharField(max_length=500, verbose_name='Description')
    address = models.CharField(max_length=500, verbose_name='Address')
    contact_number = models.CharField(max_length=20)
    email = models.EmailField()
    logo = models.ImageField(upload_to='logo')
    website_link = models.CharField(max_length=100)
    social_link = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Currency(ModelBase):
    class Meta:
        verbose_name_plural = 'Currencies'

    name = models.CharField(max_length=100)
    code = models.CharField(max_length=5)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.name + " - " + self.code

class PaymentOptions(ModelBase):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name