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

Textarea mainInfoTextArea;

Numberbox ip0;
Numberbox ip1;
Numberbox ip2;
Numberbox ip3;

Textarea ipNoteTextArea;

Textarea selectDisplayTextArea;
DropdownList selectDisplay;

void setupMainTab()
{  
	controlP5.tab("default").setLabel("Main");
	controlP5.tab("default").activateEvent(true);
	controlP5.tab("default").setHeight(verticalUnit);
	controlP5.tab("default").setWidth(horizontalUnit-8);	
	controlP5.tab("default").setId(mainTabId);
	
	// main info text
	mainInfoTextArea = controlP5.addTextarea("mainInfoText", "Welcome to vegaControl!\n\nJust click the tabs on top of this window in their given order to setup the proxy", horizontalUnit, 3 * verticalUnit, width- 2*horizontalUnit, 200);
	mainInfoTextArea.moveTo("default");	
}