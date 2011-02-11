#!/usr/bin/python
# -*- coding: utf-8 -*-
# You may use, modify and redistribute this module under the terms of the GNU GPL.

""" 
Mesh Subdivision Plugin.

**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Marc Flerackers

**Copyright(c):**      MakeHuman Team 2001-2010

**Licensing:**         GPL3 (see also http://sites.google.com/site/makehumandocs/licensing)

**Coding Standards:**  See http://sites.google.com/site/makehumandocs/developers-guide

"""

__docformat__ = 'restructuredtext'

import time
from aljabr import centroid
from fastmath import vmul3d, vadd3d, vavg2d, vavg2d4, vavg3d, vavg3d4
from animation3d import lerpVector

def createOriginalVert(object, v):
    
    o = object.createVertex(v.co[:])
    o.data = [v, [], set()] # original, faceVerts, edgeVerts
    
    return o
    
def initOriginalVert(v):
    
    v.co = v.data[0].co[:]
    
def updateOriginalVert(v):
    
    if not v.data[1] or not v.data[2]: # Joint vertex
        return
        
    if len(v.data[1]) == len(v.data[2]): # Inner vertex
        faceVertAvg = centroid([fv.co for fv in v.data[1]])
        edgeVertAvg = centroid([ev.co for ev in v.data[2]])
        n = len(v.data[1])
        v.co = vmul3d(vadd3d(vadd3d(faceVertAvg, vmul3d(edgeVertAvg, 2.0)), vmul3d(v.data[0].co, n - 3.0)), 1.0/n)
    else: # Outer vertex
        v.co = centroid([ev.co for ev in v.data[2] if len(ev.data) == 3]+[v.data[0].co])

def createFaceVert(object, f):
    
    v = object.createVertex(vavg3d4(f.verts[0].co, f.verts[1].co, f.verts[2].co, f.verts[3].co))
    object.faceVerts.append(v)
    v.data = f
    
    return v
    
def updateFaceVert(fv):
    
    fv.co = vavg3d4(fv.data.verts[0].co, fv.data.verts[1].co, fv.data.verts[2].co, fv.data.verts[3].co)

def createEdgeVert(object, edgeVerts, v1, v2, c):
    
    key = (v1.idx, v2.idx) if v1.idx < v2.idx else (v2.idx, v1.idx)
    
    if key in edgeVerts:
        v = edgeVerts[key]
        v.data.append(c)
    else:
        v = object.createVertex([0, 0, 0])
        object.edgeVerts.append(v)
        v.data = [v1, v2, c]
        edgeVerts[key] = v
        
    return v
    
def updateEdgeVert(ev):

    if len(ev.data) > 3: # Inner edge
        ev.co = vavg3d4(ev.data[0].co, ev.data[1].co, ev.data[2].co, ev.data[3].co)
    else: # Outer edge
        ev.co = vavg3d(ev.data[0].co, ev.data[1].co)

