from django.apps import apps
from django.contrib import admin
from .models import Complaint,Grievance

# class CAdmin(admin.ModelAdmin):
#    list_display = ('user','Subject','Type_of_Print','Description','Time','status')

# admin.site.register(Profile)
# admin.site.register(Complaint,CAdmin)
# admin.site.register(Grievance)
for model in apps.get_app_config('GRsystem').get_models():
    admin.site.register(model)

