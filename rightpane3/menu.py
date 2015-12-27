from gi.repository import Gtk

ui_str = """<ui>
<menubar name="MenuBar">
  <menu name="ViewMenu" action="View">
    <menuitem name="ViewRightSidePaneMenu" action="ViewRightSidePane"/>
    <separator/>
    <menuitem name="ManageRightSidePaneMenu" action="ManageRightSidePane"/>
  </menu>
</menubar>
</ui>
"""


class Menu:

    def __init__(self, window, config, panel, dialog, plugin):

        self.__window__ = window
        self.__config__ = config
        self.__panel__ = panel
        self.__dialog__ = dialog
        self.__plugin__ = plugin

        self.mainbox = window.get_child()
        self.menubar = self.mainbox.get_children()[0]
        self.menuitem = self.menubar.get_children()[2]
        self.menu = self.menuitem.get_submenu()

        self.toggle_action = Gtk.ToggleAction(
            name="ViewRightSidePane",
            label="Right Side Pane",
            tooltip="Right Pane",
            stock_id=None
        )

        self.manage_action = Gtk.Action(
            name="ManageRightSidePane",
            label="Manage Left & Right Panes",
            tooltip="Left & Right Pane Manager",
            stock_id=None
        )

        self.toggle_action.connect("toggled", lambda a: self.on_toggle_pane())
        self.manage_action.connect("activate", lambda a: self.on_dialog_show())

        self.action_group = Gtk.ActionGroup("RightPaneActionGroup1")
        self.action_group.add_toggle_actions([(
            "ViewRightSidePane",
            None,
            _("Right Side Pane"),
            "<Ctrl>F8",
            _("Right Pane"),
            self.on_toggle_pane
        )])
        self.action_group.add_action_with_accel(
            self.manage_action,
            "<Ctrl>F10"
        )

        manager = window.get_ui_manager()
        manager.insert_action_group(self.action_group, -1)
        self.ui_id = manager.new_merge_id()
        manager.add_ui_from_string(ui_str)
        manager.ensure_update()

        """
        Position the items in the view menu
        """
        items = self.menu.get_children()
        pos = len(items) - 2
        self.menu.reorder_child(items[pos - 2], 4)
        for i in range(2):
            self.menu.reorder_child(items[pos - i], 6)

    def config(self):
        return self.__config__

    def window(self):
        return self.__window__

    def dialog(self):
        return self.__dialog__

    def panel(self):
        return self.__panel__

    def set_manage_action_active(self):

        is_visible = False
        if self.config().data.has_option('rightpane', 'visible'):
            is_visible = self.config().data.getboolean('rightpane', 'visible')

    def on_dialog_show(self):
        self.dialog().show()

    def on_toggle_pane(self, toggleaction):
        self.panel().toggle_pane(toggleaction)
        self.set_manage_action_active()

    def do_deactivate(self):
        """
        Remove the right pane items in view menu
        """
        pass
