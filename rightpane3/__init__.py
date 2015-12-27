'''
Copyright (C) 2009-2015 Tournier Guillaume (tournier.guillaume@gmail.com)
Den Elston (elsthon@gmail.com)
This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
'''

from gi.repository import GObject, Gtk, Gedit
from .plugin import Plugin


class RightPanePlugin(GObject.Object, Gedit.WindowActivatable):

    __gtype_name__ = "RightPane3Plugin"
    window = GObject.property(type=Gedit.Window)

    def __init__(self):
        GObject.Object.__init__(self)
        self._instances = {}

    def _get_instance(self):
        return self._instances.get(self.__gtype_name__)

    def _set_instance(self, instance):
        self._instances[self.__gtype_name__] = instance

    def do_activate(self):
        self._set_instance(Plugin(self.window))

    def do_deactivate(self):
        self._get_instance().do_deactivate()
        self._set_instance(None)
