# -*- coding: utf-8 -*-
#
#  AppDelegate.py
#  Fuslight
#
#  Created by Kristian Botnen on 28.01.16.
#  Copyright (c) 2016 University of Bergen. All rights reserved.
#

from Foundation import *
from AppKit import *

class AppDelegate(NSObject):
    
    mainController = objc.IBOutlet()
    
    def applicationDidFinishLaunching_(self, sender):
        NSLog("Application did finish launching.")
        if self.mainController:
            self.mainController.statMenu(self)

    def applicationWillTerminate_(self, notification):
        # Be nice and remove our observers from NSWorkspace
        nc = NSWorkspace.sharedWorkspace().notificationCenter()
        nc.removeObserver_(self.mainController)

