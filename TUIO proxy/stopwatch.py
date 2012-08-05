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

import time

class stopwatchClass(object):
	starttime		= 0
	laptime			= 0
	stoptime		= 0
	average			= 0
	averageSum		= 0
	averageCount	= 0
	averageMin		= 100.0
	averageMax		= 0
	
	def start(self):
		self.starttime = time.clock()
		self.laptime = self.starttime
		
	def stop(self):
		self.stoptime = time.clock()
		self.averageSum = self.averageSum + ((self.stoptime - self.starttime)*1000)
		self.averageCount = self.averageCount + 1

	def getTime(self):
		milliseconds = ((self.stoptime - self.starttime)*1000)
		print "%.5f milliseconds" % milliseconds
		return milliseconds
	
	def getLap(self):
		now = time.clock()
		milliseconds = ((now - self.laptime)*1000)
		print "Lap: %.5f milliseconds" % milliseconds
		
		self.averageSum = self.averageSum + milliseconds
		self.averageCount = self.averageCount + 1
		if 	(0 < milliseconds < self.averageMin):
			self.averageMin = milliseconds
			
		if 	milliseconds > self.averageMax:
			self.averageMax = milliseconds
		
		self.laptime = now
		return milliseconds

	def getAverage(self):
		average = self.averageSum / self.averageCount
		print "Average:", average, "Min:", self.averageMin, "Max:", self.averageMax
		return average
		
	def reset(self):
		self.starttime	= 0
		self.laptime	= 0
		self.stoptime	= 0
		
stopwatch = stopwatchClass()