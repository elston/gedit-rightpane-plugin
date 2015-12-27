from gi.repository import Gtk, Gedit


def clone_image(image):
    """
    Clone image
    """
    storage = image.get_storage_type()
    if storage == Gtk.ImageType.PIXBUF:
        return Gtk.Image.new_from_pixbuf(image.get_pixbuf())
    if storage == Gtk.ImageType.STOCK:
        img, size = image.get_stock()
        return Gtk.Image.new_from_stock(img, size)
    if storage == Gtk.ImageType.ICON_SET:
        img, size = image.get_icon_set()
        return Gtk.Image.new_from_icon_set(img, size)
    if storage == Gtk.ImageType.ANIMATION:
        return Gtk.Image.new_from_animation(image.get_animation())
    if storage == Gtk.ImageType.ICON_NAME:
        img, size = image.get_icon_name()
        return Gtk.Image.new_from_icon_name(img, size)
    return Gtk.Image().set_from_stock(Gtk.STOCK_NEW, Gtk.IconSize.MENU)

DEFAULT_WIDTH = 200


class Mainbox(object):

    __instance__ = None

    def __init__(self, window):
        self.__instance__ = window.get_child()

    def instance(self):
        return self.__instance__

    def remove(self, arg):
        self.instance().remove(arg)

    def pack_start(self, *arg):
        self.instance().pack_start(*arg)


class Firstpaned(object):

    __instance__ = None

    def __init__(self, window):
        # ...
        self.window = window
        self.__instance__ = window\
            .get_child()\
            .get_children()[2]

    def instance(self):
        return self.__instance__


class Sidepane(object):

    __instance__ = None

    def __init__(self, window, config):
        # ...
        self.__window__ = window
        self.__instance__ = window\
            .get_child()\
            .get_children()[2]\
            .get_child1()

        self.__config__ = config
        self.__notebook__ = self.__instance__\
            .get_child()\
            .get_children()[1]

    def window(self):
        return self.__window__

    def instance(self):
        return self.__instance__

    def notebook(self):
        return self.__notebook__

    def config(self):
        return self.__config__

    def restore_visibility(self):
        """
        Display the left pane only if preference option is True
        """
        if self.config().data.has_option('sidepane', 'visible'):
            if not self.config().data.getboolean('sidepane', 'visible'):
                self.window().get_ui_manager()\
                    .get_widget("/MenuBar/ViewMenu/ViewSidePaneMenu")\
                    .set_active(False)

    def get_activated_notebook_tab(self):

        for child in self.notebook().get_children():
            if self.instance().item_is_active(child):
                return child
        return None

    def store_tabs(self):

        activated_item = self.get_activated_notebook_tab()

        for child in self.notebook().get_children():
            self.instance().activate_item(child)

            text = self.notebook().get_menu_label_text(child)
            img = clone_image(
                self.instance()
                .get_children()[0]
                .get_children()[0]
                .get_children()[0]
                .get_children()[0]
                .get_children()[0]
            )
            # GtkImage

            self.config().items.append(child)
            self.config().labels.append(text)
            self.config().images.append(img)

        if activated_item:
            self.instance().activate_item(activated_item)


class SidepaneBox(object):

    __instance__ = None

    def __init__(self, window):
        # ...
        self.window = window
        self.__instance__ = window\
            .get_child()\
            .get_children()[2]\
            .get_child1()\
            .get_child()

    def instance(self):
        return self.__instance__


class SidepaneNotebook(object):

    __instance__ = None

    def __init__(self, window):
        # ...
        self.window = window
        self.__instance__ = window\
            .get_child()\
            .get_children()[2]\
            .get_child1()\
            .get_child()\
            .get_children()[1]

    def instance(self):
        return self.__instance__

    def connect(self, *arg):
        self.instance().connect(*arg)


class Secondpaned(object):

    __instance__ = None

    def __init__(self):
        self.__instance__ = Gtk.Paned(orientation=Gtk.Orientation.HORIZONTAL)

    def instance(self):
        return self.__instance__

    def show(self):
        self.instance().show()

    def pack1(self, *arg):
        self.instance().pack1(*arg)

    def pack2(self, *arg):
        self.instance().pack2(*arg)


class Rightpane(object):

    __instance__ = None

    def __init__(self, sidepane, window, config, plugin):
        self.__instance__ = Gedit.Panel()
        self.__config__ = config
        self.__window__ = window
        self.__plugin__ = plugin
        self.__sidepane__ = sidepane

    def instance(self):
        return self.__instance__

    def config(self):
        return self.__config__

    def window(self):
        return self.__window__

    def plugin(self):
        return self.__plugin__

    def sidepane(self):
        return self.__sidepane__

    def show(self):
        self.instance().show()

    def set_size_request(self, *arg):
        self.instance().set_size_request(*arg)

    def connect(self, *arg):
        self.instance().connect(*arg)

    def restore_tabs(self):
        """
        Restore right tabs using the preferences
        """

        sidepane = self.sidepane().instance()
        rightpane = self.instance()
        config = self.config()
        plugin = self.plugin()

        labels = config.labels
        load = config.load
        items = config.items
        labels = config.labels
        images = config.images
        right_tab_indexes = config.right_tab_indexes
        transfer_tab = plugin.transfer_tab
        activated_item = None

        length = len(labels)
        for i in range(length):
            index = length - i - 1

            if load.count(labels[index]) > 0:
                transfer_tab(sidepane, rightpane, index)

                config.data.set('rightpane', 'tab' + str(index), labels[index])
                right_tab_indexes.append(str(index))
                config.data.set(
                    'rightpane', 'tabs', ','.join(right_tab_indexes))

                if config.data.has_option('rightpane', 'tab-active'):
                    tab_active = config.data.get('rightpane', 'tab-active')
                    label = labels[index]

                    if tab_active == label:
                        activated_item = items[index]

        if activated_item:
            rightpane.activate_item(activated_item)

    def set_property(self, *arg):
        self.instance().set_property(*arg)

    def restore_visibility(self):
        if self.config().data.has_option('rightpane', 'visible'):
            if self.config().data.getboolean('rightpane', 'visible'):
                self.window().get_ui_manager()\
                    .get_widget("/MenuBar/ViewMenu/ViewRightSidePaneMenu")\
                    .set_active(True)


