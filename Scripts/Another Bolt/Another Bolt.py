
import adsk.core, adsk.fusion, adsk.cam, traceback
import math

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

        #шестигранник
        sketchPolygon = rootComp.sketches.add(rootComp.xYConstructionPlane)
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
        extrudePolygonInput.setDistanceExtent(False, adsk.core.ValueInput.createByReal(0.5))
        polygon = extrudes.add(extrudePolygonInput)

        sketchCircleFillet = rootComp.sketches.add(rootComp.xYConstructionPlane)
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
        centerAxis = rootComp.yConstructionAxis
        profRevolvle = sketchCircleFillet.profiles.item(0)
        revolves = rootComp.features.revolveFeatures 
        revolveFilletInput = revolves.createInput(profRevolvle, centerAxis, adsk.fusion.FeatureOperations.CutFeatureOperation)
        angleFillet = adsk.core.ValueInput.createByReal(angFillet)
        revolveFilletInput.setAngleExtent(False, angleFillet)
        revolveFillet = revolves.add(revolveFilletInput)

        sketchCircle = rootComp.sketches.add(rootComp.xZConstructionPlane)
        sketchCir = sketchCircle.sketchCurves.sketchCircles
        centerPoint = adsk.core.Point3D.create(0, 0, -0.5)
        sketchCir.addByCenterRadius(centerPoint, 0.4)

        extCircle = adsk.core.ObjectCollection.create()
        extCircle.add(sketchCircle.profiles.item(0))
        extrudeCircle = features.extrudeFeatures 
        extrudeCircleInput = extrudeCircle.createInput(extCircle, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        extrudeCircleInput.isSolid = True
        extrudeCircleInput.setDistanceExtent(False, adsk.core.ValueInput.createByReal(-2.3))
        circle = extrudeCircle.add(extrudeCircleInput)

        edgeCol = adsk.core.ObjectCollection.create()
        edges = circle.endFaces[0].edges
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

        allsizes = threadDataQuery.allSizes(threadType)
        threadSize = allsizes[31]
        
        allDesignations = threadDataQuery.allDesignations(threadType, threadSize)
        threadDesignation = allDesignations[0]

        threadClass = '6g'
        threadInfo = threadFeatures.createThreadInfo(False, threadType, threadDesignation, threadClass)
        
        threadSideFace = circle.sideFaces.item(0)
        threadFaces = adsk.core.ObjectCollection.create()
        threadFaces.add(threadSideFace)

        threadInput = threadFeatures.createInput(threadFaces, threadInfo)
        threadInput.isFullLength = False
        threadInput.threadLength = adsk.core.ValueInput.createByReal(2.2)
        thread = threadFeatures.add(threadInput)

        # edgeCol.clear()
        # loops = circle.endFaces[0].loops
        # edgeLoop = None
        # for edgeLoop in loops:
        #     if(len(edgeLoop.edges) == 1):
        #         break
        # edgeCol.add(edgeLoop.edges[0])  
        # filletFeats = features.filletFeatures
        # filletInput = filletFeats.createInput()
        # filletRadius = adsk.core.ValueInput.createByReal(0.02)
        # filletInput.addConstantRadiusEdgeSet(edgeCol, filletRadius, True)
        # filletFeats.add(filletInput)

        folder = app.data.activeProject.rootFolder.dataFolders.itemByName('Diploma')
        doc.saveAs('Bolt', folder, '', '')

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
