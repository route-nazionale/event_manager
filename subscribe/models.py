#-*- coding: utf-8 -*-

from django.db import models, transaction
from django.core.exceptions import ValidationError
from django.conf import settings

from base.models import ScoutChief, EventHappening

class ScoutChiefSubscription(models.Model):

    scout_chief = models.ForeignKey(ScoutChief)
    event_happening = models.ForeignKey(EventHappening)
    is_locked = models.BooleanField(default=False, verbose_name=u"non si può cancellare")

    subscribed_on = models.DateTimeField(auto_now_add=True)
    unsubscribed_on = models.DateTimeField(null=True, blank=True)

    MAX_SUBSCRIPTIONS = 3

    class Meta:

        db_table = "subscriptions"
        verbose_name = "iscrizione evento"
        verbose_name_plural = "iscrizioni eventi"

    def __unicode__(self):
        return u"%s - %s" % (self.scout_chief, self.event_happening)

    def clean(self):
        """
        Checks among fields go here

        raises ValidationError if not valid
        """

        subscriptions = ScoutChiefSubscription.objects.filter(
            scout_chief=self.scout_chief
        )
        n_subscriptions = subscriptions.count()

        if n_subscriptions >= self.MAX_SUBSCRIPTIONS:
            raise ValidationError(u'Non &egrave; possibile iscriversi a pi&ugrave; di 3 eventi')

        #check no eventi sovrapposti
        if subscriptions.filter(event_happening__timeslot=self.event_happening.timeslot).count():
            raise ValidationError(u'Capo gi&agrave; iscritto ad un evento di questo turno')
        
        #check che ci siano posti liberi
        if not self.event_happening.available_seats:
            raise ValidationError(
                u"Posti esauriti per l'evento %s, si prega di ricaricare la pagina" % self.event_happening
            )
        

    def save(self, *args, **kw):
        self.full_clean()
        eh = self.event_happening
        rv = super(ScoutChiefSubscription, self).save(*args, **kw)
        eh.seats_n_chiefs += 1
        eh.save()
        return rv

    @transaction.atomic
    def delete(self):
        if self.is_locked:
            raise ValidationError(u"%s è vincolato a %s: non è possibile eliminarlo" % (
                self.scout_chief, self.event_happening
            ))

        eh = self.event_happening
        rv = super(ScoutChiefSubscription, self).delete()
        eh.seats_n_chiefs -= 1
        eh.save()
        return rv



#---------------------------------------------------------------------------------
# RABBITMQ part

from base.models import Event

MODEL_RABBITMQ_MAP = {
       EventHappening : 'event_happening',
       Event : 'campevents'
}

def get_rabbitmq_routing_key(sender, instance, created):

    basename = MODEL_RABBITMQ_MAP.get(sender)
    if basename:
        action = ['update','insert'][int(created)]
        return u"%s.%s" % (basename, action)
    else:
        return None

import pika
from django.core import serializers
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
@receiver(post_save)
def my_log_queue(sender, instance, created, **kwargs):

    data = serializers.serialize("json", [instance])

    # Publish changes to RabbitMQ server
    routing_key = get_rabbitmq_routing_key(sender, instance, created)

    if routing_key:
        #RABBITMQ_SETTINGS

        RABBITMQ_connection = pika.BlockingConnection(
            pika.ConnectionParameters(**settings.RABBITMQ)
        )
        RABBITMQ_channel = RABBITMQ_connection.channel()

        RABBITMQ_channel.basic_publish(
            exchange='application', routing_key=routing_key, body=data
        )
        RABBITMQ_connection.close()

