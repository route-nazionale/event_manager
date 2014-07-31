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
    help = 'print info PDF for all events'

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
            con['spalle'] = []

            for spalla in eh.scoutchiefsubscription_set.filter(scout_chief__is_spalla=True):
                con['spalle'].append({
                   'nome': spalla.scout_chief.name,
                   'cognome': spalla.scout_chief.surname,
                   'gruppo': spalla.scout_chief.scout_unit
                })

            done = done + 1

            write_pdf('info_evento.html', con, 'info_pdf/info_evento_%s-%s.pdf' % (eh.event.print_code, eh.timeslot.id))
            sys.stdout.write("\r%s/%s %s-%s %s%%" % (done, n_events, eh.event.print_code, eh.timeslot.id, int(100 * float(done)/float(n_events))))
            sys.stdout.flush()

        print 'fatto :)'

def write_pdf(template_src, context_dict, filename):
    template = get_template(template_src)
    context = Context(context_dict)
    html  = template.render(context)
    result = open(filename, 'wb') # Changed from file to filename
    pdf = pisa.pisaDocument(StringIO.StringIO(
        html.encode("UTF-8")), result)
    result.close()