def createSubdivisionObject(scene, object):
    
    name = object.name + '.sub'
    
    subdivisionObject = scene.newObj(name)
    subdivisionObject.x = object.x
    subdivisionObject.y = object.y
    subdivisionObject.z = object.z
    subdivisionObject.rx = object.rx
    subdivisionObject.ry = object.ry
    subdivisionObject.rz = object.rz
    subdivisionObject.sx = object.sx
    subdivisionObject.sy = object.sy
    subdivisionObject.sz = object.sz
    subdivisionObject.visibility = object.visibility
    subdivisionObject.shadeless = object.shadeless
    subdivisionObject.pickable = object.pickable
    subdivisionObject.cameraMode = object.cameraMode
    subdivisionObject.solid = object.solid
    subdivisionObject.uvValues = []
    subdivisionObject.indexBuffer = []
    
    fg = subdivisionObject.createFaceGroup('subdivision')
    
    subdivisionObject.originalVerts = [createOriginalVert(subdivisionObject, v) for v in object.verts]
    subdivisionObject.faceVerts = []
    subdivisionObject.edgeVerts = []
        
    edgeVerts = {}
    
    # Create faces
    # v0  e0  v1
    # 
    # e3  c   e1
    #
    # v3  e2  v2
    for f in object.faces:
        
        if 'joint' in f.group.name:
            continue
        
        # Create centroid vertex
        c = createFaceVert(subdivisionObject, f)
        
        for v in f.verts:
            subdivisionObject.verts[v.idx].data[1].append(c)
        
        # Create edge vertices
        e0 = createEdgeVert(subdivisionObject, edgeVerts, f.verts[0], f.verts[1], c)
        e1 = createEdgeVert(subdivisionObject, edgeVerts, f.verts[1], f.verts[2], c)
        e2 = createEdgeVert(subdivisionObject, edgeVerts, f.verts[2], f.verts[3], c)
        e3 = createEdgeVert(subdivisionObject, edgeVerts, f.verts[3], f.verts[0], c)
        
        v0 = subdivisionObject.verts[f.verts[0].idx]
        v0.data[2].add(e0)
        v0.data[2].add(e3)
        v1 = subdivisionObject.verts[f.verts[1].idx]
        v1.data[2].add(e0)
        v1.data[2].add(e1)
        v2 = subdivisionObject.verts[f.verts[2].idx]
        v2.data[2].add(e1)
        v2.data[2].add(e2)
        v3 = subdivisionObject.verts[f.verts[3].idx]
        v3.data[2].add(e2)
        v3.data[2].add(e3)
        
        uv0 = object.uvValues[f.uv[0]]
        uv1 = object.uvValues[f.uv[1]]
        uv2 = object.uvValues[f.uv[2]]
        uv3 = object.uvValues[f.uv[3]]
        
        uvc = vavg2d4(uv0, uv1, uv2, uv3)
        uve0 = vavg2d(uv0, uv1)
        uve1 = vavg2d(uv1, uv2)
        uve2 = vavg2d(uv2, uv3)
        uve3 = vavg2d(uv3, uv0)
        
        fg.createFace(v0, e0, c, e3, [uv0, uve0, uvc, uve3])
        fg.createFace(e0, v1, e1, c, [uve0, uv1, uve1, uvc])
        fg.createFace(e3, c, e2, v3, [uve3, uvc, uve2, uv3])
        fg.createFace(c, e1, v2, e2, [uvc, uve1, uv2, uve2])
    
    for v in subdivisionObject.edgeVerts:
        updateEdgeVert(v)
    for v in subdivisionObject.originalVerts:
        updateOriginalVert(v)
    
    subdivisionObject.updateIndexBuffer()
    subdivisionObject.object = object.object
    subdivisionObject.texture = object.texture

    return subdivisionObject
    
def updateSubdivisionObject(object):
    
    for v in object.originalVerts:
        initOriginalVert(v)
    for v in object.faceVerts:
        updateFaceVert(v)
    for v in object.edgeVerts:
        updateEdgeVert(v)
    for v in object.originalVerts:
        updateOriginalVert(v)

def subdivide(object, scene):

    t = time.time()
    subdivisionObject = scene.getObject(object.name + '.sub')
    if subdivisionObject:
        print 'Sub data present'
        updateSubdivisionObject(subdivisionObject)
        print 'time for subdivision: %s' % (time.time() - t)
        t = time.time()
        subdivisionObject.calcNormals()
        print 'time for normals: %s' % (time.time() - t)
        subdivisionObject.update()
    else:
        print 'Calculating sub data'
        subdivisionObject = createSubdivisionObject(scene, object)
        print 'time for subdivision: %s' % (time.time() - t)
        t = time.time()
        subdivisionObject.calcNormals()
        print 'time for normals: %s' % (time.time() - t)
        scene.update()
    
