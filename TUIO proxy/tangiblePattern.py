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

from trianglePattern 		import createTrianglesFromCursors, compareTriangles
from settings				import settings
from geometricCalculations	import pointVector, clockwiseDifferenceBetweenAngles, calcClockWiseAngle, rotateVector
from filter					import rotationFilter, positionFilter
import pickle

# class for the cursors a tangible consists of
class tangibleCursor(object):
	# declare variables
	lastKnownPositionX	= 0.0
	lastKnownPositionY	= 0.0
	lastLiveID			= 0
	offsetFromCenterX	= 0.0
	offsetFromCenterY	= 0.0
	votes = 0

	# function to make the object writable to disk
	def __getstate__(self):
		return self.__dict__
	
	# function to make the object loadable from disk
	def __setstate__(self, d):
		self.__dict__.update(d)

	# function to initalize the tangible point with values from the arguments
	def __init__(self, *args, **kwargs):
		self.id = kwargs.get('id', 0)
		self.x = kwargs.get('x', 0.0)
		self.y = kwargs.get('y', 0.0)
	
	# function calculating the poinst offset from the calibration center
	def calcOffset(self, calibrationCenter):
		self.offsetFromCenterX = self.x - calibrationCenter.x
		self.offsetFromCenterY = self.y - calibrationCenter.y
	
	# function to increase the votes to a point by one
	def vote(self):
		self.votes = self.votes + 1
		
	# function to return the points votes
	def getVotes(self):
		return self.votes
		
	# function to dump the points votes
	def deleteVotes(self):
		self.votes = 0
	
	# function returning the last live cursor id associated with this tangible cursor
	def getLastLiveID(self):
		return self.lastLiveID
	
	# function to print the points votes, position and offset from center
	def prettyPrint(self):		
		print 'ID:', self.id,'Votes:',self.votes , 'Position x:',self.x,'y:',self.y, 'Offset from center', self.offsetFromCenterX, self.offsetFromCenterY