class RightpaneNotebook(object):

    __instance__ = None

    def __init__(self, rightpane):

        self.__rightpane__ = rightpane
        self.__instance__ = rightpane.instance()\
            .get_child()\
            .get_children()[1]

    def instance(self):
        return self.__instance__

    def connect(self, *arg):
        self.instance().connect(*arg)


class Panel(object):

    def __init__(self, window, config, plugin):

        self.__plugin__ = plugin
        self.__config__ = config
        self.__window__ = window

        self.mainbox = Mainbox(window)
        self.firstpaned = Firstpaned(window)
        self.sidepane = sidepane = Sidepane(window, config)
        self.sidepanebox = SidepaneBox(window)
        self.sidepanenotebook = SidepaneNotebook(window)

        self.secondpaned = Secondpaned()
        self.rightpane = Rightpane(sidepane, window, config, plugin)

        self.rightpanenotebook = RightpaneNotebook(self.rightpane)

        self.secondpaned.show()

        rightpane_wigth = DEFAULT_WIDTH
        if config.data.has_option('rightpane', 'width'):
            rightpane_wigth = config.data.getint('rightpane', 'width')
        self.rightpane.set_size_request(rightpane_wigth, -1)

        self.rightpane.connect('hide', self.on_close_right_pane)

        self.mainbox.remove(self.firstpaned.instance())

        self.secondpaned.pack1(self.firstpaned.instance(), True, True)
        self.secondpaned.pack2(self.rightpane.instance(), False, True)
        self.rightpane.connect('size_allocate', self.on_resize_rightpane)
        self.mainbox.pack_start(self.secondpaned.instance(), True, True, 0)

    def config(self):
        return self.__config__

    def window(self):
        return self.__window__

    def plugin(self):
        return self.__plugin__

    def get_activated_item(self, pane, notebook):
        """
        Return the activate tab of a gedit Panel
        """
        children = notebook.get_children()

        for child in children:
            if pane.item_is_active(child):
                return child
        return None

    def set_right_activated_tab(self):
        """
        Save the active right pane tab in prefs
        """
        notebook = self.rightpanenotebook.instance()
        len_children = len(notebook.get_children())
        rightpane = self.rightpane.instance()
        activated_item = self.get_activated_item(rightpane, notebook)
        config_data = self.config().data

        if activated_item:
            if len_children > 1:
                label = notebook.get_menu_label_text(activated_item)
                config_data.set('rightpane', 'tab-active', label)
        else:
            config_data.remove_option('rightpane', 'tab-active')

    def save_left_pane_visibility(self):
        """
        Some plugin activate the left pane by default,
        but maybe the user doesn't want to display it...
        """
        is_visible = self.window().get_ui_manager()\
            .get_widget("/MenuBar/ViewMenu/ViewSidePaneMenu")\
            .get_active()
        config = self.config()
        config_data = config.data

        config_data.set('sidepane', 'visible', str(is_visible))
        config.save_prefs()

    def destroy_right_pane(self):
        """
        Transfer all right tabs to the left pane & destroy the right pane
        """
        right_tab_indexes = self.config().right_tab_indexes
        transfer_tab = self.plugin().transfer_tab
        rightpane = self.rightpane.instance()
        sidepane = self.sidepane.instance()
        secondpaned = self.secondpaned.instance()
        firstpaned = self.firstpaned.instance()
        mainbox = self.mainbox.instance()

        for str_index in right_tab_indexes:
            try:
                index = int(str_index)
                transfer_tab(rightpane, sidepane, index)
            except IndexError:
                True

        secondpaned.remove(firstpaned)
        mainbox.remove(secondpaned)
        mainbox.add(firstpaned)

    def on_close_right_pane(self, pane):
        """
        Deactive the checkbox in the menu and set the preference option
        """

        window = self.window()
        if window:
            window.get_ui_manager()\
                .get_widget("/MenuBar/ViewMenu/ViewRightSidePaneMenu")\
                .set_active(False)

    def on_resize_rightpane(self, widget, size):
        """
        Save the right pane width
        """

        self.config().data.set('rightpane', 'width', str(size.width))
        self.config().save_prefs()

    def toggle_pane(self, toggleaction):
        """
        Display the right pane
        """

        is_visible = toggleaction.get_active()
        self.rightpane.set_property("visible", is_visible)

        self.config().data.set('rightpane', 'visible', str(is_visible))
        if not self.config().data.has_option('rightpane', 'init'):
            self.config().data.set('rightpane', 'init', 'True')
        self.config().save_prefs()

    def do_deactivate(self):
        pass
