 # -*- coding: utf-8 -*-
"""Python e GTK 4: PyGObject Gtk.ListBox()."""

import gi

gi.require_version(namespace='Gtk', version='4.0')
gi.require_version(namespace='Adw', version='1')
from gi.repository import Gio, Gtk, Adw


def widget_vbox_01():
    vbox = Gtk.Box.new(orientation=Gtk.Orientation.VERTICAL, spacing=0)
    vbox.set_homogeneous(homogeneous=False)

    
    return vbox


def widget_stack_listbox():
    stack = Gtk.Stack.new()
    stack.set_transition_type(transition=Gtk.StackTransitionType.CROSSFADE)
    stack.set_transition_duration(duration=30)
      
    return stack
