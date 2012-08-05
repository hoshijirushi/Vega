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


Textarea selectIpTextArea;
Textarea connectInfoTextArea;

void selectConnectToProxyTab()
{
	controlP5.tab("connectTab").setLabel("1 - Connect to proxy");
	controlP5.tab("connectTab").setHeight(verticalUnit);
	controlP5.tab("connectTab").activateEvent(true);
	controlP5.tab("connectTab").setId(connectToProxyTabId);
	
	connectInfoTextArea = controlP5.addTextarea("connectInfoText", "Connect to the proxy by selecting the IP address\n\nOnce connected the red label underneath the \"MAIN\" tab turns green.", horizontalUnit, 3 * verticalUnit, width- 2*horizontalUnit, 200);
	connectInfoTextArea.moveTo("connectTab");	
		
	selectIpTextArea = controlP5.addTextarea("ipText", "Select the IP of the proxy:", horizontalUnit, (darkSquareHeight + 1) * verticalUnit, 200, 200);
	selectIpTextArea.moveTo("connectTab");
	
	ip0 = controlP5.addNumberbox("ip0",100,horizontalUnit,(darkSquareHeight + 2) * verticalUnit,horizontalUnit,verticalUnit);
	ip0.setValue(127);
	ip0.setMin(0);
	ip0.setMax(255);
	ip0.captionLabel().setVisible(false);
	controlP5.controller("ip0").moveTo("connectTab");
	
	ip1 = controlP5.addNumberbox("ip1",100,2 * horizontalUnit + 8,(darkSquareHeight + 2) * verticalUnit,horizontalUnit,verticalUnit);
	ip1.setValue(0);
	ip1.setMin(0);
	ip1.setMax(255);
	ip1.captionLabel().setVisible(false);
	controlP5.controller("ip1").moveTo("connectTab");
	  
	ip2 = controlP5.addNumberbox("ip2",100,3 * horizontalUnit + 16,(darkSquareHeight + 2) * verticalUnit,horizontalUnit,verticalUnit);
	ip2.setValue(0);
	ip2.setMin(0);
	ip2.setMax(255);
	ip2.captionLabel().setVisible(false);
	controlP5.controller("ip2").moveTo("connectTab");
  
	ip3 = controlP5.addNumberbox("ip3",100,4 * horizontalUnit + 24,(darkSquareHeight + 2) * verticalUnit,horizontalUnit,verticalUnit);
	ip3.setValue(1);
	ip3.setMin(0);
	ip3.setMax(255);
	ip3.captionLabel().setVisible(false);
	controlP5.controller("ip3").moveTo("connectTab");
	
	ipNoteTextArea = controlP5.addTextarea("ipNote", "NOTE: Normally you leave this unchanged to 127.0.0.1 because your proxy is running on the same machine.", 7 * horizontalUnit, (darkSquareHeight + 2) * verticalUnit, 270, 200);
	ipNoteTextArea.moveTo("connectTab");
}