
from subscribe.models import ScoutChiefSubscription
from varchi.models import Assegnamenti, HumenClone



def super_import_assegnamenti():

    # Capi

    humens = HumenClone.objects.using('bureau_prod').all()[::] #EVALUATE FILTER

    for s in ScoutChiefSubscription.objects.select_related():

        scout_chief = s.scout_chief
        humen = humens.get(codice_censimento=scout_chief.code)
        clan = humen.vclan
        event = s.event_happening.event
        n_slot = s.event_happening.timeslot_id

        Assegnamenti.objects.create(
            cu=humen.cu, name=humen.nome, 
            surname=humen.cognome,
            unit = clan.nome,
            sub_unit = clan.idunitagruppo,
            event = event, 
            event_print_code=event.print_code, 
            event_code=event.code, 
            slot=n_slot,
            staff_evento = scout_chief.is_spalla,
            is_capo = True
        )
        print ("%s %s" % (scout_chief, clan))

    # Ragazzi

    
