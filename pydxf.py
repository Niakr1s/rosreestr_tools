import ezdxf
from intersection import is_intersect


##dwg = ezdxf.new('R2000') # create R2000 drawing
##msp = dwg.modelspace() # add new entities to model space
##
##points = [(1,1),(3,1),(3,3),(2,4),(1,5),(1,1)]
##msp.add_lwpolyline(points)
##
##dwg.saveas('pydxf.dxf')

point = line_intersection(((1,2),(4,4)),((2,3),(3,1)))
print(point)
