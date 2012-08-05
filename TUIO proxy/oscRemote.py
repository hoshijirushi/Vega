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
import time, threading
from settings			import settings
from tangiblePattern	import tangibles

class remoteControlOverOSC(object):

	# function to start the OSC remote
	def start(self):	
		
		# setup ips and ports
		receiveAddress 		= '127.0.0.1'
		receivePort 		= settings.get('remoteIncomingPort')
		receive_settings 	= receiveAddress, 	receivePort
		
		# declare server
		self.oscServer 				= OSC.OSCServer(receive_settings)
		
		# declare message handlers
		self.oscServer.addMsgHandler("/vega/tangible"					, self.tangibleRegistration_handler)
		self.oscServer.addMsgHandler("/vega/ping"						, self.ping_handler)
		self.oscServer.addMsgHandler("/vega/settings"					, self.settings_handler)
		self.oscServer.addMsgHandler("/vega/requestForSettings"			, self.settingsRequest_handler)
		
		# start server thread
		self.oscServerThread = threading.Thread( target = self.oscServer.serve_forever )
		self.oscServerThread.start()
		
	# function to stop the OSC rermote
	def stop(self):
		print "Stopping remote OSC server"
		self.oscServer.close()
		print "Waiting for remote server thread to finish"
		self.oscServerThread.join()

	# function that is called when a message with settings are send to the proxy, also used to save settings to disk
	def settings_handler(self,addr, tags, stuff, source):
		if stuff[0] == 'save':
			settings.save()
		else:
			settings.set(stuff[0],stuff[1])
	
	# function that is called when the remote control program request the proxy settings
	def settingsRequest_handler(self,addr, tags, stuff, source):
		try:
			settingDict = settings.returnSettings()
			for key in settingDict:
				client = OSC.OSCClient()
				msg = OSC.OSCMessage()
				msg.setAddress("/vega/settings")
				msg.append(key)
				msg.append(settingDict[key])
				client.sendto(msg, (settings.get('remoteControlAddress'), settings.get('remoteControlPort')))

		except Exception, e:
			print 'Sending settings to control programm failed'
			print "Error:", e
	
	# function that is called when a tangible registration message has been send from the remote program
	def tangibleRegistration_handler(self,addr, tags, stuff, source):
		messageType = stuff[0]
		if messageType == 'register':
			print 'Register tangible request received'
			id = stuff[1]
			tangibles.registerNewTangible(id)
			
		elif messageType == 'delete':
			print 'Delete tangible request received'
			id = stuff[1]
			tangibles.deleteTangible(id)
			
		elif messageType == 'deleteAll':
			print 'Delete all tangibles request received'
			tangibles.deleteAllTangibles()
			
		elif messageType == 'saveToDisk':
			print 'Save to disk request received'
			tangibles.saveTangiblesToDisk()
	
	# function send an alive signal back to the remote program
	def ping_handler(self,addr, tags, stuff, source):
		
		# save address where ping came from
		pingSource = OSC.getUrlStr(source).split(':')[0]
		if settings.get('remoteControlAddress') != pingSource:
			settings.set('remoteControlAddress',pingSource)
		
		# read the port of the remote control programm from settings
		port = settings.get('remoteControlPort')
		
		# send pong message back
		client = OSC.OSCClient()
		msg = OSC.OSCMessage()
		msg.setAddress("/vega/pong")
		msg.append(1234)
		client.sendto(msg, (pingSource, port))

# create the remote control object
remote = remoteControlOverOSC()
