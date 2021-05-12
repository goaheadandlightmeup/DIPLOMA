import adsk.core, adsk.fusion, adsk.cam, traceback

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface

        faceSel = ui.selectEntity('Select a face.', 'Faces')
        if faceSel:
            selectedFace = adsk.fusion.BRepFace.cast(faceSel.entity)

            # Find the index of this face within the body.            
            body = selectedFace.body
            edgeCount = 0
            for face in body.faces:
                if face == selectedFace:
                    break
                
                edgeCount += 1

            ui.messageBox('The selected face is index ' + str(edgeCount))                

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))