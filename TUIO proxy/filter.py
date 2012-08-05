# Vega - A TUIO proxy with the ability of tangible recognition
# Copyright (C) 2012 Thomas Becker
# contact: thomas.heinrich.becker@web.de

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import math
from settings			import settings

# filter for "errors" in the position recognition, not implemented anymore (not needed...)
class positionFilter(object):

	x = 0.0
	y = 0.0
	
	def addXvalue(self, x):
		self.x = x
		
	def addYvalue(self, y):
		self.y = y

	def getXstate(self):
		return self.x
		
	def getYstate(self):
		return self.y

# a simple low pass rotation filter class		
class rotationFilter(object):
	
	# function that is called when object is created
	def __init__(self):
		self.filterOutput = 0.0
	
	# function to limit the change in rotation
	def limitDifference(self, difference):
			rotationLimit = settings.get('rotationLimit')
			
			# limit rotation
			if difference > rotationLimit:
				difference = rotationLimit
		
			elif difference < -rotationLimit:
				difference = -rotationLimit
			
			# check if threshold is exceeded
			elif (-0.02 < difference < 0.02):
				difference = 0.0
							
			return difference
	
	# function to add a value to the low pass filter
	def addValue(self,externallyCalculatedRotation):
	
		change = self.radianDifference(self.filterOutput,externallyCalculatedRotation)
		
		change = self.limitDifference(change)
		result = self.filterOutput + change
		
		# check if zero or 2PI are crossed
		if result < 0:
			self.filterOutput = result + 2*math.pi
		elif result > (2*math.pi):
			self.filterOutput = result - 2*math.pi
		else:
			self.filterOutput = result
		
	# function returning the filter output value
	def getState(self):
		return float(self.filterOutput)
		
	# function returning the difference in radian
	def radianDifference(self, oldAngle, newAngle):
		difference = newAngle - oldAngle
		# check if tangible as been turned to the right over zero value
		if (2*(-math.pi)) < difference < -math.pi:
			difference += 2*math.pi
			
		# check if tangible as been turned to the left over zero value
		elif math.pi < difference <= 2*math.pi:
			difference -= 2*math.pi

		return difference	