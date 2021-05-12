import adsk.core, adsk.fusion, adsk.cam, traceback
import os.path, sys

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface

        product = app.activeProduct
        design = adsk.fusion.Design.cast(product)
        rootComp = design.rootComponent
        
        h = '100.00 mm' 
        d = '5.25 mm' 
        D = '19.75 mm' 

        hParam = design.userParameters.itemByName('h')
        hParam.expression = h

        DParam = design.userParameters.itemByName('D')
        DParam.expression = D

        dParam = design.userParameters.itemByName('d')
        dParam.expression = d

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
