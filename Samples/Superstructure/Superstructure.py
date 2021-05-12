# #Author-me

# import adsk.core, adsk.fusion, adsk.cam, traceback
# import json

# # global set of event handlers to keep them referenced for the duration of the command
# handlers = []
# _app = adsk.core.Application.cast(None)
# _ui = adsk.core.UserInterface.cast(None)
# num = 0


# # Event handler for the commandExecuted event.
# # class ShowPaletteCommandExecuteHandler(adsk.core.CommandEventHandler):
# #     def __init__(self):
# #         super().__init__()
# #     def notify(self, args):
# #         try:
# #             # Create and display the palette.
# #             palette = _ui.palettes.itemById('myExport')
# #             if not palette:
# #                 #make the [close] button invisible
# #                 palette = _ui.palettes.add('myExport', 'My Export', 'palette.html', True, False, True, 800, 200)

# #                 # Dock the palette to the right side of Fusion window.
# #                 palette.dockingState = adsk.core.PaletteDockingStates.PaletteDockStateRight
    
# #                 # Add handler to HTMLEvent of the palette.
# #                 onHTMLEvent = MyHTMLEventHandler()
# #                 palette.incomingFromHTML.add(onHTMLEvent)   
# #                 handlers.append(onHTMLEvent)
    
                
# #                 # Add handler to CloseEvent of the palette.
# #                 #onClosed = MyCloseEventHandler()
# #                 #palette.closed.add(onClosed)
# #                 #handlers.append(onClosed)   
# #             else:
# #                 palette.isVisible = True                               
# #         except:
# #             _ui.messageBox('Command executed failed: {}'.format(traceback.format_exc()))


# # # Event handler for the commandCreated event.
# # class ShowPaletteCommandCreatedHandler(adsk.core.CommandCreatedEventHandler):
# #     def __init__(self):
# #         super().__init__()              
# #     def notify(self, args):
# #         try:
# #             command = args.command
# #             onExecute = ShowPaletteCommandExecuteHandler()
# #             command.execute.add(onExecute)
# #             handlers.append(onExecute)                                     
# #         except:
# #             _ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))     


# # # Event handler for the commandExecuted event.
# # class SendInfoCommandExecuteHandler(adsk.core.CommandEventHandler):
# #     def __init__(self):
# #         super().__init__()
# #     def notify(self, args):
# #         try:
# #             # Send information to the palette. This will trigger an event in the javascript
# #             # within the html so that it can be handled.
# #             palette = _ui.palettes.itemById('myPalette')
# #             if palette:
# #                 global num
# #                 num += 1
# #                 palette.sendInfoToHTML('send', 'This is a message sent to the palette from Fusion. It has been sent {} times.'.format(num))                        
# #         except:
# #             _ui.messageBox('Command executed failed: {}'.format(traceback.format_exc()))


# # # Event handler for the commandCreated event.
# # class SendInfoCommandCreatedHandler(adsk.core.CommandCreatedEventHandler):
# #     def __init__(self):
# #         super().__init__()              
# #     def notify(self, args):
# #         try:
# #             command = args.command
# #             onExecute = SendInfoCommandExecuteHandler()
# #             command.execute.add(onExecute)
# #             handlers.append(onExecute)                                     
# #         except:
# #             _ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))     


# # # Event handler for the palette close event.
# # class MyCloseEventHandler(adsk.core.UserInterfaceGeneralEventHandler):
# #     def __init__(self):
# #         super().__init__()
# #     def notify(self, args):
# #         try:
# #             _ui.messageBox('Close button is clicked.') 
# #         except:
# #             _ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))


# # # Event handler for the palette HTML event.                
# # class MyHTMLEventHandler(adsk.core.HTMLEventHandler):
# #     def __init__(self):
# #         super().__init__()
# #     def notify(self, args):
# #         try:
# #             htmlArgs = adsk.core.HTMLEventArgs.cast(args)            
# #             data = json.loads(htmlArgs.data)
            
# #             if data['action']=='cancel':
# #                     palette = _ui.palettes.itemById('myExport')
# #                     if palette :
# #                          palette.isVisible = False  
                         
# #             if data['action']=='save':
# #                     palette = _ui.palettes.itemById('myExport')
# #                     if palette :
# #                          palette.isVisible = False 
# #                          #do save
# #                          args = data['arguments']
# #                          fullFileName = args['filepath'] + '\\' + args['filename']
# #                          filetype = args['filetype']
                         
                         
# #                          design = adsk.fusion.Design.cast(_app.activeProduct)
                         
# #                          #check save type
# #                          if 'Archive' in filetype:
# #                             option = design.exportManager.createFusionArchiveExportOptions(fullFileName, design.rootComponent)
                                
# #                          elif 'IGES' in filetype:
# #                             option = design.exportManager.createIGESExportOptions(fullFileName, design.rootComponent)
# #                          elif 'SAT' in filetype:
# #                             option = design.exportManager.createSATExportOptions (fullFileName, design.rootComponent)
     
# #                          elif 'SMT' in filetype:
# #                             option = design.exportManager.createSMTExportOptions (fullFileName, design.rootComponent)
     
# #                          elif 'STEP' in filetype :
# #                             option = design.exportManager.createSTEPExportOptions (fullFileName, design.rootComponent)
     
# #                          design.exportManager.execute(option) 
                
# #         except:
# #             _ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))           


                
# def run(context):
#     ui = None
#     try:
#         _app = adsk.core.Application.get()
#         _ui  = _app.userInterface

#         #СОЗДАНИЕ КНОПКИ В ТУЛБАРЕ

