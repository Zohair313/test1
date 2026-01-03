from django.urls import path
from webapp import admin
# from . import views

urlpatterns = [
    # path('mujtahid-representative', views.get_all_mujtahid_representative),
    path('', admin.obligations_admin_site.urls),
]