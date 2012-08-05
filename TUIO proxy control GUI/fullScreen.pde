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

import java.awt.GraphicsEnvironment;
import java.awt.GraphicsDevice;

fullScreenHandler fullscreen = new fullScreenHandler();

class fullScreenHandler{
  
  int fullScreenDisplayNumber = 0;

  void on(){
    if (fs.isFullScreen() == false){
      fs = new SoftFullScreen(mainSketch, fullScreenDisplayNumber);
      GraphicsEnvironment env = GraphicsEnvironment.getLocalGraphicsEnvironment();
      GraphicsDevice[] devices = env.getScreenDevices();
      int w = devices[fullScreenDisplayNumber].getDisplayMode().getWidth();
      int h = devices[fullScreenDisplayNumber].getDisplayMode().getHeight();
      frame.setSize(w, h);
      size (w, h);
      fs.enter();
    }   
  }
  
  void forceOn(){
      fs = new SoftFullScreen(mainSketch, fullScreenDisplayNumber);
      GraphicsEnvironment env = GraphicsEnvironment.getLocalGraphicsEnvironment();
      GraphicsDevice[] devices = env.getScreenDevices();
      int w = devices[fullScreenDisplayNumber].getDisplayMode().getWidth();
      int h = devices[fullScreenDisplayNumber].getDisplayMode().getHeight();
      frame.setSize(w, h);
      size (w, h);
      fs.enter();   
  }
  
  boolean isOn(){
    return fs.isFullScreen();
  }
  
  void off(){
    fs.leave();
    frame.setSize(normalWindowWidth, normalWindowHeight);
    size (normalWindowWidth, normalWindowHeight);
  }
  
  void setScreenNumber(int num){
    this.fullScreenDisplayNumber = num;
  }
  
  int numberOfScreens(){
  GraphicsEnvironment env = GraphicsEnvironment.getLocalGraphicsEnvironment();
  GraphicsDevice[] devices = env.getScreenDevices();
  println(devices[0].getDisplayMode().getHeight());
  return devices.length;
  }
  
}
