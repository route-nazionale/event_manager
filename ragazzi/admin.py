from django.contrib import admin

from base.models import Rover


class RoverAdmin(admin.ModelAdmin):

    list_display = (
        '__unicode__', 
        'vclan', 'turno1',
        'priorita1',
        'valido1',
        'turno2',
        'priorita2',
        'valido2',
        'turno3',
        'priorita3',
        'valido3',
        'soddisfacimento'
    )

    list_editable = (
        'turno1', 'turno2', 'turno3'
    )

    list_filter = ('vclan', 'soddisfacimento')

    search_fields = ('nome', 'cognome')

admin.site.register(Rover, RoverAdmin)
