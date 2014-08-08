#-*- coding: utf-8 -*-

from django.db import models

from base.models import Event

class Assegnamenti(models.Model):

    cu = models.CharField(max_length=255, blank=True,
        verbose_name='codice unico', help_text='', null=True,
        db_column="codiceUnivoco"
    )

    name = models.CharField(max_length=32, verbose_name="nome")
    surname = models.CharField(max_length=32, verbose_name="cognome")

    event = models.ForeignKey(Event) #id dell'evento comodo per Andrea
    event_code = models.CharField(db_column="idEvento", max_length=16) # codice programmatico interno, serve alla view di Nicola
    event_print_code = models.CharField(max_length=16) #codice stampabile serve a tutti e a Barbara per vedere
    event_name = models.CharField(max_length=256) #nome dell'evento serve a Riccardo per la stampona

    unit = models.CharField(max_length=64)
    sub_unit = models.CharField(max_length=16)
    unit_with_subunit = models.CharField(max_length=128) #serve a Riccardo

    slot = models.IntegerField()
    staff_evento = models.IntegerField(db_column="staffEvento")

    is_capo = models.BooleanField(default=False)

    class Meta:
        #managed = False
        db_table = "assegnamenti"

    def __unicode__(self):
        return "%s --> %s" % (self.cu, self.event)


class HumenClone(models.Model):

    SESSO_CHOICES = (
        ('M', 'Maschio'),
        ('F', 'Femmina'),
    )
    cu = models.CharField(max_length=255, blank=True,
        verbose_name='codice unico', help_text='', null=True, unique=True
    )
    codice_censimento = models.IntegerField(blank=True, null=True,
        verbose_name='codice censimento', help_text=''
    )
    idgruppo = models.CharField(max_length=255, blank=True,
        verbose_name='ID gruppo', help_text='', null=True
    )
    idunitagruppo = models.CharField(max_length=255, blank=True,
        verbose_name=u'ID unità gruppo', help_text='', null=True
    )

    vclan = models.ForeignKey('VclansClone', db_column='vclan_id',
        verbose_name='clan', help_text='', null=True
    )

    # Anagrafiche --------------------------------------

    nome = models.CharField(max_length=255, blank=True,
        verbose_name='nome', help_text='', null=True
    )
    cognome = models.CharField(max_length=255, blank=True,
        verbose_name='cognome', help_text='', null=True
    )
    sesso = models.CharField(max_length=255, blank=True,
        verbose_name='sesso', help_text='', null=True,
        choices=SESSO_CHOICES
    )
    data_nascita = models.DateField(null=True,
        verbose_name='data di nascita (GG/MM/AAAA)', help_text=''
    )
    eta = models.IntegerField(blank=True, null=True,
        verbose_name=u'età', help_text=''
    )
    cellulare = models.CharField(max_length=255, blank=True,
        verbose_name='cellulare', help_text='', null=True
    )
    email = models.EmailField(max_length=255, blank=True,
        verbose_name='email', help_text='', null=True
    )
    abitazione = models.CharField(max_length=255, blank=True,
        verbose_name='abitazione', help_text='', null=True
    )
    indirizzo = models.CharField(max_length=255, blank=True,
        verbose_name='indirizzo', help_text='', null=True
    )
    provincia = models.CharField(max_length=255, blank=True,
        verbose_name='provincia', help_text='', null=True
    )
    cap = models.CharField(max_length=255, blank=True,
        verbose_name='CAP', help_text='', null=True
    )
    citta = models.CharField(max_length=255, blank=True,
        verbose_name='citta', help_text='', null=True
    )
    note = models.TextField(blank=True,
        verbose_name='note', help_text='', null=True)

    # Partecipazione -------------------------------

    #ruolo = models.ForeignKey(Ruolipartecipante,
    #    verbose_name='ruolo', help_text='', db_column="ruolo"
    #)
    #periodo_partecipazione = models.ForeignKey('Periodipartecipaziones', db_column='periodo_partecipazione_id',
    #    verbose_name='periodo di partecipazione', help_text='', null=True
    #)
    pagato = models.NullBooleanField(default=False,
        verbose_name='pagato', help_text=''
    )

    # Ruoli  ----------------------------
    lab = models.NullBooleanField(default=False,
        verbose_name='lab.', help_text=''
    )

    scout = models.NullBooleanField(default=True,
        verbose_name='scout', help_text=''
    )
    agesci = models.NullBooleanField(default=True,
        verbose_name='AGESCI', help_text=''
    )
    rs = models.NullBooleanField(default=True,
        verbose_name='R/S', help_text=''
    )
    capo = models.NullBooleanField(default=True,
        verbose_name='capo', help_text=''
    )
    oneteam = models.NullBooleanField(default=False,
        verbose_name='OneTeam', help_text=''
    )
    extra = models.NullBooleanField(default=False,
        verbose_name='Extra', help_text=''
    )

    # Strade di coraggio -----------------------------------

    stradadicoraggio1 = models.NullBooleanField(default=False,
        verbose_name='strada di coraggio 1', help_text=''
    )
    stradadicoraggio2 = models.NullBooleanField(default=False,
        verbose_name='strada di coraggio 2', help_text=''
    )
    stradadicoraggio3 = models.NullBooleanField(default=False,
        verbose_name='strada di coraggio 3', help_text=''
    )
    stradadicoraggio4 = models.NullBooleanField(default=False,
        verbose_name='strada di coraggio 4', help_text=''
    )
    stradadicoraggio5 = models.NullBooleanField(default=False,
        verbose_name='strada di coraggio 5', help_text=''
    )

    # Alimentazione --------------------------------------------

    colazione = models.CharField(max_length=14, db_column='colazione',
        verbose_name='tipo di colazione', help_text='', blank=True,
        choices = (('LATTE', 'LATTE'), ('THE','THE'), ('ALTRO','ALTRO'))
    )
    dieta_alimentare = models.CharField(max_length=14, db_column='dieta_alimentare',
        verbose_name='dieta alimentare', help_text='', blank=True,
        choices = (('STANDARD','STANDARD'),('VEGETARIANO','VEGETARIANO'),('VEGANO','VEGANO'))
    )
    intolleranze_alimentari = models.NullBooleanField(default=False,
        verbose_name='intolleranze alimentari', help_text=''
    )
    el_intolleranze_alimentari = models.TextField(max_length=255, blank=True,
        verbose_name='intolleranze alimentari', help_text='', null=True
    )
    allergie_alimentari = models.NullBooleanField(default=False,
        verbose_name='allergie alimentari', help_text=''
    )
    el_allergie_alimentari = models.TextField(max_length=255, blank=True,
        verbose_name='allergie alimentari', help_text='', null=True
    )
    allergie_farmaci = models.NullBooleanField(default=False,
        verbose_name='allergie farmaci', help_text=''
    )
    el_allergie_farmaci = models.TextField(max_length=255, blank=True,
        verbose_name='allergie farmaci', help_text='', null=True
    )

    # Diversamente abili ---------------------------------------

    fisiche = models.NullBooleanField(default=False,
        verbose_name=u'disabilità fisica', help_text=''
    )
    lis = models.NullBooleanField(default=False,
        verbose_name='LIS', help_text=''
    )
    psichiche = models.NullBooleanField(default=False,
        verbose_name=u'disabilità psichica', help_text=''
    )
    sensoriali = models.NullBooleanField(default=False,
        verbose_name=u'disabilità sensoriale', help_text=''
    )
    patologie = models.CharField(max_length=255, blank=True,
        verbose_name=u'patologie', help_text='', null=True
    )


    # Date di creazione ed aggiornamento

    created_at = models.DateTimeField(blank=True, null=True,
        verbose_name='data di creazione', help_text='', auto_now_add=True
    )
    updated_at = models.DateTimeField(blank=True, null=True,
        verbose_name='ultimo aggiornamento', help_text='', auto_now=True
    )

    arrivato_al_quartiere = models.NullBooleanField(default=None)
    dt_verifica_di_arrivo = models.DateTimeField(blank=True, null=True, default=None)

    #posix_group_set = models.ManyToManyField(PosixGroup,
    #    null=True, blank=True, related_name="humen_set",
    #    #through=HumenPosixGroupMap
    #)


    # Servizi -----------------------------------------

    #service = models.ForeignKey(HumenServices, blank=True, null=True, 
    #    verbose_name='servizio'
    #)


    class Meta:
        managed = False
        db_table = 'humen'
        verbose_name = 'persona'
        verbose_name_plural = 'persone'

    def __unicode__(self):
        return u"%s - %s %s" % (self.cu, self.nome, self.cognome)

    
