# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

# Project Name:        MakeHuman
# Product Home Page:   http://www.makehuman.org/
# Code Home Page:      http://code.google.com/p/makehuman/
# Authors:             Thomas Larsson
# Script copyright (C) MakeHuman Team 2001-2011
# Coding Standards:    See http://sites.google.com/site/makehumandocs/developers-guide


import bpy
from bpy.props import StringProperty, FloatProperty, IntProperty, BoolProperty, EnumProperty

from . import action

def initInterface(context):
    bpy.types.Scene.MhxBvhScale = FloatProperty(
        name="Scale", 
        description="Scale the BVH by this value", 
        min=0.0001, max=1000000.0, 
        soft_min=0.001, soft_max=100.0,
        default=0.65)

    bpy.types.Scene.MhxAutoScale = BoolProperty(
        name="Auto scale",
        description="Rescale skeleton to match target",
        default=True)

    bpy.types.Scene.MhxStartFrame = IntProperty(
        name="Start Frame", 
        description="Starting frame for the animation",
        default=1)

    bpy.types.Scene.MhxEndFrame = IntProperty(
        name="Last Frame", 
        description="Last frame for the animation",
        default=32000)

    bpy.types.Scene.MhxSubsample = IntProperty(
        name="Subsample", 
        description="Sample only every n:th frame",
        default=1)

    bpy.types.Scene.MhxDefaultSS = BoolProperty(
        name="Use default subsample",
        default=True)

    bpy.types.Scene.MhxRot90Anim = BoolProperty(
        name="Rotate 90 deg", 
        description="Rotate 90 degress so Z points up",
        default=True)

    bpy.types.Scene.MhxDoSimplify = BoolProperty(
        name="Simplify FCurves", 
        description="Simplify FCurves",
        default=True)

    bpy.types.Scene.MhxSimplifyVisible = BoolProperty(
        name="Only visible", 
        description="Simplify only visible F-curves",
        default=False)

    bpy.types.Scene.MhxSimplifyMarkers = BoolProperty(
        name="Only between markers", 
        description="Simplify only between markers",
        default=False)

    bpy.types.Scene.MhxApplyFixes = BoolProperty(
        name="Apply found fixes", 
        description="Apply found fixes",
        default=True)

    bpy.types.Scene.MhxPlantCurrent = BoolProperty(
        name="Use current", 
        description="Plant at current",
        default=True)

    bpy.types.Scene.MhxPlantLoc = BoolProperty(
        name="Loc", 
        description="Plant location keys",
        default=True)

    bpy.types.Scene.MhxPlantRot = BoolProperty(
        name="Rot", 
        description="Plant rotation keys",
        default=False)

    bpy.types.Scene.MhxErrorLoc = FloatProperty(
        name="Max loc error", 
        description="Max error for location FCurves when doing simplification",
        min=0.001,
        default=0.01)

    bpy.types.Scene.MhxErrorRot = FloatProperty(
        name="Max rot error", 
        description="Max error for rotation (degrees) FCurves when doing simplification",
        min=0.001,
        default=0.1)

    bpy.types.Scene.MhxDirectory = StringProperty(
        name="Directory", 
        description="Directory", 
        maxlen=1024,
        default='')

    bpy.types.Scene.MhxReallyDelete = BoolProperty(
        name="Really delete action", 
        description="Delete button deletes action permanently",
        default=False)

    bpy.types.Scene.MhxPrefix = StringProperty(
        name="Prefix", 
        description="Prefix", 
        maxlen=1024,
        default='')

    bpy.types.Scene.MhxActions = EnumProperty(
        items = [],
        name = "Actions")

    scn = context.scene
    if scn:
        scn['MhxPlantCurrent'] = True
        scn['MhxPlantLoc'] = True
        scn['MhxBvhScale'] = 0.65
        scn['MhxAutoScale'] = True
        scn['MhxStartFrame'] = 1
        scn['MhxEndFrame'] = 32000
        scn['MhxSubsample'] = 1
        scn['MhxDefaultSS'] = True
        scn['MhxRot90Anim'] = True
        scn['MhxDoSimplify'] = True
        scn['MhxSimplifyVisible'] = False
        scn['MhxSimplifyMarkers'] = False
        scn['MhxApplyFixes'] = True

        scn['MhxPlantLoc'] = True
        scn['MhxPlantRot'] = False
        scn['MhxErrorLoc'] = 0.01
        scn['MhxErrorRot'] = 0.1

        scn['MhxPrefix'] = "Female1_A"
        scn['MhxDirectory'] = "~/makehuman/bvh/Female1_bvh"
        scn['MhxReallyDelete'] = False
        action.listAllActions(context)
    else:
        print("Warning - no scene - scene properties not set")

    bpy.types.Object.MhxArmature = StringProperty()
    
    bpy.types.Object.MhxTogglePoleTargets = BoolProperty(default=True)
    bpy.types.Object.MhxToggleIkLimits = BoolProperty(default=False)
    bpy.types.Object.MhxToggleLimitConstraints = BoolProperty(default=True)


#
#    ensureInited(context):
#

def ensureInited(context):
    try:
        context.scene['MhxBvhScale']
        inited = True
    except:
        inited = False
    if not inited:
        initInterface(context)
    return

#
#    loadDefaults(context):
#

def loadDefaults(context):
    if not context.scene:
        return
    filename = os.path.realpath(os.path.expanduser("~/makehuman/mhx_defaults.txt"))
    try:
        fp = open(filename, "r")
    except:
        print("Unable to open %s for reading" % filename)
        return
    for line in fp:
        words = line.split()
        try:
            val = eval(words[1])
        except:
            val = words[1]
        context.scene[words[0]] = val
    fp.close()
    return

#
#    saveDefaults(context):
#    class VIEW3D_OT_MhxSaveDefaultsButton(bpy.types.Operator):
#

def saveDefaults(context):
    if not context.scene:
        return
    filename = os.path.realpath(os.path.expanduser("~/makehuman/mhx_defaults.txt"))
    try:

        fp = open(filename, "w")
    except:
        print("Unable to open %s for writing" % filename)
        return
    for (key,value) in context.scene.items():
        if key[:3] == 'Mhx':
            fp.write("%s %s\n" % (key, value))
    fp.close()
    return