#         workSpace = _ui.workspaces.itemById('FusionSolidEnvironment')
#         tbPanels = workSpace.toolbarPanels
        
#         tbPanel = tbPanels.itemById('NewPanel')
#         if tbPanel:
#             tbPanel.deleteMe()
#         tbPanel = tbPanels.add('NewPanel', 'Муфты', 'SelectPanel', False)
        
#         # Empty panel can't be displayed. Add a command to the panel
#         cmdDef = _ui.commandDefinitions.itemById('NewCommand')
#         if cmdDef:
#             cmdDef.deleteMe()
#         cmdDef = _ui.commandDefinitions.addButtonDefinition('NewCommand', 'Муфты', 'Demo for new command')
#         tbPanel.controls.addCommand(cmdDef)

#          workSpace = ui.workspaces.itemById('FusionSolidEnvironment')
#         tbPanels = workSpace.toolbarPanels
        
#         global tbPanel
#         tbPanel = tbPanels.itemById('NewPanel')
#         if tbPanel:
#             tbPanel.deleteMe()
#         tbPanel = tbPanels.add('NewPanel', 'New Panel', 'SelectPanel', False)
        

#         sampleCommandCreated = SampleCommandCreatedEventHandler()
#         cmdDef.commandCreated.add(sampleCommandCreated)
#         handlers.append(sampleCommandCreated)


#         #СОЗДАНИЕ ОКНА
        
#         # # Add a command that displays the panel.
#         # showPaletteCmdDef = _ui.commandDefinitions.itemById('showPalette')
#         # if not showPaletteCmdDef:
#         #     showPaletteCmdDef = _ui.commandDefinitions.addButtonDefinition('showPalette', 'Show custom palette', 'Show the custom palette', '')

#         #     # Connect to Command Created event.
#         #     onCommandCreated = ShowPaletteCommandCreatedHandler()
#         #     showPaletteCmdDef.commandCreated.add(onCommandCreated)
#         #     handlers.append(onCommandCreated)
        
         
#         # # Add a command under ADD-INS panel which sends information from Fusion to the palette's HTML.
#         # sendInfoCmdDef = _ui.commandDefinitions.itemById('sendInfoToHTML')
#         # if not sendInfoCmdDef:
#         #     sendInfoCmdDef = _ui.commandDefinitions.addButtonDefinition('sendInfoToHTML', 'Send info to Palette', 'Send Info to Palette HTML', '')

#         #     # Connect to Command Created event.
#         #     onCommandCreated = SendInfoCommandCreatedHandler()
#         #     sendInfoCmdDef.commandCreated.add(onCommandCreated)
#         #     handlers.append(onCommandCreated)

#         # # Add the command to the toolbar.
#         # panel = _ui.allToolbarPanels.itemById('SolidScriptsAddinsPanel')
#         # cntrl = panel.controls.itemById('showPalette')
#         # if not cntrl:
#         #     panel.controls.addCommand(showPaletteCmdDef)

#         # cntrl = panel.controls.itemById('sendInfoToHTML')
#         # if not cntrl:
#         #     panel.controls.addCommand(sendInfoCmdDef)
#     except:
#         if _ui:
#             _ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))


# def stop(context):
#     ui = None
#     try:
        
#         ui.messageBox('Stop addin')

#     except:
#         if ui:
#             ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

import adsk.core, adsk.fusion, adsk.cam, traceback

handlers = []
app = adsk.core.Application.get()
ui  = app.userInterface

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface
        ui.messageBox('Hello addin')
        workSpace = ui.workspaces.itemById('FusionSolidEnvironment')
        tbPanels = workSpace.toolbarPanels
                

        tbPanel = tbPanels.itemById('NewPanel')
        if tbPanel:
            tbPanel.deleteMe()
        tbPanel = tbPanels.add('NewPanel', 'Муфты', 'SelectPanel', False)
        cmdDef = ui.commandDefinitions.itemById('NewCommand')
        if cmdDef:
            cmdDef.deleteMe()
        cmdDef = ui.commandDefinitions.addButtonDefinition('NewCommand', 'Создать муфту', 'Ввод параметром и построение муфты','.//resource')
        tbPanel.controls.addCommand(cmdDef)
           # Connect to the command created event.
        sampleCommandCreated = SampleCommandCreatedEventHandler()
        cmdDef.commandCreated.add(sampleCommandCreated)
        handlers.append(sampleCommandCreated)
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
# Event handler for the commandCreated event.
class SampleCommandCreatedEventHandler(adsk.core.CommandCreatedEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):
        eventArgs = adsk.core.CommandCreatedEventArgs.cast(args)
        cmd = eventArgs.command

        # Connect to the execute event.
        onExecute = SampleCommandExecuteHandler()
        cmd.execute.add(onExecute)
        handlers.append(onExecute)


# Event handler for the execute event.
class SampleCommandExecuteHandler(adsk.core.CommandEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):
        try:
            app = adsk.core.Application.get()
            ui  = app.userInterface
            # Create and display the palette.
            palette = ui.palettes.itemById('myExport')
            if palette:
                palette.deleteMe()
            if not palette:
                #make the [close] button invisible
                palette = ui.palettes.add('myExport', 'Муфты', 'Test.html', True, True, True, 600, 200)

                # Dock the palette to the right side of Fusion window.
                palette.dockingState = adsk.core.PaletteDockingStates.PaletteDockStateRight
    
            else: 
                palette.isVisible = True  
        except:
            _ui.messageBox('Command executed failed: {}'.format(traceback.format_exc()))

   
    
        
def stop(context):
    ui = None
    try:
        
        ui.messageBox('Stop addin')

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))