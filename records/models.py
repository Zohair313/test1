from django.db import models
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children')
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"

class Status(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Statuses"

class Record(models.Model):
    # Foreign Keys for Dynamic Choices
    category = models.ForeignKey(Category, on_delete=models.CASCADE, help_text="Select category to fill relevant details below.", null=True, blank=True)
    status = models.ForeignKey(Status, on_delete=models.CASCADE, null=True, blank=True)

    # Header Fields
    date = models.DateField(default=timezone.now)
    order_no = models.CharField(max_length=50, blank=True, default='')
    by_person = models.CharField(max_length=100, verbose_name="By", blank=True, default='')
    mobile = models.CharField(max_length=20, blank=True, default='', verbose_name="Mobile No")
    marhoom = models.CharField(max_length=100, blank=True, default='', verbose_name="Marhoom")
    deadline = models.DateField(null=True, blank=True)

    # Namaz Specific Fields
    years = models.PositiveIntegerField(default=0)
    months = models.PositiveIntegerField(default=0)
    days = models.PositiveIntegerField(default=0)
    rate_namaz_roza = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="@ (Rate)")
    notes = models.TextField(blank=True, verbose_name="Note", default='')

    # Roza Specific Fields
    years_roza = models.PositiveIntegerField(default=0, verbose_name="Years (Roza)")
    months_roza = models.PositiveIntegerField(default=0, verbose_name="Months (Roza)")
    days_roza = models.PositiveIntegerField(default=0, verbose_name="Days (Roza)")
    rate_roza = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="@ (Rate Roza)")
    notes_roza = models.TextField(blank=True, verbose_name="Note (Roza)", default='')

    # Qurbani Specific Fields
    janwar = models.CharField(max_length=100, blank=True, verbose_name="Janwar", default='')
    qty_qurbani = models.PositiveIntegerField(default=0, verbose_name="Qty")
    reason = models.CharField(max_length=255, blank=True, default='')
    rate_qurbani = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="@ (Rate Qurbani)")

    class Meta:
        verbose_name = "Record"
        verbose_name_plural = "Records"

    @staticmethod
    def get_next_order_no(category_obj):
        # Access name from object
        cat_name = category_obj.name if category_obj else 'Unknown'
        
        prefix_map = {
            'Namaz': 'NMZ',
            'Roza': 'RZA',
            'Qurbani': 'QBR'
        }
        prefix = prefix_map.get(cat_name, 'REC')
        current_year = timezone.now().year
        search_pattern = f"{prefix}-{current_year}-"
        
        last_record = Record.objects.filter(
            category=category_obj,
            order_no__startswith=search_pattern
        ).order_by('order_no').last()
        
        if last_record:
            try:
                last_sequence = int(last_record.order_no.split('-')[-1])
                new_sequence = last_sequence + 1
            except (ValueError, IndexError):
                new_sequence = 1
        else:
            new_sequence = 1
            
        return f"{prefix}-{current_year}-{str(new_sequence).zfill(4)}"

    def save(self, *args, **kwargs):
        if not self.order_no and self.category:
            self.order_no = self.get_next_order_no(self.category)
        super(Record, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.category} - {self.order_no}"

class Mobile(models.Model):
    record = models.ForeignKey(Record, on_delete=models.CASCADE, related_name='mobiles', null=True)
    number = models.CharField(max_length=20)
    
    class Meta:
        verbose_name = "Mobile"
        verbose_name_plural = "Mobiles"

class Marhoom(models.Model):
    record = models.ForeignKey(Record, on_delete=models.CASCADE, related_name='marhooms', null=True)
    name = models.CharField(max_length=100)
    
    class Meta:
        verbose_name = "Marhoom"
        verbose_name_plural = "Marhooms"

class Fulfillment(models.Model):
    record = models.ForeignKey(Record, on_delete=models.CASCADE, related_name='fulfillments')
    given_to = models.CharField(max_length=100, blank=True, verbose_name="Given To", default='')
    quantity_fulfillment = models.PositiveIntegerField(default=0, verbose_name="Quantity")
    giv_date = models.DateField(null=True, blank=True, verbose_name="Giv. Date")
    comp_date = models.DateField(null=True, blank=True, verbose_name="Comp. Date")
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Cost")
    paid = models.BooleanField(default=False, verbose_name="Paid")
    
    class Meta:
        verbose_name = "Fulfillment"
        verbose_name_plural = "Fulfillments"
    
    def __str__(self):
        return f"Fulfillment for {self.record.order_no} - {self.given_to}"
