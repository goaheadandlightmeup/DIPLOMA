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
        distanceExtrude = adsk.core.ValueInput.createByReal(0.65)
        extrudePolygonInput.setDistanceExtent(False, distanceExtrude)
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
        revolveFillet = revolves.add(revolveFilletInput)

        edgeCol = adsk.core.ObjectCollection.create()

        edges = polygon.endFaces[0].edges
        for edgeI  in edges:
            edgeCol.add(edgeI)

        chamferFeats = rootComp.features.chamferFeatures
        chamferInput = chamferFeats.createInput(edgeCol, True)
        chamferDistance = adsk.core.ValueInput.createByReal(0.02)
        chamferInput.setToEqualDistance(chamferDistance)
        chamferComp = chamferFeats.add(chamferInput)
    
        planes = rootComp.constructionPlanes
        prof = sketchPolygon.profiles.item(0)

        planeInput = planes.createInput()

        offsetValue = adsk.core.ValueInput.createByReal(0.65 / 2)
        planeInput.setByOffset(prof, offsetValue)
        planeFillet = planes.add(planeInput)
        planeFillet.isLightBulbOn = False

        mirrorFeatures = rootComp.features.mirrorFeatures 
        faceCollection = adsk.core.ObjectCollection.create()

        endFaces = revolveFillet.faces
        faceFillet = endFaces.item(0)
        faceCollection.add(faceFillet)
        mirrorInput = mirrorFeatures.createInput(faceCollection, planeFillet)
        mirrorFeatures.add(mirrorInput)

        endFacesChamfer = chamferComp.faces
        faceChamfer = endFacesChamfer.item(0)
        faceCollection.add(faceChamfer)
        mirrorInputChamfer = mirrorFeatures.createInput(faceCollection, planeFillet)
        mirrorChamfer = mirrorFeatures.add(mirrorInputChamfer)
        
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

        # filedlg = ui.createFileDialog()
        # filedlg.initialDirectory = '/Samples'
        # filedlg.filter = '*.f3d'
        # if filedlg.showSave() == adsk.core.DialogResults.DialogOK:
        #     design = adsk.fusion.Design.cast(app.activeProduct)
        #     option = design.exportManager.createFusionArchiveExportOptions(filedlg.filename, design.rootComponent)
        #     design.exportManager.execute(option)

        folder = app.data.activeProject.rootFolder.dataFolders.itemByName('Diploma')
        doc.saveAs('Nut', folder, '', '')
        # ret = doc.close(True)
        # ui.messageBox(str(ret))
        
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
