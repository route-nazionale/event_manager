from django.contrib import admin

from subscribe.models import ScoutChiefSubscription

class ScoutChiefSubscriptionAdmin(admin.ModelAdmin):

    list_display = ('scout_chief', 'turno', 'codice_evento', 'nome_evento', 'quartiere', 'posti', 'subscribed_on')
    search_fields = ('scout_chief__scout_unit',)
    #list_editable = ('scout_chief', 'event')

    def turno(self, obj):
        return obj.event_happening.timeslot.name

    def codice_evento(self, obj):
        return obj.event_happening.event.code

    def nome_evento(self, obj):
        return obj.event_happening.event.name

    def quartiere(self, obj):
        return obj.event_happening.event.district
    
    def posti(self, obj):
        a = obj.event_happening
        return "%s/%s" % (a.seats_n_chiefs, a.event.max_chiefs_seats)

    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False

admin.site.register(ScoutChiefSubscription, ScoutChiefSubscriptionAdmin)
