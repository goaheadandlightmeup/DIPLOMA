#Author-
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

        sketches = rootComp.sketches
        features = rootComp.features
        extrudes = features.extrudeFeatures
        fillets = rootComp.features.filletFeatures

        #Основной эскиз
        sketch1 = sketches.add(rootComp.xYConstructionPlane)
        lines1 = sketch1.sketchCurves.sketchLines
        
        #Линии для основы полумуфты
        line1 = lines1.addByTwoPoints(adsk.core.Point3D.create(-7,0,0), adsk.core.Point3D.create(7,0,0))
        line2 = lines1.addByTwoPoints(adsk.core.Point3D.create(-7,0,0), adsk.core.Point3D.create(-7,5,0))
        line3 = lines1.addByTwoPoints(adsk.core.Point3D.create(7,12.5,0), adsk.core.Point3D.create(7,0,0))
        line4 = lines1.addByTwoPoints(adsk.core.Point3D.create(3.5,12.5,0), adsk.core.Point3D.create(7,12.5,0))
        line5 = lines1.addByTwoPoints(adsk.core.Point3D.create(-7,5,0), adsk.core.Point3D.create(3.5,5,0))
        line6 = lines1.addByTwoPoints(adsk.core.Point3D.create(3.5,12.5,0), adsk.core.Point3D.create(3.5,5,0))

        #Создание вращения основного эскиза
        prof1 = sketch1.profiles.item(0)
        revolves = rootComp.features.revolveFeatures
        revInput = revolves.createInput(prof1, line1, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        angle = adsk.core.ValueInput.createByReal(math.pi * 2)
        revInput.setAngleExtent(False, angle)
        rev = revolves.add(revInput)

        body1 = rev.bodies[0]

        #Эскиз для шпонки
        sketch2 = sketches.add(rootComp.yZConstructionPlane)
        lines2 = sketch2.sketchCurves.sketchLines
        arcs = sketch2.sketchCurves.sketchArcs

        #Создание дуги для шпонки
        PointArc1 = adsk.core.Point3D.create(-0.7,2.1383,0)
        PointArc2 = adsk.core.Point3D.create(0,-2.25,0)
        PointArc3 = adsk.core.Point3D.create(0.7,2.1383,0)
        arc = arcs.addByThreePoints(PointArc1, PointArc2, PointArc3)

        #Создание паза для шпонки
        line_key1 = lines2.addByTwoPoints(adsk.core.Point3D.create(-0.7,2.63,0), adsk.core.Point3D.create(0.7,2.63,0))
        line_key2 = lines2.addByTwoPoints(adsk.core.Point3D.create(-0.7,2.63,0), adsk.core.Point3D.create(-0.7,2.1383,0))
        line_key3 = lines2.addByTwoPoints(adsk.core.Point3D.create(0.7,2.63,0), adsk.core.Point3D.create(0.7,2.1383,0))

        arcFil1 = arcs.addFillet(line_key1, line_key1.endSketchPoint.geometry, line_key2, line_key2.startSketchPoint.geometry, 0.025)
        arcFil2 = arcs.addFillet(line_key3, line_key3.endSketchPoint.geometry, line_key1, line_key1.startSketchPoint.geometry, 0.025)


        #Выдавливание шпонки
        prof_key1 = sketch2.profiles.item(0)

        distance = adsk.core.ValueInput.createByReal(7)
        extrude1 = extrudes.createInput(prof_key1, adsk.fusion.FeatureOperations.CutFeatureOperation) 
        extrude1.setSymmetricExtent(distance, False)
        extrudeAll = extrudes.add(extrude1)


        #Эскиз первой окружности для массива
        sketch3 = sketches.add(rootComp.yZConstructionPlane)
        sketchCircles2 = sketch3.sketchCurves.sketchCircles
        #Первая окружность для массива
        centerPoint1 = adsk.core.Point3D.create(0, 9, 3.5)
        sketchCircle2 = sketchCircles2.addByCenterRadius(centerPoint1, 1.8)

        prof2 = sketch3.profiles.item(0)

        #Эскиз второй окружности для массива
        sketch4 = sketches.add(rootComp.yZConstructionPlane)
        sketchCircles3 = sketch4.sketchCurves.sketchCircles
        #Вторая окружность для массива
        centerPoint2 = adsk.core.Point3D.create(0, 9, 7)
        sketchCircle3 = sketchCircles3.addByCenterRadius(centerPoint2, 2.5)

        prof3 = sketch4.profiles.item(0)

        #Лофт от первой окружности до второй
        loftFeats = rootComp.features.loftFeatures
        loftInput = loftFeats.createInput(adsk.fusion.FeatureOperations.CutFeatureOperation)
        loftSectionsObj = loftInput.loftSections
        loftSectionsObj.add(prof2)
        loftSectionsObj.add(prof3)
        loftF = loftFeats.add(loftInput)

        #Грань для массива
        s4_body = loftF.bodies.item(0)
        s4_face = s4_body.faces.item(0)

        #Круговой массив
        inputEntites = adsk.core.ObjectCollection.create()
        inputEntites.add(s4_face)

        xAxis = rootComp.xConstructionAxis

        circularFeats = rootComp.features.circularPatternFeatures
        circularFeatInput = circularFeats.createInput(inputEntites, xAxis)
        circularFeatInput.quantity = adsk.core.ValueInput.createByReal(6)
        circularFeatInput.totalAngle = adsk.core.ValueInput.createByString('360 deg')
        circularFeatInput.isSymmetric = False
        circularFeat = circularFeats.add(circularFeatInput)


        #Материал
        lib = app.materialLibraries.itemByName('Fusion 360 Appearance Library')
        favAppear = lib.appearances.itemByName('Steel - Satin')

        appear = lib.appearances.item(0)
 
        appear.copyTo(design)
        
        body2 = rootComp.bRepBodies.item(0)
        body2.appearance = favAppear

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
