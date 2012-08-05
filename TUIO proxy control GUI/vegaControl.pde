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

import fullscreen.*;
import controlP5.*;
import oscP5.*;
import netP5.*;
import TUIO.*;
TuioProcessing tuioClient;

boolean mainTab				= true;
boolean connectToProxyTab	        = false;
boolean selectDisplayTab	        = false;
boolean frameCalibrationTab	        = false;
boolean registerTangibleTab	        = false;
boolean fineTuneTab			= false;

boolean connected			= false;

boolean showTuioObjects     = false;
boolean showTuioCursers     = false;

final int mainTabId = 1;
final int connectToProxyTabId = 2;
final int selctDisplayTabId = 3;
final int registerTangibleTabId = 4;
final int fineTuneTabId = 5;

// fullscreen object
SoftFullScreen fs;

// graphical units
int verticalUnit			= 18;
int horizontalUnit			= 40;
int darkSquareHeight		= 6;

int normalWindowHeight		= verticalUnit * 21;
int normalWindowWidth		= int(normalWindowHeight * 1.618);

OscP5 oscP5;
NetAddress myRemoteLocation;
ControlP5 controlP5;
int myColor = color(0, 0, 0);


vegaControl mainSketch = this;

void setup() {
  frameRate(120);
  println (this.getClass());
  size(normalWindowWidth, normalWindowHeight);
  fs = new SoftFullScreen(this, 0);

  // Set title of the window
  frame.setTitle("Vega Control");

  // Set up the receiver for this programm
  oscP5 = new OscP5(this, 3331);

  // Address of the receiving proxy
  myRemoteLocation = new NetAddress("127.0.0.1", 3330);

  controlP5 = new ControlP5(this);
  setupButtonsAndFields();
}

void draw() {
  smooth();
  background(70);
  noStroke();
  connectionToProxy.check();

  fill(30);
  rect(0, 0, width, verticalUnit * darkSquareHeight);


  if (registerTangibleTab)
  {
    paintRegisterTangibleTab();
  }

  if (showTuioObjects  && (!mainTab)&& (!selectDisplayTab))
  {


    try {
      Vector tuioObjectList = tuioClient.getTuioObjects();
      for (int i=0;i<tuioObjectList.size();i++) {
        TuioObject tobj = (TuioObject)tuioObjectList.elementAt(i);

        pushMatrix();
        translate(tobj.getScreenX(width), tobj.getScreenY(height));
        rotate(tobj.getAngle());

        int diameter = int(height *(2.0/5.0));
        // grey arcs
        noStroke();
        fill(30);
        arc(0, 0, diameter, diameter, radians(51), radians(90));
        arc(0, 0, diameter, diameter, radians(206), radians(270));
        // white arcs
        fill(220);
        arc(0, 0, diameter, diameter, radians(274), radians(360));
        arc(0, 0, diameter, diameter, radians(136), radians(180));

        fill(255);
        textSize(26);
        text(""+tobj.getSymbolID(), (diameter/2+30), 0);
        popMatrix();
      }
    }
    catch (Exception e) {
      System.out.println("problem: "+e.getMessage());
    }
  }

  if (showTuioCursers && (!mainTab)&& (!selectDisplayTab))
  {

    try {

      Vector tuioCursorList = tuioClient.getTuioCursors();
      for (int i=0;i<tuioCursorList.size();i++) {
        TuioCursor tcur = (TuioCursor)tuioCursorList.elementAt(i);
        Vector pointList = tcur.getPath();

        if (pointList.size()>0) {
          noStroke();
          fill(255, 20, 0);
          ellipse( tcur.getScreenX(width), tcur.getScreenY(height), 40, 40);
          // Point number text
          stroke(255, 20, 0);
          textSize(16);
          text(""+ tcur.getCursorID(), tcur.getScreenX(width)+25, tcur.getScreenY(height)+5);
        }
      }
    }
    catch (Exception e) {
      System.out.println("problem: "+e.getMessage());
    }
  }
}


///////////// functions called by changing switches


///// fine tune tab

