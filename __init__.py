# -*- coding: utf-8 -*-
################################################################################

from modules.core.props import Property, StepProperty
from modules.core.step import StepBase
from modules import cbpi
from modules.core.hardware import SensorPassive

################################################################################
@cbpi.sensor
class TrailingAverageSensor(SensorPassive):

	sensor = Property.Sensor("Sensor", description="Select a sensor to average readings of.")
	count = Property.Number("Count", configurable=True, default_value=5, description="Number of readings to average.")
	weighting = Property.Number("Weighting", configurable=True, default_value=0.75, description="Should be between 0 and 1. A value of 0.5 means each prior reading has half the weight of the next in sequence. A value of 1.0 is equivalent to no weighting.")
	decimals = Property.Number("Decimals", configurable=True, default_value=1, description="How many decimals to round the average to.")

	def init(self):
		self.values = list()

	def stop(self):
		pass

	def read(self):
		self.values.append(cbpi.cache.get("sensors")[self.sensor].instance.last_value)
		while len(self.values) > self.count:
			self.values.pop(0)
		numerator = 0.0
		denominator = 0.0
		weight = 1.0
		for value in reversed(self.values):
			numerator += value * weight
			denominator += weight
			weight = weight * self.weighting

		self.data_received(round(numerator/denominator, int(self.decimals)))

	def get_unit(self):
		return cbpi.cache.get("sensors")[self.sensor].instance.get_unit()
