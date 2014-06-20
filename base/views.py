import json
from django.shortcuts import render, get_object_or_404
from django.db import models
from django.core.context_processors import csrf
from django.core.exceptions import PermissionDenied
from django.db.models import Max

from base.models import *
from base.views_support import HttpJSONResponse

# Ok. It's horrible
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
    eh.event.name = data['name']
    eh.event.description = data['description']
    eh.event.kind = data['kind']
    eh.event.num = data['num']
    eh.event.district = _getDistrict(data.get('district'))
    eh.event.topic = _getTopic(data.get('topic'))
    eh.event.max_boys_seats = data['max_boys_seats']
    eh.event.max_chiefs_seats = data['max_chiefs_seats']
    eh.event.min_age = data['min_age']
    eh.event.max_age = data['max_age']
    eh.event.state_handicap = data['state_handicap']
    eh.event.state_chief = data['state_chief']
    eh.event.state_activation = data['state_activation']
    eh.event.state_subscription = data['state_subscription']
    eh.event.save()
    eh.save()
    result = {}
    return HttpJSONResponse(result)

def events(request):
    """
    Return all subscriptable events.

    """

    #NOTE: weird login check... as usual unfortunately
    if not request.session.get('valid'):
        rv = API_ERROR_response(u'non hai effettuato il login')
    else:
        events = []
        eh_qs = EventHappening.objects.all()
        for eh in eh_qs:
            obj = eh.as_dict()
            events.append(obj)
        rv = HttpJSONResponse(events)

    return rv


def units(request):

    # Units autocompletion -> no login required
    units = []
    for unit in Unit.objects.all():
        units.append(unit.name)

    return HttpJSONResponse(units)


def districts(request):

    result = []
    for item in District.objects.all():
        result.append(item.name)
    return HttpJSONResponse(result)


def timeslots(request):

    result = []
    for item in EventTimeSlot.objects.all():
        result.append(unicode(item))
    return HttpJSONResponse(result)

def topics(request):

    result = []
    for item in HeartBeat.objects.all():
        result.append(item.name)
    return HttpJSONResponse(result)
