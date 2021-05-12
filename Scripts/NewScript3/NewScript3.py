
import adsk.core, adsk.fusion, adsk.cam, traceback
from .HTTPRequest import requests
import base64
import tempfile
import uuid

app = None
ui  = None
commandId = 'CommandInputHTTPRequest'
commandName = 'Command Input HTTP Request'
commandDescription = 'Command Input HTTP Request'

payload_data = dict()

handlers = [] 

class MyCommandDestroyHandler(adsk.core.CommandEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):
        try:
            # When the command is done, terminate the script
            # This will release all globals which will remove all event handlers
            adsk.terminate()
        except:
            if ui:
                ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

class MyCommandCreatedHandler(adsk.core.CommandCreatedEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):
        try:            
            ui.messageBox('fired!')
            
            url = 'http://posttestserver.com/post.php'
            payload_data['post body string 1'] =  'post body value 1'
            payload_data['post body string 2'] =  'post body value 2'
            payload_data['post body string 3'] =  'post body value 3'
            payload_data['post body string 4'] =  'post body value 4'
            
            # Instantiate Export Manager
            current_design_context = app.activeProduct
            export_manager = current_design_context.exportManager
            
            #temp id for the file name
            transaction_id = str(uuid.uuid1())

            #snapshot of the model
            ui.activeSelections.clear()
            output_snapshot_name = tempfile.mkdtemp()+'//'+ transaction_id +'.jpg'
            app.activeViewport.saveAsImageFile(output_snapshot_name, 300, 300)  
            #base64 string of the image
            encoded_string = ''
            with open(output_snapshot_name, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read())                
            payload_data['snapshot'] = encoded_string 
            
            
            #upload a Fusion 360 file 
            payload_data['uuid'] = transaction_id + '.f3d'
            output_file_name = tempfile.mkdtemp()+'//'+ transaction_id +'.f3d'
            options = export_manager.createFusionArchiveExportOptions(output_file_name)
            export_manager.execute(options)
            fusion_file = {'file': open(output_file_name, 'rb')}
            
            #upload a step file 
            #payload_data['uuid'] = transaction_id + '.step'
            #output_file_name = tempfile.mkdtemp()+'//'+ transaction_id +'.step'
            #options = export_manager.createSTEPExportOptions(output_file_name)
            #export_manager.execute(options)
            #temp = {'file': open(output_file_name, 'rb')}                           

             # Send to platform
            try:
                message = "Error: "

                # POST response               
                res = requests.post(url, data=payload_data,files=fusion_file)

                # Check status
                if res.status_code == 200:  # success
                    message = "Posting Succeeded! "  + res.text          

                else:  # failure/res.status_code==422           
                    message += str(res.status_code)

            # Connection timed out
            except requests.exceptions.ConnectTimeout:
                message += "Connection timed out."

            # Failed to connect
            except requests.exceptions.ConnectionError:
                message += "Connection erroraa."
            
            #display the message of post response 
            cmd = args.command             
            inputs = cmd.commandInputs                                  
            txtBox = inputs.addTextBoxCommandInput('postresponse', 'Post Response', '', 5, True)
            txtBox.text = message 
                    
        except:
            if ui:
                ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
                
def run(context):
    ui = None
    try:
        global app
        app = adsk.core.Application.get()
        global ui
        ui = app.userInterface

        global commandId
        global commandName
        global commandDescription

        # Create command defintion
        cmdDef = ui.commandDefinitions.itemById(commandId)
        if not cmdDef:
            cmdDef = ui.commandDefinitions.addButtonDefinition(commandId, commandName, commandDescription)

        # Add command created event
        onCommandCreated = MyCommandCreatedHandler()
        cmdDef.commandCreated.add(onCommandCreated)
        # Keep the handler referenced beyond this function
        handlers.append(onCommandCreated)

        # Execute command
        cmdDef.execute()

        # Prevent this module from being terminate when the script returns, because we are waiting for event handlers to fire
        adsk.autoTerminate(False) 

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc())) 