# class defining a tangible
class tangible(object):
	
	# function called when object is created
	def __init__(self):
		
		self.id					= 0
		self.position			= pointVector()
		self.rotation			= 0.0
		self.outOfJailCard		= 2
		self.tangibleCursors		= {}
		self.tangibleTriangles	= []
		self.currentlyRecognized = False
		self.lastSuccesfulRunIDs = []
		self.externalIDtoTangibleCursorIDdict = {}
		self.externalIDtoTangibleCursorIDdictReverse = {}
		
		self.tangiblePositionFilter = positionFilter()
		self.tangibleRotationFilter = rotationFilter()
	
	# function to set the tangible up with the cursors in the argument
	def registerCursors(self, *args,**kwargs):
		self.id = kwargs.get('id', 0)
		cursors = args[0]
		
		# set the center for tangible creation, if not provdided otherwise
		calibrationCenter = pointVector(settings.get('calibrationCenter')[0],settings.get('calibrationCenter')[1])
		
		# add points to dictionary
		for c in cursors:
				self.tangibleCursors[c.id] = tangibleCursor(x=c.x,y=c.y)
				self.tangibleCursors[c.id].calcOffset(calibrationCenter)
		# create triangles from points	
		self.tangibleTriangles = createTrianglesFromCursors(cursors)
	
	# function to vote for points with a IDs in argument
	def voteForIDs(self, arg):
		for id in arg:
			self.tangibleCursors[id].vote()
	
	# function to delete the votes of every tangible point
	def dropVotes(self):
		for id in self.tangibleCursors.keys():
			self.tangibleCursors[id].deleteVotes()
	
	# function to retrieve the tangible cursor id that belongs to a live cursor 
	def externalIDtoTangibleCursorID(self, externalID):
		if externalID in self.externalIDtoTangibleCursorIDdict:
			tangibleCursorID = self.externalIDtoTangibleCursorIDdict[externalID]
			return tangibleCursorID
		else:
			return []
	
	# function to link live cursors with tangible cursors
	def combineExternalIdWithTangibleCursorID(self, externalID, tangibleCursorID):
		try:
			# if one entry(exID) already has this entry (curID)
			if tangibleCursorID in self.externalIDtoTangibleCursorIDdictReverse:
				# delete this entry
				# get the key the normal dictionary has
				externalIDtoDelete = self.externalIDtoTangibleCursorIDdictReverse[tangibleCursorID]
				# delete this entry
				del self.externalIDtoTangibleCursorIDdict[externalIDtoDelete]
				# delete also in the inverse dict
				del self.externalIDtoTangibleCursorIDdictReverse[tangibleCursorID]

			if externalID in self.externalIDtoTangibleCursorIDdict:
				tangibleCursorIDtoDelete = self.externalIDtoTangibleCursorIDdict[externalID]
				del self.externalIDtoTangibleCursorIDdictReverse[tangibleCursorIDtoDelete]
				del self.externalIDtoTangibleCursorIDdict[externalID]
		
			self.externalIDtoTangibleCursorIDdict[externalID] = tangibleCursorID
			self.externalIDtoTangibleCursorIDdictReverse[tangibleCursorID] = externalID

		except Exception, e:
			print "Failure: %s" % e
			print 'Error in combineExternalIdWithTangibleCursorID'
	
	
		
	
	# function to retrieve the last live id belonging to tangible cursor
	def tangibleCursorIDtoExternalID(self, tangibleCursorID):
		if tangibleCursorID in self.externalIDtoTangibleCursorIDdictReverse:
			externalID = self.externalIDtoTangibleCursorIDdictReverse[tangibleCursorID]
			return externalID
		else:
			return []	
		
	# function to set update the last position where a set of tangible cursors has been seen
	def setLastKnownPositions(self, ids, triangle):
		self.tangibleCursors[ids[0]].lastKnownPositionX = triangle.v1.x
		self.tangibleCursors[ids[0]].lastKnownPositionY = triangle.v1.y
		self.combineExternalIdWithTangibleCursorID(triangle.v1.id, ids[0])
		self.tangibleCursors[ids[0]].lastLiveID			= triangle.v1.id
		
		self.tangibleCursors[ids[1]].lastKnownPositionX = triangle.v2.x
		self.tangibleCursors[ids[1]].lastKnownPositionY = triangle.v2.y
		self.combineExternalIdWithTangibleCursorID(triangle.v2.id, ids[1])
		self.tangibleCursors[ids[1]].lastLiveID			= triangle.v2.id
		
		self.tangibleCursors[ids[2]].lastKnownPositionX = triangle.v3.x
		self.tangibleCursors[ids[2]].lastKnownPositionY = triangle.v3.y
		self.combineExternalIdWithTangibleCursorID(triangle.v3.id, ids[2])
		self.tangibleCursors[ids[2]].lastLiveID			= triangle.v3.id
	
	# function to compare momentary triangles with the triangles defining the pattern
	def compareTangibleTrianglesAndExternalTriangles(self, *args):
		self.externalCursors = args[0]
		# create all possible triangles from received cursors
		externalTriangles = createTrianglesFromCursors(self.externalCursors)
		
		tolerance = settings.get('tolerance')
		
		for externalTriangle in externalTriangles:
			for internalTriangle in self.tangibleTriangles:
		
				if compareTriangles(externalTriangle,internalTriangle,tolerance):
					# set last known position of tangible cursors and vote for them
					ids = internalTriangle.getIDs()
					self.setLastKnownPositions(ids, externalTriangle)
					self.voteForIDs(ids)
		
		# sort points by their received votes
		sortedKeys = []
		for key, value in sorted(self.tangibleCursors.iteritems(), key=lambda (k,v): (v.votes,k), reverse=True):
			sortedKeys.append(key)
		

		# check if their have been enough votes
		highestVotes	= self.tangibleCursors[sortedKeys[1]].votes
		neededVotes		= settings.get('neededVotes')
		if settings.get('debugVotes'):
			print "Highest",	highestVotes
			print "Needed",		neededVotes
		
		if highestVotes >= neededVotes:
			self.currentlyRecognized = True
			self.outOfJailCard = settings.get('outOfJailCard')
			
			self.lastSuccesfulRunIDs = []
			for tangibleCursorID in sortedKeys:
				oneSuccessful = self.tangibleCursorIDtoExternalID(tangibleCursorID)
				if oneSuccessful != []:
					self.lastSuccesfulRunIDs.append(oneSuccessful)
			
			# calculate tangible postion and rotation with best recognized cursors
			id1 = sortedKeys[0]
			id2 = sortedKeys[1]
			self.calculateTangiblePositionAndRotation(id1,id2)
			
		else:
			#compare current live IDs with last succeful recognized IDs
			liveIDs = []
			for externalCursor in self.externalCursors:
				liveIDs.append(externalCursor.id)
			try:
				cursorIntersection = filter(set(liveIDs).__contains__, self.lastSuccesfulRunIDs)
			except Exception, e:
				print "Failure: %s" % e
				print "liveIDs", liveIDs
				print "LSFR", self.lastSuccesfulRunIDs
			
			
			#check if at least two cursors are left
			if len(cursorIntersection) > 1:
				self.currentlyRecognized = True
				self.outOfJailCard = settings.get('outOfJailCard')
				
				# take first two live ids and calculate with them
				id1 = cursorIntersection[0]
				id2 = cursorIntersection[1]
				self.calculateTangiblePositionAndRotationWithLiveIDs(id1,id2)
				
			else:
				# to prevent single "glitches" from disturbing the signal the tangible has some out of jail cards
				if self.outOfJailCard > 0:
					self.outOfJailCard -= 1
					self.currentlyRecognized = True
				else:
					self.currentlyRecognized = False
					if settings.get('debugVotes'):
						print 'No match for ID:', self.id		
				
		self.dropVotes()


	# function to calculate the current position and rotation out of two known tangible cursors
	def calculateTangiblePositionAndRotationWithLiveIDs(self,id1,id2) :
		
		#translate from live ID to internal ID
		internalCursorID1 = self.externalIDtoTangibleCursorID(id1)
		internalCursorID2 = self.externalIDtoTangibleCursorID(id2)
		
		# create dictionary with live cursors

		liveCursors = {}
		for c in self.externalCursors:
			liveCursors[c.id] = c

		# calculate original rotation angle
		p1old = pointVector(self.tangibleCursors[internalCursorID1].offsetFromCenterX, self.tangibleCursors[internalCursorID1].offsetFromCenterY)
		p2old = pointVector(self.tangibleCursors[internalCursorID2].offsetFromCenterX, self.tangibleCursors[internalCursorID2].offsetFromCenterY)
		rotationAngleInCenteredTangible = calcClockWiseAngle(p1old,p2old)
		
		# calculate the current angle
		
		p1now = pointVector(liveCursors[id1].x, liveCursors[id1].y)
		p2now = pointVector(liveCursors[id2].x, liveCursors[id2].y)
		rotationAngleOfTangibleNow = calcClockWiseAngle(p1now, p2now);   
		
		# calculate the difference between the two angles
		currentRotation = clockwiseDifferenceBetweenAngles(rotationAngleInCenteredTangible, rotationAngleOfTangibleNow); 
		
		# check if the rotation filter is set to pre
		if settings.get('rotationFilterPosition') == 'pre':
			# add current rotation value to the rotation filter
			self.tangibleRotationFilter.addValue(currentRotation)
			# get rotation value from filter 
			currentRotation = self.tangibleRotationFilter.getState()
		
		# calculate the vector form current p1 to the tangible center
		shiftOfId1 = rotateVector(p1old, currentRotation)
		# calculate position
		currentPosition = p1now - shiftOfId1
		
		# check if the position filter is active
		if settings.get('positionFilterActive'):
			# add current position to filter
			self.tangiblePositionFilter.addXvalue(currentPosition.x)
			self.tangiblePositionFilter.addYvalue(currentPosition.y)
			# get position from filter
			currentPosition.x = self.tangiblePositionFilter.getXstate()
			currentPosition.y = self.tangiblePositionFilter.getYstate()
						
		# check if post rotation filter is active
		if settings.get('rotationFilterPosition') == 'post':
			# add current rotation value to the rotation filter
			self.tangibleRotationFilter.addValue(currentRotation)
			# get rotation value from filter 
			currentRotation = self.tangibleRotationFilter.getState()
		
		# set position and rotation
		self.position = currentPosition
		self.rotation = currentRotation	
				
	# function to calculate the current position and rotation out of two known tangible cursors
	def calculateTangiblePositionAndRotation(self,id1,id2) :
		
		# calculate original rotation angle
		p1old = pointVector(self.tangibleCursors[id1].offsetFromCenterX,self.tangibleCursors[id1].offsetFromCenterY)
		p2old = pointVector(self.tangibleCursors[id2].offsetFromCenterX,self.tangibleCursors[id2].offsetFromCenterY)
		rotationAngleInCenteredTangible = calcClockWiseAngle(p1old,p2old)
		
		# calculate the current angle
		p1now = pointVector(self.tangibleCursors[id1].lastKnownPositionX,self.tangibleCursors[id1].lastKnownPositionY)
		p2now = pointVector(self.tangibleCursors[id2].lastKnownPositionX,self.tangibleCursors[id2].lastKnownPositionY)
		rotationAngleOfTangibleNow = calcClockWiseAngle(p1now, p2now);   
		
		# calculate the difference between the two angles
		currentRotation = clockwiseDifferenceBetweenAngles(rotationAngleInCenteredTangible, rotationAngleOfTangibleNow); 
		
		# check if the rotation filter is set to pre
		if settings.get('rotationFilterPosition') == 'pre':
			# add current rotation value to the rotation filter
			self.tangibleRotationFilter.addValue(currentRotation)
			# get rotation value from filter 
			currentRotation = self.tangibleRotationFilter.getState()
			
		# calculate the vector form current p1 to the tangible center
		shiftOfId1 = rotateVector(p1old, currentRotation)
		# calculate position
		currentPosition = p1now - shiftOfId1
		
		# check if the position filter is active
		if settings.get('positionFilterActive'):
			# add current position to filter
			self.tangiblePositionFilter.addXvalue(currentPosition.x)
			self.tangiblePositionFilter.addYvalue(currentPosition.y)
			# get position from filter
			currentPosition.x = self.tangiblePositionFilter.getXstate()
			currentPosition.y = self.tangiblePositionFilter.getYstate()
						
		# check if post rotation filter is active
		if settings.get('rotationFilterPosition') == 'post':
			# add current rotation value to the rotation filter
			self.tangibleRotationFilter.addValue(currentRotation)
			# get rotation value from filter 
			currentRotation = self.tangibleRotationFilter.getState()
			
		# set position and rotation
		self.position = currentPosition
		self.rotation = currentRotation
	
	# function returning a list of all live ids that have been lately identified to belong to the tangible
	def getLiveCursorIDs(self):
		cursors = []
		for c in self.tangibleCursors:
			id = self.tangibleCursors[c].getLastLiveID()
			cursors.append(id)
		return cursors 
	
	# function to make the tangible savable to disk
	def __getstate__(self):
		try:
			list = []
			list.append(self.__dict__)
			list.append(self.tangibleCursors)
			list.append(self.externalIDtoTangibleCursorIDdict)
			list.append(self.externalIDtoTangibleCursorIDdictReverse)
			return list
	
		except Exception, e:
			print "Failure: %s" % e
			print "in function tangible getstate"
	
	# function to make the tangbile loadable from disk
	def __setstate__(self, d):
		try:
			self.__dict__.update(d[0])
			self.tangibleCursors							= d[1]
			self.externalIDtoTangibleCursorIDdict			= d[2]
			self.externalIDtoTangibleCursorIDdictReverse	= d[3]
	
		except Exception, e:
			print "Failure: %s" % e
			print "in function tangible setstate"
		
