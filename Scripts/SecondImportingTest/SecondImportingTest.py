import adsk.core, adsk.fusion, adsk.cam, traceback

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface
        folder = app.data.activeProject.rootFolder.dataFolders.itemByName('Diploma') 
        folder2 = app.data.activeProject.rootFolder.dataFolders.itemByName('folder')
        transform = adsk.core.Matrix3D.create()

        product = app.activeProduct
        app.activeDocument.saveAs('Assembly', folder2, '', '')
        design = adsk.fusion.Design.cast(product)
        rootComp = design.rootComponent
        allOccs = rootComp.occurrences
        joints = rootComp.joints
        features = rootComp.features
        inputEntites = adsk.core.ObjectCollection.create()
        yAxis = rootComp.yConstructionAxis


        filesHub = folder.dataFiles
        filesName = ['Half-Coupling', 'Half-Coupling', 'Nut', 'Bolt']

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

        NutOccs = allOccs.item(2).bRepBodies.item(0)
        NutEdges = NutOccs.edges

        BoltOccs = allOccs.item(3).bRepBodies.item(0)
        BoltOccs2 = allOccs.item(3).bRepBodies.item(1)
        BoltFaces = BoltOccs.faces
        BoltEdges = BoltOccs.edges

        HCJoint = HCEdges.item(0)
        NutJoint = NutEdges.item(1)
        
        geoNut = adsk.fusion.JointGeometry.createByCurve(NutJoint, adsk.fusion.JointKeyPointTypes.CenterKeyPoint)
        geoHC = adsk.fusion.JointGeometry.createByCurve(HCJoint, adsk.fusion.JointKeyPointTypes.CenterKeyPoint)
    
        jointInput = joints.createInput(geoNut, geoHC)
        offset = adsk.core.ValueInput.createByString('0 mm')
        jointInput.isFlipped = False
        joint = joints.add(jointInput)

        circularFeats = features.circularPatternFeatures
        inputEntites.add(NutOccs)

        circularFeatInput = circularFeats.createInput(inputEntites, yAxis)
        circularFeatInput.quantity = adsk.core.ValueInput.createByReal(4)
        circularFeatInput.totalAngle = adsk.core.ValueInput.createByString('360 deg')
        circularFeatInput.isSymmetric = False
        circularFeat = circularFeats.add(circularFeatInput)

        HCPlanar = HCFaces.item(12)
        HC2Planar = HC2Faces.item(12)

        geoHC2Planar = adsk.fusion.JointGeometry.createByPlanarFace(HC2Planar, None, adsk.fusion.JointKeyPointTypes.CenterKeyPoint)
        geoHCPlanar = adsk.fusion.JointGeometry.createByPlanarFace(HCPlanar, None, adsk.fusion.JointKeyPointTypes.CenterKeyPoint)
    
        jointInputHC = joints.createInput(geoHC2Planar, geoHCPlanar)
        angle = adsk.core.ValueInput.createByString('180 deg')
        jointInputHC.angle = angle
        jointInputHC.isFlipped = True
        jointHC = joints.add(jointInputHC)

        BoltJoint = BoltEdges.item(6)
        HC2Joint = HC2Edges.item(1)

        geoBolt = adsk.fusion.JointGeometry.createByCurve(BoltJoint, adsk.fusion.JointKeyPointTypes.CenterKeyPoint)
        geoHC2 = adsk.fusion.JointGeometry.createByCurve(HC2Joint, adsk.fusion.JointKeyPointTypes.CenterKeyPoint)

        jointBoltHCInput = joints.createInput(geoBolt, geoHC2)
        angle = adsk.core.ValueInput.createByString('180 deg')
        jointBoltHCInput.angle = angle
        offsetBolt = adsk.core.ValueInput.createByString('13.00 mm')
        jointBoltHCInput.offset = offsetBolt
        jointBoltHCInput.isFlipped = False
        jointHCBolt = joints.add(jointBoltHCInput)

        inputEntitesBolt = adsk.core.ObjectCollection.create()
        inputEntitesBolt.add(BoltOccs)
        circularBoltHC2FeatInput = circularFeats.createInput(inputEntitesBolt, yAxis)
        circularBoltHC2FeatInput.quantity = adsk.core.ValueInput.createByReal(4)
        circularBoltHC2FeatInput.totalAngle = adsk.core.ValueInput.createByString('360 deg')
        circularBoltHC2FeatInput.isSymmetric = False
        circularFeatBoltHC2 = circularFeats.add(circularBoltHC2FeatInput)

        inputEntitesBolt2 = adsk.core.ObjectCollection.create()
        inputEntitesBolt2.add(BoltOccs2)
        circularBoltHC2FeatInput2 = circularFeats.createInput(inputEntitesBolt2, yAxis)
        circularBoltHC2FeatInput2.quantity = adsk.core.ValueInput.createByReal(4)
        circularBoltHC2FeatInput2.totalAngle = adsk.core.ValueInput.createByString('360 deg')
        circularBoltHC2FeatInput2.isSymmetric = False
        circularFeat2BoltHC2 = circularFeats.add(circularBoltHC2FeatInput2)

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

