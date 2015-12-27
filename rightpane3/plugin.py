from gi.repository import Gtk

from .config import Config
from .dialog import Dialog
from .panel import Panel, clone_image
from .menu import Menu


class Plugin:
    # ...
    def __init__(self, window):
        # ...
        self.window = window

        self.config = Config(
            window
        )

        self.panel = Panel(
            window,
            self.config,
            self
        )

        self.dialog = Dialog(
            window,
            self.config,
            self
        )

        self.menu = Menu(
            window,
            self.config,
            self.panel,
            self.dialog,
            self
        )

        self.lock, self.delete = False, False
        # ...
        self.window.connect("show", self.on_gedit_show)
        self.window.connect('delete-event', self.on_gedit_delete)

    def do_deactivate(self):
        self.config.do_deactivate()
        self.dialog.do_deactivate()
        self.panel.do_deactivate()
        self.menu.do_deactivate()
        # ...
        self.window = None
        self.config = None
        self.dialog = None
        self.menu = None
        self.panel = None

    def on_gedit_show(self, widget):
        """
        Store all tabs & restore on right pane
        """
        # ...
        self.panel.sidepane.restore_visibility()
        self.panel.sidepane.store_tabs()
        # ...
        self.panel.rightpane.restore_visibility()
        self.panel.rightpane.restore_tabs()
        # ...
        self.menu.set_manage_action_active()
        # ...
        self.dialog.build()
        # ...
        self.panel.sidepanenotebook.connect('page-added', self.on_page_added)
        self.panel.sidepanenotebook.connect(
            'page-removed', self.on_page_removed)

    def on_page_added(self, widget, page, position):
        """
        Observe plugins which are not yet loaded
        """
        if self.lock:
            return
        # ...
        sidepane = self.panel.sidepane.instance()
        sidepanenotebook = self.panel.sidepanenotebook.instance()
        get_activated_item = self.panel.get_activated_item
        activated_item = get_activated_item(sidepane, sidepanenotebook)
        labels = self.config.labels
        images = self.config.images
        items = self.config.items
        popup = self.dialog.popup
        add_tab = self.dialog.add_tab
        # ...
        sidepane.activate_item(page)
        img = clone_image(
            sidepane
            .get_children()[0]
            .get_children()[0]
            .get_children()[0]
            .get_children()[0]
            .get_children()[0]
        )
        text = sidepanenotebook.get_menu_label_text(page)
        # ...
        labels.append(text)
        images.append(img)
        items.append(page)

        if popup:
            add_tab(text, img, -1)

    def on_page_removed(self, widget, page, position):
        """
        When a plugin is removed from left panel, remove it also in popup
        """
        if not self.config:
            return
        # ...
        items = self.config.items
        labels = self.config.labels
        images = self.config.images
        index = items.index(page)
        popup_tab_list = self.dialog.popup_tab_list
        popup_tab_item = popup_tab_list.get_children()[index]

        # ..
        if (0 == items.count(page) or self.lock or self.delete):
            return
        items.remove(page)
        labels.pop(index)
        images.pop(index)
        try:
            popup_tab_list.remove(popup_tab_item)
        except IndexError:
            True

    def on_gedit_delete(self, widget=None, truc=None):
        """
        Must be done before deactivate all plugins
        """
        # ...
        if self.window:
            self.delete = True
            self.panel.set_right_activated_tab()
            self.panel.save_left_pane_visibility()
            self.config.save_prefs()
            self.panel.destroy_right_pane()

    def on_click_left(self, widget):
        """
        Transfer a left pane tab to the right pane
        """
        # ...
        if not widget.get_active():
            return
        # ...
        index = self.dialog.left_radios.index(widget)
        sidepane = self.panel.sidepane.instance()
        rightpane = self.panel.rightpane.instance()
        right_tab_indexes = self.config.right_tab_indexes
        # ...
        self.transfer_tab(rightpane, sidepane, index)
        right_tab_indexes.remove(str(index))
        # ...
        self.config.data.remove_option('rightpane', 'tab' + str(index))
        if 0 == len(right_tab_indexes):
            self.config.data.remove_option('rightpane', 'tabs')
        else:
            self.config.data.set(
                'rightpane', 'tabs', ','.join(right_tab_indexes))
        self.config.save_prefs()
        return

    def on_click_right(self, widget):
        """
        Transfer a right pane tab to the left pane
        """
        # ...
        if not widget.get_active():
            return
        # ...
        index = self.dialog.right_radios.index(widget)
        label = self.config.labels[index]
        # ...
        sidepane = self.panel.sidepane.instance()
        rightpane = self.panel.rightpane.instance()
        right_tab_indexes = self.config.right_tab_indexes

        # ...
        self.transfer_tab(sidepane, rightpane, index)
        right_tab_indexes.append(str(index))
        # ...
        self.config.data.set('rightpane', 'tab' + str(index), label)
        self.config.data.set('rightpane', 'tabs', ','.join(right_tab_indexes))
        self.config.save_prefs()
        return

    def transfer_tab(self, from_pane, to_pane, index):
        """
        Transfer a tab between panes
        """
        panel = self.config.items[index]
        label = self.config.labels[index]
        id = ''.join([panel.get_name(), label]).replace(' ', '')
        image = self.config.images[index]
        # ...
        self.lock = True
        # ..
        from_pane.remove_item(panel)
        to_pane.add_item(panel, id, label, image)
        to_pane.activate_item(panel)
        # ..
        self.lock = False
