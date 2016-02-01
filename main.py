# -*- coding: utf-8 -*-
#
#  main.py
#  Fuslight
#
#  Created by Kristian Botnen on 28.01.16.
#  Copyright (c) 2016 University of Bergen. All rights reserved.
#

# Do we need the 3 imports below?
import objc
import Foundation
import AppKit

from PyObjCTools import AppHelper

# Import modules containing classes required to start application and load MainMenu.nib
import AppDelegate

# Our application
import MainController

# Pass control to AppKit
AppHelper.runEventLoop()
