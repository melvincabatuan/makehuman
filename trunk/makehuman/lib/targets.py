#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Glynn Clements

**Copyright(c):**      MakeHuman Team 2001-2013

**Licensing:**         AGPL3 (see also http://www.makehuman.org/node/318)

**Coding Standards:**  See http://www.makehuman.org/node/165

Abstract
--------

TODO
"""

import os
import log

class Component(object):
    _cat_data = [
        ('gender',   ['male', 'female']),
        ('age',      ['child', 'young', 'old']),
        ('race',     ['caucasian', 'asian', 'african']),
        ('tone',     ['muscle', 'averageTone', 'flaccid']),
        ('weight',   ['light', 'averageWeight', 'heavy']),
        ('height',   ['dwarf', 'giant']),
        ('cup',      ['cup1', 'cup2']),
        ('firmness', ['firmness0', 'firmness1'])
        ]

    _cat_values = dict(_cat_data)
    _categories = [cat for cat, value in _cat_data]
    _value_cat = dict([(value, cat)
                       for cat, values in _cat_data
                       for value in values])
    del cat, value, values

    def __init__(self, other = None):
        self.path = None
        if other is None:
            self.key = []
            self.data = {}
        else:
            self.key = other.key[:]
            self.data = other.data.copy()

    def __repr__(self):
        return repr((self.key, self.data, self.path))

    def set_data(self, category, value):
        orig = self.data.get(category)
        if orig is not None and orig != value:
            raise RuntimeError('%s already set' % category)
        self.data = self.data.copy()
        self.data[category] = value

    def add_key(self, value):
        self.key.append(value)

    def clone(self):
        return Component(self)

    def update(self, value, last=False):
        category = self._value_cat.get(value)
        if category is not None:
            self.set_data(category, value)
        elif value == 'target':
            pass
        else:
            self.add_key(value)

    def finish(self, path):
        self.path = path
        for category in self._categories:
            if category not in self.data:
                self.data[category] = None
        if self.key in [['macrodetails', 'universal'], ['breast']]:
            if self.data['tone'] is None:
                self.data['tone'] = 'averageTone'
            if self.data['weight'] is None:
                self.data['weight'] = 'averageWeight'

class Targets(object):
    def __init__(self, root):
        self.targets = []
        self.groups = {}
        self.images = {}
        self.walk(root, Component())

    @staticmethod
    def is_fake(name, dirs):
        if name == 'caucasian':
            for race in ("asian", "african"):
                if race in dirs:
                    return False
            return True
        if name == 'female_young':
            for gender_age in ("male_child", "male_young", "male_old",
                               "female_child", "female_old"):
                    if gender_age in dirs:
                        return False
            return True
        return False

    def walk(self, root, base = None):
        dirs = os.listdir(root)
        xdirs = [dir.replace('-','_') for dir in dirs]
        for name in sorted(dirs):
            path = os.path.join(root, name).replace('\\','/')
            if os.path.isfile(path) and not path.lower().endswith('.target'):
                if path.lower().endswith('.png'):
                    self.images[name.lower()] = path
                continue
            item = base.clone()
            if not self.is_fake(name, xdirs):
                parts = name.replace('_','-').replace('.','-').split('-')
                if root.endswith('macrodetails') and parts[0] == 'neutral':
                    parts[0] = 'caucasian'
                for part in parts[:-1]:
                    item.update(part)
                item.update(parts[-1], True)
            if os.path.isdir(path):
                self.walk(path, item)
            else:
                item.finish(path)
                self.targets.append(item)
                key = tuple(item.key)
                if key not in self.groups:
                    self.groups[key] = []
                self.groups[key].append(item)

_targets = None

def getTargets():
    global _targets
    if _targets is None:
        _targets = Targets('data/targets')
    return _targets