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

class numberGenerator(object):		
		
	#start values
	touchIdCounter = 1000
	fseqCounter = 1000
	
	def newTouchId(self):
		self.touchIdCounter += 1
		return self.touchIdCounter


	def newFseq(self):
		self.fseqCounter = self.fseqCounter + 1
		return self.fseqCounter

numberGenerator 	= numberGenerator()