void tangibleCursorFilter(boolean theFlag) {
  String value;
  if (theFlag)
  {
    value = "on";
  }
  else
  {
    value = "off";
  }
  OscMessage myOscMessage = new OscMessage("/vega/settings");
  myOscMessage.add("tangibleCursorFilter");
  myOscMessage.add(value);
  OscP5.flush(myOscMessage, myRemoteLocation);
}

void realFingerFilter(boolean theFlag) {
  String value;
  if (theFlag)
  {
    value = "on";
  }
  else
  {
    value = "off";
  }
  OscMessage myOscMessage = new OscMessage("/vega/settings");
  myOscMessage.add("realFingerFilter");
  myOscMessage.add(value);
  OscP5.flush(myOscMessage, myRemoteLocation);
}

void realFingerFilterRadius(float radius) {
  OscMessage myOscMessage = new OscMessage("/vega/settings");
  myOscMessage.add("realFingerFilterRadius");
  myOscMessage.add(radius);
  OscP5.flush(myOscMessage, myRemoteLocation);
}

// rotation filter position is called with events

void rotationLimit(float speed) {
  OscMessage myOscMessage = new OscMessage("/vega/settings");
  myOscMessage.add("rotationLimit");
  myOscMessage.add(speed);
  OscP5.flush(myOscMessage, myRemoteLocation);
}

void positionFilterActive(boolean theFlag) {
  int value;
  if (theFlag)
  {
    value = 1;
  }
  else
  {
    value = 0;
  }
  OscMessage myOscMessage = new OscMessage("/vega/settings");
  myOscMessage.add("positionFilterActive");
  myOscMessage.add(value);
  OscP5.flush(myOscMessage, myRemoteLocation);
}

void tolerance(float tolerance) {
  OscMessage myOscMessage = new OscMessage("/vega/settings");
  myOscMessage.add("tolerance");
  myOscMessage.add(tolerance);
  OscP5.flush(myOscMessage, myRemoteLocation);
}

void neededVotes(int neededVotes) {
  OscMessage myOscMessage = new OscMessage("/vega/settings");
  myOscMessage.add("neededVotes");
  myOscMessage.add(neededVotes);
  OscP5.flush(myOscMessage, myRemoteLocation);
}

void debugVotes(boolean theFlag) {
  int value;
  if (theFlag)
  {
    value = 1;
  }
  else
  {
    value = 0;
  }
  OscMessage myOscMessage = new OscMessage("/vega/settings");
  myOscMessage.add("debugVotes");
  myOscMessage.add(value);
  OscP5.flush(myOscMessage, myRemoteLocation);
}


void touchScreenAspect(String aspectString) {
  float aspect = float(aspectString);
  OscMessage myOscMessage = new OscMessage("/vega/settings");
  myOscMessage.add("touchScreenAspect");
  myOscMessage.add(aspect);
  OscP5.flush(myOscMessage, myRemoteLocation);
}

//////// tangible registration tab

public void registerTangible(int theValue) {
  OscMessage myOscMessage = new OscMessage("/vega/tangible");
  myOscMessage.add("register");
  myOscMessage.add(Integer.parseInt(tangibleIdField.getText()));
  OscP5.flush(myOscMessage, myRemoteLocation);
}

public void deleteTangible(int theValue) {
  println("Sending command to delete tangible with id "+ tangibleIdField.getText());
  OscMessage myOscMessage = new OscMessage("/vega/tangible");
  myOscMessage.add("delete");
  myOscMessage.add(Integer.parseInt(tangibleIdField.getText()));
  OscP5.flush(myOscMessage, myRemoteLocation);
}

public void deleteAllTangibles(int theValue) {
  println("Sending command to delete all tangibles");
  OscMessage myOscMessage = new OscMessage("/vega/tangible");
  myOscMessage.add("deleteAll");
  OscP5.flush(myOscMessage, myRemoteLocation);
}

public void saveTangibles(int theValue) {
  println("Sending command to save tangibles");
  OscMessage myOscMessage = new OscMessage("/vega/tangible");
  myOscMessage.add("saveToDisk");
  OscP5.flush(myOscMessage, myRemoteLocation);
}

