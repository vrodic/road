# This example assumes we have a mesh object in edit-mode

import bpy
import bmesh
import math
import mathutils
import pprint

# Get the active mesh
#obj = bpy.context.edit_object
# Or by name
obj = bpy.data.objects["Landscape"]
me = obj.data


# Get a BMesh representation
bm = bmesh.from_edit_mesh(me)
bmesh.ops.triangulate(bm,faces=bm.faces)

nVerts = len(bm.verts)

#initialize kdtree
kd = mathutils.kdtree.KDTree(nVerts)

for i, v in enumerate(bm.verts):
    kd.insert(v.co, i)

kd.balance()


bm.faces.active = None

# Modify the BMesh, can do anything here...
start = bm.verts[0].co;
end = bm.verts[len(bm.verts)-1].co
distance = start - end
print("Distance start end")
pprint.pprint(distance)

#get distance between two blocks
blockDist = max(abs(bm.verts[1].co.x  - start.x), abs(bm.verts[1].co.y  - start.y)
, abs(bm.verts[1].co.z  - start.z)) 
print("Blockdist")
pprint.pprint(blockDist)

side = int(math.sqrt(nVerts))
print (side)

old = bm.verts[0].co
dStep = 0.5
dStep = 0.1

liftedVerts = {}

for i in range(side):

    vert = bm.verts[i*(side+1)].co
    print ("Current vert")
    pprint.pprint(vert)
    #bm.verts[i*(side+1)].co.z += dStep;   
    for (co, index, dist) in kd.find_range(vert, blockDist   ):
        if (liftedVerts.get(index) != True):
            liftedVerts[index] = True
            bm.verts[index].co.z +=dStep
            print("lifting    ", co, index, dist)
#    bm.verts[nVerts -1 -i].co.z +=dStep;   
    old = vert
    print (i)
    
#bm.verts[0].co.z -=1;
#bm.verts[16383].co.z -=1;


#for v in bm.verts:
#    pprint.pprint(v.co)
#    v.co.y += 1.0


# Show the updates in the viewport
# and recalculate n-gon tessellation.
bmesh.update_edit_mesh(me, True)
