""" 
**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Thomas Larsson

**Copyright(c):**      MakeHuman Team 2001-2011

**Licensing:**         GPL3 (see also http://sites.google.com/site/makehumandocs/licensing)

**Coding Standards:**  See http://sites.google.com/site/makehumandocs/developers-guide

Abstract
Utility for making rig to MH characters.

For more info see: http://sites.google.com/site/makehumandocs/blender-export-and-mhx/making-rig

"""
bl_info = {
    "name": "Make Rig",
    "author": "Thomas Larsson",
    "version": "0.1",
    "blender": (2, 6, 1),
    "api": 40000,
    "location": "View3D > Properties > Make MH rig",
    "description": "Make rigs for MakeHuman characters",
    "warning": "",
    'wiki_url': '',
    "category": "MakeHuman"}


if "bpy" in locals():
    print("Reloading makerig")
    import imp
    imp.reload(main)
else:
    print("Loading makerig")
    import bpy
    import os
    from bpy.props import *
    from . import main
  
#
#    class MakeRigPanel(bpy.types.Panel):
#

Confirm = None
ConfirmString = "?"

def isInited(scn):
    global Confirm
    try:
        scn.MRDirectory
        Confirm
        return True
    except:
        return False
    


class MakeRigPanel(bpy.types.Panel):
    bl_label = "Make rig"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    
    @classmethod
    def poll(cls, context):
        return (context.object)

    def draw(self, context):
        global Confirm, ConfirmString
        layout = self.layout
        scn = context.scene
        if not isInited(scn):
            layout.operator("mhrig.init_interface", text="Initialize")
            return
        if Confirm:
            layout.label(ConfirmString)
            layout.operator(Confirm, text="yes")
            layout.operator("mhrig.skip")
            return
        layout.label("Initialization")
        layout.operator("mhrig.init_interface", text="ReInitialize")
        layout.operator("mhrig.factory_settings")
        layout.operator("mhrig.save_settings")

        layout.separator()
        layout.label("Weighting")      
        layout.prop(scn, "MRMakeHumanDir")
        layout.operator("mhrig.auto_weight_body")
        layout.operator("mhrig.auto_weight_helpers")
        layout.operator("mhrig.unvertex_diamonds")
        layout.operator("mhrig.unvertex_selected")
        layout.operator("mhrig.unvertex_all")

        layout.separator()
        layout.label("Export rig")      
        layout.prop(scn, "MRDirectory")
        layout.operator("mhrig.export_rig_file")

        layout.separator()
        layout.label("Licensing")
        layout.prop(scn, "MRAuthor")
        layout.prop(scn, "MRLicense")
        layout.prop(scn, "MRHomePage")
    
        return

#
#    Buttons
#

class OBJECT_OT_InitInterfaceButton(bpy.types.Operator):
    bl_idname = "mhrig.init_interface"
    bl_label = "Init"

    def execute(self, context):
        main.initInterface()
        main.readDefaultSettings(context)
        print("Interface initialized")
        return{'FINISHED'}    

class OBJECT_OT_FactorySettingsButton(bpy.types.Operator):
    bl_idname = "mhrig.factory_settings"
    bl_label = "Restore factory settings"

    def execute(self, context):
        main.initInterface()
        return{'FINISHED'}    

class OBJECT_OT_SaveSettingsButton(bpy.types.Operator):
    bl_idname = "mhrig.save_settings"
    bl_label = "Save settings"

    def execute(self, context):
        main.saveDefaultSettings(context)
        return{'FINISHED'}    

class OBJECT_OT_ExportRigFileButton(bpy.types.Operator):
    bl_idname = "mhrig.export_rig_file"
    bl_label = "Export Rig file"

    def execute(self, context):
        main.exportRigFile(context)
        return{'FINISHED'}    

class OBJECT_OT_AutoWeightBodyButton(bpy.types.Operator):
    bl_idname = "mhrig.auto_weight_body"
    bl_label = "Auto weight MH body"

    def execute(self, context):
        main.autoWeightBody(context)
        return{'FINISHED'}    

class OBJECT_OT_AutoWeightHelpersButton(bpy.types.Operator):
    bl_idname = "mhrig.auto_weight_helpers"
    bl_label = "Auto weight MH helpers"

    def execute(self, context):
        main.autoWeightHelpers(context)
        return{'FINISHED'}    

class VIEW3D_OT_UnvertexDiamondsButton(bpy.types.Operator):
    bl_idname = "mhrig.unvertex_diamonds"
    bl_label = "Unvertex diamonds"

    def execute(self, context):
        main.unVertexDiamonds(context)
        print("Diamonds unvertexed")
        return{'FINISHED'}    

class VIEW3D_OT_UnvertexSelectedButton(bpy.types.Operator):
    bl_idname = "mhrig.unvertex_selected"
    bl_label = "Unvertex selected"

    def execute(self, context):
        global Confirm, ConfirmString
        if not Confirm:
            Confirm = "mhrig.unvertex_selected"
            ConfirmString = "Really unvertex selected?"
            return{'FINISHED'}
        else:
            Confirm = None
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.object.vertex_group_remove_from(all=True)
        bpy.ops.object.mode_set(mode='OBJECT')
        print("Selected unvertexed")
        return{'FINISHED'}    

class VIEW3D_OT_UnvertexAllGroupsButton(bpy.types.Operator):
    bl_idname = "mhrig.unvertex_all"
    bl_label = "Unvertex all"

    def execute(self, context):
        global Confirm, ConfirmString
        if not Confirm:
            Confirm = "mhrig.unvertex_all"
            ConfirmString = "Really remove all vertex groups?"
            return{'FINISHED'}
        else:
            Confirm = None
        ob = context.object
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.vertex_group_remove(all=True)
        print("All vertex groups removed")
        return{'FINISHED'}    

class VIEW3D_OT_SkipButton(bpy.types.Operator):
    bl_idname = "mhrig.skip"
    bl_label = "No"

    def execute(self, context):
        global Confirm, ConfirmString
        print("Skipped:", ConfirmString)
        Confirm = None
        ConfirmString = "?"
        return{'FINISHED'}            

#
#    Init and register
#

def register():
    main.initInterface()
    bpy.utils.register_module(__name__)

def unregister():
    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    register()
