# This example assumes we have a mesh object in edit-mode

import bpy
import bmesh
import math
import mathutils
import pprint

# Get the active mesh
obj = bpy.context.edit_object
# Or by name
#obj = bpy.data.objects["Landscape"]
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

path = []

currentIndex = 0
for i in range(side):
    #print ("Current vert")
    #pprint.pprint(vert)
    #bm.verts[i*(side+1)].co.z += dStep;   
    zDiffMin = 10000
    foundToEnd = 10000
    vert = bm.verts[currentIndex].co
    curToEnd = (end-vert).length
    oldIndex = currentIndex
        
    for (co, index, dist) in kd.find_range(vert, blockDist*5):
        zDiff = abs(vert.z-co.z)
        nextToEnd = (end-co).length
        print ("nextToEnd ", nextToEnd)
        #print ("index ", index)
        if (zDiff <= zDiffMin and nextToEnd < curToEnd and currentIndex != index 
            and nextToEnd < foundToEnd):
            foundToEnd = nextToEnd
            zDiffMin = zDiff
            currentIndex = index
            print ("currentIndex ", currentIndex)
    
    if (oldIndex != currentIndex):
        path.append(currentIndex)
    #bm.verts[currentIndex].co.z += dStep;       
    print (i)

startZ = bm.verts[path[0]].co.z
startZ = 1
for i in path:
    vert = bm.verts[i].co
    print ("Vertex ", i)
    for (co, index, dist) in kd.find_range(vert, blockDist*5):
        print ("Dist ", dist)
        #bm.verts[index].co.z = bm.verts[index].co.z*0.1+startZ*0.9
        bm.verts[index].co.z = bm.verts[index].co.z*dist+startZ*(1-dist)
        #bm.verts[index].co.z = 1
    startZ = bm.verts[index].co.z
                  
bmesh.update_edit_mesh(me, True)
