from django.contrib import admin

from subscribe.models import ScoutChiefSubscription
from base.models import EventHappening, ScoutChief

class ScoutChiefSubscriptionAdmin(admin.ModelAdmin):

    list_display = ('scout_chief', 'turno', 'codice_stampa', 'nome_evento', 'quartiere', 'posti', 'subscribed_on')
    search_fields = ('scout_chief__scout_unit',)
    #list_editable = ('scout_chief', 'event')

    fields = ('scout_chief', 'turno', 'quartiere', 'event_happening') #, 'is_locked')
    readonly_fields = ['quartiere', 'turno']

    def turno(self, obj):
        return obj.event_happening.timeslot.name

    def codice_stampa(self, obj):
        return obj.event_happening.event.print_code

    def nome_evento(self, obj):
        return obj.event_happening.event.name

    def quartiere(self, obj):
        return obj.event_happening.event.district
    
    def posti(self, obj):
        a = obj.event_happening
        return "%s/%s" % (a.seats_n_chiefs, a.event.max_chiefs_seats)

    #def has_add_permission(self, request):
    #    return False
    #
    #def has_delete_permission(self, request, obj=None):
    #    return False

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # if we are changing a person and we are not a superuser
        if db_field.name == "event_happening":
            eh_qs = EventHappening.objects.exclude(event__print_code="ELIMINATO")
            eh_qs = eh_qs.exclude(event__print_code__startswith="X").select_related()
            if self._obj:
                eh_qs = eh_qs.filter(timeslot=self._obj.event_happening.timeslot)
            kwargs["queryset"] = eh_qs.order_by("event__print_code")
        elif db_field.name == "scout_chief":
            qs = ScoutChief.objects.select_related()
            kwargs["queryset"] = qs.order_by("scout_unit")
            
        return super(ScoutChiefSubscriptionAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
    
    def get_form(self, request, obj=None):
        self._obj = obj #Hack to filter formfield_for_foreignkey
        if self._obj:
            if 'scout_chief' not in self.readonly_fields:
                self.readonly_fields.append('scout_chief')
        else:
            if 'scout_chief' in self.readonly_fields:
                self.readonly_fields.remove('scout_chief')

        form = super(ScoutChiefSubscriptionAdmin, self).get_form(request, obj)
        return form

admin.site.register(ScoutChiefSubscription, ScoutChiefSubscriptionAdmin)
