from django.shortcuts import render

from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from base.views_support import HttpJSONResponse

from base.models import Rover, Event
from base.models.event import EventTurno1, EventTurno2, EventTurno3

import json

@csrf_exempt
@require_POST
def boy_evaluate(request, pk):

    if not request.user.is_staff or request.session.get('valid'):
        raise PermissionDenied()

    data = json.loads(request.body)
    rover = get_object_or_404(Rover, pk=pk)

    # Step 1: simulation of new labs assignment
    rover.turno1 = EventTurno1.objects.get(code=data[turn_name])
    rover.turno2 = EventTurno2.objects.get(code=data[turn_name])
    rover.turno3 = EventTurno3.objects.get(code=data[turn_name])

    # Step 2: check constraints

    msgs_constraints = rover.check_constraints()

    msgs_constraints['satisfaction'] = rover.calculate_satisfaction()

    return HttpJSONResponse(msgs_constraints)
    
    

