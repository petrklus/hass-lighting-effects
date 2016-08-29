import logging

# Import the device class from the component that you want to support
import homeassistant.util.color as color_util
from homeassistant.components.light import Light, ATTR_BRIGHTNESS, ATTR_COLOR_TEMP, ATTR_RGB_COLOR, ATTR_TRANSITION, ATTR_XY_COLOR, SUPPORT_BRIGHTNESS, SUPPORT_COLOR_TEMP, SUPPORT_RGB_COLOR, SUPPORT_TRANSITION, SUPPORT_XY_COLOR

# Home Assistant depends on 3rd party packages for API specific code.
#REQUIREMENTS = ['awesome_lights==1.2.3']

_LOGGER = logging.getLogger(__name__)

SUPPORT_VIRTUAL = (SUPPORT_BRIGHTNESS | SUPPORT_COLOR_TEMP | SUPPORT_RGB_COLOR |
                SUPPORT_TRANSITION | SUPPORT_XY_COLOR)

def setup_platform(hass, config, add_devices, discovery_info=None):
    """Setup the Awesome Light platform."""
    # # Validate passed in config
    # host = config.get(CONF_HOST)
    # username = config.get(CONF_USERNAME)
    # password = config.get(CONF_PASSWORD)
    #
    # if host is None or username is None or password is None:
    #     _LOGGER.error('Invalid config. Expected %s, %s and %s',
    #                   CONF_HOST, CONF_USERNAME, CONF_PASSWORD)
    #     return False
    #
    # # Setup connection with devices/cloud
    # hub = genericlights.Hub(host, username, password)
    #
    # # Verify that passed in config works
    # if not hub.is_valid_login():
    #     _LOGGER.error('Could not connect to GenericLight hub')
    #     return False
    #
    # Add devices    
    light_names = config.get("light_names")
    add_devices(GenericLight(light_name) for light_name in light_names)
    _LOGGER.info("Lights initialised")        
    


class GenericLight(Light):
    """Representation of an Awesome Light."""

    def __init__(self, light_name):
        """Initialize an GenericLight."""
        self.light_name = light_name
        self._brightness = 0
        self._is_on = False
        self._xy_color = 0.0, 0.0
    
    @property
    def name(self):
        """Return the display name of this light."""
        return self.light_name

    @property
    def brightness(self):
        """Brightness of the light (an integer in the range 1-255).

        This method is optional. Removing it indicates to Home Assistant
        that brightness is not supported for this light.
        """
        return self._brightness

    @property
    def supported_features(self):
        """Flag supported features."""
        return SUPPORT_VIRTUAL
    

    @property
    def xy_color(self):
        """Return the XY color value [float, float]."""
        return self._xy_color

    @property
    def rgb_color(self):
        """Return the RGB color value [int, int, int]."""
        return color_util.color_xy_brightness_to_RGB(*self._xy_color, self._brightness)

    @property
    def is_on(self):
        """Return true if light is on."""
        return self._is_on

    def turn_on(self, **kwargs):
        """Instruct the light to turn on.

        You can skip the brightness part if your light does not support
        brightness control.
        """
        
        if ATTR_XY_COLOR in kwargs:
            xycolor = kwargs[ATTR_XY_COLOR]
        elif ATTR_RGB_COLOR in kwargs:
            xycolor = color_util.color_RGB_to_xy(
                *(int(val) for val in kwargs[ATTR_RGB_COLOR]))
            kwargs.setdefault(ATTR_BRIGHTNESS, xycolor[2])
        else:
            xycolor = None
        
        self._brightness = kwargs.get(ATTR_BRIGHTNESS, 255)
        self._is_on = True
        _LOGGER.info("Light state changed: %s %s %s", *self.rgb_color)        
        

    def turn_off(self, **kwargs):
        """Instruct the light to turn off."""
        self._is_on = False

    def update(self):
        """Fetch new state data for this light.

        This is the only method that should fetch new data for Home Assistant.
        """
        pass


