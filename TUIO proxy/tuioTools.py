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
import threading
from settings 				import settings
from numberGenerator 		import numberGenerator
from tangiblePattern		import tangibles
from trianglePattern		import createTrianglesFromCursors
from stopwatch				import stopwatch
from geometricCalculations	import isPointInCircle

# a 2D cursor object
class two2dCur(object):
	
	# function called when object is created
	def __init__(self, *args, **kwargs):
	
		self.id 	= kwargs.get('id', 0)
		self.x 		= kwargs.get('x', 0.0)
		self.xRaw 	= kwargs.get('xRaw', 0.0)
		self.y 		= kwargs.get('y', 0.0)
		self.vX 	= kwargs.get('vX', 0)
		self.vY 	= kwargs.get('vY', 0)
		self.mA 	= kwargs.get('mA', 0)
		
	# function that makes the object printable
	def __repr__(self):
		return "ID: %s x: %s y: %s" % (self.id, self.x, self.y)

# a buffer to store all received TUIO cursors
class two2dCurBuffer(object):
	
	dictOfTuioCursors = {}
	
	# function to remove to all cursors from buffer if they are not in the argument of the function
	def cleanNonAliveCursors(self,*args):
		oldCursors = set(self.dictOfTuioCursors.keys())
		aliveCursors = set(args[0])
		cursorsToDelete = oldCursors-aliveCursors
		for c in list(cursorsToDelete):
			del self.dictOfTuioCursors[c]
	
	# function to remove all cursors with IDs provided in the argument
	def removeCursorsWithIDs(self,*args):
		cursorsToDelete = args[0]
		if cursorsToDelete != []:
			for c in cursorsToDelete:
				if c in self.dictOfTuioCursors:
					del self.dictOfTuioCursors[c]
			
	# function to add and change cursors in the buffer
	def setCursor(self, **kwargs):
		self.dictOfTuioCursors[kwargs.get('id')] = (two2dCur(id=kwargs.get('id'),x=kwargs.get('x'),
													xRaw=kwargs.get('xRaw'),y=kwargs.get('y'),
													vX=kwargs.get('vX'), vY=kwargs.get('vY'),
													mA=kwargs.get('mA')))
													
	# function to return the IDs of all cursors in the buffer
	def getCursorIDs(self):
		ids = self.dictOfTuioCursors.keys()
		return ids
		
	# function to return the number of alive cursors in the buffer
	def getNumberOfAliveCursors(self):
		number = len(self.dictOfTuioCursors)
		return number
		
	# function returning all objects in the buffer
	def getCursors(self):
		cursors = self.dictOfTuioCursors.values()
		return cursors

