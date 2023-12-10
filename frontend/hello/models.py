from django.db import models

# Create your models here.

class ShipGrid(models.Model):
    def __init__(self):
        self.bay = None
    
    def read_bay(self,ship):
        self.bay = [[val for val in row] for row in ship.bay]