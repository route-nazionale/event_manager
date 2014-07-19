from django.contrib import admin
from django import forms

from base.models import Rover

#--------------------------------------------------------------------------------


class RoverForm(forms.ModelForm):

    stradadicoraggio1 = forms.BooleanField(required=False, label="Il coraggio di amare (1)")
    stradadicoraggio2 = forms.BooleanField(required=False, label="Il coraggio di farsi ultimi (2)")
    stradadicoraggio3 = forms.BooleanField(required=False, label="Il coraggio di essere chiesa (3)")
    stradadicoraggio4 = forms.BooleanField(required=False, label="Il coraggio di essere cittadini (4)")
    stradadicoraggio5 = forms.BooleanField(required=False, label="Il coraggio di liberare il futuro (5)")


class RoverAdmin(admin.ModelAdmin):

    form = RoverForm

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

    #KO: meglio non dare questa funzionalita'. Non riusciremmo a fare il calcolo del soddisfacimento
    #KO: list_editable = (
    #KO:     'turno1', 'turno2', 'turno3'
    #KO: )

    list_filter = ('vclan', 'soddisfacimento')

    search_fields = ('nome', 'cognome')

    fields = (
        '__unicode__', 'codicecensimento', 'soddisfacimento',
        'eta', 'handicap', 
        'stradadicoraggio1', 'stradadicoraggio2', 'stradadicoraggio3', 'stradadicoraggio4', 'stradadicoraggio5',
        'turno1',
        'priorita1',
        'valido1',
        'turno2',
        'priorita2',
        'valido2',
        'turno3',
        'priorita3',
        'valido3',
    )
    readonly_fields = (
        '__unicode__',
        'codicecensimento',
        'eta', 'soddisfacimento',
        'handicap', 
        'valido3', 'valido2', 'valido1',
        'stradadicoraggio1', 'stradadicoraggio2', 'stradadicoraggio3', 'stradadicoraggio4', 'stradadicoraggio5',
        'priorita1', 'priorita2', 'priorita3'
    )

admin.site.register(Rover, RoverAdmin)
