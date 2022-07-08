from django.contrib import admin
from .models import Profile, Item,User,Customer,Vendor
from import_export.admin import ImportExportModelAdmin
from django.conf import settings
# admin.site.register(Profile)

# settings.AUTH_USER_MODEL


admin.site.register(User)
admin.site.register(Customer)
admin.site.register(Vendor)
admin.site.register(Item)

@admin.register(Profile)
class ProfileImportExport(ImportExportModelAdmin):
    pass
