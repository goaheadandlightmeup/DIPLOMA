#Author-Misha
#Description-

import adsk.core, adsk.fusion, adsk.cam, traceback, math

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface
        #doc = app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType)
        doc = app.documents.item(0)
        #doc.design.allComponents.add()
        design = app.activeProduct

        # Get the root component of the active design.
        rootComp = design.rootComponent
        # Get all components
        components = design.allComponents

        # Get array of occurrences
        # occurrences = rootComp.occurrences.asList

        # Create new bearing component
        occurence = rootComp.occurrences.addNewComponent(adsk.core.Matrix3D.create())
        # Get last components of design
        if(components.count == 0):
            comp = components.item(0)
        else:
            comp = components.item(components.count-1)
        
        # Get extrudes for bearing component
        extrudes = comp.features.extrudeFeatures

        # Create a new sketch on the xy plane.
        sketches = comp.sketches
        xyPlane = comp.xYConstructionPlane
        yzPlane = comp.yZConstructionPlane
        sketch = sketches.add(xyPlane)


        # Draw connected lines.
        lines = sketch.sketchCurves.sketchLines
        
        UR_line1 = lines.addByTwoPoints(adsk.core.Point3D.create(-1, 5, 0), adsk.core.Point3D.create(1, 5, 0))
        UR_line2 = lines.addByTwoPoints(UR_line1.endSketchPoint, adsk.core.Point3D.create(1, 4, 0))
        UR_line3 = lines.addByTwoPoints(UR_line2.endSketchPoint, adsk.core.Point3D.create(-1, 4, 0))
        UR_line4 = lines.addByTwoPoints(UR_line3.endSketchPoint, UR_line1.startSketchPoint)

        # Draw connected lines.
        DR_line1 = lines.addByTwoPoints(adsk.core.Point3D.create(-1, 3, 0), adsk.core.Point3D.create(-0.5, 3, 0))
        DR_line2 = lines.addByTwoPoints(DR_line1.endSketchPoint, adsk.core.Point3D.create(-0.5, 2.5, 0))
        DR_line3 = lines.addByTwoPoints(DR_line2.endSketchPoint, adsk.core.Point3D.create(0.5, 2.5, 0))
        DR_line4 = lines.addByTwoPoints(DR_line3.endSketchPoint, adsk.core.Point3D.create(0.5, 3, 0))
        DR_line5 = lines.addByTwoPoints(DR_line4.endSketchPoint, adsk.core.Point3D.create(1, 3, 0))
        DR_line6 = lines.addByTwoPoints(DR_line5.endSketchPoint, adsk.core.Point3D.create(1, 2, 0))
        DR_line7 = lines.addByTwoPoints(DR_line6.endSketchPoint, adsk.core.Point3D.create(-1, 2, 0))
        DR_line8 = lines.addByTwoPoints(DR_line7.endSketchPoint, DR_line1.startSketchPoint)
            
        # Draw a line to use as the axis of revolution.
        axisLine = lines.addByTwoPoints(adsk.core.Point3D.create(-1, 0, 0), adsk.core.Point3D.create(1, 0, 0))

        # Get the profile defined by the circle.
        profs = adsk.core.ObjectCollection.create()
        profs.add(sketch.profiles.item(0))
        profs.add(sketch.profiles.item(1))
            
        # Create an revolution input to be able to define the input needed for a revolution
        # while specifying the profile and that a new component is to be created
        revolves = comp.features.revolveFeatures
        revInput = revolves.createInput(profs, axisLine, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)

        # Define that the extent is an angle of pi to get half of a torus.
        angle = adsk.core.ValueInput.createByReal(math.pi*2)
        revInput.setAngleExtent(False, angle)

        # Create the extrusion.
        ext = revolves.add(revInput)

        # Create new sketch
        sketch2 = sketches.add(yzPlane)

        circles = sketch2.sketchCurves.sketchCircles

        circle1 = circles.addByCenterRadius(adsk.core.Point3D.create(0, 3.25, 0), 0.75)

        #if(occurrences.count == 0):
        #    occurrence_last = occurrences.item(0)
        #else:
        #    occurrence_last = occurrences.item(occurrences.count-1)
        
        # Set parametrs 
        isFullLength = True
        mm10 = adsk.core.ValueInput.createByString("10 mm")
        deg0 = adsk.core.ValueInput.createByString("0 deg")

    
        extrudeInput = extrudes.createInput(sketch2.profiles.item(0), adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        extrudeInput.setSymmetricExtent(mm10, isFullLength, deg0)
        
        # Create the extrusion
        extrude1 = extrudes.add(extrudeInput)

        # Get cilinder body
        body = comp.bRepBodies.item(comp.bRepBodies.count - 1)

        # Create input entities for circular pattern
        inputEntites = adsk.core.ObjectCollection.create()
        inputEntites.add(body)

        # Get X axis for circular pattern
        xAxis = comp.xConstructionAxis

        # Create the input for circular pattern
        circularFeats = comp.features.circularPatternFeatures
        circularFeatInput = circularFeats.createInput(inputEntites, xAxis)

        # Set the quantity of the elements
        circularFeatInput.quantity = adsk.core.ValueInput.createByReal(6)

        # Set symmetry of the circular pattern
        circularFeatInput.isSymmetric = True

        # Change component name
        comp.name = "ГОСТ 8328-75 - 2000"

        # Create the circular pattern
        circularFeat = circularFeats.add(circularFeatInput)

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
