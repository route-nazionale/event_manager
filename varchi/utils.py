
from subscribe.models import ScoutChiefSubscription
from varchi.models import Assegnamenti, HumenClone
from base.models import Rover



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
            unit_with_subunit = "%s (%s)" % (clan.nome, clan.idunitagruppo),
            event = event, 
            event_print_code=event.print_code, 
            event_code=event.code, 
            event_name=event.name,
            slot=n_slot,
            staff_evento = scout_chief.is_spalla,
            is_capo = True
        )
        print ("%s %s" % (scout_chief, clan))

    # Ragazzi
    for r in Rover.objects.select_related():

        humen = humens.get(codice_censimento=r.codicecensimento)
        clan = humen.vclan
        for n_slot_from_0, slotname in enumerate(('turno1', 'turno2', 'turno3')):
            event = getattr(r,slotname)
            n_slot = n_slot_from_0+1
            Assegnamenti.objects.create(
                cu=humen.cu, name=humen.nome, 
                surname=humen.cognome,
                unit = clan.nome,
                sub_unit = clan.idunitagruppo,
                unit_with_subunit = "%s (%s)" % (clan.nome, clan.idunitagruppo),
                event = event, 
                event_print_code=event.print_code, 
                event_code=event.code, 
                event_name=event.name,
                slot=n_slot,
                staff_evento = False,
                is_capo = False
            )
            print ("%s %s" % (r, clan))
        
