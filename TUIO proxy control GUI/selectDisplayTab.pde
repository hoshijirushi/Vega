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

Textarea selectDisplayInfoTextArea;

void setupSelectDisplayTab()
{
	// connect to proxy tab
	controlP5.tab("displayTab").setLabel("2 - Select display");
	controlP5.tab("displayTab").setHeight(verticalUnit);
	controlP5.tab("displayTab").activateEvent(true);
	controlP5.tab("displayTab").setId(selctDisplayTabId);
	
	// select display info text
	selectDisplayInfoTextArea = controlP5.addTextarea("selectDisplayInfoText", "Select the display where the touch-frame is attached to.\n\nThe folowing steps will be displayed on this screen", horizontalUnit, 3 * verticalUnit, width- 2*horizontalUnit, 200);
	selectDisplayInfoTextArea.moveTo("displayTab");	
	
	// fullscreen display selector
	selectDisplayTextArea = controlP5.addTextarea("calibrationinst", "Select the display with touchscreen", horizontalUnit , (darkSquareHeight + 1) * verticalUnit, 200, 200);
	selectDisplayTextArea.moveTo("displayTab");

	selectDisplay = controlP5.addDropdownList("displayList", horizontalUnit, (darkSquareHeight + 3) * verticalUnit, 160, 100);
	selectDisplay.setBackgroundColor(color(190));
	selectDisplay.setItemHeight(20);
	selectDisplay.setBarHeight(15);
	selectDisplay.captionLabel().set("Display with touchscreen");
	selectDisplay.captionLabel().style().marginTop = 3;
	selectDisplay.captionLabel().style().marginLeft = 3;
	selectDisplay.valueLabel().style().marginTop = 3;
	for (int i=0;i<fullscreen.numberOfScreens();i++)
	{
	selectDisplay.addItem("Display "+i, i);
	}
	selectDisplay.setColorBackground(color(60));
	selectDisplay.setColorActive(color(255, 128));
	selectDisplay.moveTo("displayTab");
	
}