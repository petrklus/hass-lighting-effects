import appdaemon.appapi as appapi

class VirtualLights(appapi.AppDaemon):
    
    presets = {
        "preset_1" : []
    }
    
    kelvin_gradients = {
        "default" : (1200, 5000), # candlelight to bright daylight
    }
    
    def initialize(self):
        if "preset_1" in self.args:
            self.log("Setting light modules..")         
            for device in self.split_device_list(self.args["preset_1"]):
                self.log("Adding light %s to preset_1" % device)         
                self.presets["preset_1"].append(device)
                
        self.run_at_sunrise(self.sunrise_cb, 0)
        self.run_at_sunset(self.sunset_cb, 0)
        self.log("Lights module test") 
          
        self.listen_state(self.sun_changed, "sun.sun")
    
    def sun_changed(self, entity, attribute, old, new, kwargs):
      self.log("TEST{} is {}".format(self.friendly_name(entity), new))
      print(entity)
      print(attribute)
      print(**kwargs)
      self.log("Elevation is {}".format(entity.elevation))
      
      # now recalculate color
      
      #self.notify("{} is {}".format(self.friendly_name(entity), new))
    
    def sunrise_cb(self, args, **kwargs):
        self.turn_on(self.args["off_scene"])
    
    def sunset_cb(self, args, **kwargs):
        self.turn_on(self.args["on_scene"])