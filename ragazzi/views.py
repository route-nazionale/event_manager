from django.shortcuts import render

from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

import json

@csrf_exempt
@require_POST
def boy_evaluate(request, pk):

    if not request.user.is_staff or request.session.get('valid'):
        raise PermissionDenied()

    data = json.loads(request.body)
    boy = get_object_or_404(Rover, pk=pk)

