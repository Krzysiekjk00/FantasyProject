from django.contrib import admin

# Register your models here.
from import_export.admin import ImportExportModelAdmin

from Ekstraklasa.models import Players


@admin.register(Players)
class PlayerAdmin(ImportExportModelAdmin):
    pass