
class SliderSettings(object):

    @property
    def INSTALLED_APPS(self):
        return super().INSTALLED_APPS + [
            'slider'
        ]

default = SliderSettings
