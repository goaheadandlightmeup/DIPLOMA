import adsk.core, adsk.fusion, traceback, math

def run(context):
    ui = None
    try: 
        app = adsk.core.Application.get()
        ui = app.userInterface

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
        chamferFeats = rootComp.features.chamferFeatures

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

        sketchSec = rootComp.sketches.add(rootComp.xZConstructionPlane)
        sketchCircles = sketchSec.sketchCurves.sketchCircles
        centerPoint = adsk.core.Point3D.create(2.75, 0, 0) 
        sketchCircles.addByCenterRadius(centerPoint, 0.42)

        extAll = adsk.core.ObjectCollection.create()
        extAll.add(sketchSec.profiles.item(0))
        extrudeFeature = features.extrudeFeatures 
        extrudeFeatureInput = extrudeFeature.createInput(extAll, adsk.fusion.FeatureOperations.CutFeatureOperation)
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

        # sketchChamfer = rootComp.sketches.add(rootComp.xYConstructionPlane)
        # sketchCh = sketchChamfer.sketchCurves.sketchCircles

        # edgeCol = adsk.core.ObjectCollection.create()
        # edges = ext.endFaces[0].edges
        # for edgeI  in edges:
        #     edgeCol.add(edgeI)

        # chamferInput = chamferFeats.createInput(edgeCol, True)
        # distanceChamfer = adsk.core.ValueInput.createByReal(0.02)
        # chamferInput.setToEqualDistance(distanceChamfer)
        # chamferFeats.add(chamferInput)
        folder = app.data.activeProject.rootFolder.dataFolders.itemByName('Diploma')
        doc.saveAs('Half-Coupling', folder, '', '')
        
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

