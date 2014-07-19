from django.shortcuts import render

from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from base.views_support import HttpJSONResponse

from base.models import Rover, Event

import json

@csrf_exempt
@require_POST
def boy_evaluate(request, pk):

    if not request.user.is_staff or request.session.get('valid'):
        raise PermissionDenied()

    data = json.loads(request.body)
    rover = get_object_or_404(Rover, pk=pk)

    # Step 1: simulation of new labs assignment

    for turn_name in 'turno1', 'turno2', 'turno3':

        if data.get(turn_name):
            event = Event.objects.get(code=data[turn_name])
        else:
            event = None

        # Setta turno1 turno2 turno3
        setattr(rover, turn_name, event)

    # Step 2: check constraints

    msgs_constraints = rover.check_constraints()

    msgs_constraints['satisfaction'] = rover.calculate_satisfaction()

    return HttpJSONResponse(msgs_constraints)
    
    

