#-*- coding: utf-8 -*-

from django.core.management.base import BaseCommand, CommandError

from django.template.loader import get_template
from django.template import Context

from base.models import *
from subscribe.models import *

from xhtml2pdf import pisa
import cStringIO as StringIO
import cgi
import sys

class Command(BaseCommand):
    args = ''
    help = 'print info PDF for all events, listing people'

    def handle(self, *args, **options):

        events = EventHappening.objects.select_related('event').exclude(event__state_activation='DISMISSED')
        n_events = events.count()
        done = 0

        for eh in events:

            con = {}
            con['nome'] = eh.event.name
            con['descrizione'] = eh.event.description
            con['turno'] = eh.timeslot.name
            con['print_code'] = eh.event.print_code
            con['capi'] = []
            con['ragazzi'] = []

            for capo in eh.scoutchiefsubscription_set.filter(scout_chief__is_spalla=False):
                con['capi'].append({
                   'nome': capo.scout_chief.name,
                   'cognome': capo.scout_chief.surname,
                   'gruppo': capo.scout_chief.scout_unit
                })

            turno = eh.timeslot.id
            print_code = eh.event.code

            if turno == 1:
                iscritti = Rover.objects.filter(turno1=print_code)
            if turno == 2:
                iscritti = Rover.objects.filter(turno2=print_code)
            if turno == 3:
                iscritti = Rover.objects.filter(turno3=print_code)

            for r in iscritti:
                con['ragazzi'].append({
                  'nome': r.nome,
                  'cognome': r.cognome,
                  'gruppo': r.vclan.nome
                })

            done = done + 1

            write_pdf('iscritti_evento.html', con, 'iscritti_pdf/iscritti_evento_%s-%s.pdf' % (eh.event.print_code, eh.timeslot.id))
            sys.stdout.write("\r%s/%s %s-%s %s%%" % (done, n_events, eh.event.print_code, eh.timeslot.id, int(100 * float(done)/float(n_events))))
            sys.stdout.flush()

def write_pdf(template_src, context_dict, filename):
    template = get_template(template_src)
    context = Context(context_dict)
    html  = template.render(context)
    result = open(filename, 'wb') # Changed from file to filename
    pdf = pisa.pisaDocument(StringIO.StringIO(
        html.encode("UTF-8")), result)
    result.close()

