from django.db import models

# Rover model should be here!
# Import always from here!
from base.models import Rover

class MyRover(Rover):

    class Meta:
        proxy = True
        verbose_name = 'ragazzo problematico'
        verbose_name_plural = 'ragazzi problematici'

