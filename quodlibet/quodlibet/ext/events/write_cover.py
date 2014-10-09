# Copyright 2005 Joe Wreschnig
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation

import os
import shutil

from gi.repository import Gtk

from quodlibet import config
from quodlibet.const import USERDIR
from quodlibet.plugins.events import EventPlugin


def get_path():
    out = os.path.join(USERDIR, "current.cover")
    return config.get("plugins", __name__, out)


def set_path(value):
    config.set("plugins", __name__, value)


class PictureSaver(EventPlugin):
    PLUGIN_ID = "Picture Saver"
    PLUGIN_NAME = _("Picture Saver")
    PLUGIN_DESC = _("The cover image of the current song is saved to a file.")
    PLUGIN_ICON = Gtk.STOCK_SAVE
    PLUGIN_VERSION = "0.21"

    def plugin_on_song_started(self, song):
        outfile = get_path()
        if song is None:
            try:
                os.unlink(outfile)
            except EnvironmentError:
                pass
        else:
            cover = song.find_cover()
            if cover is None:
                try:
                    os.unlink(outfile)
                except EnvironmentError:
                    pass
            else:
                f = file(outfile, "wb")
                f.write(cover.read())
                f.close()

    def PluginPreferences(self, parent):
        def changed(entry):
            fn = entry.get_text()
            try:
                shutil.move(get_path(), fn)
            except EnvironmentError:
                pass
            else:
                set_path(fn)

        hb = Gtk.HBox(spacing=6)
        hb.set_border_width(6)
        hb.pack_start(Gtk.Label(label=_("File:")), False, True, 0)
        e = Gtk.Entry()
        e.set_text(get_path())
        e.connect('changed', changed)
        hb.pack_start(e, True, True, 0)
        return hb