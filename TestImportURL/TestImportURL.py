#Author-
#Description-

import adsk.core, adsk.fusion, adsk.cam, traceback

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface
        importManager = app.importManager

        product = app.activeProduct
        design = adsk.fusion.Design.cast(product)
        rootComp = design.rootComponent

        filesname = ['HC.f3d']

        for fn in filesname:

            wayfile = 'C:/Users/Xylia/Desktop/test'+ fn

            archiveOptionsNew = importManager.createFusionArchiveImportOptions(wayfile)
            importManager.importToTarget(archiveOptionsNew, rootComp)


    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
