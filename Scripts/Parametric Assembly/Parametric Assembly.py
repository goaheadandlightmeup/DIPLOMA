import adsk.core, adsk.fusion, adsk.cam, traceback

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface
        folder = app.data.activeProject.rootFolder.dataFolders.itemByName('Parametric Models') 
        folder2 = app.data.activeProject.rootFolder.dataFolders.itemByName('Couplings')
        transform = adsk.core.Matrix3D.create()

        product = app.activeProduct
        app.activeDocument.saveAs('Муфта фланцевая', folder2, '', '')
        design = adsk.fusion.Design.cast(product)
        rootComp = design.rootComponent
        allOccs = rootComp.occurrences
        joints = rootComp.joints
        features = rootComp.features
        inputEntites = adsk.core.ObjectCollection.create()
        circularFeats = features.circularPatternFeatures
        yAxis = rootComp.yConstructionAxis

        d_1HC = design.userParameters.itemByName('d_1HC')
        d_1HC_1 = design.userParameters.itemByName('d_1HC_1')
        
        filesHub = folder.dataFiles
        filesName = ['Полумуфта (16-11-1 УЗ ГОСТ 20761-96)', 'Полумуфта (16-11-1 УЗ ГОСТ 20761-96)', 'БОЛТ ГОСТ 7796', 'Болт ГОСТ 7817', 'Гайка ГОСТ', 'Гайка ГОСТ']

        models = []
        for fileName in filesName:
            for file in filesHub:
                if (file.name == fileName):
                    models.append(file)
        
        if (models is None):
            return

        for model in models:
            allOccs.addByInsert(model, transform, False)
        
        allOccs.item(0).isGrounded = True

        HC = allOccs.item(0).bRepBodies.item(0)
        HCEdges = HC.edges
        HCFaces = HC.faces

        HC2 = allOccs.item(1).bRepBodies.item(0)
        HC2Edges = HC2.edges
        HC2Faces = HC2.faces

        Bolt1 = allOccs.item(2).bRepBodies.item(0)
        Bolt1Edges = Bolt1.edges

        Bolt2 = allOccs.item(3).bRepBodies.item(0)
        Bolt2Edges = Bolt2.edges

        Nut = allOccs.item(4).bRepBodies.item(0)
        NutEdges = Nut.edges

        Nut2 = allOccs.item(5).bRepBodies.item(0)
        Nut2Edges = Nut2.edges

        HCJoint = HCEdges.item(5)
        Bolt1Joint = Bolt1Edges.item(1)

        geoHC = adsk.fusion.JointGeometry.createByCurve(HCJoint, adsk.fusion.JointKeyPointTypes.CenterKeyPoint)
        geoBolt1 = adsk.fusion.JointGeometry.createByCurve(Bolt1Joint, adsk.fusion.JointKeyPointTypes.CenterKeyPoint)
    
        jointInput_HCBolt1 = joints.createInput(geoBolt1, geoHC)
        offsetHCBolt1 = adsk.core.ValueInput.createByString('-21 mm')
        jointInput_HCBolt1.offset = offsetHCBolt1
        jointInput_HCBolt1.isFlipped = True
        joint_HCBolt1 = joints.add(jointInput_HCBolt1)

        HCJoint2 = HCEdges.item(4)
        Bolt2Joint = Bolt2Edges.item(3)

        geoHC2 = adsk.fusion.JointGeometry.createByCurve(HCJoint2, adsk.fusion.JointKeyPointTypes.CenterKeyPoint)
        geoBolt2 = adsk.fusion.JointGeometry.createByCurve(Bolt2Joint, adsk.fusion.JointKeyPointTypes.CenterKeyPoint)
    
        jointInput_HCBolt2 = joints.createInput(geoBolt2, geoHC2)
        offsetHCBolt2 = adsk.core.ValueInput.createByString('8.5 mm')
        jointInput_HCBolt2.offset = offsetHCBolt2
        jointInput_HCBolt2.isFlipped = True
        joint_HCBolt2 = joints.add(jointInput_HCBolt2)

        HCPlanar = HCFaces.item(2)
        HC2Planar = HC2Faces.item(2)

        geoHC2Planar = adsk.fusion.JointGeometry.createByPlanarFace(HC2Planar, None, adsk.fusion.JointKeyPointTypes.CenterKeyPoint)
        geoHCPlanar = adsk.fusion.JointGeometry.createByPlanarFace(HCPlanar, None, adsk.fusion.JointKeyPointTypes.CenterKeyPoint)
    
        jointInputHC = joints.createInput(geoHC2Planar, geoHCPlanar)
        angle = adsk.core.ValueInput.createByString('180 deg')
        jointInputHC.angle = angle
        jointInputHC.isFlipped = True
        jointHC = joints.add(jointInputHC)

        NutJoint = NutEdges.item(0)
        BoltJoint1 = Bolt1Edges.item(1)

        geoNut = adsk.fusion.JointGeometry.createByCurve(NutJoint, adsk.fusion.JointKeyPointTypes.CenterKeyPoint)
        geoBolt1New = adsk.fusion.JointGeometry.createByCurve(BoltJoint1, adsk.fusion.JointKeyPointTypes.CenterKeyPoint)

        jointNutBoltInput = joints.createInput(geoNut, geoBolt1New)
        offsetNut = adsk.core.ValueInput.createByString('-6.00 mm')
        jointNutBoltInput.offset = offsetNut
        jointNutBoltInput.isFlipped = False
        jointNutBolt = joints.add(jointNutBoltInput)

        Nut2Joint = Nut2Edges.item(1)
        BoltJoint2 = Bolt2Edges.item(2)

        geoNut2 = adsk.fusion.JointGeometry.createByCurve(Nut2Joint, adsk.fusion.JointKeyPointTypes.CenterKeyPoint)
        geoBolt2New= adsk.fusion.JointGeometry.createByCurve(BoltJoint2, adsk.fusion.JointKeyPointTypes.CenterKeyPoint)

        jointNut2Bolt2Input = joints.createInput(geoNut2, geoBolt2New)
        offsetNut2 = adsk.core.ValueInput.createByString('-27.50 mm')
        jointNut2Bolt2Input.offset = offsetNut2
        jointNut2Bolt2Input.isFlipped = False
        jointNut2Bolt2 = joints.add(jointNut2Bolt2Input)

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
