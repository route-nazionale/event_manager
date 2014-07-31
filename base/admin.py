from django.contrib import admin

from base.models import (
    ScoutChief, District, Unit, Event,
    HeartBeat, EventHappening, EventTimeSlot
)

class ScoutChiefAdmin(admin.ModelAdmin):

    list_display = (
        '__unicode__', 'scout_unit', 'code',
        'name', 'surname', 'birthday'
    )
    list_filter = ('scout_unit', 'name', 'surname', 'birthday')

class DistrictAdmin(admin.ModelAdmin):

    list_display = ('__unicode__', 'code', 'n_objs')

class UnitAdmin(admin.ModelAdmin):

    list_display = ('__unicode__', 'print_events')
    search_fields = ('nome',)
    readonly_fields = ['nome']

class EventAdmin(admin.ModelAdmin):

    list_display = (
        'code', 'num', 'name', 'district', 'seats_tot'
    )
    list_editable = (
        'name', 'district', 'seats_tot'
    )

class EventHappeningAdmin(admin.ModelAdmin):

    list_display = (
        'nome', 'codice_stampa', 'quartiere', 'timeslot',
        'seats_n_boys', 'seats_n_chiefs',
        'print_info', 'print_people',
    )

    readonly_fields = ['nome', 'codice_stampa', 'quartiere']

    list_filter = ['timeslot', 'event__district']

    search_fields = ['event__print_code']

    def nome(self, obj):
        return obj.event.name

    def codice_stampa(self, obj):
        return obj.event.print_code

    def quartiere(self, obj):
        return obj.event.district

class HeartBeatAdmin(admin.ModelAdmin):

    list_display = ('__unicode__', 'code')

class EventTimeSlotAdmin(admin.ModelAdmin):

    list_display = ('__unicode__', 'name', 'dt_start', 'dt_stop')

admin.site.register(ScoutChief, ScoutChiefAdmin)
admin.site.register(District, DistrictAdmin)
admin.site.register(Unit, UnitAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(EventHappening, EventHappeningAdmin)
admin.site.register(HeartBeat, HeartBeatAdmin)
admin.site.register(EventTimeSlot, EventTimeSlotAdmin)
