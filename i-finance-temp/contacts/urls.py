from django.urls import path
from contacts import admin  # 👈 Import your custom site

urlpatterns = [
    # Point the admin path to your custom site's URLs
    path('', admin.contacts_admin_site.urls),
]