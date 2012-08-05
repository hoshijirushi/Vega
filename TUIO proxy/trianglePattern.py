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
import itertools
from geometricCalculations import distance

# class describing a triangle
class triangle(object):
	
	# The side between vertices 1 and 2 has to be the shortest side
    # The side between vertices 2 and 3 has to be he intermediate side
    # The side between vertices 3 and 1 has to be the longest side
	
	counterClockwiseRotation	= True
	
	# function calculate the side lengths and orientation of the trinagle
	def setCursors(self, p1, p2, p3):
	
		# get the length of the triangle sides and put them in order
		a = distance(p1, p2) + 0.000000001 # prevent same size sides
		b = distance(p2, p3)
		c = distance(p3, p1) - 0.000000001 # prevent same size sides
		
		#
		if (a > b) & (a > c):
			# a is longest
			if b > c:
				# b is middle
				# c is shortest
				self.v1 = p1
				self.v2 = p3
				self.v3 = p2
				self.lengthLongSide		= a
				self.lengthMiddleSide	= b
				self.lengthShortSide	= c
			else:
				# c is middle
				# b is shortest
				self.v1 = p2;
				self.v2 = p3;
				self.v3 = p1;
				self.lengthLongSide		= a
				self.lengthMiddleSide	= c
				self.lengthShortSide	= b

		elif (b > a) & (b > c):
			# b is longest
			if a > c:
				# a is middle
				# c is shortest
				self.v1 = p3
				self.v2 = p1
				self.v3 = p2
				self.lengthLongSide		= b
				self.lengthMiddleSide	= a
				self.lengthShortSide	= c
			else:
				# c is middle
				# a is shortest
				self.v1 = p2
				self.v2 = p1
				self.v3 = p3
				self.lengthLongSide		= b
				self.lengthMiddleSide	= c
				self.lengthShortSide	= a
				
		elif (c > a) & (c > b):
			# c is longest
			if a > b:
				# a is middle
				# b is shortest
				self.v1 = p3
				self.v2 = p2
				self.v3 = p1
				self.lengthLongSide		= c
				self.lengthMiddleSide	= a
				self.lengthShortSide	= b
			else:
				# b is middle
				# a is shortest
				self.v1 = p1
				self.v2 = p2
				self.v3 = p3
				self.lengthLongSide		= c
				self.lengthMiddleSide	= b
				self.lengthShortSide	= a
				
		# check for rotation order (v2 left or right of v1 to v3)
		if ((self.v3.x - self.v1.x)*(self.v2.y - self.v1.y) - (self.v3.y - self.v1.y)*(self.v2.x - self.v1.x)) > 0:
			self.counterClockwiseRotation = True
		else:
			self.counterClockwiseRotation = False
	
	# function to return the IDs of the cursor points building the triangle
	def getIDs(self):
		idList = [self.v1.id, self.v2.id, self.v3.id]
		return idList
	
	# function to print a fancy info about the triangle to console
	def prettyPrint(self):
		print
		print '--------Triangle -------------------'
		print 'Ids are:', self.getIDs()
		print self.v1
		print self.v2
		print self.v3
		print
		print 'Longest side	v3-v1:', self.lengthLongSide
		print 'Middle side	v2-v3:', self.lengthMiddleSide
		print 'Shortest side	v1-v2:', self.lengthShortSide
		if self.counterClockwiseRotation:
			print 'Middle side is counter clockwise oriented'
		else:
			print 'Middle side is clockwise oriented'


# function to create all possible triangles from a list of points 
def createTrianglesFromCursors(*args):
	
	listOfCursors = args[0]
	triangles = []
	
	# create  tuples with the length of 3 points, in sorted order, no repeated elements
	for combination in list(itertools.combinations(listOfCursors,3)):
		# create triangles from the tuples
		t = triangle()
		t.setCursors(combination[0],combination[1],combination[2])
		triangles.append(t)
	
	return triangles
	
# function to compare two triangles on their similarity
def compareTriangles (t1, t2, tolerance):
	# check if both triangles have the same rotation
	if t1.counterClockwiseRotation == t2.counterClockwiseRotation:
	
		# check if the difference of the long sides is within tolerance
		longSideDifference = math.fabs(t1.lengthLongSide - t2.lengthLongSide)		
		if longSideDifference <= tolerance:
	
			# check if the difference of the middle sides is within tolerance
			middleSideDifference = math.fabs(t1.lengthMiddleSide - t2.lengthMiddleSide)
			if middleSideDifference <= tolerance:
			
				# check if the difference of the short sides is within tolerance
				shortSideDifference = math.fabs(t1.lengthShortSide - t2.lengthShortSide)
				if shortSideDifference <= tolerance:
					
					# triangles are considered equal
					return True
	else:
		# triangles are considered different
		return False