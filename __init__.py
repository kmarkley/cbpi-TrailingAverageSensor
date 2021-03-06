# -*- coding: utf-8 -*-
################################################################################

from modules import cbpi
from modules.core.props import Property
from modules.core.hardware import SensorPassive

################################################################################
@cbpi.sensor
class TrailingAverageSensor(SensorPassive):
    sensor_prop = Property.Sensor("Sensor", description="Select a sensor to average readings of.")
    count_prop = Property.Number("Count", configurable=True, default_value=12, description="Number of readings to average.")
    decimals_prop = Property.Number("Decimals", configurable=True, default_value=1, description="How many decimals to round the average to.")

    #-------------------------------------------------------------------------------
    def init(self):
        self.values = list()
        self.sensor_id = int(self.sensor_prop)
        self.count = int(self.count_prop)
        self.weight = 1.0/self.count
        self.decimals = int(self.decimals_prop)

    #-------------------------------------------------------------------------------
    def read(self):
        self.values.append(float(cbpi.cache.get("sensors")[int(self.sensor_id)].instance.last_value))
        while len(self.values) > self.count:
            self.values.pop(0)
        numerator = 0.0
        denominator = 0.0
        weight = 1.0
        for value in reversed(self.values):
            numerator += value * weight
            denominator += weight
            weight = weight - self.weight
        self.data_received(round(numerator/denominator, self.decimals))

    #-------------------------------------------------------------------------------
    def get_unit(self):
        return cbpi.cache.get("sensors")[int(self.sensor_id)].instance.get_unit()

    #-------------------------------------------------------------------------------
    def stop(self):
        pass
