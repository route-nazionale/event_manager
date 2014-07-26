import json
from django.shortcuts import render, get_object_or_404
from django.db import models
from django.core.context_processors import csrf
from django.core.exceptions import PermissionDenied
from django.db.models import Max

import logging

from base.models import *
from base.models.base import *
from base.models.event import *
from base.views_support import HttpJSONResponse

logger = logging.getLogger('pippo')

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

def _getNextNum(k):
    try:
        return Event.objects.filter(kind=k).aggregate(Max('num'))['num__max'] + 1
    except:
        return 1

def _getTopic(v):
    result = HeartBeat.objects.filter(name=v)
    if result:
        return result[0]
    else:
        raise Exception()

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
    data['num'] = _getNextNum(data['kind'])

    district_code = data['district'].letter
    #logger.debug(data['district'].pk)
    code = "%s-%s-%s-%s" % (
        data['kind'],
        district_code,
        data['topic'].code,
        data['num']
    )
    data['code'] = code
    # logger.debug("[code] >> %s" % data['code'])

    seats_n_boys = data['seats_n_boys']
    data['seats_tot'] = data['max_boys_seats'] + data['max_chiefs_seats']
    del data['seats_n_boys']
    seats_n_chiefs = data['seats_n_chiefs']
    del data['seats_n_chiefs']
    event = Event.objects.create(**data)
    if data['kind'] == 'LAB':
        for timeslot in EventTimeSlot.objects.all():
            eh = EventHappening.objects.create(
                timeslot=timeslot,
                event=event,
                seats_n_boys=seats_n_boys,
                seats_n_chiefs=seats_n_chiefs
            )
    else:
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

    e = Event.objects.get(code=data['code'])
    e.print_code = data['print_code']
    e.name = data['name']
    e.description = data['description']          
    e.kind = data['kind']                                                               
    e.district = get_object_or_404(District, name=data.get('district'))
    e.topic = get_object_or_404(HeartBeat, name=data.get('topic'))
    e.max_boys_seats = data['max_boys_seats']          
    e.max_chiefs_seats = data['max_chiefs_seats']
    e.min_age = data['min_age']                                                         
    e.max_age = data['max_age']                                     
    e.state_handicap = data['state_handicap']                           
    e.state_chief = data['state_chief']
    e.state_activation = data['state_activation']     
 
    e.state_subscription = data['state_subscription']
    e.save()

    #KO: perche' qui e = Event non EventTurno1
    #KO: boys_qs = e.turno1_rover_set.all()
    boys_qs = EventTurno1.objects.get(pk=e.pk).turno1_rover_set.all()
    boys_qs.update(valido1=data['state_activation'] == Event.ACTIVATION_ACTIVE)

    assigned_boys = boys_qs.count()

    boys_qs = EventTurno2.objects.get(pk=e.pk).turno2_rover_set.all()
    boys_qs.update(valido2=data['state_activation'] == Event.ACTIVATION_ACTIVE)
    assigned_boys += boys_qs.count()
    
    boys_qs = EventTurno3.objects.get(pk=e.pk).turno3_rover_set.all()
    boys_qs.update(valido3=data['state_activation'] == Event.ACTIVATION_ACTIVE)
    
    assigned_boys +=  boys_qs.count()

    result = { 'msg' : 'Sono stati coinvolti nella modifica %s ragazzi.' % assigned_boys}
    return HttpJSONResponse(result)

def events(request):
    if not request.session.get('valid'):
        raise PermissionDenied()
    events = []
    eh_qs = EventHappening.objects.all()#.select_related()
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

def persons(request):
    if not request.session.get('valid'):
        raise PermissionDenied()
    sc = Person.objects.all()
    result = []
    for item in sc:
        result.append(item.as_dict())
    return HttpJSONResponse(result)
