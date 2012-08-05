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

import OSC
import pickle
from decimal import *

# class that holds all settings, saves and loads them
class settingsManager(object):

	# function called when object is created
	def __init__(self, filename):
		self.fileName = filename
		self.settingsDictionary = {}
		self.default = {}
	
	# function to get a certain setting
	def get(self, arg):
		return self.settingsDictionary[arg]
		
	# function to set a certain setting
	def set(self, name, value):
		self.settingsDictionary[name] = value
		print name,'changed to', value
		
	# function to load settings from disk
	def load(self):
		try:
			file = open(self.fileName, "rb")
			self.settingsDictionary = pickle.load(file)
			print self.fileName + ' loaded from disk'
		except:
			print 'Loading of ' + self.fileName + ' failed.'
			# load default values instead
			self.setDefaults()
		
	# function to save settings to disk
	def save(self):
		try:
			file = open(self.fileName, "wb") # write mode
			pickle.dump(self.settingsDictionary, file)
			file.close()
			print "Settings written to " +self.fileName
		except:
			print 'Could not write ' + self.fileName + ' to disk'
			
	# function to load the default values
	def setDefaults(self):
		self.settingsDictionary = self.default
		print 'Default values loaded'
		
	# function to return the whole dictionary of settings
	def returnSettings(self):
		return self.settingsDictionary
	
settings = settingsManager('settings.cfg')
# tuio proxy settings
settings.default['receiveAddress']					= '127.0.0.1'
settings.default['receivePort']						= 3332
settings.default['sendAddress']						= '127.0.0.1'
settings.default['sendPort']						= 3333
# remote control settings
settings.default['remoteIncomingPort']				= 3330
settings.default['remoteControlPort']				= 3331
settings.default['remoteControlAddress']			= '127.0.0.1'
# touch screen settings
settings.default['touchScreenAspect']				= (16.0/9.0)
settings.default['calibrationCenter']				= (0.5*(16.0/9.0),0.5)
# triangle settings
settings.default['tolerance']						= 0.008
settings.default['neededVotes']						= 1
settings.default['debugVotes']						= 0

# Position filter settings
settings.default['positionFilterActive']			= 0
# rotation filter settings
settings.default['rotationFilterPosition']			= 'off' #pre/post/off
settings.default['rotationLimit']					= 0.05 # limit in rad
# filter for tangible fingers settings
settings.default['tangibleCursorFilter']			= 'off' #on/off
# filter for real fingers arround tangible
settings.default['realFingerFilter']				= 'off' #on/off
settings.default['realFingerFilterRadius']			= 0.3 

settings.default['outOfJailCard']					= 3