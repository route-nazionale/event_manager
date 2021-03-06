#-*- coding: utf-8 -*-

from django.db import models
from django.utils.html import format_html

import datetime

class Unit(models.Model):

    nome = models.CharField(max_length=128, primary_key=True)

    class Meta:

        db_table = "scout_units"
        verbose_name = "gruppo scout"
        verbose_name_plural = "gruppi scout"

    def __unicode__(self):
        return self.nome

    def print_events(self):
        return format_html('<a target="_blank" href="/print-events/%s/">PDF</a>' % self.nome)
    
    print_events.short_description = 'Stampa eventi'        
    print_events.allow_tags = True

    #def n_chiefs(self):
    #    return self.scoutchief_set.count()
    #n_chiefs.short_description = "num. capi"

    #n_objs = n_chiefs

#--------------------------------------------------------------------------------

class ScoutChief(models.Model):

    FIELDS_TO_SERIALIZE = [
        "id",
        "code",
        "scout_unit",
        "name",
        "surname",
        # "birthday",
        "is_spalla",
        "region",
        "quartier",
        # "language",
    ]
    code = models.CharField(max_length=128, unique=True,
        verbose_name="codice censimento"
    )
    scout_unit = models.CharField(max_length=512, db_column="scout_unit_id")

    name = models.CharField(max_length=32, verbose_name="nome")
    surname = models.CharField(max_length=32, verbose_name="cognome")
    birthday = models.DateField(verbose_name="data di nascita");
    is_spalla = models.BooleanField(default=False, verbose_name=u"è un capo spalla",
        help_text=u"questo capo verrà iscritto dalla 'pattuglia eventi' con criteri supersonici"
    )

    region = models.CharField(max_length=50,verbose_name="regione")
    quartier = models.CharField(max_length=50, verbose_name="Sottocampo")

    ## A flag to communicate if a chief is busy in turns
    ## todo: set this when assigning thi chief to a lab
    # turn1_filled = models.BooleanField(default=False)
    # turn2_filled = models.BooleanField(default=False)
    # turn3_filled = models.BooleanField(default=False)


    class Meta:

        db_table = "scout_chiefs"
        verbose_name = "capo scout"
        verbose_name_plural = "capi scout"

    def __unicode__(self):
        return u"%s - %s %s" % (self.scout_unit, self.name, self.surname)

    @property
    def age(self):
        return datetime.date.today().year - self.birthday.year
    
    def as_dict(self):
        obj = {}
        for field in self.FIELDS_TO_SERIALIZE:
            v = getattr(self, field)
            if isinstance(v, (models.Field, models.Model)):
                v = unicode(v)
            elif isinstance(v, datetime.datetime):
                v = v.strftime("%s")
            obj[field] = v
        return obj


#--------------------------------------------------------------------------------

class Person(models.Model):
    """
    Generic person to be bound to one or more events.

    QUESTION: how do we get different people? For a chief
    a unique code is the membership code, but for a "guest"?
    who is he?
    """

    FIELDS_TO_SERIALIZE = [
        "id",
        "name",
        "code",
        "city",
        "kind",
        "description",
    ]

    KIND_CHIEF = "CHIEF"
    KIND_GUEST = "GUEST"
    KIND_CHOICES = (
        (KIND_CHIEF, "capo"),
        (KIND_GUEST, "ospite")
    )

    name = models.CharField(max_length=128)
    code = models.CharField(max_length=128, blank=True,
        verbose_name="codice censimento"
    )
    city = models.CharField(max_length=128, blank=True)
    kind = models.CharField(max_length=16,
        choices=KIND_CHOICES, default=KIND_CHIEF
    )
    description = models.TextField(blank=True)

    def as_dict(self):
        obj = {}
        for field in self.FIELDS_TO_SERIALIZE:
            v = getattr(self, field)
            if isinstance(v, (models.Field, models.Model)):
                v = unicode(v)
            elif isinstance(v, datetime.datetime):
                v = v.strftime("%s")
            obj[field] = v
        return obj

#--------------------------------------------------------------------------------

class District(models.Model):
    """
    District entity
    """
    
    FIELDS_TO_SERIALIZE = [
        "code",
        "name",
    ]

    code = models.CharField(max_length=8, primary_key=True)
    name = models.CharField(max_length=128, unique=True)
    letter = models.CharField(max_length=8)

    class Meta:

        db_table = "camp_districts"
        verbose_name = "sottocampo"
        verbose_name_plural = "sottocampi"
        ordering = ('code',)

    def __unicode__(self):
        return self.code

    def n_events(self):
        return self.event_set.count()
    n_events.short_description = "num. eventi"

    n_objs = n_events

    def as_dict(self):
        obj = {}
        for field in self.FIELDS_TO_SERIALIZE:
            v = getattr(self, field)
            if isinstance(v, (models.Field, models.Model)):
                v = unicode(v)
            elif isinstance(v, datetime.datetime):
                v = v.strftime("%s")
            obj[field] = v
        return obj
        

#--------------------------------------------------------------------------------

class HeartBeat(models.Model):

    name = models.CharField(max_length=128, unique=True)
    code = models.IntegerField(blank=True, unique=True)

    def __unicode__(self):
        return self.name

# --------------------------------------------------------------------

class Animatori(models.Model):
    code = models.ForeignKey('Event', to_field='code', db_column='code')
    cu = models.CharField(max_length=14, primary_key=True)
    cucode = models.IntegerField(blank=True, null=True)
    nome = models.CharField(max_length=255, blank=True)
    cognome = models.CharField(max_length=255, blank=True)
    quartiere = models.IntegerField(blank=True, null=True)
    contrada = models.IntegerField(blank=True, null=True)
    codicecensimento = models.IntegerField(blank=True, null=True)
    vclan = models.IntegerField(blank=True, null=True)
    idgruppo = models.CharField(max_length=255, blank=True)
    idunita = models.CharField(max_length=255, blank=True)
    ruolo = models.IntegerField(blank=True, null=True)
    disabilitato = models.IntegerField(blank=True, null=True)
    contatto = models.CharField(max_length=255, blank=True)
    email = models.CharField(max_length=255, blank=True)

    class Meta:
        managed = False
        db_table = 'animatori'

    def __unicode__(self):
        return "%s %s - %s" % (self.nome, self.cognome, self.code)

