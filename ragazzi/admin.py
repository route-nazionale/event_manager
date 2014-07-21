# -*- coding: utf-8 -*-
from django.contrib import admin
from django import forms

from base.models import Rover, Event

#KLUDGE proxy klass
from base.models.event import EventTurno1, EventTurno2, EventTurno3

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
        'vclan',
        'soddisfacimento',
        'turno1',
        'valido1',
        'turno2',
        'valido2',
        'turno3',
        'valido3',
    )

    #KO: meglio non dare questa funzionalita'. Non riusciremmo a fare il calcolo del soddisfacimento
    #KO: list_editable = (
    #KO:     'turno1', 'turno2', 'turno3'
    #KO: )

    list_filter = ('vclan', 'soddisfacimento', 'district')

    search_fields = ('nome', 'cognome')

    fields = (
        '__unicode__', 'codicecensimento', 'soddisfacimento',
        'district','eta', 'handicap',
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
        'priorita1', 'priorita2', 'priorita3',
        'district'
    )

    change_list_template = "admin/change_list_pagination_on_top.html"

    def has_add_permission(self, request):
        return False

    # Non occorre mostrare alcuna azione
    actions_on_top = False
    actions_on_bottom = False

    def get_actions(self, request):
        return []

    def __get_events_by_turn_num(self, turn_num, obj):
        """HYPER KLUDGE!! return Events included in a ordered timeslot"""

        event_model = globals()["EventTurno%s" % turn_num]
        qs = event_model.objects.select_related('district').filter(timeslot_set__pk=turn_num) #Use pk = turn_num!!!
        if 0: #obj:
            qs = qs.filter(code__startswith='TAV') | \
                (qs.filter(district=obj.district).exclude(code__startswith='TAV').order_by('district__code'))
        else:
            qs = qs.order_by('district__code')

        return qs
            
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "turno1":
            kwargs["queryset"] = self.__get_events_by_turn_num(1, self._obj)
        elif db_field.name == "turno2":
            kwargs["queryset"] = self.__get_events_by_turn_num(2, self._obj)
        elif db_field.name == "turno3":
            kwargs["queryset"] = self.__get_events_by_turn_num(3, self._obj)
        return super(RoverAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def get_form(self, request, obj=None, **kwargs):
        self._obj = obj
        form_class = super(RoverAdmin, self).get_form(request, obj, **kwargs)
        return form_class

    # v. implementazione kobe per colonne "arrivato al campo o al quartiere
    # def turno1_carino(self, obj):
    #    return u"<btn class=
    # turno1_carino.short_description = 'turno1'

admin.site.register(Rover, RoverAdmin)
