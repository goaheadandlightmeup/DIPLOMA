import adsk.core, adsk.fusion, adsk.cam, traceback

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface
        folder = app.data.activeProject.rootFolder.dataFolders.itemByName('Diploma')
        # newFolder = app.data.activeProject.rootFolder.dataFolders.itemByName('newDiploma')
        transform = adsk.core.Matrix3D.create()

        product = app.activeProduct
        app.activeDocument.saveAs('Main Assembly', folder, '', '')
        design = adsk.fusion.Design.cast(product)
        rootComp = design.rootComponent
        allOccs = rootComp.occurrences
        joints = rootComp.joints
            
        for file in folder.dataFiles:
            if (file.name == 'Nut' or file.name == 'Half-Coupling' or file.name == 'Bolt GOST' or file.name == 'Bolt'):
                allOccs.addByInsert(file, transform, False) 
            continue 

        # bodyNut = allOccs.item(0).bRepBodies.item(0)
        # edgesNut = bodyNut.edges()

        # bodyHC = allOccs.item(1).bRepBodies.item(0)
        # edgesHC = bodyHC.edges

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
