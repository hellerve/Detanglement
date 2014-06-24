from django.contrib import admin
from datavis.models import Api

class ApiAdmin(admin.ModelAdmin):
    list_display = ['api']
    list_filter = ['api']
    search_field = ['api']
    save_on_top = True

admin.site.register(Api, ApiAdmin)
