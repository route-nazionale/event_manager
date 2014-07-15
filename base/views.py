import json
from django.shortcuts import render, get_object_or_404
from django.db import models
from django.core.context_processors import csrf
from django.core.exceptions import PermissionDenied
from django.db.models import Max

from base.models import *
from base.models.base import *
from base.models.event import *
from base.views_support import HttpJSONResponse

# Ok, this function is horrible - I know :-(
def _getEventTimeslot(v):
    for item in EventTimeSlot.objects.all():
        if v == unicode(item):
            return item
    raise Exception()

def _getDistrict(v):
    result = District.objects.filter(name=v)
    if result:
        return result[0]
    else:
        raise Exception()

def _getTopic(v):
    result = HeartBeat.objects.filter(name=v)
    if result:
        return result[0]
    else:
        raise Exception()

def _getNextNum():
    try:
        return Event.objects.all().aggregate(Max('num'))['num__max'] + 1
    except:
        return 1

def _isSharedEvent(eh):
    return EventHappening.objects.filter(event=eh.event.pk).count()

def createEvent(request):
    if not request.session.get('valid'):
        raise PermissionDenied()
    data = json.loads(request.body)
    timeslot = _getEventTimeslot(data.get('timeslot'))
    del data['timeslot']
    data['district'] = _getDistrict(data.get('district'))
    data['topic'] = _getTopic(data.get('topic'))
    data['num'] = _getNextNum()
    # code = "%s-%s%s%s" % (data['kind'],
    #         data['district'].code,
    #         data['topic'].code,
    #         data['num'])
    # data['name'] = code + " - " + data['name']
    seats_n_boys = data['seats_n_boys']
    data['seats_tot'] = data['max_boys_seats'] + data['max_chiefs_seats']
    del data['seats_n_boys']
    seats_n_chiefs = data['seats_n_chiefs']
    del data['seats_n_chiefs']
    event = Event.objects.create(**data)
    eh = EventHappening.objects.create(
        timeslot=timeslot,
        event=event,
        seats_n_boys=seats_n_boys,
        seats_n_chiefs=seats_n_chiefs
    )
    result = {}
    return HttpJSONResponse(result)

def storeEvent(request):
    if not request.session.get('valid'):
        raise PermissionDenied()
    data = json.loads(request.body)
    eh = EventHappening.objects.get(pk=data['id'])
    eh.timeslot = _getEventTimeslot(data.get('timeslot'))
    if _isSharedEvent(eh):
        e = eh.event
        e.name = data['name']
        e.num = _getNextNum()
        e.topic = _getTopic(data.get('topic'))
        e.district = _getDistrict(data.get('district'))
        e.name = e.code + " - " + e.name
        e.pk = None # add another object copy
        e.save()
        eh.event = e
    else:
        eh.event.name = data['name']
    eh.event.description = data['description']
    eh.event.kind = data['kind']
    eh.event.district = _getDistrict(data.get('district'))
    eh.event.topic = _getTopic(data.get('topic'))
    eh.event.max_boys_seats = data['max_boys_seats']
    eh.event.max_chiefs_seats = data['max_chiefs_seats']
    eh.event.min_age = data['min_age']
    eh.event.max_age = data['max_age']
    eh.event.state_handicap = data['state_handicap']
    eh.event.state_chief = data['state_chief']
    eh.event.state_activation = data['state_activation']

    assigned_boys = 0

    # aggiorna lo stato dell'assegnamento per chi ha questo
    # evento al turno 1
    rs_turno1 = Rover.objects.filter(seq1=eh.event.num)
    for rs in rs_turno1:
        rs.valido1 = data['state_activation'] == Event.ACTIVATION_ACTIVE
        assigned_boys+=1

    # aggiorna lo stato dell'assegnamento per chi ha questo
    # evento al turno 2
    rs_turno2 = Rover.objects.filter(seq2=eh.event.num)
    for rs in rs_turno2:
        rs.valido2 = data['state_activation'] == Event.ACTIVATION_ACTIVE
        assigned_boys+=1

    # aggiorna lo stato dell'assegnamento per chi ha questo
    # evento al turno 3
    rs_turno3 = Rover.objects.filter(seq3=eh.event.num)
    for rs in rs_turno3:
        rs.valido3 = data['state_activation'] == Event.ACTIVATION_ACTIVE
        assigned_boys+=1

    eh.event.state_subscription = data['state_subscription']
    eh.event.save()
    eh.save()
    result = { 'msg' : 'Sono stati coinvolti nella modifica ' + str(assigned_boys) + ' ragazzi.'}
    print("==> " + result['msg'])
    return HttpJSONResponse(result)

def events(request):
    if not request.session.get('valid'):
        raise PermissionDenied()
    events = []
    eh_qs = EventHappening.objects.all()
    for eh in eh_qs:
        obj = eh.as_dict()
        if ' - ' not in obj['name']:
            obj['name'] = obj['code'] + ' - ' + obj['name']
        events.append(obj)
    return HttpJSONResponse(events)


def units(request):
    # Units autocompletion -> no login required
    units = []
    for unit in Unit.objects.all():
        units.append(unit.name)

    return HttpJSONResponse(units)


def districts(request):
    if not request.session.get('valid'):
        raise PermissionDenied()
    result = []
    for item in District.objects.all():
        result.append(item.name)
    return HttpJSONResponse(result)


def timeslots(request):
    if not request.session.get('valid'):
        raise PermissionDenied()
    result = []
    for item in EventTimeSlot.objects.all():
        result.append(unicode(item))
    return HttpJSONResponse(result)


def topics(request):
    if not request.session.get('valid'):
        raise PermissionDenied()
    result = []
    for item in HeartBeat.objects.all():
        result.append(item.name)
    return HttpJSONResponse(result)


def chiefs(request):
    if not request.session.get('valid'):
        raise PermissionDenied()
    sc = ScoutChief.objects.filter(is_spalla=True)
    # sc = ScoutChief.objects.all()
    result = []
    for item in sc:
        result.append(item.as_dict())
    return HttpJSONResponse(result)

def boys(request):
    if not request.session.get('valid'):
        raise PermissionDenied()
    sc = Rover.objects.all()
    result = []
    for item in sc:
        result.append(item.as_dict())
    return HttpJSONResponse(result)

def boys_paginate(request, frm):
    if not request.session.get('valid'):
        raise PermissionDenied()
    f = int(frm)
    sc = Rover.objects.all()[f:500]
    result = []
    for item in sc:
        result.append(item.as_dict())
    return HttpJSONResponse(result)

def boy_assign(request, codice_censimento):
    if not request.session.get('valid'):
        raise PermissionDenied()
    data = json.loads(request.body)
    boy = Rover.objects.get(codice_censimento=data['codice_censimento'])
    response_body = {}
    check_constraints

def boy_evaluate(request, codice_censimento):
    if not request.session.get('valid'):
        raise PermissionDenied()
    data = json.loads(request.body)
    boy = Rover.objects.get(codice_censimento=data['codice_censimento'])
    boy.turno

def persons(request):
    if not request.session.get('valid'):
        raise PermissionDenied()
    sc = Person.objects.all()
    result = []
    for item in sc:
        result.append(item.as_dict())
    return HttpJSONResponse(result)
