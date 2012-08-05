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

int ip0Value;
int ip1Value;
int ip2Value;
int ip3Value;

connectionChecker connectionToProxy = new connectionChecker();

class connectionChecker
{
  boolean firstConnect = true;
  boolean connectionAlive = false;
  int timeout = 100;     // in frames 
  int timeForPing = 10;  // in frames
  int timer   = 0;

  void check()
  {
    timer++;

    if (timer == (timeout - timeForPing))
    {
      connectionAlive = false;
      pingProxy();
    }

    if (timer > timeout)
    {
      connectedToggle.setState(connectionAlive);
      timer = 0;
    }
  }

  void isAlive(boolean value)
  {
    if (firstConnect) {
      getSettingsFromProxy();
      firstConnect = false;
    }

    connectionAlive = value;
  }
}

void pingProxy() {
  println("Pinging proxy ");
  OscMessage myOscMessage = new OscMessage("/vega/ping");
  myOscMessage.add(0);
  OscP5.flush(myOscMessage, myRemoteLocation);
}

void ip0 (int ipBlock) {
  String newIp = ( int(ip0.value()) + "." + int(ip1.value()) + "." + int(ip2.value()) + "." + int(ip3.value()));
  myRemoteLocation = new NetAddress(newIp, 3330);
  println("proxy ip changed to " + newIp);
}

void ip1 (int ipBlock) {
  String newIp = ( int(ip0.value()) + "." + int(ip1.value()) + "." + int(ip2.value()) + "." + int(ip3.value()));
  myRemoteLocation = new NetAddress(newIp, 3330);
  println("proxy ip changed to " + newIp);
}

void ip2 (int ipBlock) {
  String newIp = ( int(ip0.value()) + "." + int(ip1.value()) + "." + int(ip2.value()) + "." + int(ip3.value()));
  myRemoteLocation = new NetAddress(newIp, 3330);
  println("proxy ip changed to " + newIp);
}

void ip3 (int ipBlock) {
  String newIp = ( int(ip0.value()) + "." + int(ip1.value()) + "." + int(ip2.value()) + "." + int(ip3.value()));
  myRemoteLocation = new NetAddress(newIp, 3330);
  println("proxy ip changed to " + newIp);
}

void oscEvent(OscMessage theOscMessage) {

  if (theOscMessage.checkAddrPattern("/vega/pong")==true) {
    connectionToProxy.isAlive(true);
    println("CONNECTED");
  }

  if (theOscMessage.checkAddrPattern("/vega/settings")==true) {
    String settingName = theOscMessage.get(0).stringValue();
    
    if (settingName.equals("tolerance") == true)
    {
      float receivedValue = theOscMessage.get(1).floatValue();
      controlP5.controller("tolerance").changeValue(receivedValue);
    } 

    if (settingName.equals("neededVotes") == true)
    {
      int receivedValue = theOscMessage.get(1).intValue();
      controlP5.controller("neededVotes").changeValue(receivedValue);
    } 

    if (settingName.equals("debugVotes") == true)
    {
      boolean receivedValue = (theOscMessage.get(1).intValue() != 0);
      dv.setValue(receivedValue);
    } 

    if (settingName.equals("rotationFilterPosition") == true)
    {   
      String receivedValue = (theOscMessage.get(1).stringValue());
      if (receivedValue.equals("off"))
      {
        rotationFilterSwitchDrop.setValue(0);
      }
      else if (receivedValue.equals("post"))
      {
        rotationFilterSwitchDrop.setValue(1);
      }
      if (receivedValue.equals("pre"))
      {
        rotationFilterSwitchDrop.setValue(2);
      }
    }

    if (settingName.equals("rotationLimit") == true)
    {
      float receivedValue = theOscMessage.get(1).floatValue();
      controlP5.controller("rotationLimit").changeValue(receivedValue);
    } 

    if (settingName.equals("realFingerFilter") == true)
    {   
      String receivedValue = (theOscMessage.get(1).stringValue());
      if (receivedValue.equals("off"))
      {
        rff.setValue(false);
      }
      else if (receivedValue.equals("on"))
      {
        rff.setValue(true);
      }
    }

    if (settingName.equals("realFingerFilterRadius") == true)
    {   
      float receivedValue = theOscMessage.get(1).floatValue();
      controlP5.controller("realFingerFilterRadius").changeValue(receivedValue);
    }

    if (settingName.equals("tangibleCursorFilter") == true)
    {   
      String receivedValue = (theOscMessage.get(1).stringValue());
      if (receivedValue.equals("off"))
      {
        tcf.setValue(false);
      }
      else if (receivedValue.equals("on"))
      {
        tcf.setValue(true);
      }

    }

    if (settingName.equals("positionFilterActive") == true)
    {
      boolean receivedValue = (theOscMessage.get(1).intValue() != 0);
      pfa.setValue(receivedValue);
    } 

    if (settingName.equals("touchScreenAspect") == true)
    {
      float receivedValue = (theOscMessage.get(1).floatValue());
      println(receivedValue);
      aspect.setText(Float.toString(receivedValue));
    } 

  }
}


void getSettingsFromProxy()
{
  println("Requesting settings from proxy");
  OscMessage myOscMessage = new OscMessage("/vega/requestForSettings");
  myOscMessage.add(0);
  OscP5.flush(myOscMessage, myRemoteLocation);
}

void refresh(TuioTime bundleTime) { 
  redraw();
}