void saveAlgorithmSettings() {
  println("Saving algorithm settings");
  OscMessage myOscMessage = new OscMessage("/vega/settings");
  myOscMessage.add("save");
  OscP5.flush(myOscMessage, myRemoteLocation);
}
///////////// show tuio messages


void tuioObjectsToggle(boolean theFlag) {
  if (theFlag==true) {
    println("start showing tuio objects");
    if (showTuioCursers == false)
    {
      tuioClient  = new TuioProcessing(this);
    }
    showTuioObjects = true;
  } 
  else {
    println("stop showing tuio objects");
    if (showTuioCursers == false)
    {
      tuioClient.dispose();
    }
    showTuioObjects = false;
  }
}

void tuioCursersToggle(boolean theFlag) {
  if (theFlag==true) {
    println("start showing tuio cursers");
    if (showTuioObjects == false)
    {
      tuioClient  = new TuioProcessing(this);
    }  
    showTuioCursers = true;
  } 
  else {
    println("stop showing tuio cursers");
    if (showTuioObjects == false)
    {
      tuioClient.dispose();
    }  
    showTuioCursers = false;
  }
}


//////////////////////////////////////

void controlEvent(ControlEvent theControlEvent) {
  if (theControlEvent.isController()) {
    
  } 

  else if (theControlEvent.isTab())
  {
    switch(theControlEvent.tab().id()) {

    case mainTabId: // main tab
      mainTab				= true;
      connectToProxyTab	= false;
      selectDisplayTab	= false;
      registerTangibleTab	= false;
      fineTuneTab			= false;
      controlP5.controller("tuioObjectsToggle").setVisible(false);	  
      controlP5.controller("tuioCursersToggle").setVisible(false);
      fullscreen.off();
      break;

    case connectToProxyTabId:
      mainTab	            = false;
      connectToProxyTab     = true;
      selectDisplayTab	    = false;
      registerTangibleTab   = false;
      fineTuneTab	    = false;
      controlP5.controller("tuioObjectsToggle").setVisible(false);	  
      controlP5.controller("tuioCursersToggle").setVisible(false);
      fullscreen.off();
      break;

    case selctDisplayTabId:
      mainTab				= false;
      connectToProxyTab	= false;
      selectDisplayTab	= true;
      registerTangibleTab	= false;
      fineTuneTab			= false;
      controlP5.controller("tuioObjectsToggle").setVisible(false);	  
      controlP5.controller("tuioCursersToggle").setVisible(false);
      fullscreen.off();
      break;


    case registerTangibleTabId:
      mainTab				= false;
      connectToProxyTab	= false;
      selectDisplayTab	= false;
      registerTangibleTab	= true;
      fineTuneTab			= false;
      controlP5.controller("tuioCursersToggle").setVisible(true);
      controlP5.controller("tuioObjectsToggle").setVisible(true);
      fullscreen.on();
      break;

    case fineTuneTabId:
      mainTab              = false;
      connectToProxyTab    = false;
      selectDisplayTab     = false;
      registerTangibleTab  = false;
      fineTuneTab          = true;
      controlP5.controller("tuioCursersToggle").setVisible(true);
      controlP5.controller("tuioObjectsToggle").setVisible(true);
      fullscreen.on();
      break;
    }

    println("Switched to tab : " + theControlEvent.tab().name());
  }

  else if (theControlEvent.isGroup()) {
    if (theControlEvent.group().name() == "displayList") {
      int dn =  int(theControlEvent.group().value());
      fullscreen.setScreenNumber(dn);
      if (fullscreen.isOn() == true)
      {
        fullscreen.off();
        fullscreen.forceOn();
      }
    }
    if (theControlEvent.group().name() == "rotationFilterPosition") {
      int flag =  int(theControlEvent.group().value());
      String value = "";  
      switch(flag) {
      case 0: 
        value = "off";
        break;
      case 1: 
        value = "post";
        break;
      case 2: 
        value = "pre";
        break;
      }

      OscMessage myOscMessage = new OscMessage("/vega/settings");
      myOscMessage.add("rotationFilterPosition");
      myOscMessage.add(value);
      OscP5.flush(myOscMessage, myRemoteLocation);
    }
  }
}