# an object that receives all tuio signals and deals with them
class tuioServerClass(object):

	# alive point vars
	alivePointCount = 0
	
	# the cursor buffer
	cursorBuffer = two2dCurBuffer()
	
	# bundles for TUIO messages, one for cursors, one for objects
	twoDcurBundle = OSC.OSCBundle()
	twoDobjBundle = OSC.OSCBundle()
	
	# connect the tangibles container function getAllCursorsInBuffer with buffer
	tangibles.registerCursorProvider(cursorBuffer.getCursors)

	# function to start the TUIO server
	def start(self):
		print "Starting OSC server"
		
		# setup ips and ports
		receiveAddress 	= settings.get('receiveAddress')
		receivePort 	= settings.get('receivePort')
		sendAddress 	= settings.get('sendAddress')
		sendPort 		= settings.get('sendPort')
	
		receive_settings 	= receiveAddress, 	receivePort
		send_settings		= sendAddress,		sendPort
		
		# declare server and client
		self.oscServer = OSC.OSCServer(receive_settings)
		self.oscClient = OSC.OSCClient()
		self.oscClient.connect(send_settings)
		
		# declare message handler
		self.oscServer.addMsgHandler("/tuio/2Dobj", self.twoDobj_handler)
		self.oscServer.addMsgHandler("/tuio/2Dcur", self.twoDcur_handler)
		
		# start server thread
		self.oscServerThread = threading.Thread( target = self.oscServer.serve_forever )
		self.oscServerThread.start()
	
	# function to stop the TUIO server
	def stop(self):
		print "Stopping OSC server"
		self.oscServer.close()
		
		print "Waiting for server thread to finish"
		self.oscServerThread.join()
		
	# function that is called when a message with "/tuio/2Dobj" is received
	def twoDobj_handler(self, addr, tags, payload, source):
				
		messageType = payload[0]
		
		if messageType == 'alive':
			#print "2Dobj ALIVE", tags, payload[1:]
			pass
		
		elif messageType == 'set':
			#print "2Dobj SET"
			pass
		
		elif messageType == 'fseq':
			#print "2Dobj FSEQ"
			pass

	# function that is called when a message with "/tuio/2Dcur" is received
	def twoDcur_handler(self,addr, tags, payload, source):
		#print "A"		
		messageType = payload[0]
		
		if messageType == 'alive':
			#start stopwatch
			#stopwatch.start()
			
			# save number of alive points
			self.alivePointCount = tags.count('i')
			# delete non alive point from cursor buffer
			cursorIDs = payload[1:]
			self.cursorBuffer.cleanNonAliveCursors(cursorIDs)
		
		elif messageType == 'set':
			# set 2Dcur in 2Dcur buffer
			self.cursorBuffer.setCursor(id = payload[1],
										x = payload[2]*settings.get('touchScreenAspect'),
										xRaw = payload[2],y = payload[3], vX = payload[4], vY = payload[5],
										mA = payload[6])
			#print "B"
			
		elif messageType == 'fseq':
			#check number of alive points
			if self.alivePointCount < 3:
				# create 2Dcur bundle with the points in the buffer
				self.addAliveIDsTo2DcurBundle()
				self.addCursorsTo2DcurBundle()
				self.addFseqTo2DcurBundle()
				# send 2Dcur bundle
				self.send2DcurBundle()
				# create empty 2Dobj message bundle
				self.addEmptyAliveTo2DobjBundle()
				self.addFseqTo2DobjBundle()
				# send 2Dobj bundle
				self.send2DobjBundle()
				
				#stopwatch.stop()
				#stopwatch.getAverage()
				
			else:
				cursorsOnScreen = self.cursorBuffer.getCursors()
					# compare registered tangible triangles with triangles created at the moment
					# calculate tangible postions and rotations
				tangibles.checkForKnownTriangles(cursorsOnScreen)

				
				# remove points belonging to recognized tangibles from 2Dcur buffer
				if (settings.get('tangibleCursorFilter') == 'on'):
					self.cursorBuffer.removeCursorsWithIDs(tangibles.getRecognizedCursors())

				# remove cursors that could be created by fingers touching the tangible
				if (settings.get('realFingerFilter') == 'on'):
					self.removeRealFingersAroundTangibles()
				
				# create 2Dcur bundle with the points in the buffer
				self.addAliveIDsTo2DcurBundle()
				self.addCursorsTo2DcurBundle()
				self.addFseqTo2DcurBundle()
				# send 2Dcur bundle
				self.send2DcurBundle()

				# create 2Dobj message bundle with all tangibles
				self.addAliveIDsTo2DobjBundle()
				self.addObjectsTo2DobjBundle()
				self.addFseqTo2DobjBundle()
				# send 2Dobj bundle
				self.send2DobjBundle()
				#print "H"
				#stopwatch.stop()
				#stopwatch.getAverage()

	# function to remove all cursors in a circle around the tangible
	def removeRealFingersAroundTangibles(self):
		radius = settings.get('realFingerFilterRadius')
		aspectCorrectionFactor = settings.get('touchScreenAspect')
		
		cursorsToDelete = []
		
		for tan in tangibles.getRecognizedTangibles():
			#get tangible position
			centerX = tan.position.x /aspectCorrectionFactor
			centerY = tan.position.y
						
			
			# check for all cursors in the 2DCur buffer if they are in a circle around the tangible center
			for cursor in self.cursorBuffer.getCursors():
				pointX = cursor.x /aspectCorrectionFactor
				pointY = cursor.y
				if isPointInCircle(centerX, centerY, radius, pointX, pointY, aspectCorrectionFactor):
					cursorsToDelete.append(cursor.id)
					
					
		self.cursorBuffer.removeCursorsWithIDs(cursorsToDelete)
	
	# function to add an initial alive message to the cursor bundle
	def addAliveIDsTo2DcurBundle(self):
		message = OSC.OSCMessage()
		message.setAddress("/tuio/2Dcur")
		message.append('alive')
		for id in self.cursorBuffer.getCursorIDs():
			message.append(id)
		self.twoDcurBundle.append(message)
	
	# function to add all cursors in the buffer to the cursor bundle
	def addCursorsTo2DcurBundle(self):
		# load the aspect correction to set the TUIO cursor x values back to a range between 0 and 1
		aspectCorrectionFactor = settings.get('touchScreenAspect')
		
		for cursor in self.cursorBuffer.getCursors():
			message = OSC.OSCMessage()
			message.setAddress("/tuio/2Dcur")
			message.append('set')
			message.append(cursor.id)
			message.append(cursor.x / aspectCorrectionFactor)
			message.append(cursor.y)
			message.append(cursor.vX)
			message.append(cursor.vY)
			message.append(cursor.mA)
			self.twoDcurBundle.append(message)
	
	# function to add a seqence message to the cursor bundle
	def addFseqTo2DcurBundle(self):
		message = OSC.OSCMessage()
		message.setAddress("/tuio/2Dcur")
		message.append('fseq')
		message.append(numberGenerator.newFseq())
		self.twoDcurBundle.append(message)
	
	# function to send the bundle of TUIO cursor messages over OSC
	def send2DcurBundle(self):
		self.oscClient.send(self.twoDcurBundle)
		self.twoDcurBundle = OSC.OSCBundle()

	# function to add an initial alive message to the object bundle
	def addAliveIDsTo2DobjBundle(self):
		message = OSC.OSCMessage()
		message.setAddress("/tuio/2Dobj")
		message.append('alive')
		for id in tangibles.getRecognizedTangibleIDs():
			message.append(id)
		self.twoDobjBundle.append(message)
		
	# function to create an empty 2d object bundle header
	def addEmptyAliveTo2DobjBundle(self):
		message = OSC.OSCMessage()
		message.setAddress("/tuio/2Dobj")
		message.append('alive')
		self.twoDobjBundle.append(message)
	
	# function to add all recognized objects in the buffer to the object bundle
	def addObjectsTo2DobjBundle(self):
		# load the aspect correction to set the TUIO cursor x values back to a range between 0 and 1
		aspectCorrectionFactor = settings.get('touchScreenAspect')
		
		for tan in tangibles.getRecognizedTangibles():
			message = OSC.OSCMessage()
			message.setAddress("/tuio/2Dobj")
			message.append('set')
			message.append(tan.id)									#s,id
			message.append(tan.id)									#marker Id
			message.append(tan.position.x / aspectCorrectionFactor)	#x
			message.append(tan.position.y)							#y
			message.append(tan.rotation)							#angle in radiant
			message.append(0.0)										#vX
			message.append(0.0)										#vY
			message.append(0.0)										#vA
			message.append(0.0)										#m
			message.append(0.0)										#rotation acceleration
			self.twoDobjBundle.append(message)
		
	# function to add a seqence message to the object bundle
	def addFseqTo2DobjBundle(self):
		message = OSC.OSCMessage()
		message.setAddress("/tuio/2Dobj")
		message.append('fseq')
		message.append(numberGenerator.newFseq())
		self.twoDobjBundle.append(message)
		
	# function to send the bundle of TUIO object messages over OSC
	def send2DobjBundle(self):
		self.oscClient.send(self.twoDobjBundle)
		self.twoDobjBundle = OSC.OSCBundle()
		
	# function to return all cursors curently in the 2D cursor buffer
	def getAllCursorsInBuffer(self):
		return self.cursorBuffer.values()
		
# creates an instance of the tuioServerClass that can be imported
tuioServer = tuioServerClass()