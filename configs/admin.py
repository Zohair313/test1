from django.contrib import admin

from .models import Organization, Currency, PaymentOptions

admin.site.register(Organization)
admin.site.register(Currency)
admin.site.register(PaymentOptions)

