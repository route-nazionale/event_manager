from django.contrib import admin

from base.models import Rover


class RoverAdmin(admin.ModelAdmin):

    list_display = (
        '__unicode__', 
    )

admin.site.register(Rover, RoverAdmin)
