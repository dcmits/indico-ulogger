from indico.core.plugins import IndicoPlugin
from addLogger import do_addLogger

class IndicoUserLoggerPlugin(IndicoPlugin):
    """Indico User Logger Plugin

    Logs login and logouts
    """
    configurable = False

    def init(self):
        super(IndicoUserLoggerPlugin, self).init()
        do_addLogger()


