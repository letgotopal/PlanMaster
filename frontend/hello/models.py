from django.db import models
import sys
sys.path.append("..")
from backend import ship

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
    # convert ship to model
    def read_bay(self,ship):
        for row in ship.bay:
            sr = self.shiprow_set.create()
            sr.read_row(row)
            sr.save()

    # convert model to ship
    def to_ship(self):

        grid_rows = self.shiprow_set.all()
        if grid_rows.count() == 0: return

        grid_cols = grid_rows[0].shipcell_set.all()
        if grid_cols.count() == 0: return

        out_ship = ship.Ship(
            r=grid_rows.count(),
            c=grid_cols.count(),
            bay=[[(cell.weight,cell.description) for cell in row.shipcell_set.all()] for row in grid_rows]
        )

        # recalculate heights
        out_ship.calculateColHeight()

        return out_ship


class Instruction(models.Model):
    start_x = models.IntegerField()
    start_y = models.IntegerField()
    end_x = models.IntegerField()
    end_y = models.IntegerField()
    description = models.CharField(max_length=255)
    instructionlist = models.ForeignKey('InstructionList',null=True,on_delete=models.CASCADE)

class InstructionList(models.Model):
    def read_trace(self,trace):
        for step in trace:
            # subject to change depending on format of trace
            s = self.instruction_set.create(
                start_x=step.lastMove[0][0],
                start_y=step.lastMove[0][1],
                end_x=step.lastMove[1][0],
                end_y=step.lastMove[1][1],
                description=step.bay[step.lastMove[1][0]][step.lastMove[1][1]][1]
            )

