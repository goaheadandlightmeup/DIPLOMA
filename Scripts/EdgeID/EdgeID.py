#Author-
#Description-

import adsk.core, adsk.fusion, adsk.cam, traceback

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface

        faceSel = ui.selectEntity('Select a face.', 'Faces')
        edgeSel = ui.selectEntity('Select a edge.', 'Edges')
        if edgeSel and faceSel:
            selectedEdge = adsk.fusion.BRepEdge.cast(edgeSel.entity)
            selectedFace = adsk.fusion.BRepFace.cast(faceSel.entity)
            
            Facebody = selectedFace.body
            edgeCount = 0
            for face in Facebody.faces:
                if face == selectedFace:
                    for edge in selectedFace.edges:
                        if edge == selectedEdge:
                            break
                        
                        edgeCount += 1
            
            ui.messageBox('The selected edge is index ' + str(edgeCount))  

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
