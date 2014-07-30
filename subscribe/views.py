#-*- coding: utf-8 -*-

from django.shortcuts import render, redirect, render_to_response, HttpResponse
from django.core.exceptions import PermissionDenied, ValidationError
from django.core.context_processors import csrf
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from django.template.loader import get_template
from django.template.context import Context

from base.models import ScoutChief, Unit, EventHappening, Rover, EventTimeSlot
from base.views_support import API_response, API_ERROR_response, HttpJSONResponse
from subscribe.models import ScoutChiefSubscription

from recaptcha.client import captcha

from datetime import *
import json
import StringIO
from itertools import chain

from xhtml2pdf import pisa

# simple redirect to landing page
def index(request):
    return redirect('/login-gestione-eventi/')

# landing page: chief validate through AGESCI code, unit name and birthday
def subscribe(request):

    # if user is logged, redirect to event choose view
    if request.session.get('valid') == True:
        return redirect('/gestione-eventi/')

    c = {}
    c.update(csrf(request))
    c['recaptcha_public_key'] = settings.RECAPTCHA_PUBLIC_KEY
    c['recaptcha_private_key'] = settings.RECAPTCHA_PRIVATE_KEY
    c['support_email'] = settings.SUPPORT_EMAIL
    return render_to_response('index.html', c)

# API view, used to validate chief
def validate(request):
    if request.method == 'POST':

        user = request.POST.get('username')
        passw = request.POST.get('password')    

        u = authenticate(username=user, password=passw)
        if u is None:
            return API_ERROR_response(u"Nome o password non validi")

        # check captcha
        recaptcha_challenge_field = request.POST.get('recaptcha_challenge_field')
        if not recaptcha_challenge_field:
            return API_ERROR_response(u"RECAPTCHA non inizializzato correttamente. Prego contattare %s" % settings.SUPPORT_EMAIL)

        recaptcha_response_field = request.POST.get('recaptcha_response_field')
        if not recaptcha_response_field:
            return API_ERROR_response(u"Devi inserire il codice che leggi nell'immagine")

        # talk to the reCAPTCHA service
        response = captcha.submit(
            recaptcha_challenge_field,
            recaptcha_response_field,
            settings.RECAPTCHA_PRIVATE_KEY,
            request.META['REMOTE_ADDR'],
        )

        # see if the user correctly entered CAPTCHA information
        # and handle it accordingly.
        if not response.is_valid:
            return API_ERROR_response(u"Il codice che hai ricopiato non è corretto")

        # login is valid
        request.session['valid'] = True
        return API_response()

    # method is GET
    else:
        raise PermissionDenied

def gestioneEventi(request):
    if not request.session.get('valid'):
        return redirect('/login-gestione-eventi/')
    return render_to_response('choose.html', {})

def gestioneRagazzi(request):
    if not request.session.get('valid'):
        return redirect('/login-gestione-eventi/')
    bs = Rover.objects.all()
    res = []
    for b in bs:
        res.append(b.as_dict())
    return render_to_response('ragazzi.html', {'boys': res})

# logout view
def logout(request):
    if 'valid' in request.session:
        request.session['valid'] = False
    return redirect('/login-gestione-eventi/')

# subscribe API view
def event_subscribe(request, happening_id, chief_code):
    if not request.session.get('valid'):
        return API_ERROR_response(u'Non hai effettuato il login')
    chief = get_object_or_404(ScoutChief, code=chief_code)
    if not chief.is_spalla:
        return API_ERROR_response(u'Selezionare un capo spalla')
    eh = get_object_or_404(EventHappening, pk=happening_id)
    subscription = ScoutChiefSubscription(scout_chief=chief, event_happening=eh)
    try:
        subscription.save()
        return API_response()
    except ValidationError as e:
        return API_ERROR_response(unicode(e))

def event_unsubscribe(request, happening_id, chief_code):
    if not request.session.get('valid'):
        return API_ERROR_response(u'Non hai effettuato il login')
    chief = get_object_or_404(ScoutChief, code=chief_code)
    if not chief.is_spalla:
        return API_ERROR_response(u'Selezionare un capo spalla')
    eh = get_object_or_404(EventHappening, pk=happening_id)
    subscription = get_object_or_404(ScoutChiefSubscription, scout_chief=chief, event_happening=eh)
    try:
        subscription.delete()
        return API_response()
    except ValidationError as e:
        return API_ERROR_response(unicode(e))

