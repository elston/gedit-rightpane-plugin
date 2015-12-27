import os
import os.path
import configparser

PREFS_PATH = os.path.dirname(__file__) + '/rightpane-prefs'


class Config(object):

    def __init__(self, window):

        self.window = window

        self.data = configparser.ConfigParser()
        self.right_tab_indexes, self.load = [], []

        self.items = []
        self.labels = []
        self.images = []

        # Load preferences
        self.data.read([PREFS_PATH, 'test.ini'])
        if not self.data.has_section('rightpane'):
            self.data.add_section('rightpane')

        if not self.data.has_section('sidepane'):
            self.data.add_section('sidepane')

        if self.data.has_option('rightpane', 'tabs'):
            for i in self.data.get('rightpane', 'tabs').split(','):
                if self.data.has_option('rightpane', 'tab' + i):
                    self.load.append(self.data.get('rightpane', 'tab' + i))
                    self.data.remove_option('rightpane', 'tab' + i)

    def save_prefs(self):
        """
        Save preferences
        """
        f = open(PREFS_PATH, 'w')
        self.data.write(f)
        f.close()

    def do_deactivate(self):
        pass
