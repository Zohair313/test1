from django.contrib import admin
from django.contrib.admin import AdminSite
from django.core.exceptions import ValidationError
from django.forms.models import BaseInlineFormSet

from contacts.models import Contact, PhoneNumber, Address
# from contacts.admin.site import contacts_admin_site
# from .validations import PhoneNumberInlineFormSet


class ContactsAdminSite(AdminSite):
    # You can customize the look and feel here
    site_header = 'Contacts Administration'
    site_title = 'Contacts Admin Portal'
    index_title = 'Welcome to the Contacts Admin'


class PhoneNumberInlineFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        primary_count = 0

        for form in self.forms:
            if form.cleaned_data.get('DELETE'):
                continue
            if form.cleaned_data.get('is_primary'):
                primary_count += 1

        if primary_count > 1:
            raise ValidationError("Only one phone number can be marked as primary.")
        # if primary_count == 0:
        #     raise ValidationError("At least one phone number must be marked as primary.")


class PhoneNumberInline(admin.TabularInline):  # or admin.StackedInline for vertical layout
    model = PhoneNumber
    extra = 1
    min_num = 0
    max_num = 3
    formset = PhoneNumberInlineFormSet
    fields = ['number', 'is_primary', 'is_whatsapp']
    verbose_name = "Phone Number"
    verbose_name_plural = "Phone Numbers"


class AddressInline(admin.StackedInline):
    model = Address
    extra = 1
    fields = ['country', 'state', 'city', 'line_1', 'line_2', 'landmark']
    verbose_name = "Address"
    verbose_name_plural = "Addresses"


# Define your ModelAdmin as usual
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'gender', 'cnic',)
    inlines = (PhoneNumberInline, AddressInline,)

# Create an instance of your custom admin site
contacts_admin_site = ContactsAdminSite(name='contacts_admin')
contacts_admin_site.register(Contact, ContactAdmin)
