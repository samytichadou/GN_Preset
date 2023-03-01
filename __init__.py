'''
Copyright (C) 2018 Samy Tichadou (tonton)
samytichadou@gmail.com

Created by Samy Tichadou

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

bl_info = {
    "name": "GN Preset",
    "description": "",
    "author": "Samy Tichadou (tonton)",
    "version": (0, 1, 0),
    "blender": (3, 0, 0),
    "location": "",
    "wiki_url": "https://github.com/samytichadou/GN_Preset/blob/master/README.md",
    "tracker_url": "https://github.com/samytichadou/GN_Preset/issues/new",
    "category": "Mesh" }

# IMPORT SPECIFICS
##################################

from . import (
    properties,
    save_preset,
    load_preset,
    remove_preset,
    gui,
)


# register
##################################

def register():
    properties.register()
    save_preset.register()
    load_preset.register()
    remove_preset.register()
    gui.register()

def unregister():
    properties.unregister()
    save_preset.unregister()
    load_preset.unregister()
    remove_preset.unregister()
    gui.unregister()
