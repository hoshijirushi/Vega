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

registerCenterStar centerStar = new registerCenterStar();
Textfield tangibleIdField;
Textarea registerTangibleInfoTextArea;

void setupRegisterTangibleTab()
{
	// Register tangible tab
	controlP5.tab("tangible").setLabel("3 - Register tangible");
	controlP5.tab("tangible").activateEvent(true);
	controlP5.tab("tangible").setHeight(verticalUnit);
	controlP5.tab("tangible").setId(registerTangibleTabId);

	// Register tangible info text
	registerTangibleInfoTextArea = controlP5.addTextarea("registerTangibleInfoText", "Enable \"SHOW TUIO OBJECTS\" and place the tangible you want to register on the center of the pattern. On the left select the TUIO object ID and click \"Register tangible\".\n\nTo delete a tangible enter its ID and click \"Delete tangible\". Once you are satisfied, save them to disk for the proxy to know them after a restart.", horizontalUnit, 3 * verticalUnit, width- 2*horizontalUnit+600, 200);
	registerTangibleInfoTextArea.moveTo("tangible");	
	
	controlP5.addTextlabel("registerLabel", "Register tangibles", horizontalUnit, (darkSquareHeight + 5) * verticalUnit);
	controlP5.controller("registerLabel").moveTo("tangible");

	tangibleIdField = controlP5.addTextfield("tangibleId", horizontalUnit, (darkSquareHeight + 6) * verticalUnit, 40, 20);
	tangibleIdField.setCaptionLabel("tangibleId");
	tangibleIdField.captionLabel().toUpperCase(false);
	tangibleIdField.setText("44");
	tangibleIdField.setWidth(horizontalUnit);
	controlP5.controller("tangibleId").moveTo("tangible");

	controlP5.Button b = controlP5.addButton("registerTangible", 0, horizontalUnit*2 + 8, (darkSquareHeight + 6) * verticalUnit, 100, 19);
	b.setCaptionLabel("Register tangible");
	b.captionLabel().toUpperCase(false);
	controlP5.controller("registerTangible").moveTo("tangible");

	controlP5.Button deleteTangible = controlP5.addButton("deleteTangible", 0, horizontalUnit*2 +8, (darkSquareHeight + 8) * verticalUnit, 100, 19);
	deleteTangible.setCaptionLabel("Delete tangible");
	deleteTangible.captionLabel().toUpperCase(false);
	controlP5.controller("deleteTangible").moveTo("tangible");

	controlP5.Button deleteTangibles = controlP5.addButton("deleteAllTangibles", 0, horizontalUnit, (darkSquareHeight + 10) * verticalUnit,  100 + 8 +horizontalUnit, 19);
	deleteTangibles.setCaptionLabel("        Delete all tangibles");
	deleteTangibles.captionLabel().toUpperCase(false);
	controlP5.controller("deleteAllTangibles").moveTo("tangible");

	// save tangibles button
	controlP5.Button saveTangibles = controlP5.addButton("saveTangibles", 0,  horizontalUnit, (darkSquareHeight + 12) * verticalUnit, 100 + 8 +horizontalUnit, 19);
	saveTangibles.setCaptionLabel("         SAVE TO DISK");
	saveTangibles.captionLabel().toUpperCase(false);
	saveTangibles.setColorBackground(color(90, 0, 0));
	controlP5.controller("saveTangibles").moveTo("tangible");
}

void paintRegisterTangibleTab()
{
	centerStar.paint();
}


class registerCenterStar
{
  void paint()
  {
    int diameter = int(height *(3.0/5.0));
    // grey arcs
    fill(30);
    arc(width/2, height/2, diameter, diameter, radians(0), radians(50));
    arc(width/2, height/2, diameter, diameter, radians(180), radians(205));
    // white arcs
    fill(220);
    arc(width/2, height/2, diameter, diameter, radians(270), radians(273));
    arc(width/2, height/2, diameter, diameter, radians(90), radians(135));
  }
}
