#!/usr/bin/python
# -*- coding: utf-8 -*-
# We need this for gui controls

import gui3d, events3d
    
class AppShortcutEdit(gui3d.ShortcutEdit):
    def __init__(self, parent, position, method):
        gui3d.ShortcutEdit.__init__(self, parent, position, parent.app.getShortcut(method))
        self.method = method

    def onChanged(self, shortcut):
        if not self.app.setShortcut(shortcut[0], shortcut[1], self.method):
            self.setShortcut(self.app.getShortcut(self.method))

class ShortcutsTaskView(gui3d.TaskView):

    def __init__(self, category):
        gui3d.TaskView.__init__(self, category, 'Shortcuts')

        y = 80
        gui3d.GroupBox(self, [10, y, 9.0], 'Actions', gui3d.GroupBoxStyle._replace(height=80));y+=25
        gui3d.TextView(self, [18,y + 5, 9.2], "Undo");AppShortcutEdit(self, [68,y, 9.2], self.app.undo);y+=25
        gui3d.TextView(self, [18,y + 5, 9.2], "Redo");AppShortcutEdit(self, [68,y, 9.2], self.app.redo);y+=25
        y+= 10
        
        gui3d.GroupBox(self, [10, y, 9.0], 'Navigation', gui3d.GroupBoxStyle._replace(height=205));y+=25
        gui3d.TextView(self, [18,y + 5, 9.2], "Modelling");AppShortcutEdit(self, [68,y, 9.2], self.app.goToModelling);y+=25
        gui3d.TextView(self, [18,y + 5, 9.2], "Save");AppShortcutEdit(self, [68,y, 9.2], self.app.goToSave);y+=25
        gui3d.TextView(self, [18,y + 5, 9.2], "Load");AppShortcutEdit(self, [68,y, 9.2], self.app.goToLoad);y+=25
        gui3d.TextView(self, [18,y + 5, 9.2], "Export");AppShortcutEdit(self, [68,y, 9.2], self.app.goToExport);y+=25
        gui3d.TextView(self, [18,y + 5, 9.2], "Rendering");AppShortcutEdit(self, [68,y, 9.2], self.app.goToRendering);y+=25
        gui3d.TextView(self, [18,y + 5, 9.2], "Help");AppShortcutEdit(self, [68,y, 9.2], self.app.goToHelp);y+=25
        gui3d.TextView(self, [18,y + 5, 9.2], "Exit");AppShortcutEdit(self, [68,y, 9.2], self.app.stop);y+=25
        
        y = 80
        gui3d.GroupBox(self, [650, y, 9.0], 'Camera', gui3d.GroupBoxStyle._replace(height=380));y+=25
        gui3d.TextView(self, [658,y + 5, 9.2], "Turn left");AppShortcutEdit(self, [708,y, 9.2], self.app.rotateLeft);y+=25
        gui3d.TextView(self, [658,y + 5, 9.2], "Turn up");AppShortcutEdit(self, [708,y, 9.2], self.app.rotateUp);y+=25
        gui3d.TextView(self, [658,y + 5, 9.2], "Turn down");AppShortcutEdit(self, [708,y, 9.2], self.app.rotateDown);y+=25
        gui3d.TextView(self, [658,y + 5, 9.2], "Turn right");AppShortcutEdit(self, [708,y, 9.2], self.app.rotateRight);y+=25
        gui3d.TextView(self, [658,y + 5, 9.2], "Pan up");AppShortcutEdit(self, [708,y, 9.2], self.app.panUp);y+=25
        gui3d.TextView(self, [658,y + 5, 9.2], "Pan down");AppShortcutEdit(self, [708,y, 9.2], self.app.panDown);y+=25
        gui3d.TextView(self, [658,y + 5, 9.2], "Pan right");AppShortcutEdit(self, [708,y, 9.2], self.app.panRight);y+=25
        gui3d.TextView(self, [658,y + 5, 9.2], "Pan left");AppShortcutEdit(self, [708,y, 9.2], self.app.panLeft);y+=25
        gui3d.TextView(self, [658,y + 5, 9.2], "Zoom in");AppShortcutEdit(self, [708,y, 9.2], self.app.zoomIn);y+=25
        gui3d.TextView(self, [658,y + 5, 9.2], "Zoom out");AppShortcutEdit(self, [708,y, 9.2], self.app.zoomOut);y+=25
        gui3d.TextView(self, [658,y + 5, 9.2], "Front view");AppShortcutEdit(self, [708,y, 9.2], self.app.frontView);y+=25
        gui3d.TextView(self, [658,y + 5, 9.2], "Top view");AppShortcutEdit(self, [708,y, 9.2], self.app.topView);y+=25
        gui3d.TextView(self, [658,y + 5, 9.2], "Side view");AppShortcutEdit(self, [708,y, 9.2], self.app.sideView);y+=25
        gui3d.TextView(self, [658,y + 5, 9.2], "Reset view");AppShortcutEdit(self, [708,y, 9.2], self.app.resetView);y+=25

def load(app):
    category = app.getCategory('Settings')
    taskview = ShortcutsTaskView(category)
    print 'Shortcuts imported'

def unload(app):
    pass

