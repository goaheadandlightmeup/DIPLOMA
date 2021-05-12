#Author-
#Description-

import adsk.core, adsk.fusion, adsk.cam, traceback, math

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface
        # ui.messageBox('Hello script')

        doc = app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType)
        design = app.activeProduct
        rootComp = design.rootComponent

        sketch = rootComp.sketches.add(rootComp.xYConstructionPlane)
        points = adsk.core.ObjectCollection.create()
        pointsGroove = adsk.core.ObjectCollection.create()
        lines = sketch.sketchCurves.sketchLines
        features = rootComp.features
        extrudes = features.extrudeFeatures
        circlesPatterns = features.circularPatternFeatures
        allOccs = rootComp.occurrences
        transform = adsk.core.Matrix3D.create()
        planes = rootComp.constructionPlanes
        threadFeatures = rootComp.features.threadFeatures


        points.add(adsk.core.Point3D.create(0.55, 3, 0))
        points.add(adsk.core.Point3D.create(1.4, 3, 0))
        points.add(adsk.core.Point3D.create(1.4, 0.8, 0))
        points.add(adsk.core.Point3D.create(4, 0.8, 0))
        points.add(adsk.core.Point3D.create(4, 0, 0))
        points.add(adsk.core.Point3D.create(1.25, 0, 0))
        points.add(adsk.core.Point3D.create(1.25, 2, 0))
        points.add(adsk.core.Point3D.create(0.55, 2, 0))
        points.add(adsk.core.Point3D.create(0.55, 3, 0))

        for i in range(points.count-1):
            pt1 = points.item(i)
            pt2 = points.item(i+1)
            sketch.sketchCurves.sketchLines.addByTwoPoints(pt1, pt2)
        
        centerLine = lines.addByTwoPoints(adsk.core.Point3D.create(0, 0, 0), adsk.core.Point3D.create(0, 100, 0))
        profRevolvle = sketch.profiles.item(0)
        revolves = rootComp.features.revolveFeatures
        revInput = revolves.createInput(profRevolvle, centerLine, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        angle = adsk.core.ValueInput.createByReal(math.pi*2)
        revInput.setAngleExtent(False, angle)
        ext = revolves.add(revInput)

        sketchGroove = rootComp.sketches.add(rootComp.xZConstructionPlane)
        pointsGroove.add(adsk.core.Point3D.create(0.461, 0.3, 3))
        pointsGroove.add(adsk.core.Point3D.create(0.661, 0.3, 3))
        pointsGroove.add(adsk.core.Point3D.create(0.661, -0.3, 3))
        pointsGroove.add(adsk.core.Point3D.create(0.461, -0.3, 3))
        pointsGroove.add(adsk.core.Point3D.create(0.461, 0.3, 3))

        for i in range(pointsGroove.count-1):
            ptGroove1 = pointsGroove.item(i)
            ptGroove2 = pointsGroove.item(i+1)
            sketchGroove.sketchCurves.sketchLines.addByTwoPoints(ptGroove1, ptGroove2)
            
        extGroove = adsk.core.ObjectCollection.create()
        extGroove = sketchGroove.profiles.item(0)
        extrudeFeatureGroove = features.extrudeFeatures 
        extrudeFeatureInputGroove = extrudes.createInput(extGroove, adsk.fusion.FeatureOperations.CutFeatureOperation)
        extrudeFeatureInputGroove.isSolid = True
        extrudeFeatureInputGroove.setDistanceExtent(True, adsk.core.ValueInput.createByReal(500))
        extGrooveInput = extrudes.add(extrudeFeatureInputGroove)

        subOcc0 = allOccs.addNewComponent(transform)
        subComp0 = subOcc0.component
        sketches0 = subComp0.sketches
        sketchSec = sketches0.add(rootComp.xZConstructionPlane)
        sketchCircles = sketchSec.sketchCurves.sketchCircles
        centerPoint = adsk.core.Point3D.create(2.75, 0, 0) 
        sketchCircles.addByCenterRadius(centerPoint, 0.42)

        extAll = adsk.core.ObjectCollection.create()
        circleProfile = sketchSec.profiles.item(0)
        extrudeFeature = subComp0.features.extrudeFeatures 
        extrudeFeatureInput = extrudeFeature.createInput(circleProfile, adsk.fusion.FeatureOperations.CutFeatureOperation)
        extrudeFeatureInput.isSolid = True
        extrudeFeatureInput.setDistanceExtent(False, adsk.core.ValueInput.createByReal(10))
        hole = extrudeFeature.add(extrudeFeatureInput)

        patternsBody = hole.bodies.item(0)
        patternsFace = patternsBody.faces.item(0)

        inputEntites = adsk.core.ObjectCollection.create()
        inputEntites.add(patternsFace)

        yAxis = rootComp.yConstructionAxis

        circularFeats = rootComp.features.circularPatternFeatures
        circularFeatInput = circularFeats.createInput(inputEntites, yAxis)
        circularFeatInput.quantity = adsk.core.ValueInput.createByReal(4)
        circularFeatInput.totalAngle = adsk.core.ValueInput.createByString('360 deg')
        circularFeatInput.isSymmetric = False
        circularFeat = circularFeats.add(circularFeatInput)

        # создание фаски 
        # sketchChamfer = rootComp.sketches.add(rootComp.xYConstructionPlane)
        # sketchCh = sketchChamfer.sketchCurves.sketchCircles

    #    # создание новой плоскости для добавления нового компонента в проект 
    #     endFaceOfHole = ext.endFaceOfHole.item(12)

    #     constructionPlanes = subComp0.constructionPlanes
    #     constructionPlaneInput = constructionPlanes.createInput()
    #     constructionPlaneInput.setByOffset(endFaceOfHole, adsk.core.ValueInput.createByString("20 mm"))
    #     constructionPlane = constructionPlanes.add(constructionPlaneInput)
    #     constructionPlaneProxy = constructionPlane.createForAssemblyContext(subOcc0)

        #BOLT

        # Create construction plane input
        
        # prof = sketch.profiles.item(0)
        # planeInput = planes.createInput()

        # # Add construction plane by offset
        # offsetValue = adsk.core.ValueInput.createByReal(10.0)
        # planeInput.setByOffset(prof, offsetValue)
        # planeOne = planes.add(planeInput)

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
        extrudePolygonInput = extrudes.createInput(extPolygon, adsk.fusion.FeatureOperations.NewComponentFeatureOperation)
        extrudePolygonInput.isSolid = True
        extrudePolygonInput.setDistanceExtent(False, adsk.core.ValueInput.createByReal(0.55))
        polygon = extrudes.add(extrudePolygonInput)

        sketchCircle = rootComp.sketches.add(rootComp.xZConstructionPlane)
        sketchCir = sketchCircle.sketchCurves.sketchCircles
        centerPoint = adsk.core.Point3D.create(0, 0, 0)
        sketchCir.addByCenterRadius(centerPoint, 0.45)

        extCircle = adsk.core.ObjectCollection.create()
        extCircle.add(sketchCircle.profiles.item(0))
        extrudeCircle = features.extrudeFeatures 
        extrudeCircleInput = extrudeCircle.createInput (extCircle, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        extrudeCircleInput.isSolid = True
        extrudeCircleInput.setDistanceExtent(False, adsk.core.ValueInput.createByReal(1.35))
        circle = extrudeCircle.add(extrudeCircleInput)

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
        centerAxis = rootComp.zConstructionAxis
        profRevolvle = sketchCircleFillet.profiles.item(0)
        revolves = rootComp.features.revolveFeatures 
        revolveFilletInput = revolves.createInput(profRevolvle, centerAxis, adsk.fusion.FeatureOperations.CutFeatureOperation)
        angleFillet = adsk.core.ValueInput.createByReal(angFillet)
        revolveFilletInput.setAngleExtent(False, angleFillet)
        extFillet = revolves.add(revolveFilletInput) 

        # sketchNewCircle = rootComp.sketches.add(rootComp.xYConstructionPlane)
        # sketchCircleThread = sketchNewCircle.sketchCurves.sketchCircles
        # centerPointThread = adsk.core.Point3D.create(0, 0, 1.9)
        # sketchCircleThread.addByCenterRadius(centerPointThread, 0.4)

        # extCircleThread = adsk.core.ObjectCollection.create()
        # extCircleThread.add(sketchNewCircle.profiles.item(0))
        # extrudeCircleThread = features.extrudeFeatures
        # extrudeCircleThreadInput = extrudeCircleThread.createInput(extCircleThread, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        # extrudeCircleThreadInput.isSolid = True
        # extrudeCircleThreadInput.setDistanceExtent(False, adsk.core.ValueInput.createByReal(1.2))
        # threadCircle = extrudeCircleThread.add(extrudeCircleThreadInput)

        # threadDataQuery = threadFeatures.threadDataQuery

        # threadTypes = threadDataQuery.allThreadTypes
        # print(threadTypes)
        # threadType = threadTypes[10]
        # # ui.messageBox(threadType)

        # allsizes = threadDataQuery.allSizes(threadType)
        # threadSize = allsizes[31]
        # # ui.messageBox(threadSize)
        
        # allDesignations = threadDataQuery.allDesignations(threadType, threadSize)
        # threadDesignation = allDesignations[0]
        # ui.messageBox(threadDesignation)
        # threadClass = '6g'
        # threadInfo = threadFeatures.createThreadInfo(False, threadType, threadDesignation, threadClass)
        
        # threadSideFace = threadCircle.sideFaces.item(0)
        # threadFaces = adsk.core.ObjectCollection.create()
        # threadFaces.add(threadSideFace)

        # threadInput = threadFeatures.createInput(threadFaces, threadInfo)
        # threadInput.isFullLength = True
        # thread = threadFeatures.add(threadInput)

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
        extrudePolygonInput.setDistanceExtent(False, adsk.core.ValueInput.createByReal(0.65))
        polygon = extrudes.add(extrudePolygonInput)
        
        sketchCircle = rootComp.sketches.add(rootComp.xZConstructionPlane)
        sketchCir = sketchCircle.sketchCurves.sketchCircles
        centerPoint = adsk.core.Point3D.create(0, 0, 0)
        sketchCir.addByCenterRadius(centerPoint, 0.4)

        extCircle = adsk.core.ObjectCollection.create()
        extCircle.add(sketchCircle.profiles.item(0))
        extrudeCircle = features.extrudeFeatures 
        extrudeCircleInput = extrudeCircle.createInput(extCircle, adsk.fusion.FeatureOperations.CutFeatureOperation)
        extrudeCircleInput.isSolid = True
        extrudeCircleInput.setDistanceExtent(True, adsk.core.ValueInput.createByReal(10))
        circle = extrudeCircle.add(extrudeCircleInput)

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
        extFillet = revolves.add(revolveFilletInput)

        # filletBody = extFillet.bodies.item(0)
        # filletFace = filletBody.faces.item(0)
        # mirrorPlane = rootComp.constructionPlanes
        # mirrorPlaneInput = mirrorPlane.createInput()
        # offsetDistanceMirror = adsk.core.ValueInput.createByString('3.25 cm')
        # mirrorPlaneInput.setByOffset(filletFace, offsetDistanceMirror)
        # inputEntites = adsk.core.ObjectCollection.create()
        # inputEntites.add(filletBody)
        # mirrorFeatures = features.mirrorFeatures
        # mirrorInput = mirrorFeatures.createInput(inputEntites, mirrorPlane)
        # mirrorFeature = mirrorFeatures.add(mirrorInput)
        
        sketchCircleFilletBottom = rootComp.sketches.add(rootComp.xYConstructionPlane)
        pointsCirlceFilletBottom = adsk.core.ObjectCollection.create()
        pointsCirlceFilletBottom.add(adsk.core.Point3D.create(0, -0.65, -0.53))
        pointsCirlceFilletBottom.add(adsk.core.Point3D.create(0, -0.5194, -0.7556))
        pointsCirlceFilletBottom.add(adsk.core.Point3D.create(0, -0.65, -0.7556 ))
        pointsCirlceFilletBottom.add(adsk.core.Point3D.create(0, -0.65, -0.53))

        for i in range(pointsCirlceFilletBottom.count-1):
            ptCFB1= pointsCirlceFilletBottom.item(i)
            ptCFB2 = pointsCirlceFilletBottom.item(i+1)
            sketchCircleFilletBottom.sketchCurves.sketchLines.addByTwoPoints(ptCFB1, ptCFB2)
        

        profRevolvleBottom = sketchCircleFilletBottom.profiles.item(0) 
        revolveFilletInputBottom = revolves.createInput(profRevolvleBottom, centerAxis, adsk.fusion.FeatureOperations.CutFeatureOperation)
        revolveFilletInputBottom.setAngleExtent(False, angleFillet)
        extFilletBottom = revolves.add(revolveFilletInputBottom)

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
        threadClass = '6H'
        threadInfo = threadFeatures.createThreadInfo(True, threadType, threadDesignation, threadClass)
        
        threadSideFace = circle.sideFaces.item(0)
        threadFaces = adsk.core.ObjectCollection.create()
        threadFaces.add(threadSideFace)

        threadInput = threadFeatures.createInput(threadFaces, threadInfo)
        threadInput.isFullLength = True
       # threadInput.threadLength = adsk.core.ValueInput.createByReal(1.25)
        thread = threadFeatures.add(threadInput)


    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
