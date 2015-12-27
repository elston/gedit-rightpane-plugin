from gi.repository import Gtk
from .panel import clone_image


class Dialog(object):

    def __init__(self, window, config, plugin):

        self.window = window
        self.config = config
        self.plugin = plugin

        self.popup = None
        self.popup_tab_list = None

        self.left_radios, self.right_radios = [], []

    def build(self):
        """
        Build popup elements
        """
        self.popup = Gtk.Window(type=Gtk.WindowType.TOPLEVEL)
        self.popup_tab_list = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        paddingH = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        paddingV = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        self.popup.set_title("Left-Right Pane Manager (Ctrl+F10)")
        self.popup.set_position(Gtk.WindowPosition.CENTER)
        self.popup.set_destroy_with_parent(True)
        self.popup.set_deletable(True)
        self.popup.set_icon_name(Gtk.STOCK_PREFERENCES)
        self.popup.connect('delete_event', self.on_close, None)

        paddingH.show()
        paddingV.show()

        self.popup_tab_list.show()

        paddingH.pack_start(paddingV, True, True, 15)
        paddingV.pack_start(self.popup_tab_list, True, True, 15)

        self.popup.add(paddingH)

        index = 0
        for lbl in self.config.labels:
            self.add_tab(lbl, self.config.images[index], index)
            index += 1

    def add_tab(self, text, img, index):
        """
        Tab line info in popup
        """
        right_tab_indexes = self.config.right_tab_indexes

        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        box.set_homogeneous(False)
        box.show()
        self.popup_tab_list.pack_start(box, False, True, 5)
        img = clone_image(img)
        img.show()
        box.pack_start(img, False, True, 5)
        label = Gtk.Label(label=text)
        label.set_alignment(0, 0.5)
        label.show()
        box.pack_start(label, True, True, 5)
        box2 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        box2.set_homogeneous(True)
        box2.show()
        box.pack_start(box2, False, True, 0)

        # left
        left = Gtk.RadioButton(group=None, label='Left')
        left.show()
        self.left_radios.append(left)

        # ON_CLICK_LEFT
        left.connect('toggled', self.plugin.on_click_left)
        box2.pack_start(left, True, True, 5)

        # right
        right = Gtk.RadioButton(group=left, label='Right')
        right.show()
        if right_tab_indexes.count(str(index)) > 0:
            right.set_active(True)
        self.right_radios.append(right)

        # ON_CLICK_RIGHT
        right.connect('toggled', self.plugin.on_click_right)
        box2.pack_start(right, True, True, 5)

    def show(self):
        """
        Left-right pane manager
        """
        if self.popup:
            self.popup.show()

        if not self.config.data.has_option('rightpane', 'init'):
            self.config.data.set('rightpane', 'init', 'True')

    def on_close(self, widget, event, data=None):
        """
        Don't destroy the popup. Just hide it.
        """
        self.popup.hide()
        return True

    def do_deactivate(self):
        pass
