# from burp import IBurpExtender
# from burp import IContextMenuFactory
# from burp import IExtensionHelpers
# from javax.swing import JMenuItem
# from java.awt.event import ActionListener
# from java.awt.event import ActionEvent
# from java.awt.event import KeyEvent
# import traceback
# # Burp is configured to look for python modules in c:\python27\lib.
# # If the following file exists in that directory, it will be loaded
# import UniqueParamValues
#
#
# class BurpExtender(IBurpExtender, IContextMenuFactory, ActionListener):
#     def __init__(self):
#         self.menuItem = JMenuItem('Print Unique Parameter Values')
#         self.menuItem.addActionListener(self)
#
#     def actionPerformed(self, actionEvent):
#
#         print "*" * 60
#         # Here is the reload. You can place this anywhere you wantm but you will
#         # most likely want to place this within an action (request recieved, menu
#         # item clicked, scanner started, etc).
#         reload(UniqueParamValues)
#         # This try statement, and the traceback included in the except, are what
#         # allowed me to finally get the trace information I needed to debug my
#         # issues.  I highly recommned including these when developing Burp
#         # Extensions
#         try:
#             UniqueParamValues.getUniqueParams(self)
#         except:
#             tb = traceback.format_exc()
#             print tb
#
#             # implement IBurpExtender
#
#
#     def registerExtenderCallbacks(self, callbacks):
#         # keep a reference to our callbacks object (Burp Extensibility Feature)
#         self._callbacks = callbacks
#         self._helpers = callbacks.getHelpers()
#         # set our extension name
#         callbacks.setExtensionName("Unique Parameter Values")
#         callbacks.registerContextMenuFactory(self)
#         return
#
#
#     def createMenuItems(self, ctxMenuInvocation):
#         self.ctxMenuInvocation = ctxMenuInvocation
#
#         return [self.menuItem]