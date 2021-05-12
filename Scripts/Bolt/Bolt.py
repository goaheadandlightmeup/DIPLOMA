import adsk.core, adsk.fusion, adsk.cam, traceback, math

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface

        doc = app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType)
        design = app.activeProduct
        rootComp = design.rootComponent
        features = rootComp.features
        extrudes = features.extrudeFeatures 
        threadFeatures = rootComp.features.threadFeatures

        sketchPolygon = rootComp.sketches.add(rootComp.xZConstructionPlane)
        
        pointsPolygon = adsk.core.ObjectCollection.create()
        pointsPolygon.add(adsk.core.Point3D.create(0, 0, 0.6928))
        pointsPolygon.add(adsk.core.Point3D.create(-0.6, 0, 0.3464))
        pointsPolygon.add(adsk.core.Point3D.create(-0.6, 0, -0.3464))
        pointsPolygon.add(adsk.core.Point3D.create(0, 0, -0.6928))
        pointsPolygon.add(adsk.core.Point3D.create(0.6, 0, -0.3464))
        pointsPolygon.add(adsk.core.Point3D.create(0.6, 0, 0.3464))
        pointsPolygon.add(adsk.core.Point3D.create(0, 0, 0.6928))

        for i in range(pointsPolygon.count-1):
            ptP1 = pointsPolygon.item(i)
            ptP2 = pointsPolygon.item(i+1)
            sketchPolygon.sketchCurves.sketchLines.addByTwoPoints(ptP1, ptP2)

        extPolygon = adsk.core.ObjectCollection.create()
        extPolygon = sketchPolygon.profiles.item(0)
        extrudePolygon = features.extrudeFeatures
        extrudePolygonInput = extrudes.createInput(extPolygon, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        extrudePolygonInput.isSolid = True
        extrudePolygonInput.setDistanceExtent(False, adsk.core.ValueInput.createByReal(0.55))
        polygon = extrudes.add(extrudePolygonInput)

        sketchCircle = rootComp.sketches.add(rootComp.xYConstructionPlane)
        sketchCir = sketchCircle.sketchCurves.sketchCircles
        centerPoint = adsk.core.Point3D.create(0, 0, 0.55)
        sketchCir.addByCenterRadius(centerPoint, 0.45)

        extCircle = adsk.core.ObjectCollection.create()
        extCircle.add(sketchCircle.profiles.item(0))
        extrudeCircle = features.extrudeFeatures 
        extrudeCircleInput = extrudeCircle.createInput(extCircle, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        extrudeCircleInput.isSolid = True
        extrudeCircleInput.setDistanceExtent(False, adsk.core.ValueInput.createByReal(1.35))
        circle = extrudeCircle.add(extrudeCircleInput)

        sketchCircleFillet = rootComp.sketches.add(rootComp.xZConstructionPlane)
        pointsCirlceFillet = adsk.core.ObjectCollection.create()
        pointsCirlceFillet.add(adsk.core.Point3D.create(0, 0, -0.53))
        pointsCirlceFillet.add(adsk.core.Point3D.create(0, 0, -0.8396))
        pointsCirlceFillet.add(adsk.core.Point3D.create(0, -0.1788, -0.8396 ))
        pointsCirlceFillet.add(adsk.core.Point3D.create(0, 0, -0.53))

        for i in range(pointsCirlceFillet.count-1):
            ptCF1= pointsCirlceFillet.item(i)
            ptCF2 = pointsCirlceFillet.item(i+1)
            sketchCircleFillet.sketchCurves.sketchLines.addByTwoPoints(ptCF1, ptCF2)
        
        angFillet = math.pi*2
        centerAxis = rootComp.zConstructionAxis
        profRevolvle = sketchCircleFillet.profiles.item(0)
        revolves = rootComp.features.revolveFeatures 
        revolveFilletInput = revolves.createInput(profRevolvle, centerAxis, adsk.fusion.FeatureOperations.CutFeatureOperation)
        angleFillet = adsk.core.ValueInput.createByReal(angFillet)
        revolveFilletInput.setAngleExtent(False, angleFillet)
        extFillet = revolves.add(revolveFilletInput) 

        sketchNewCircle = rootComp.sketches.add(rootComp.xYConstructionPlane)
        sketchCircleThread = sketchNewCircle.sketchCurves.sketchCircles
        centerPointThread = adsk.core.Point3D.create(0, 0, 1.9)
        sketchCircleThread.addByCenterRadius(centerPointThread, 0.4)

        extCircleThread = adsk.core.ObjectCollection.create()
        extCircleThread.add(sketchNewCircle.profiles.item(0))
        extrudeCircleThread = features.extrudeFeatures
        extrudeCircleThreadInput = extrudeCircleThread.createInput(extCircleThread, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        extrudeCircleThreadInput.isSolid = True
        extrudeCircleThreadInput.setDistanceExtent(False, adsk.core.ValueInput.createByReal(1.2))
        threadCircle = extrudeCircleThread.add(extrudeCircleThreadInput)

        edgeCol = adsk.core.ObjectCollection.create()
        edges = threadCircle.endFaces[0].edges
        for edgeI  in edges:
            edgeCol.add(edgeI)

        chamferFeats = rootComp.features.chamferFeatures
        chamferInput = chamferFeats.createInput(edgeCol, True)

        chamferDistance = adsk.core.ValueInput.createByReal(0.05)
        chamferInput.setToEqualDistance(chamferDistance)
        chamferComp = chamferFeats.add(chamferInput)

        threadDataQuery = threadFeatures.threadDataQuery

        threadTypes = threadDataQuery.allThreadTypes
        print(threadTypes)
        threadType = threadTypes[10]
        ui.messageBox(threadType)

        allsizes = threadDataQuery.allSizes(threadType)
        threadSize = allsizes[31]
        ui.messageBox(threadSize)
        
        allDesignations = threadDataQuery.allDesignations(threadType, threadSize)
        threadDesignation = allDesignations[0]
        ui.messageBox(threadDesignation)
        threadClass = '6g'
        threadInfo = threadFeatures.createThreadInfo(False, threadType, threadDesignation, threadClass)
        
        threadSideFace = threadCircle.sideFaces.item(0)
        threadFaces = adsk.core.ObjectCollection.create()
        threadFaces.add(threadSideFace)

        threadInput = threadFeatures.createInput(threadFaces, threadInfo)
        threadInput.isFullLength = True
        thread = threadFeatures.add(threadInput)

        folder = app.data.activeProject.rootFolder.dataFolders.itemByName('Diploma')
        doc.saveAs('Bolt GOST', folder, '', '')

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

