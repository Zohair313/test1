
import datetime
import tempfile
from django.contrib.admin import AdminSite
from django import forms
from django.contrib import admin
from django.http import HttpResponse
from django.template.loader import render_to_string
from django_object_actions import DjangoObjectActions
try:
    from weasyprint import HTML
    from weasyprint.text.fonts import FontConfiguration
except Exception:
    HTML = None
    FontConfiguration = None

from configs.models import *
from webapp.models import *

class ObligationsAdminSite(AdminSite):
    # You can customize the look and feel here
    site_header = 'Obligations Administration'
    site_title = 'Obligations Admin Portal'
    index_title = 'Welcome to the Obligations Admin'


obligations_admin_site = ObligationsAdminSite(name='obligations_admin')
# contacts_admin_site.register(Contact, ContactAdmin)

# admin.site.register(Contact')
obligations_admin_site.register(Mujtahid)
obligations_admin_site.register(MujtahidRepresentative)
obligations_admin_site.register(ObligationType)
obligations_admin_site.register(Organization)
obligations_admin_site.register(Obligation)


@admin.register(Currency)
class CurrencyAdmin(DjangoObjectActions, admin.ModelAdmin):
    list_display = ['name', 'code', 'is_active']
    search_fields = ['name', 'code', 'is_active']
    ordering = ('-is_active', 'name',)
    readonly_fields = ('name', 'code')

    def has_add_permission(self, request):
        return False


@admin.register(Obligation)
class ObligationAdmin(DjangoObjectActions, admin.ModelAdmin):
    change_form_template = 'admin/obligation/change_form.html'

    def get_form(self, request, obj=None, **kwargs):
        count = Obligation.objects.count()
        form = super(ObligationAdmin, self).get_form(request, obj, **kwargs)

        # Set receipt
        form.base_fields['receipt_no'].initial = datetime.date.today().strftime('%Y%m%d') + f"{(count + 1):04}"
        form.base_fields['receipt_no'].disabled = True

        # Set received date
        form.base_fields['received_date'].initial = datetime.date.today()

        # set receiver(admin)
        form.base_fields['currency'].widget.can_add_related = False
        form.base_fields['currency'].widget.can_change_related = False
        form.base_fields['currency'].widget.can_view_related = False

        # set receiver(admin)
        form.base_fields['receiver'].initial = request.user
        form.base_fields['receiver'].disabled = True
        form.base_fields['receiver'].widget.can_add_related = False
        form.base_fields['receiver'].widget.can_change_related = False
        form.base_fields['receiver'].widget.can_view_related = False

        return form

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "currency":
            kwargs["queryset"] = Currency.objects.filter(is_active=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    list_display = ['receipt_no', 'received_date', 'sender', 'reference', 'amount', 'currency', 'payment_mode', 'type',
                    'mujtahid_repr']
    list_filter = ['receipt_no', 'received_date', 'sender', 'reference', 'amount', 'currency', 'payment_mode', 'type',
                   'mujtahid_repr']
    search_fields = ['receipt_no', 'received_date', 'sender__name', 'reference__name', 'amount', 'currency',
                     'payment_mode', 'type__name']

    def print_receipt_english(self, request, obj):
        # queryset
        # problems = Problem.objects.all()

        # context passed in the template
        # context = {'problems': problems}
        # render
        # html_string = render_to_string('english_receipt.html')


        # %%%%%%%%%%%%%%%%%%%%%%%%% WORKING %%%%%%%%%%%%%%%%%%%%%%%%% #
        html_string = render_to_string('english_receipt.html')
        html = HTML(string=html_string, base_url=request.build_absolute_uri())
        result = html.write_pdf()

        # http response
        response = HttpResponse(content_type='application/pdf;')
        response['Content-Disposition'] = 'inline; filename=obligation.pdf'
        response['Content-Transfer-Encoding'] = 'binary'
        with tempfile.NamedTemporaryFile(delete=True) as output:
            output.write(result)
            output.flush()
            output = open(output.name, 'rb')
            response.write(output.read())

        return response
        # %%%%%%%%%%%%%%%%%%%%%%%%% WORKING %%%%%%%%%%%%%%%%%%%%%%%%% #

        # pass
        # from reportlab.lib.pagesizes import A6, landscape
        # from reportlab.pdfgen import canvas
        #
        # buffer = io.BytesIO()
        #
        # w, h = A6
        # print(w)
        # print(h)
        # c = canvas.Canvas(buffer, pagesize=landscape(A6))
        # c.drawImage('C:\My Documents\Projects\i-finance\logo\darul-quran-logo-v4.png', w - 240, h - 420, width=300,
        #             height=300, mask=[0, 0, 0, 0, 0, 0])
        # c.setFont('Helvetica', 20, leading=None)
        # c.drawString(w - 150, h - 180, Organization.objects.get().name_english)
        # c.drawString(w - 150, h - 280, 'Contact Name')
        # c.drawString(w - 150, h - 380, 'Reference Name')
        # c.drawString(w - 150, h - 480, 'Amount')
        # # c.drawString(w - 225, h - 250, "Hello, world!")
        # c.showPage()
        # c.save()
        #
        # buffer.seek(0)
        # return FileResponse(buffer, as_attachment=True, filename='obligation.pdf')

    def print_receipt_urdu(self, request, obj):
        font_configs = FontConfiguration()
        html_string = render_to_string('urdu_receipt.html')
        html = HTML(string=html_string, base_url=request.build_absolute_uri())
        result = html.write_pdf(font_config=font_configs)

        # http response
        response = HttpResponse(content_type='application/pdf;')
        response['Content-Disposition'] = 'inline; filename=obligation.pdf'
        response['Content-Transfer-Encoding'] = 'binary'
        with tempfile.NamedTemporaryFile(delete=True) as output:
            output.write(result)
            output.flush()
            output = open(output.name, 'rb')
            response.write(output.read())

        return response

    print_receipt_english.label = "Print (English)"
    print_receipt_english.short_description = "Print the receipt"

    print_receipt_urdu.label = "Print (Urdu)"
    print_receipt_urdu.short_description = "Print the receipt"

    change_actions = ('print_receipt_english', 'print_receipt_urdu',)


class LiabilityInlineFormset(forms.models.BaseInlineFormSet):
    def clean(self):
        # get forms that actually have valid data
        count = 0
        sum = 0
        for form in self.forms:
            try:
                if form.cleaned_data:
                    count += 1
                    sum += form.cleaned_data['percentage']
            except AttributeError:
                # annoyingly, if a subform is invalid Django explicity raises
                # an AttributeError for cleaned_data
                pass
        if count < 1:
            raise forms.ValidationError('You must have at least one Liability/Income')
        if sum != 100:
            raise forms.ValidationError('Distribution sum should be equal to 100')


class LiabilityInline(admin.TabularInline):
    model = ObligationDistribution
    formset = LiabilityInlineFormset


@admin.register(WakalaType)
class WakalaTypeAdmin(admin.ModelAdmin):
    change_form_template = 'admin/my_change_form.html'

    inlines = [
        LiabilityInline,
    ]

