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

    def has_add_permission(self, request):
        if request.user.is_readonly():
            return False
        else:
            return True

    def change_view(self, request, *args, **kw):
        if request.user.is_readonly():
            self.readonly_fields = self.list_editable
        return super(EventAdmin, self).change_view(request, *args, **kw)

    def add_view(self, request, *args, **kw):
        self.readonly_fields = []
        return super(EventAdmin, self).add_view(request, *args, **kw)

class EventHappeningAdmin(admin.ModelAdmin):

    list_display = (
        'nome', 'codice_stampa', 'quartiere', 'timeslot',
        'ragazzi_iscritti', 'capi_iscritti',
        'print_info', 'print_people',
    )

    #readonly_fields = ['nome', 'codice_stampa', 'quartiere']

    list_filter = ['timeslot', 'event__district']

    search_fields = ['event__print_code']

    def nome(self, obj):
        return obj.event.name

    def codice_stampa(self, obj):
        return obj.event.print_code

    def quartiere(self, obj):
        return obj.event.district

    def ragazzi_iscritti(self, obj):
        return obj.seats_n_boys

    def capi_iscritti(self, obj):
        return obj.seats_n_chiefs

    def has_add_permission(self, request):
        if request.user.is_readonly():
            return False
        else:
            return True

    def change_view(self, request, *args, **kw):
        if request.user.is_readonly():
            self.readonly_fields = [
                'nome', 'codice_stampa', 'quartiere',
                'timeslot', 'event', 'seats_n_boys', 'seats_n_chiefs',
            ]
        else:
            self.readonly_fields = [
                'nome', 'codice_stampa', 'quartiere',
            ]
        return super(EventHappeningAdmin, self).change_view(request, *args, **kw)

    def add_view(self, request, *args, **kw):
        self.readonly_fields = ['nome', 'codice_stampa', 'quartiere']
        return super(EventHappeningAdmin, self).add_view(request, *args, **kw)

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