# class to store the tangible objects
class tangibleContainer(object):

	# function is called when the container is created
	def __init__(self):
		self.dictOfTangibles = {}

	# function to check if tangibles can be recognized in the current cursors
	def checkForKnownTriangles(self,*args):
		try:
			trianglesOnScreen = args[0]
			for tan in self.dictOfTangibles:
				self.dictOfTangibles[tan].compareTangibleTrianglesAndExternalTriangles(trianglesOnScreen)			
		except Exception, e:
			print "Failure: %s" % e
			print "Type tan:",type(tan)
			print "Tan:",tan
			print "trianglesOnScreen type:",type(trianglesOnScreen)
			print "trianglesOnScreen:",trianglesOnScreen
			print 'Check checkForKnownTriangles'
		

	# function to return the IDs of all recognized tangibles
	def getRecognizedTangibleIDs(self):
		ids = []
		for tan in self.dictOfTangibles:
			if (self.dictOfTangibles[tan].currentlyRecognized == True):
				ids = ids + [tan]
		return ids
		
	# function to return the recognized tangibles
	def getRecognizedTangibles(self):
		recognizedTangibles = []
		for tan in self.dictOfTangibles:
			if (self.dictOfTangibles[tan].currentlyRecognized == True):
				recognizedTangibles.append(self.dictOfTangibles[tan])
		return recognizedTangibles
		
	# function returning all cursors that are part of the recognized tangibles
	def getRecognizedCursors(self):
		recognizedCursors = []
		for tan in self.dictOfTangibles:
			# get cursor IDs from tangible
			recognizedCursors = recognizedCursors + self.dictOfTangibles[tan].getLiveCursorIDs()
		return recognizedCursors
		
	# register the getAllCursorsInBuffer function
	def registerCursorProvider(self, cursorProvider):
		self.getAllCursorsInBuffer = cursorProvider
		
	# function to register a new tangible with a certain id
	def registerNewTangible(self,id):
		tan = tangible()
		tan.registerCursors(self.getAllCursorsInBuffer(),id=id)
		self.dictOfTangibles[id] = tan
		print 'Tangible added, ID:', id
		
	# function to delete a tangible with a certain id
	def deleteTangible(self,id):
		try:
			del self.dictOfTangibles[id]
			print 'Tangible deleted, ID:',id
		except:
			print "Deletion of tangible failed, no tangible with ID", id

	# function to delete all tangibles (not deleted from hard disk!)
	def deleteAllTangibles(self):
		self.dictOfTangibles.clear()
		print 'All tangibles deleted'

	# function to save all tangibles in memory to disk
	def saveTangiblesToDisk(self):
		try:
			file = open("tangibles.db", "wb") # wb = write mode
			pickle.dump(self.dictOfTangibles, file)
			file.close()
			print "Tangibles written to disk"

		except Exception, e:
			print "Failure: %s" % e
			print 'Could not save tangibles to disk'
			
	# function to load tangibles from disk to memory
	def loadTangiblesFromDisk(self):
		try:			
			file = open("tangibles.db", "rb") # read mode
			self.dictOfTangibles = pickle.load(file)
			print 'Tangibles loaded from disk'	
		
		except Exception, e:
			print "Failure: %s" % e
			print 'Loading tangibles from file failed.'
	
# create a container object that can be imported
tangibles = tangibleContainer()