class VclansClone(models.Model):

    idvclan = models.CharField(max_length=255, blank=True)
    idgruppo = models.CharField(verbose_name="ID gruppo", max_length=255, blank=True)
    idunitagruppo = models.CharField(verbose_name="ID unità gruppo", max_length=255, blank=True)
    # ordinale = models.CharField(max_length=255, blank=True)
    nome = models.CharField(max_length=255, blank=True)
    regione = models.CharField(max_length=255, blank=True)
    updated_at = models.DateTimeField(blank=True, null=True, auto_now=True)
    created_at = models.DateTimeField(blank=True, null=True, auto_now_add=True)

    arrivato_al_campo = models.NullBooleanField(default=None)
    dt_verifica_di_arrivo = models.DateTimeField(blank=True, null=True, default=None)

    arrivato_al_quartiere = models.NullBooleanField(default=None)
    dt_arrivo_quartiere = models.DateTimeField(blank=True, null=True, default=None)

    route_num = models.IntegerField(db_column='route', null=True)
    #is_ospitante = models.NullBooleanField(default=None)

    #quartiere = models.IntegerField(blank=True, null=True)
    quartiere = models.CharField(max_length=8, db_column='quartiere',
       verbose_name='quartiere'
    )
    contrada = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "vclans"

    def __unicode__(self):
        return u"%s (%s)" % (self.nome, self.idunitagruppo)

