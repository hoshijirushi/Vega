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

Textarea fineTuneInfoTextArea;

DropdownList rotationFilterSwitchDrop;
Textfield aspect;
Toggle dv,rff,tcf, pfa;

void setupFineTuneTab()
{
  controlP5.tab("fineTune").setLabel("4 - Fine-tune recognition");
  controlP5.tab("fineTune").activateEvent(true);
  controlP5.tab("fineTune").setHeight(verticalUnit);
  controlP5.tab("fineTune").setId(fineTuneTabId);

  // fine tune info text
  fineTuneInfoTextArea = controlP5.addTextarea("fineTuneInfoText", "First tune the tolerance of the algorithm. After that block recognitions with not enough votes.\n\nEnable and tune position and rotation filtering as you wish.", horizontalUnit, 3 * verticalUnit, width- 2*horizontalUnit+600, 200);
  fineTuneInfoTextArea.moveTo("fineTune");



  // tangible cursor filter
  controlP5.addTextlabel("CursorFilterInfoText", "Tangible cursor filter - removes all cursors belonging to detected tangibles (in proxy! don't confuse this with SHOW TUIO CURSORS option above which just doesn't display the cursors in the config program)", horizontalUnit, (darkSquareHeight + 5) * verticalUnit);
  controlP5.controller("CursorFilterInfoText").moveTo("fineTune");

  tcf = controlP5.addToggle("tangibleCursorFilter", false, horizontalUnit, (darkSquareHeight + 6) * verticalUnit, 20, 20);
  controlP5.controller("tangibleCursorFilter").setVisible(true);
  controlP5.controller("tangibleCursorFilter").moveTo("fineTune");
  controlP5.controller("tangibleCursorFilter").setCaptionLabel("Filter cursors belonging to tangibles");

  // real finger filter
  controlP5.addTextlabel("realFingerFilterInfoText", "Real finger filter - removes all cursors in a radius around the tangible center - good for removing fingers grabbing the tangible", horizontalUnit, (darkSquareHeight + 12) * verticalUnit);
  controlP5.controller("realFingerFilterInfoText").moveTo("fineTune");

  rff = controlP5.addToggle("realFingerFilter", false, horizontalUnit, (darkSquareHeight + 13) * verticalUnit, 20, 20);
  controlP5.controller("realFingerFilter").setVisible(true);
  controlP5.controller("realFingerFilter").moveTo("fineTune");
  controlP5.controller("realFingerFilter").setCaptionLabel("Filter cursors close to the tangible");

  // real finger filter radius
  controlP5.addSlider("realFingerFilterRadius", 0.0F, 1.0F, 0.3F, horizontalUnit, (darkSquareHeight + 15) * verticalUnit, 400, 20);
  controlP5.controller("realFingerFilterRadius").setCaptionLabel("Finger filter radius");
  controlP5.controller("realFingerFilterRadius").captionLabel().toUpperCase(false);
  controlP5.controller("realFingerFilterRadius").moveTo("fineTune");

  // rotation filter switch

  controlP5.addTextlabel("rotationFilterSwitchInfoText", "Rotation filter - A simple low pass filter that limits the movement per refresh cycle ", horizontalUnit, (darkSquareHeight + 20) * verticalUnit);
  controlP5.controller("rotationFilterSwitchInfoText").moveTo("fineTune"); 

  rotationFilterSwitchDrop = controlP5.addDropdownList("rotationFilterPosition", horizontalUnit, (darkSquareHeight + 23) * verticalUnit, 160, 100);
  rotationFilterSwitchDrop.setBackgroundColor(color(190));
  rotationFilterSwitchDrop.setItemHeight(20);
  rotationFilterSwitchDrop.setBarHeight(20);
  rotationFilterSwitchDrop.captionLabel().set("Rotation filter setting");
  rotationFilterSwitchDrop.captionLabel().style().marginTop = 3;
  rotationFilterSwitchDrop.captionLabel().style().marginLeft = 3;
  rotationFilterSwitchDrop.valueLabel().style().marginTop = 3;        
  rotationFilterSwitchDrop.addItem("OFF", 0);
  rotationFilterSwitchDrop.addItem("POST", 1);
  rotationFilterSwitchDrop.addItem("PRE", 2);
  rotationFilterSwitchDrop.setColorBackground(color(60));
  rotationFilterSwitchDrop.setColorActive(color(255, 128));
  rotationFilterSwitchDrop.moveTo("fineTune");

  // rotation filter limiter
  controlP5.addSlider("rotationLimit", 0.0F, 0.2F, 0.05F, horizontalUnit, (darkSquareHeight + 27) * verticalUnit, 400, 20);
  controlP5.controller("rotationLimit").setCaptionLabel("Rotation filter limiter");
  controlP5.controller("rotationLimit").captionLabel().toUpperCase(false);
  controlP5.controller("rotationLimit").moveTo("fineTune");

  // position filter active
  controlP5.addTextlabel("positionFilterInfoText", "Position filter - NOT IMPLEMENTED - can be implemented in the python source, normally not needed", horizontalUnit, (darkSquareHeight + 30) * verticalUnit);
  controlP5.controller("positionFilterInfoText").moveTo("fineTune"); 

  pfa = controlP5.addToggle("positionFilterActive", false, horizontalUnit, (darkSquareHeight + 31) * verticalUnit, 20, 20);
  controlP5.controller("positionFilterActive").setVisible(true);
  controlP5.controller("positionFilterActive").setCaptionLabel("Filter position");
  controlP5.controller("positionFilterActive").moveTo("fineTune");

  // triangle algorithm settings

  controlP5.addTextlabel("algorithmFilterInfoText", "Change the properties of the triangle detection algorithm", horizontalUnit, (darkSquareHeight + 35) * verticalUnit);
  controlP5.controller("algorithmFilterInfoText").moveTo("fineTune");

  controlP5.addSlider("tolerance", 0.0F, 0.01F, 0.005F, horizontalUnit, (darkSquareHeight + 36) * verticalUnit, 400, 20);
  controlP5.controller("tolerance").setCaptionLabel("Tolerance");
  controlP5.controller("tolerance").captionLabel().toUpperCase(false);
  controlP5.controller("tolerance").moveTo("fineTune");

  controlP5.addSlider("neededVotes", 0, 10, 128, horizontalUnit, (darkSquareHeight + 38) * verticalUnit, 400, 20);
  controlP5.controller("neededVotes").setCaptionLabel("Needed votes");
  controlP5.controller("neededVotes").captionLabel().toUpperCase(false);
  controlP5.controller("neededVotes").moveTo("fineTune");

  dv = controlP5.addToggle("debugVotes", false, horizontalUnit, (darkSquareHeight + 40) * verticalUnit, 20, 20);
  controlP5.controller("debugVotes").setVisible(true);
  controlP5.controller("debugVotes").setCaptionLabel("Print votes for tangibes in the proxy console");
  controlP5.controller("debugVotes").moveTo("fineTune");

  // screen aspect
  controlP5.addTextlabel("aspectInfoText", "Adjust the aspect ratio of your touch screen - For example 16 / 9 = 1.777777778 - set value with enter key", horizontalUnit, (darkSquareHeight + 44) * verticalUnit);
  controlP5.controller("aspectInfoText").moveTo("fineTune");

  aspect = controlP5.addTextfield("touchScreenAspect", horizontalUnit, (darkSquareHeight + 45) * verticalUnit, 100, 20);
  controlP5.controller("touchScreenAspect").setVisible(true);
  aspect.setAutoClear(false);
  aspect.setInputFilter(ControlP5.FLOAT);
  aspect.setText("1.777777778");
  controlP5.controller("touchScreenAspect").setCaptionLabel("aspect ratio of the screen");
  controlP5.controller("touchScreenAspect").moveTo("fineTune");



  // save settings button
  controlP5.Button saveFineTuning = controlP5.addButton("saveAlgorithmSettings", 0, horizontalUnit, (darkSquareHeight + 49) * verticalUnit, 100 + 8 +horizontalUnit, verticalUnit);
  saveFineTuning.setCaptionLabel("         SAVE TO DISK");
  saveFineTuning.captionLabel().toUpperCase(false);
  saveFineTuning.setColorBackground(color(90, 0, 0));
  controlP5.controller("saveAlgorithmSettings").moveTo("fineTune");
}

