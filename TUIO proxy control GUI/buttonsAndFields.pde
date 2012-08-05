// Copyright (C) 2012 Thomas Becker
// contact: thomas.heinrich.becker@web.de

// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.

// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.

// You should have received a copy of the GNU General Public License
// along with this program.  If not, see <http://www.gnu.org/licenses/>.

Toggle connectedToggle;

void setupButtonsAndFields() {

	setupMainTab();
	selectConnectToProxyTab();
	setupSelectDisplayTab();
	setupRegisterTangibleTab();
	setupFineTuneTab();

	//connection indicator  
	connectedToggle = controlP5.addToggle("connected", true, 0, verticalUnit, horizontalUnit, verticalUnit);
	connectedToggle.lock();
	connectedToggle.setColorActive(color(50, 118, 32));
	connectedToggle.setColorBackground(color(90, 0, 0));
	connectedToggle.setCaptionLabel("");
	connectedToggle.setState(false);
	connectedToggle.moveTo("global");
	
	controlP5.addToggle("tuioCursersToggle",false,horizontalUnit,(darkSquareHeight + 1) * verticalUnit,20,20);
	controlP5.controller("tuioCursersToggle").setVisible(false);
	controlP5.controller("tuioCursersToggle").moveTo("global");
	controlP5.controller("tuioCursersToggle").setCaptionLabel("Show TUIO cursers");
	
	controlP5.addToggle("tuioObjectsToggle",false,horizontalUnit*4,(darkSquareHeight + 1) * verticalUnit,20,20);
	controlP5.controller("tuioObjectsToggle").setVisible(false);
	controlP5.controller("tuioObjectsToggle").moveTo("global");
	controlP5.controller("tuioObjectsToggle").setCaptionLabel("Show TUIO objects");
}

