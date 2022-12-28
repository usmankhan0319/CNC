from django.contrib import admin
from webapi.models import *
from import_export.admin import ImportExportModelAdmin


class productinfo(ImportExportModelAdmin):
    pass

# Register your models here.
admin.site.register(Account)
admin.site.register(Productinfo,productinfo)
admin.site.register(whitelistToken)

