#Author-me
#Description-

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
        allOccs = rootComp.occurrences
        revolves = rootComp.features.revolveFeatures
        transform = adsk.core.Matrix3D.create()
        
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
        extrudePolygonInput.setDistanceExtent(False, adsk.core.ValueInput.createByReal(0.65))
        polygon = extrudes.add(extrudePolygonInput)

        subOcc0 = allOccs.addNewComponent(transform)
        subComp0 = subOcc0.component
        sketches0 = subComp0.sketches
        sketchCircle = sketches0.add(subComp0.xZConstructionPlane)

        sketchCir = sketchCircle.sketchCurves.sketchCircles
        centerPoint = adsk.core.Point3D.create(0, 0, 0)
        sketchCir.addByCenterRadius(centerPoint, 0.4)

        extCircle = adsk.core.ObjectCollection.create()
        extCircle.add(sketchCircle.profiles.item(0))
        extrudeCircle = subComp0.features.extrudeFeatures 
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
        revolveFilletInput = revolves.createInput(profRevolvle, centerAxis, adsk.fusion.FeatureOperations.CutFeatureOperation)
        angleFillet = adsk.core.ValueInput.createByReal(angFillet)
        revolveFilletInput.setAngleExtent(False, angleFillet)
        extFillet = revolves.add(revolveFilletInput)

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

        allsizes = threadDataQuery.allSizes(threadType)
        threadSize = allsizes[31]
        
        
        allDesignations = threadDataQuery.allDesignations(threadType, threadSize)
        threadDesignation = allDesignations[0]
        
        threadClass = '6H'
        threadInfo = threadFeatures.createThreadInfo(True, threadType, threadDesignation, threadClass)
        
        threadSideFace = circle.sideFaces.item(0)
        threadFaces = adsk.core.ObjectCollection.create()
        threadFaces.add(threadSideFace)

        threadInput = threadFeatures.createInput(threadFaces, threadInfo)
        threadInput.isFullLength = True
        thread = threadFeatures.add(threadInput)

        # #new joint plane

        # sketchCircles1 = sketch1.sketchCurves.sketchCircles
        # sketchCircles1.addByCenterRadius(centerPoint, 0.5)
        # # Get the profile defined by the circle
        # prof1 = sketch1.profiles.item(0)
        # # Create an extrude input and make sure it's in the new component
        # extrudes1 = subComp1.features.extrudeFeatures
        # extInput1 = extrudes1.createInput(prof1, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        # # Set the extrude input
        # distance1 = adsk.core.ValueInput.createByString("50 mm")
        # extInput1.setDistanceExtent(False, distance1)
        # extInput1.isSolid = False
        # # Create the extrude
        # extrudes1.add(extInput1)
        # Create the AsBuiltJointInput

        #Bolt
        endFaceOfNut = polygon.endFaces.item(0)

        constructionPlanes = subComp0.constructionPlanes
        constructionPlaneInput = constructionPlanes.createInput()
        constructionPlaneInput.setByOffset(endFaceOfNut, adsk.core.ValueInput.createByString("20 mm"))
        constructionPlane = constructionPlanes.add(constructionPlaneInput)
        constructionPlaneProxy = constructionPlane.createForAssemblyContext(subOcc0)
        
        subOcc1 = allOccs.addNewComponent(transform)
        subComp1 = subOcc1.component
        sketches1 = subComp1.sketches
        sketch1 = sketches1.add(constructionPlaneProxy)

        #создание шестигранной головки болта
        sketchBoltPolygon = sketches1.add(constructionPlaneProxy)

        pointsBoltPolygon = adsk.core.ObjectCollection.create()

        pointsBoltPolygon.add(adsk.core.Point3D.create(0, 0.6928, 0))
        pointsBoltPolygon.add(adsk.core.Point3D.create(-0.6, 0.3464, 0))
        pointsBoltPolygon.add(adsk.core.Point3D.create(-0.6, -0.3464, 0))
        pointsBoltPolygon.add(adsk.core.Point3D.create(0, -0.6928, 0))
        pointsBoltPolygon.add(adsk.core.Point3D.create(0.6, -0.3464, 0))
        pointsBoltPolygon.add(adsk.core.Point3D.create(0.6, 0.3464, 0))
        pointsBoltPolygon.add(adsk.core.Point3D.create(0, 0.6928, 0))

        for i in range(pointsBoltPolygon.count-1):
            ptP1Bolt = pointsBoltPolygon.item(i)
            ptP2Bolt = pointsBoltPolygon.item(i+1)
            sketchBoltPolygon.sketchCurves.sketchLines.addByTwoPoints(ptP1Bolt, ptP2Bolt)

        extBoltPolygon = adsk.core.ObjectCollection.create()
        extBoltPolygon = sketchBoltPolygon.profiles.item(0)

        extrudeBoltPolygon = subComp1.features.extrudeFeatures
        extrudeBoltPolygonInput = extrudeBoltPolygon.createInput(extBoltPolygon, adsk.fusion.FeatureOperations.NewComponentFeatureOperation)
        extrudeBoltPolygonInput.isSolid = True
        extrudeBoltPolygonInput.setDistanceExtent(False, adsk.core.ValueInput.createByReal(0.55))
        polygonBolt = extrudes.add(extrudeBoltPolygonInput)

        #Создание цилиндрической части болта 
   
        sketchCircleBolt = sketches1.add(constructionPlaneProxy)
        sketchCir = sketchCircleBolt.sketchCurves.sketchCircles
        centerPointBolt = adsk.core.Point3D.create(0, 0, 0.55)
        sketchCir.addByCenterRadius(centerPointBolt, 0.45)

        extCircleBolt = adsk.core.ObjectCollection.create()
        extCircleBolt.add(sketchCircleBolt.profiles.item(0))
        extrudeCircleBolt = features.extrudeFeatures 
        extrudeCircleInputBolt = extrudeCircleBolt.createInput(extCircleBolt,  adsk.fusion.FeatureOperations.NewComponentFeatureOperation)
        extrudeCircleInputBolt.isSolid = True
        extrudeCircleInputBolt.setDistanceExtent(False, adsk.core.ValueInput.createByReal(1.25))
        circleBolt = extrudeCircleBolt.add(extrudeCircleInputBolt)

        sketchCircleFilletBolt = sketches1.add(constructionPlaneProxy)
        pointsCirlceFilletBolt = adsk.core.ObjectCollection.create()
        pointsCirlceFilletBolt.add(adsk.core.Point3D.create(0, 0, -0.53))
        pointsCirlceFilletBolt.add(adsk.core.Point3D.create(0, 0, -0.8396))
        pointsCirlceFilletBolt.add(adsk.core.Point3D.create(0, -0.1788, -0.8396 ))
        pointsCirlceFilletBolt.add(adsk.core.Point3D.create(0, 0, -0.53))

        for i in range(pointsCirlceFilletBolt.count-1):
            ptCF1B = pointsCirlceFilletBolt.item(i)
            ptCF2B = pointsCirlceFilletBolt.item(i+1)
            sketchCircleFilletBolt.sketchCurves.sketchLines.addByTwoPoints(ptCF1Bolt, ptCF2Bolt)
        
        angFillet = math.pi*2
        centerAxis = rootComp.zConstructionAxis
        profRevolvle = sketchCircleFillet.profiles.item(0)
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
        extrudeCircleThreadInput.setDistanceExtent(False, adsk.core.ValueInput.createByReal(0.9))
        threadCircle = extrudeCircleThread.add(extrudeCircleThreadInput)

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

        asBuiltJoints_ = rootComp.asBuiltJoints
        asBuiltJointInput = asBuiltJoints_.createInput(subOcc0, subOcc1, None)

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
