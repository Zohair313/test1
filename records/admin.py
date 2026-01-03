from django.contrib import admin
from django import forms
from .models import Record, Mobile, Marhoom, Fulfillment
from .models import Category, Status

class MobileInline(admin.StackedInline):
    model = Mobile
    extra = 1
    classes = ('collapse',)

class MarhoomInline(admin.StackedInline):
    model = Marhoom
    extra = 1
    classes = ('collapse',)

class FulfillmentInline(admin.StackedInline):
    model = Fulfillment
    extra = 1
    verbose_name = "Fulfillment Information"
    verbose_name_plural = "Fulfillment Information"
    classes = ('collapse',)

# Category and Status are hidden from admin - only accessible via Record form
# @admin.register(Category)
# class CategoryAdmin(admin.ModelAdmin):
#     list_display = ('name',)
#     search_fields = ['name']
#     fields = ('name',)

# @admin.register(Status)
# class StatusAdmin(admin.ModelAdmin):
#     list_display = ('name',)
#     search_fields = ['name']
#     fields = ('name',)

# Simple Record Admin
@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    list_display = ('order_no', 'category', 'status', 'date', 'by_person')
    list_filter = ('category', 'status', 'date')
    search_fields = ('order_no', 'by_person')
    
    fieldsets = (
        ('Header Information', {
            'fields': ('date', 'by_person', 'deadline', 'category', 'status'),
            'classes': ('collapse',)
        }),
        ('Namaz Fields', {
            'fields': ('years', 'months', 'days', 'rate_namaz_roza', 'notes'),
            'classes': ('collapse', 'namaz-fields'),
        }),
        ('Roza Fields', {
            'fields': ('years_roza', 'months_roza', 'days_roza', 'rate_roza', 'notes_roza'),
            'classes': ('collapse', 'roza-fields'),
        }),
        ('Qurbani Fields', {
            'fields': ('janwar', 'qty_qurbani', 'reason', 'rate_qurbani'),
            'classes': ('collapse', 'qurbani-fields'),
        }),
    )
    
    inlines = [MobileInline, MarhoomInline, FulfillmentInline]
    
    class Media:
        js = ('records/js/simple_category_toggle.js',)

admin.site.site_header = "IJARA"
admin.site.site_title = "IJARA"
admin.site.index_title = "IJARA Portal"
