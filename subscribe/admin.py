from django.contrib import admin

from subscribe.models import ScoutChiefSubscription

class ScoutChiefSubscriptionAdmin(admin.ModelAdmin):

    list_display = ('scout_chief', 'event_happening', 'subscribed_on')
    #list_editable = ('scout_chief', 'event')

admin.site.register(ScoutChiefSubscription, ScoutChiefSubscriptionAdmin)
