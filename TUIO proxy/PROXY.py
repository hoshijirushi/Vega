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

# This is the TUIO proxy main script

import os
from settings			import settings
from oscRemote			import remote
from tuioTools 			import tuioServer
from tangiblePattern	import tangibles


# clear screen and print program info
os.system('cls' if os.name=='nt' else 'clear')

print "Vega - TUIO proxy Copyright (C) 2012 Thomas Becker"
print "This program comes with ABSOLUTELY NO WARRANTY."
print "This is free software, and you are welcome to redistribute it"
print "under certain conditions."
print ""

print "TUIO proxy started"

# load settings from files
settings.load()

# load tangibles from disk
tangibles.loadTangiblesFromDisk()

# start the tuio proxy
tuioServer.start()

# start remote control for this programm
remote.start()

print "TUIO proxy up and running..."

try :
	while 1 :
		pass
		
except KeyboardInterrupt :
	tuioServer.stop()
	remote.stop()
	print "TUIO proxy aborted by keyboard"	