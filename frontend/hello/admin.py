from django.contrib import admin
from .models import ShipGrid,ShipRow,ShipCell,Instruction,InstructionList

# Register your models here.
admin.site.register(ShipGrid)
admin.site.register(ShipRow)
admin.site.register(ShipCell)
admin.site.register(Instruction)
admin.site.register(InstructionList)