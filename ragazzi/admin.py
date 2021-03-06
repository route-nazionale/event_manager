# -*- coding: utf-8 -*-
from django.contrib import admin
from django import forms
from django.db.models import Q

from base.models import Event
from ragazzi.models import Rover, MyRover

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

    search_fields = ('nome', 'cognome', 'turno1__print_code', 'turno2__print_code', 'turno3__print_code')

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
    base_readonly_fields = [
        '__unicode__',
        'codicecensimento',
        'eta', 'soddisfacimento',
        'handicap', 
        'valido3', 'valido2', 'valido1',
        'stradadicoraggio1', 'stradadicoraggio2', 'stradadicoraggio3', 'stradadicoraggio4', 'stradadicoraggio5',
        'priorita1', 'priorita2', 'priorita3',
        'district'
    ]

    change_list_template = "admin/change_list_pagination_on_top.html"

    def has_add_permission(self, request):
        return False

    # Non occorre mostrare alcuna azione
    actions_on_top = False
    actions_on_bottom = False

    def change_view(self, request, *args, **kw):
        if request.user.is_readonly():
            self.readonly_fields = self.base_readonly_fields + [
                'turno1', 'turno2', 'turno3',
            ]
        else:
            self.readonly_fields = self.base_readonly_fields

        return super(RoverAdmin, self).change_view(request, *args, **kw)

    def add_view(self, request, *args, **kw):
        self.readonly_fields = self.base_readonly_fields
        return super(RoverAdmin, self).add_view(request, *args, **kw)

    def get_actions(self, request):
        return []

    def __get_events_by_turn_num(self, turn_num, obj):
        """HYPER KLUDGE!! return Events included in a ordered timeslot"""

        event_model = globals()["EventTurno%s" % turn_num]
        qs = event_model.objects.select_related('district').filter(timeslot_set__pk=turn_num) #Use pk = turn_num!!!
        if obj:
            qs = qs.filter(code__startswith='TAV') | \
                (qs.filter(district__code__in=(obj.district.code, 'Q0')).exclude(code__startswith='TAV').order_by('district__code', 'name'))
        else:
            qs = qs.order_by('district__code', 'name')

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

class MyRoverAdmin(RoverAdmin):

    list_display = (
        '__unicode__',
        'vclan',
        'soddisfacimento',
        'turno1',
        'valido1',
        'evento1_stato',
        'turno2',
        'valido2',
        'evento2_stato',
        'turno3',
        'valido3',
        'evento3_stato',
    )

    def evento1_stato(self, obj):
        return obj.turno1.state_activation

    def evento2_stato(self, obj):
        return obj.turno2.state_activation

    def evento3_stato(self, obj):
        return obj.turno3.state_activation

    def get_queryset(self, request):
        return self.model.objects.filter( Q(turno1__state_activation='DISMISSED') | Q(turno2__state_activation='DISMISSED') | Q(turno3__state_activation='DISMISSED') )


admin.site.register(Rover, RoverAdmin)
admin.site.register(MyRover, MyRoverAdmin)
