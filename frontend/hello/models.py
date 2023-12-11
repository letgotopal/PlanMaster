from django.db import models

# Create your models here.
class ShipCell(models.Model):
    weight = models.IntegerField()
    description = models.CharField(max_length=255)
    shiprow = models.ForeignKey('ShipRow',null=True,on_delete=models.CASCADE)

class ShipRow(models.Model):
    shipgrid = models.ForeignKey('ShipGrid',null=True,on_delete=models.CASCADE)
    def read_row(self,row):
        for cell in row:
            c = self.shipcell_set.create(
                weight=cell[0],
                description=cell[1])
            
class ShipGrid(models.Model):
    def read_bay(self,ship):
        for row in ship.bay:
            sr = self.shiprow_set.create()
            sr.read_row(row)
            sr.save()

