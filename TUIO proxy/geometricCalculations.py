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

# class of a 2 dimensional vector
class pointVector(object):
	
	# function called when object is created
	def __init__(self, *args, **kwargs):
		if len(args) == 0:
			self.x = kwargs.get('x', 0.0)
			self.y = kwargs.get('y', 0.0)
		else:
			self.x = args[0]
			self.y = args[1]

	# function to add two vectors
	def __add__(self, other):
		return pointVector(x=self.x+other.x,y=self.y+other.y)
	
	# function to subtract vectors
	def __sub__(self, other):
		return pointVector(x=self.x-other.x,y=self.y-other.y)

	# make the vector printable
	def __repr__(self):
		return "x: %s y: %s" % (self.x, self.y)

# function to calculate the distance between two points
def distance(p1, p2):
	dist = 	math.sqrt( ((p2.x - p1.x)**2) + ((p2.y - p1.y)**2));
	return dist

# function to calculate the clockwise angle between 12 o'clock (on screen)coming out of p1 and p1-p2
def calcClockWiseAngle(p1, p2):
	origin = p1
	a = pointVector(p1.x,-500.0)
	b = p2
	v1 = a - origin
	v2 = b - origin
	angle = -math.atan2(v2.x*v1.y - v2.y*v1.x, v2.x*v1.x+v2.y*v1.y)

	if (angle < 0):
		angle += 2*math.pi
	
	return angle

# function to rotate a vector by a certain angle
def rotateVector (vec, angle):
	rotatedVector = pointVector()
	cosAngle = math.cos(angle)
	sinAngle = math.sin(angle)
	rotatedVector.x = vec.x*cosAngle - vec.y*sinAngle
	rotatedVector.y = vec.x*sinAngle + vec.y*cosAngle
	return rotatedVector

# function to calculate the clockwise difference between two angles
def clockwiseDifferenceBetweenAngles(originalAngle, rotatedAngle):
	if originalAngle > rotatedAngle:
		rotatedAngle += 2*math.pi
	angle = rotatedAngle - originalAngle
	return angle
# function to check if a point lies in a circle 
def isPointInCircle(centerX, centerY, radius, pointX, pointY, aspectCorrectionFactor):
	distanceFromCenter = math.sqrt(((centerX - pointX)* aspectCorrectionFactor) ** 2  + (centerY - pointY) ** 2)
	return distanceFromCenter <= radius