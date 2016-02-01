# -*- coding: utf-8 -*-
#
#  FuslightController.py
#  Fuslight
#
#  Created by Kristian Botnen on 28.01.16.
#  Copyright (c) 2016 University of Bergen. All rights reserved.
#

from objc import YES, NO, IBAction, IBOutlet
from Foundation import *
from AppKit import *

# UiB Tools
import sys
sys.path.append('/usr/local/uibtools')
import uiblibrary

import subprocess
import time

class MainController(NSObject):
    
    mainMenu = objc.IBOutlet()
    
    def statMenu(self, sender):
        # Make statusbar item
        statusbar = NSStatusBar.systemStatusBar()
        self.statusitem = statusbar.statusItemWithLength_(NSVariableStatusItemLength)
        # Icon code
        self.icon = NSImage.alloc().initByReferencingFile_('/usr/local/share/uib/UiBmerke_grayscale_96.png')
        self.icon.setScalesWhenResized_(YES)
        self.icon.setSize_((19, 19))
        self.statusitem.setImage_(self.icon)
        
        self.statusitem.setHighlightMode_(True)
        self.statusitem.setTitle_('Fuslight StatusItem Title')
        self.statusitem.setAttributedTitle_('')
        
        # Make the menu
        
        #NSFullUserName()
        self.menubarMenu = NSMenu.alloc().init()
        #self.menubarMenu.setAutoenablesItems_(NO)
        
        #Add the users name
        self.menuItem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(NSFullUserName(), '', '')
        self.menuItem.setTarget_(self)
        self.menubarMenu.addItem_(self.menuItem)
        
        self.menuItem = NSMenuItem.separatorItem()
        self.menubarMenu.addItem_(self.menuItem)
        
        self.menuItem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_('Windows homefolder', 'launchUibMountWindowsfolder:', '')
        self.menuItem.setTarget_(self)
        self.menubarMenu.addItem_(self.menuItem)
        
        self.menuItem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_('Unix homefolder', 'launchUibMountUnixfolder:', '')
        self.menuItem.setTarget_(self)
        self.menubarMenu.addItem_(self.menuItem)
        
        self.menuItem = NSMenuItem.separatorItem()
        self.menubarMenu.addItem_(self.menuItem)
        
        #self.menuItem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_('UiB VPN', 'launchUibVpn:', '')
        #self.menuItem.setTarget_(self)
        #self.menubarMenu.addItem_(self.menuItem)
        
        #self.menuItem = NSMenuItem.separatorItem()
        #self.menuItem.setTarget_(self)
        #self.menubarMenu.addItem_(self.menuItem)
        
        self.menuItem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_('UiB Tools', 'launchUibtools:', '')
        self.menuItem.setTarget_(self)
        self.menubarMenu.addItem_(self.menuItem)
        
        self.menuItem = NSMenuItem.separatorItem()
        self.menubarMenu.addItem_(self.menuItem)
        
        self.menuItem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_('Login window', 'loginWindow:', '')
        self.menuItem.setTarget_(self)
        self.menubarMenu.addItem_(self.menuItem)
        
        self.menuItem = NSMenuItem.separatorItem()
        self.menubarMenu.addItem_(self.menuItem)
                
        self.menuItem = NSMenuItem.separatorItem()
        self.menubarMenu.addItem_(self.menuItem)
        
        self.quit = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_('Quit UiB-tool menu', 'terminate:', '')
        self.menuItem.setTarget_(self)
        self.menubarMenu.addItem_(self.quit)
        
        #add menu to statusitem
        self.statusitem.setMenu_(self.menubarMenu)
        #self.statusitem.setMenu_(self.mainMenu)
        self.statusitem.setToolTip_('FUS Light')
    
    def loginWindow_(self, notification):
        #notification is <NSMenuItem: 0x1020c4370 Switch user>
        try:
            proc = subprocess.Popen(["/System/Library/CoreServices/Menu Extras/User.menu/Contents/Resources/CGSession","-suspend"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
        except (OSError) as e:
            NSLog(e)

    def launchUibtools_(self, notification):
        try:
            proc = subprocess.Popen(["/Applications/UiB\ Tools.app/Contents/MacOS/UiB\ Tools",], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        except (OSError) as e:
            NSLog(e)

    def launchUibVpn_(self, notification):
        try:
            uiblibrary.connectvpn("UiB Ansatt VPN", "%s@ansatt" % NSUserName())
        except (OSError) as e:
            NSLog(e)
                
    def launchUibMountWindowsfolder_(self, notification):
        try:
            uibip = uiblibrary.getstatusuibnet()
            if (uibip):
                uiblibrary.openuriinfinder(uiblibrary.findwindowshomedirectory(NSUserName()))
                s = NSAppleScript.alloc().initWithSource_("tell app \"Finder\" to activate")
                s.executeAndReturnError_(None)
            else:
                uiblibrary.connectvpn("UiB Ansatt VPN", "%s@ansatt" % NSUserName())
                timeout = 0
                while not uibip and timeout < 5:
                    time.sleep(1)
                    uibip = uiblibrary.getstatusuibnet()
                    print "DEBUG: Waiting for UiB IP"
                    timeout += 1
                if (uibip):
                    uiblibrary.openuriinfinder(uiblibrary.findwindowshomedirectory(NSUserName()))
                    s = NSAppleScript.alloc().initWithSource_("tell app \"Finder\" to activate")
                    s.executeAndReturnError_(None)
                else:
                    print "DEBUG: Still no UiB IP-address, giving up."
                    self.notify("Cant establish connection", "Missing uib-ip", "Please connect to VPN and retry")
                    pass
        except (OSError) as e:
            NSLog(e)

    def launchUibMountUnixfolder_(self, notification):
        try:
            uiblibrary.openuriinfinder(uiblibrary.findunixhomedirectory(NSUserName()))
            s = NSAppleScript.alloc().initWithSource_("tell app \"Finder\" to activate")
            s.executeAndReturnError_(None)
        except (OSError) as e:
            NSLog(e)
                
    def notify(self, title, subtitle, text):
        notification = NSUserNotification.alloc().init()
        notification.setTitle_(str(title))
        notification.setSubtitle_(str(subtitle))
        notification.setInformativeText_(str(text))
        notification.setSoundName_("NSUserNotificationDefaultSoundName")
        NSUserNotificationCenter.defaultUserNotificationCenter().scheduleNotification_(notification)