def subscribedChiefs(request, happening_id):
    if not request.session.get('valid'):
        return API_ERROR_response(u'Non hai effettuato il login')
    eh = get_object_or_404(EventHappening, pk=happening_id)
    result = []
    for item in ScoutChiefSubscription.objects.filter(event_happening=eh):
        result.append(item.scout_chief.code)
    return HttpJSONResponse(result)

def freeChiefs(request, happening_id):
    if not request.session.get('valid'):
        return API_ERROR_response(u'Non hai effettuato il login')
    result = []
    eh = get_object_or_404(EventHappening, pk=happening_id)
    ehs = EventHappening.objects.filter(timeslot=eh.timeslot)
    scs = [x.scout_chief.pk for x in ScoutChiefSubscription.objects.filter(event_happening=ehs)]
    for item in ScoutChief.objects.exclude(pk__in=scs):
        if item.is_spalla == 1:
            result.append(item.code)
    return HttpJSONResponse(result)


def print_events(request, unit):

    rovers = Rover.objects.filter(
        vclan_id__nome=unit
    ).order_by('vclan')
    #.prefetch_related(Event)

    res = []
    for r in rovers:
        res.append(
            (r.nome + " " + r.cognome,
                "8 mattina",
                r.turno1.name, r.turno1.print_code,r.turno1.topic.name
            )
        )
        res.append(
            ("",
                "8 pomeriggio",
                r.turno2.name, r.turno2.print_code,r.turno2.topic.name
            )
        )
        res.append(
            ("",
                "9 mattina",
                r.turno3.name, r.turno3.print_code,r.turno3.topic.name
            )
        )

    turno1 = EventTimeSlot.objects.get(id=1)
    turno2 = EventTimeSlot.objects.get(id=2)
    turno3 = EventTimeSlot.objects.get(id=3)

    chiefs = ScoutChief.objects.filter(scout_unit=unit)

    ch = []    

    for chief in chiefs:
        el = {
            'name': chief.name+' '+chief.surname,
            'turno1': {'nome': '', 'codice': '', 'coraggio': ''},
            'turno2': {'nome': '', 'codice': '', 'coraggio': ''},
            'turno3': {'nome': '', 'codice': '', 'coraggio': ''},
        }

        evento1 = chief.scoutchiefsubscription_set.filter(event_happening__timeslot=turno1)
        print evento1[0].event_happening.event.name
        if evento1:
            evento1 = evento1[0].event_happening.event 
            el['turno1']['nome'] = evento1.name
            el['turno1']['codice'] = evento1.code
            el['turno1']['coraggio'] = evento1.topic.name

        evento2 = chief.scoutchiefsubscription_set.filter(event_happening__timeslot=turno2)
        if evento2:
            evento2 = evento2[0].event_happening.event 
            el['turno2']['nome'] = evento2.name
            el['turno2']['codice'] = evento2.code
            el['turno2']['coraggio'] = evento2.topic.name
        
        evento3 = chief.scoutchiefsubscription_set.filter(event_happening__timeslot=turno3)
        if evento3:
            evento3 = evento3[0].event_happening.event 
            el['turno3']['nome'] = evento3.name
            el['turno3']['codice'] = evento3.code
            el['turno3']['coraggio'] = evento3.topic.name
        
        ch.append(el)

    con = {}
    # c.update(csrf(request))
    con['chief'] = {}
    con['chief']['group'] = unit
    con['res'] = res
    con['capi'] = ch

    context = Context(con)
    template = get_template('rover_list_pdf.html')
    html = template.render(context)

    result = StringIO.StringIO()

    pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("UTF-8")),
                                        dest=result,
                                        encoding='UTF-8')
    if not pdf.err:

        filename = 'Lista_Laboratori_Clan.pdf'

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="'+filename+'"'
        response.write(result.getvalue())
    return response

    #return HttpResponse('Errore durante la generazione del PDF<pre>%s</pre>' % escape(html))

