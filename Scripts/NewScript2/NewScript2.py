
#Description-Test Detail 1

import adsk.core, adsk.fusion, traceback
import math

defaultDetailName = 'Detail 1'
defaultDetailHeight = 2.5
defaultDetailWidth = 3.8
defaultDetailThicknes = 0.4
defaultDetailWidth1 = 2.8
defaultDetailHeight1 = 1.5
defaultDetailBHoled = 0.4
bottomCenter = adsk.core.Point3D.create(0, 0, 0)


# global set of event handlers to keep them referenced for the duration of the command
handlers = []
app = adsk.core.Application.get()
if app:
    ui = app.userInterface

newComp = None

def createNewComponent():
    # Get the active design.
    product = app.activeProduct
    design = adsk.fusion.Design.cast(product)
    rootComp = design.rootComponent
    allOccs = rootComp.occurrences
    newOcc = allOccs.addNewComponent(adsk.core.Matrix3D.create())
    return newOcc.component
    
    
class DetailCommandExecuteHandler(adsk.core.CommandEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):
        try:
            unitsMgr = app.activeProduct.unitsManager
            command = args.firingEvent.sender
            inputs = command.commandInputs
            
            detail = Detail()
            for input in inputs:
                if input.id == 'detailName':
                    detail.detailName = input.value
                elif input.id == 'detailHeight':
                    detail.detailHeight = unitsMgr.evaluateExpression(input.expression, "mm")
                elif input.id == 'detailHeight1':
                    detail.detailHeight1 = unitsMgr.evaluateExpression(input.expression, "mm")
                elif input.id == 'detailWidth':
                    detail.detailWidth = unitsMgr.evaluateExpression(input.expression, "mm")
                elif input.id == 'detailThicknes':
                    detail.detailThicknes = unitsMgr.evaluateExpression(input.expression, "mm")
                elif input.id == 'detailWidth1':
                    detail.detailWidth1 = unitsMgr.evaluateExpression(input.expression, "mm")
                elif input.id == 'detailBHoleD':
                    detail.detaildetailBHoleD = unitsMgr.evaluateExpression(input.expression, "mm")   
                
                    
            detail.buildDetail();
            args.isValidResult = True
        except:
            if ui:
                ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

class DetailCommandDestroyHandler(adsk.core.CommandEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):
        try:
            # when the command is done, terminate the script
            # this will release all globals which will remove all event handlers
            adsk.terminate()
        except:
            if ui:
                ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

class DetailCommandCreatedHandler(adsk.core.CommandCreatedEventHandler):    
    def __init__(self):
        super().__init__()        
    def notify(self, args):
        try:
            cmd = args.command
            onExecute = DetailCommandExecuteHandler()
            cmd.execute.add(onExecute)
            onExecutePreview = DetailCommandExecuteHandler()
            cmd.executePreview.add(onExecutePreview)
            onDestroy = DetailCommandDestroyHandler()
            cmd.destroy.add(onDestroy)
            # keep the handler referenced beyond this function
            handlers.append(onExecute)
            handlers.append(onExecutePreview)
            handlers.append(onDestroy)

            #define the inputs
            inputs = cmd.commandInputs
            inputs.addStringValueInput('detailName', 'Detail Name', defaultDetailName)

            initDetailHeight = adsk.core.ValueInput.createByReal(defaultDetailHeight)
            inputs.addValueInput('detailHeight', 'Detail Height','mm',initDetailHeight)
            
            initDetailHeight1 = adsk.core.ValueInput.createByReal(defaultDetailHeight1)
            inputs.addValueInput('detailHeight1', 'Detail Height1','mm',initDetailHeight1)
            
            initDetailWidth = adsk.core.ValueInput.createByReal(defaultDetailWidth)
            inputs.addValueInput('detailWidth', 'Detail Width','mm',initDetailWidth)
            
            initDetailThicknes = adsk.core.ValueInput.createByReal(defaultDetailThicknes)
            inputs.addValueInput('detailThicknes', 'Detail Thickness','mm',initDetailThicknes)
            
            initDetailWidth1 = adsk.core.ValueInput.createByReal(defaultDetailWidth1)
            inputs.addValueInput('detailWidth1', 'Dlina','mm',initDetailWidth1)
            
            initDetailBHoled = adsk.core.ValueInput.createByReal(defaultDetailBHoled)
            inputs.addValueInput('detailBholed', 'Diameter of Big Hole','mm',initDetailBHoled)
            
        except:
            if ui:
                ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

class Detail:
    def __init__(self):
        self._detailName = defaultDetailName
        self._detailHeight = defaultDetailHeight
        self._detailHeight1 = defaultDetailHeight1
        self._detailWidth = defaultDetailWidth
        self._detailThicknes = defaultDetailThicknes
        self._detailWidth1 = defaultDetailWidth1
        self._detailBHoled = defaultDetailBHoled 
        
       
        
    #properties
    @property
    def detailName(self):
        return self._detailName
    @detailName.setter
    def detailName(self, value):
        self._detailName = value

    @property
    def detailHeight(self):
        return self._detailHeight
    @detailHeight.setter
    def detailHeight(self, value):
        self._detailHeight = value
        
    @property
    def detailHeight1(self):
        return self._detailHeight1
    @detailHeight1.setter
    def detailHeight1(self, value):
        self._detailHeight1 = value
                
        
    @property
    def detailWidth(self):
        return self._detailWidth
    @detailWidth.setter
    def detailWidth(self, value):
        self._detailWidth = value
        
    @property
    def detailThicknes(self):
        return self._detailThicknes
    @detailThicknes.setter
    def detailThicknes(self, value):
        self._detailThicknes = value
        
    @property
    def detailWidth1(self):
        return self._detailWidth1
    @detailWidth1.setter
    def detailWidth1(self, value):
        self._detailWidth1 = value
        
    @property
    def detailBHoled(self):
        return self._detailBHoled
    @detailName.setter
    def detailBholed(self, value):
        self._detailBHoled = value    
        
   

    def buildDetail(self):
        global newComp
        newComp = createNewComponent()
        if newComp is None:
            ui.messageBox('New component failed to create', 'New Component Failed')
            return
        
              
        sketches = newComp.sketches
        
        
        xyPlane = newComp.xYConstructionPlane
        xzPlane = newComp.xZConstructionPlane
        yzPlane = newComp.yZConstructionPlane
        
        sketch1 = sketches.add(xyPlane)
        point1 = []
        point1 = adsk.core.Point3D.create(0,self.detailHeight1+self.detailHeight*0.20,0)
        point2 = adsk.core.Point3D.create(self.detailWidth*0.132,self.detailHeight,0)
        point3 = adsk.core.Point3D.create(self.detailWidth1+self.detailWidth*0.132,self.detailHeight,0)
        point4 = adsk.core.Point3D.create(self.detailWidth,self.detailHeight*0.20+self.detailHeight1,0)
        point5 = adsk.core.Point3D.create(self.detailWidth,self.detailHeight*0.20,0)
        point6 = adsk.core.Point3D.create(self.detailWidth-self.detailWidth*0.132,0,0)
        point7 = adsk.core.Point3D.create(self.detailWidth*0.132,0,0)
        point8 = adsk.core.Point3D.create(0,self.detailHeight*0.20,0)
        
        sketch1.sketchCurves.sketchLines.addByTwoPoints(point1,point2)
        sketch1.sketchCurves.sketchLines.addByTwoPoints(point2,point3)
        sketch1.sketchCurves.sketchLines.addByTwoPoints(point3,point4)
        sketch1.sketchCurves.sketchLines.addByTwoPoints(point4,point5)
        sketch1.sketchCurves.sketchLines.addByTwoPoints(point5,point6)
        sketch1.sketchCurves.sketchLines.addByTwoPoints(point6,point7)
        sketch1.sketchCurves.sketchLines.addByTwoPoints(point7,point8)
        sketch1.sketchCurves.sketchLines.addByTwoPoints(point8,point1)
            
        extrudes = newComp.features.extrudeFeatures
        prof = sketch1.profiles[0]
        extInput = extrudes.createInput(prof, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)

        distance = adsk.core.ValueInput.createByReal(self.detailThicknes*-1/2)
        extInput.setDistanceExtent(True, distance)
        detailExt = extrudes.add(extInput)

        fc = detailExt.faces[0]
        bd = fc.body
        bd.name = self.detailName
        
        
        
        sketch2 = sketches.add(xyPlane)
        point10 = []
        point10 = adsk.core.Point3D.create(self.detailWidth*0.026,self.detailHeight1+self.detailHeight*0.20-self.detailWidth*0.026,self.detailThicknes/2)
        point11 = adsk.core.Point3D.create(self.detailWidth*0.13+self.detailWidth*0.026,self.detailHeight-self.detailWidth*0.026,self.detailThicknes/2)
        point12 = adsk.core.Point3D.create(self.detailWidth1+self.detailWidth*0.13-self.detailWidth*0.026,self.detailHeight-self.detailWidth*0.026,self.detailThicknes/2)
        point13 = adsk.core.Point3D.create(self.detailWidth-self.detailWidth*0.026,self.detailHeight1+self.detailHeight*0.20-self.detailWidth*0.026,self.detailThicknes/2)
        point14 = adsk.core.Point3D.create(self.detailWidth-self.detailWidth*0.026,self.detailHeight*0.20+self.detailWidth*0.026,self.detailThicknes/2)
        point15 = adsk.core.Point3D.create(self.detailWidth-self.detailWidth*0.13-self.detailWidth*0.026,self.detailWidth*0.026,self.detailThicknes/2)
        point16 = adsk.core.Point3D.create(self.detailWidth*0.13+self.detailWidth*0.026,self.detailWidth*0.026,self.detailThicknes/2)
        point17 = adsk.core.Point3D.create(self.detailWidth*0.026,self.detailHeight*0.20+self.detailWidth*0.026,self.detailThicknes/2)
        
        sketch2.sketchCurves.sketchLines.addByTwoPoints(point10,point11)
        sketch2.sketchCurves.sketchLines.addByTwoPoints(point11,point12)
        sketch2.sketchCurves.sketchLines.addByTwoPoints(point12,point13)
        sketch2.sketchCurves.sketchLines.addByTwoPoints(point13,point14)
        sketch2.sketchCurves.sketchLines.addByTwoPoints(point14,point15)
        sketch2.sketchCurves.sketchLines.addByTwoPoints(point15,point16)
        sketch2.sketchCurves.sketchLines.addByTwoPoints(point16,point17)
        sketch2.sketchCurves.sketchLines.addByTwoPoints(point17,point10)
        
        sketch2Prof = sketch2.profiles[0]
        sketch2ExtInput = extrudes.createInput(sketch2Prof, adsk.fusion.FeatureOperations.CutFeatureOperation)
        
        distance1 = adsk.core.ValueInput.createByReal(-self.detailThicknes*0.37)
        sketch2ExtInput.setDistanceExtent(False, distance1)
        sketch2Ext = extrudes.add(sketch2ExtInput)
        
        sketch3 = sketches.add(xyPlane) 
        
        point18 = adsk.core.Point3D.create(self.detailWidth*0.026,self.detailHeight*0.26,-self.detailThicknes*0.5)
        point19 = adsk.core.Point3D.create(self.detailWidth*0.026,self.detailHeight*0.74,-self.detailThicknes*0.5)
        point20 = adsk.core.Point3D.create(self.detailWidth*0.97,self.detailHeight*0.74,-self.detailThicknes*0.5)
        point21 = adsk.core.Point3D.create(self.detailWidth*0.97,self.detailHeight*0.26,-self.detailThicknes*0.5)
        
        sketch3.sketchCurves.sketchLines.addByTwoPoints(point18,point19)
        sketch3.sketchCurves.sketchLines.addByTwoPoints(point19,point20)
        sketch3.sketchCurves.sketchLines.addByTwoPoints(point20,point21)
        sketch3.sketchCurves.sketchLines.addByTwoPoints(point21,point18)
        
        sketch3Prof = sketch3.profiles[0]
        sketch3ExtInput = extrudes.createInput(sketch3Prof, adsk.fusion.FeatureOperations.CutFeatureOperation)
        
        distance4 = adsk.core.ValueInput.createByReal(self.detailThicknes*0.375)
        sketch3ExtInput.setDistanceExtent(False, distance4)
        sketch3Ext = extrudes.add(sketch3ExtInput)
        
        
        
        sketch4 = sketches.add(xyPlane)
        
        point22 = adsk.core.Point3D.create(self.detailWidth*0.342,self.detailHeight*0.34)
        point23 = adsk.core.Point3D.create(self.detailWidth*0.342,self.detailHeight*0.66)
        point24 = adsk.core.Point3D.create(self.detailWidth*0.342+self.detailWidth*0.079,self.detailHeight*0.66)
        point25 = adsk.core.Point3D.create(self.detailWidth*0.342+self.detailWidth*0.079+self.detailWidth*0.158/2,self.detailHeight*0.66+self.detailHeight*0.04)
        point26 = adsk.core.Point3D.create(self.detailWidth*0.579,self.detailHeight*0.66)
        point27 = adsk.core.Point3D.create(self.detailWidth*0.658,self.detailHeight*0.66)
        point28 = adsk.core.Point3D.create(self.detailWidth*0.658,self.detailHeight*0.34)
        point29 = adsk.core.Point3D.create(self.detailWidth*0.579,self.detailHeight*0.34)
        point30 = adsk.core.Point3D.create(self.detailWidth*0.342+self.detailWidth*0.079+self.detailWidth*0.158/2,self.detailHeight*0.34-self.detailHeight*0.04)
        point31 = adsk.core.Point3D.create(self.detailWidth*0.342+self.detailWidth*0.079,self.detailHeight*0.34)
        
        sketch4.sketchCurves.sketchLines.addByTwoPoints(point22,point23)
        sketch4.sketchCurves.sketchLines.addByTwoPoints(point23,point24)
        sketch4.sketchCurves.sketchArcs.addByThreePoints(point24,point25,point26)
        sketch4.sketchCurves.sketchLines.addByTwoPoints(point26,point27)
        sketch4.sketchCurves.sketchLines.addByTwoPoints(point27,point28)
        sketch4.sketchCurves.sketchLines.addByTwoPoints(point28,point29)
        sketch4.sketchCurves.sketchArcs.addByThreePoints(point29,point30,point31)
        sketch4.sketchCurves.sketchLines.addByTwoPoints(point31,point22)
         
        point32 = adsk.core.Point3D.create(self.detailWidth*0.342 + (self.detailHeight)*0.04,self.detailHeight*0.34 + (self.detailHeight)*0.04)
        point33 = adsk.core.Point3D.create(self.detailWidth*0.342 + (self.detailHeight)*0.04,self.detailHeight*0.66 - self.detailHeight*0.04)
        point34 = adsk.core.Point3D.create(self.detailWidth*0.342+self.detailWidth*0.079,self.detailHeight*0.66 - self.detailHeight*0.04)
        point35 = adsk.core.Point3D.create(self.detailWidth*0.342+self.detailWidth*0.079+self.detailWidth*0.158/2,self.detailHeight*0.66+self.detailHeight*0.04 - self.detailHeight*0.04)
        point36 = adsk.core.Point3D.create(self.detailWidth*0.579,self.detailHeight*0.66 - self.detailHeight*0.04)
        point37 = adsk.core.Point3D.create(self.detailWidth*0.658 - (self.detailHeight*0.04),self.detailHeight*0.66 - self.detailHeight*0.04)
        point38 = adsk.core.Point3D.create(self.detailWidth*0.658 - (self.detailHeight*0.04),self.detailHeight*0.34 + (self.detailHeight)*0.04)
        point39 = adsk.core.Point3D.create(self.detailWidth*0.579,self.detailHeight*0.34 + (self.detailHeight)*0.04)
        point40 = adsk.core.Point3D.create(self.detailWidth*0.342+self.detailWidth*0.079+self.detailWidth*0.158/2,self.detailHeight*0.34-self.detailHeight*0.04 + (self.detailHeight)*0.04 )
        point41 = adsk.core.Point3D.create(self.detailWidth*0.342+self.detailWidth*0.079,self.detailHeight*0.34 + (self.detailHeight)*0.04)
        
        sketch4.sketchCurves.sketchLines.addByTwoPoints(point32,point33)
        sketch4.sketchCurves.sketchLines.addByTwoPoints(point33,point34)
        sketch4.sketchCurves.sketchArcs.addByThreePoints(point34,point35,point36)
        sketch4.sketchCurves.sketchLines.addByTwoPoints(point36,point37)
        sketch4.sketchCurves.sketchLines.addByTwoPoints(point37,point38)
        sketch4.sketchCurves.sketchLines.addByTwoPoints(point38,point39)
        sketch4.sketchCurves.sketchArcs.addByThreePoints(point39,point40,point41)
        sketch4.sketchCurves.sketchLines.addByTwoPoints(point41,point32)
        
        sketch4Prof = sketch4.profiles[0]
        sketch4ExtInput = extrudes.createInput(sketch4Prof, adsk.fusion.FeatureOperations.JoinFeatureOperation)
        
        distance2 = adsk.core.ValueInput.createByReal(self.detailThicknes*0.5)
        sketch4ExtInput.setDistanceExtent(True, distance2)
        sketch4Ext = extrudes.add(sketch4ExtInput)
        
        
        sketch5 = sketches.add(xyPlane)
        
        point42 = adsk.core.Point3D.create(self.detailWidth*0.342 + (self.detailHeight)*0.04,self.detailHeight*0.34 + (self.detailHeight)*0.04)
        point43 = adsk.core.Point3D.create(self.detailWidth*0.342 + (self.detailHeight)*0.04,self.detailHeight*0.66 - self.detailHeight*0.04)
        point44 = adsk.core.Point3D.create(self.detailWidth*0.342+self.detailWidth*0.079,self.detailHeight*0.66 - self.detailHeight*0.04)
        point45 = adsk.core.Point3D.create(self.detailWidth*0.342+self.detailWidth*0.079+self.detailWidth*0.158/2,self.detailHeight*0.66+self.detailHeight*0.04 - self.detailHeight*0.04)
        point46 = adsk.core.Point3D.create(self.detailWidth*0.579,self.detailHeight*0.66 - self.detailHeight*0.04)
        point47 = adsk.core.Point3D.create(self.detailWidth*0.658 - (self.detailHeight*0.04),self.detailHeight*0.66 - self.detailHeight*0.04)
        point48 = adsk.core.Point3D.create(self.detailWidth*0.658 - (self.detailHeight*0.04),self.detailHeight*0.34 + (self.detailHeight)*0.04)
        point49 = adsk.core.Point3D.create(self.detailWidth*0.579,self.detailHeight*0.34 + (self.detailHeight)*0.04)
        point50 = adsk.core.Point3D.create(self.detailWidth*0.342+self.detailWidth*0.079+self.detailWidth*0.158/2,self.detailHeight*0.34-self.detailHeight*0.04 + (self.detailHeight)*0.04 )
        point51 = adsk.core.Point3D.create(self.detailWidth*0.342+self.detailWidth*0.079,self.detailHeight*0.34 + (self.detailHeight)*0.04)
        
        sketch5.sketchCurves.sketchLines.addByTwoPoints(point42,point43)
        sketch5.sketchCurves.sketchLines.addByTwoPoints(point43,point44)
        sketch5.sketchCurves.sketchArcs.addByThreePoints(point44,point45,point46)
        sketch5.sketchCurves.sketchLines.addByTwoPoints(point46,point47)
        sketch5.sketchCurves.sketchLines.addByTwoPoints(point47,point48)
        sketch5.sketchCurves.sketchLines.addByTwoPoints(point48,point49)
        sketch5.sketchCurves.sketchArcs.addByThreePoints(point49,point50,point51)
        sketch5.sketchCurves.sketchLines.addByTwoPoints(point51,point42)
        
        sketch5Prof = sketch5.profiles[0]
        sketch5ExtInput = extrudes.createInput(sketch5Prof, adsk.fusion.FeatureOperations.CutFeatureOperation)
        
        distance3 = adsk.core.ValueInput.createByReal(self.detailThicknes)
        sketch5ExtInput.setDistanceExtent(True, distance3)
        sketch5Ext = extrudes.add(sketch5ExtInput)
        
        
        sketch6 = sketches.add(xyPlane)
        distance5 = adsk.core.ValueInput.createByReal(self.detailThicknes/2)
        CDpoint = adsk.core.Point3D.create(self.detailWidth*0.2895,self.detailHeight*0.5)
        CDpoint2 = adsk.core.Point3D.create(self.detailWidth*0.7105,self.detailHeight*0.5)
        sketch6.sketchCurves.sketchCircles.addByCenterRadius(CDpoint, self.detailBHoled/2)     
        sketch6.sketchCurves.sketchCircles.addByCenterRadius(CDpoint2, self.detailBHoled/2)  
        sketch6Prof = sketch6.profiles[0]
        sketch6Prof = sketch6.profiles[1]
        
        for i in range(2):
            sketch6ExtInput = extrudes.createInput(sketch6.profiles[i], adsk.fusion.FeatureOperations.JoinFeatureOperation)
            sketch6ExtInput.setDistanceExtent(True, distance5)
            sketch6Ext = extrudes.add(sketch6ExtInput)
        
        sketch7 = sketches.add(xyPlane)
        sketch7.sketchCurves.sketchCircles.addByCenterRadius(CDpoint, self.detailBHoled/4)
        sketch7.sketchCurves.sketchCircles.addByCenterRadius(CDpoint2, self.detailBHoled/4)
        sketch7Prof = sketch7.profiles[0]
        sketch7Prof = sketch7.profiles[1]
        
        for i in range(2):
            sketch7ExtInput = extrudes.createInput(sketch7.profiles[i], adsk.fusion.FeatureOperations.CutFeatureOperation)
            sketch7ExtInput.setDistanceExtent(True, distance5)
            sketch7Ext = extrudes.add(sketch7ExtInput)
        
        
        sketch8 = sketches.add(xzPlane)
        
        distance6 =  adsk.core.ValueInput.createByReal(-self.detailHeight*0.2)
        
        
        CDpoint3 = adsk.core.Point3D.create(self.detailWidth*0.184,self.detailThicknes/2,self.detailHeight)
        CDpoint4 = adsk.core.Point3D.create(self.detailWidth*0.184 + self.detailWidth * 0.21,self.detailThicknes/2,self.detailHeight)
        CDpoint5 = adsk.core.Point3D.create(self.detailWidth*0.184 + self.detailWidth * 0.42,self.detailThicknes/2,self.detailHeight)
        CDpoint6 = adsk.core.Point3D.create(self.detailWidth*0.184 + self.detailWidth * 0.63,self.detailThicknes/2,self.detailHeight)
        sketch8.sketchCurves.sketchCircles.addByCenterRadius(CDpoint3, self.detailBHoled/4)
        sketch8.sketchCurves.sketchCircles.addByCenterRadius(CDpoint4, self.detailBHoled/4)
        sketch8.sketchCurves.sketchCircles.addByCenterRadius(CDpoint5, self.detailBHoled/4)
        sketch8.sketchCurves.sketchCircles.addByCenterRadius(CDpoint6, self.detailBHoled/4)
        
        sketch8Prof = sketch8.profiles[0]
        sketch8Prof = sketch8.profiles[1]
        sketch8Prof = sketch8.profiles[2]
        sketch8Prof = sketch8.profiles[3]
            
        for i in range(4): 
            
            sketch8ExtInput = extrudes.createInput(sketch8.profiles[i], adsk.fusion.FeatureOperations.CutFeatureOperation)
            sketch8ExtInput.setDistanceExtent(False, distance6)
            sketch8Ext = extrudes.add(sketch8ExtInput)
        
        
        sketch9 = sketches.add(xzPlane)
        
        distance7 =  adsk.core.ValueInput.createByReal(self.detailHeight*0.2)
        
        
        CDpoint7 = adsk.core.Point3D.create(self.detailWidth*0.184,self.detailThicknes/2,0)
        CDpoint8 = adsk.core.Point3D.create(self.detailWidth*0.184 + self.detailWidth * 0.21,self.detailThicknes/2,0)
        CDpoint9 = adsk.core.Point3D.create(self.detailWidth*0.184 + self.detailWidth * 0.42,self.detailThicknes/2,0)
        CDpoint10 = adsk.core.Point3D.create(self.detailWidth*0.184 + self.detailWidth * 0.63,self.detailThicknes/2,0)
        sketch9.sketchCurves.sketchCircles.addByCenterRadius(CDpoint7, self.detailBHoled/4)
        sketch9.sketchCurves.sketchCircles.addByCenterRadius(CDpoint8, self.detailBHoled/4)
        sketch9.sketchCurves.sketchCircles.addByCenterRadius(CDpoint9, self.detailBHoled/4)
        sketch9.sketchCurves.sketchCircles.addByCenterRadius(CDpoint10, self.detailBHoled/4)
        
        sketch9Prof = sketch9.profiles[0]
        sketch9Prof = sketch9.profiles[1]
        sketch9Prof = sketch9.profiles[2]
        sketch9Prof = sketch9.profiles[3]
            
        for i in range(4): 
            
            sketch9ExtInput = extrudes.createInput(sketch9.profiles[i], adsk.fusion.FeatureOperations.CutFeatureOperation)
            sketch9ExtInput.setDistanceExtent(False, distance7)
            sketch9Ext = extrudes.add(sketch9ExtInput)
            
        sketch10 = sketches.add(xyPlane)
        distance8 = adsk.core.ValueInput.createByReal(self.detailThicknes)
        
        point52 = adsk.core.Point3D.create(self.detailWidth*0.026,self.detailHeight*0.4,0)
        point53 = adsk.core.Point3D.create(self.detailWidth*0.026,self.detailHeight*0.6,0)
        point54 = adsk.core.Point3D.create(self.detailWidth*0.13,self.detailHeight*0.6,0)
        point55 = adsk.core.Point3D.create(self.detailWidth*0.13,self.detailHeight*0.4,0)
        
        sketch10.sketchCurves.sketchLines.addByTwoPoints(point52,point53)
        sketch10.sketchCurves.sketchLines.addByTwoPoints(point53,point54)
        sketch10.sketchCurves.sketchLines.addByTwoPoints(point54,point55)
        sketch10.sketchCurves.sketchLines.addByTwoPoints(point55,point52)
        
        point56 = adsk.core.Point3D.create(self.detailWidth - self.detailWidth*0.026  ,self.detailHeight*0.4,0)
        point57 = adsk.core.Point3D.create(self.detailWidth - self.detailWidth*0.026,self.detailHeight*0.6,0)
        point58 = adsk.core.Point3D.create(self.detailWidth*0.87,self.detailHeight*0.6,0)
        point59 = adsk.core.Point3D.create(self.detailWidth*0.87,self.detailHeight*0.4,0)
        
        sketch10.sketchCurves.sketchLines.addByTwoPoints(point56,point57)
        sketch10.sketchCurves.sketchLines.addByTwoPoints(point57,point58)
        sketch10.sketchCurves.sketchLines.addByTwoPoints(point58,point59)
        sketch10.sketchCurves.sketchLines.addByTwoPoints(point59,point56)
        
        sketch10Prof = sketch10.profiles[0]
        sketch10Prof = sketch10.profiles[1]
        
        for i in range(2):
            
            sketch10ExtInput = extrudes.createInput(sketch10.profiles[i], adsk.fusion.FeatureOperations.CutFeatureOperation)
            sketch10ExtInput.setDistanceExtent(True, distance8)
            sketch10Ext = extrudes.add(sketch10ExtInput)  
            
        sketch11 = sketches.add(xyPlane) 
        distance9 = adsk.core.ValueInput.createByReal(self.detailThicknes/2)
        
        CDpoint11 = adsk.core.Point3D.create(self.detailWidth * 0.079 , self.detailHeight*0.18,0)
        CDpoint12 = adsk.core.Point3D.create(self.detailWidth * 0.079 + self.detailWidth * 0.21 , self.detailHeight*0.18,0)
        CDpoint13 = adsk.core.Point3D.create(self.detailWidth * 0.079 + self.detailWidth * 0.42 , self.detailHeight*0.18,0)
        CDpoint14 = adsk.core.Point3D.create(self.detailWidth * 0.079 + self.detailWidth * 0.63 , self.detailHeight*0.18,0)
        CDpoint15 = adsk.core.Point3D.create(self.detailWidth * 0.079 + self.detailWidth * 0.84 , self.detailHeight*0.18,0)
        
        sketch11.sketchCurves.sketchCircles.addByCenterRadius(CDpoint11, self.detailBHoled/2)
        sketch11.sketchCurves.sketchCircles.addByCenterRadius(CDpoint12, self.detailBHoled/2)
        sketch11.sketchCurves.sketchCircles.addByCenterRadius(CDpoint13, self.detailBHoled/2)
        sketch11.sketchCurves.sketchCircles.addByCenterRadius(CDpoint14, self.detailBHoled/2)
        sketch11.sketchCurves.sketchCircles.addByCenterRadius(CDpoint15, self.detailBHoled/2)
        
        CDpoint16 = adsk.core.Point3D.create(self.detailWidth * 0.079 , self.detailHeight * 0.82 ,0)
        CDpoint17 = adsk.core.Point3D.create(self.detailWidth * 0.079 + self.detailWidth * 0.21 , self.detailHeight*0.82,0)
        CDpoint18 = adsk.core.Point3D.create(self.detailWidth * 0.079 + self.detailWidth * 0.42 , self.detailHeight*0.82,0)
        CDpoint19 = adsk.core.Point3D.create(self.detailWidth * 0.079 + self.detailWidth * 0.63 , self.detailHeight*0.82,0)
        CDpoint20 = adsk.core.Point3D.create(self.detailWidth * 0.079 + self.detailWidth * 0.84 , self.detailHeight*0.82,0)
        
       
        sketch11.sketchCurves.sketchCircles.addByCenterRadius(CDpoint16, self.detailBHoled/2)
        sketch11.sketchCurves.sketchCircles.addByCenterRadius(CDpoint17, self.detailBHoled/2)
        sketch11.sketchCurves.sketchCircles.addByCenterRadius(CDpoint18, self.detailBHoled/2)
        sketch11.sketchCurves.sketchCircles.addByCenterRadius(CDpoint19, self.detailBHoled/2)
        sketch11.sketchCurves.sketchCircles.addByCenterRadius(CDpoint20, self.detailBHoled/2)
        
      

    
        
        
        for i in range(10): 
            
            sketch11ExtInput = extrudes.createInput(sketch11.profiles[i], adsk.fusion.FeatureOperations.JoinFeatureOperation)
            sketch11ExtInput.setDistanceExtent(False, distance9)
            sketch11Ext = extrudes.add(sketch11ExtInput)    
            
            
        sketch12 = sketches.add(xyPlane)   
        
        CDpoint11 = adsk.core.Point3D.create(self.detailWidth * 0.079 , self.detailHeight*0.18,0)
        CDpoint12 = adsk.core.Point3D.create(self.detailWidth * 0.079 + self.detailWidth * 0.21 , self.detailHeight*0.18,0)
        CDpoint13 = adsk.core.Point3D.create(self.detailWidth * 0.079 + self.detailWidth * 0.42 , self.detailHeight*0.18,0)
        CDpoint14 = adsk.core.Point3D.create(self.detailWidth * 0.079 + self.detailWidth * 0.63 , self.detailHeight*0.18,0)
        CDpoint15 = adsk.core.Point3D.create(self.detailWidth * 0.079 + self.detailWidth * 0.84 , self.detailHeight*0.18,0)
        
        sketch12.sketchCurves.sketchCircles.addByCenterRadius(CDpoint11, self.detailBHoled/4)
        sketch12.sketchCurves.sketchCircles.addByCenterRadius(CDpoint12, self.detailBHoled/4)
        sketch12.sketchCurves.sketchCircles.addByCenterRadius(CDpoint13, self.detailBHoled/4)
        sketch12.sketchCurves.sketchCircles.addByCenterRadius(CDpoint14, self.detailBHoled/4)
        sketch12.sketchCurves.sketchCircles.addByCenterRadius(CDpoint15, self.detailBHoled/4)
        
        CDpoint16 = adsk.core.Point3D.create(self.detailWidth * 0.079 , self.detailHeight * 0.82 ,0)
        CDpoint17 = adsk.core.Point3D.create(self.detailWidth * 0.079 + self.detailWidth * 0.21 , self.detailHeight*0.82,0)
        CDpoint18 = adsk.core.Point3D.create(self.detailWidth * 0.079 + self.detailWidth * 0.42 , self.detailHeight*0.82,0)
        CDpoint19 = adsk.core.Point3D.create(self.detailWidth * 0.079 + self.detailWidth * 0.63 , self.detailHeight*0.82,0)
        CDpoint20 = adsk.core.Point3D.create(self.detailWidth * 0.079 + self.detailWidth * 0.84 , self.detailHeight*0.82,0)
        
       
        sketch12.sketchCurves.sketchCircles.addByCenterRadius(CDpoint16, self.detailBHoled/4)
        sketch12.sketchCurves.sketchCircles.addByCenterRadius(CDpoint17, self.detailBHoled/4)
        sketch12.sketchCurves.sketchCircles.addByCenterRadius(CDpoint18, self.detailBHoled/4)
        sketch12.sketchCurves.sketchCircles.addByCenterRadius(CDpoint19, self.detailBHoled/4)
        sketch12.sketchCurves.sketchCircles.addByCenterRadius(CDpoint20, self.detailBHoled/4)
        
        for i in range(10): 
            
            sketch12ExtInput = extrudes.createInput(sketch12.profiles[i], adsk.fusion.FeatureOperations.CutFeatureOperation)
            sketch12ExtInput.setDistanceExtent(True, distance8)
            sketch12Ext = extrudes.add(sketch12ExtInput)
        
        sketch13 = sketches.add(xyPlane)
        
        point1 = adsk.core.Point3D.create(0,self.detailHeight1+self.detailHeight*0.20,0)
        point2 = adsk.core.Point3D.create(self.detailWidth*0.132,self.detailHeight,0)
        point3 = adsk.core.Point3D.create(0,self.detailHeight)
        point4 = adsk.core.Point3D.create(self.detailWidth,self.detailHeight1+self.detailHeight*0.20,0)
        point5 = adsk.core.Point3D.create(self.detailWidth - self.detailWidth*0.14 , self.detailHeight ,0)
        point6 = adsk.core.Point3D.create(self.detailWidth , self.detailHeight ,0)
        point7 = adsk.core.Point3D.create(0 ,self.detailHeight*0.20 ,0)
        point8 = adsk.core.Point3D.create(self.detailWidth*0.132 , 0 ,0)
        point9 = adsk.core.Point3D.create(0, 0 ,0)
        point10 = adsk.core.Point3D.create(self.detailWidth - self.detailWidth*0.132 , 0 ,0)
        point11 = adsk.core.Point3D.create(self.detailWidth , self.detailHeight*0.20 ,0)
        point12 = adsk.core.Point3D.create(self.detailWidth , 0 ,0)
        
        
           
        
        sketch13.sketchCurves.sketchLines.addByTwoPoints(point1,point2)
        sketch13.sketchCurves.sketchLines.addByTwoPoints(point2,point3)
        sketch13.sketchCurves.sketchLines.addByTwoPoints(point3,point1)
        sketch13.sketchCurves.sketchLines.addByTwoPoints(point4,point5)
        sketch13.sketchCurves.sketchLines.addByTwoPoints(point5,point6)
        sketch13.sketchCurves.sketchLines.addByTwoPoints(point6,point4)
        sketch13.sketchCurves.sketchLines.addByTwoPoints(point7,point8)
        sketch13.sketchCurves.sketchLines.addByTwoPoints(point8,point9)
        sketch13.sketchCurves.sketchLines.addByTwoPoints(point9,point7)
        sketch13.sketchCurves.sketchLines.addByTwoPoints(point10,point11)
        sketch13.sketchCurves.sketchLines.addByTwoPoints(point11,point12)
        sketch13.sketchCurves.sketchLines.addByTwoPoints(point12,point10)
        
        
        for i in range(4): 
            
            sketch13ExtInput = extrudes.createInput(sketch13.profiles[i], adsk.fusion.FeatureOperations.CutFeatureOperation)
            sketch13ExtInput.setDistanceExtent(True, distance8)
            sketch13Ext = extrudes.add(sketch13ExtInput)
            
            
        sketch14 = sketches.add(yzPlane)
        point10 = adsk.core.Point3D.create(-self.detailThicknes*0.5,self.detailHeight*0.41)
        point11 = adsk.core.Point3D.create(-self.detailThicknes*0.5,self.detailHeight*0.59)
        point12 = adsk.core.Point3D.create(self.detailThicknes*0.375,self.detailHeight*0.59)
        point13 = adsk.core.Point3D.create(self.detailThicknes*0.375,self.detailHeight*0.47)
        point14 = adsk.core.Point3D.create(-self.detailThicknes*0.375,self.detailHeight*0.47)
        point15 = adsk.core.Point3D.create(-self.detailThicknes*0.375,self.detailHeight*0.59)
        point16 = adsk.core.Point3D.create(self.detailThicknes*0.5,self.detailHeight*0.59)
        point17 = adsk.core.Point3D.create(self.detailThicknes*0.5,self.detailHeight*0.41)
        
        sketch14.sketchCurves.sketchLines.addByTwoPoints(point10,point11)
        sketch14.sketchCurves.sketchLines.addByTwoPoints(point11,point12)
        sketch14.sketchCurves.sketchLines.addByTwoPoints(point12,point13)
        sketch14.sketchCurves.sketchLines.addByTwoPoints(point13,point14)
        sketch14.sketchCurves.sketchLines.addByTwoPoints(point14,point15)
        sketch14.sketchCurves.sketchLines.addByTwoPoints(point15,point16)
        sketch14.sketchCurves.sketchLines.addByTwoPoints(point16,point17)
        sketch14.sketchCurves.sketchLines.addByTwoPoints(point17,point10)
        
        sketch14Prof = sketch14.profiles[0]
        sketch14ExtInput = extrudes.createInput(sketch14Prof, adsk.fusion.FeatureOperations.CutFeatureOperation)
        
        distance9 = adsk.core.ValueInput.createByReal(self.detailThicknes*0.25)
        sketch14ExtInput.setDistanceExtent(False, distance9)
        sketch14Ext = extrudes.add(sketch14ExtInput)    
        
        
        sketch15 = sketches.add(yzPlane)
        point10 = adsk.core.Point3D.create(-self.detailThicknes*0.5,self.detailHeight*0.41,self.detailWidth)
        point11 = adsk.core.Point3D.create(-self.detailThicknes*0.5,self.detailHeight*0.59,self.detailWidth)
        point12 = adsk.core.Point3D.create(self.detailThicknes*0.375,self.detailHeight*0.59,self.detailWidth)
        point13 = adsk.core.Point3D.create(self.detailThicknes*0.375,self.detailHeight*0.47,self.detailWidth)
        point14 = adsk.core.Point3D.create(-self.detailThicknes*0.375,self.detailHeight*0.47,self.detailWidth)
        point15 = adsk.core.Point3D.create(-self.detailThicknes*0.375,self.detailHeight*0.59,self.detailWidth)
        point16 = adsk.core.Point3D.create(self.detailThicknes*0.5,self.detailHeight*0.59,self.detailWidth)
        point17 = adsk.core.Point3D.create(self.detailThicknes*0.5,self.detailHeight*0.41,self.detailWidth)
        
        sketch15.sketchCurves.sketchLines.addByTwoPoints(point10,point11)
        sketch15.sketchCurves.sketchLines.addByTwoPoints(point11,point12)
        sketch15.sketchCurves.sketchLines.addByTwoPoints(point12,point13)
        sketch15.sketchCurves.sketchLines.addByTwoPoints(point13,point14)
        sketch15.sketchCurves.sketchLines.addByTwoPoints(point14,point15)
        sketch15.sketchCurves.sketchLines.addByTwoPoints(point15,point16)
        sketch15.sketchCurves.sketchLines.addByTwoPoints(point16,point17)
        sketch15.sketchCurves.sketchLines.addByTwoPoints(point17,point10)
        
        sketch15Prof = sketch15.profiles[0]
        sketch15ExtInput = extrudes.createInput(sketch15Prof, adsk.fusion.FeatureOperations.CutFeatureOperation)
        
        distance9 = adsk.core.ValueInput.createByReal(-self.detailThicknes*0.25)
        sketch15ExtInput.setDistanceExtent(False, distance9)
        sketch15Ext = extrudes.add(sketch15ExtInput)    
        
        sketch16 = sketches.add(yzPlane) 
        distance9 = adsk.core.ValueInput.createByReal(self.detailHeight*0.24)
        
        CDpoint1 = adsk.core.Point3D.create(0 , self.detailHeight*0.67)
        CDpoint2 = adsk.core.Point3D.create(0 , self.detailHeight*0.33)
       
        sketch16.sketchCurves.sketchCircles.addByCenterRadius(CDpoint1, self.detailBHoled*0.4375)
        sketch16.sketchCurves.sketchCircles.addByCenterRadius(CDpoint2, self.detailBHoled*0.4375)
        
        sketch16Prof = sketch16.profiles[0]
        sketch16Prof = sketch16.profiles[1]
        
        for i in range(2):
            sketch16ExtInput = extrudes.createInput(sketch16.profiles[i], adsk.fusion.FeatureOperations.JoinFeatureOperation)
            sketch16ExtInput.setDistanceExtent(False, distance9)
            sketch16Ext = extrudes.add(sketch16ExtInput)  
            
            
        sketch17 = sketches.add(yzPlane) 
        distance9 = adsk.core.ValueInput.createByReal(-self.detailHeight*0.24)
        
        CDpoint1 = adsk.core.Point3D.create(0 , self.detailHeight*0.67, self.detailWidth)
        CDpoint2 = adsk.core.Point3D.create(0 , self.detailHeight*0.33, self.detailWidth)
       
        sketch17.sketchCurves.sketchCircles.addByCenterRadius(CDpoint1, self.detailBHoled*0.4375)
        sketch17.sketchCurves.sketchCircles.addByCenterRadius(CDpoint2, self.detailBHoled*0.4375)
        
        sketch17Prof = sketch17.profiles[0]
        sketch17Prof = sketch17.profiles[1]
        
        for i in range(2):
            sketch17ExtInput = extrudes.createInput(sketch17.profiles[i], adsk.fusion.FeatureOperations.JoinFeatureOperation)
            sketch17ExtInput.setDistanceExtent(False, distance9)
            sketch17Ext = extrudes.add(sketch17ExtInput)  
            
            
        sketch18 = sketches.add(yzPlane) 
        distance9 = adsk.core.ValueInput.createByReal(-self.detailHeight*0.20)
        
        CDpoint1 = adsk.core.Point3D.create(0 , self.detailHeight*0.67, self.detailWidth)
        CDpoint2 = adsk.core.Point3D.create(0 , self.detailHeight*0.33, self.detailWidth)
       
        sketch18.sketchCurves.sketchCircles.addByCenterRadius(CDpoint1, self.detailBHoled*0.3125)
        sketch18.sketchCurves.sketchCircles.addByCenterRadius(CDpoint2, self.detailBHoled*0.3125)
        
        sketch18Prof = sketch18.profiles[0]
        sketch18Prof = sketch18.profiles[1]
        
        for i in range(2):
            sketch18ExtInput = extrudes.createInput(sketch18.profiles[i], adsk.fusion.FeatureOperations.CutFeatureOperation)
            sketch18ExtInput.setDistanceExtent(False, distance9)
            sketch18Ext = extrudes.add(sketch18ExtInput)       
            
            
        sketch19 = sketches.add(yzPlane) 
        distance9 = adsk.core.ValueInput.createByReal(self.detailHeight*0.20)
        
        CDpoint1 = adsk.core.Point3D.create(0 , self.detailHeight*0.67)
        CDpoint2 = adsk.core.Point3D.create(0 , self.detailHeight*0.33)
       
        sketch19.sketchCurves.sketchCircles.addByCenterRadius(CDpoint1, self.detailBHoled*0.3125)
        sketch19.sketchCurves.sketchCircles.addByCenterRadius(CDpoint2, self.detailBHoled*0.3125)
        
        sketch19Prof = sketch19.profiles[0]
        sketch19Prof = sketch19.profiles[1]
        
        for i in range(2):
            sketch19ExtInput = extrudes.createInput(sketch19.profiles[i], adsk.fusion.FeatureOperations.CutFeatureOperation)
            sketch19ExtInput.setDistanceExtent(False, distance9)
            sketch19Ext = extrudes.add(sketch19ExtInput)  
            
              
        sketch21 = sketches.add(xyPlane) 
        distance12 = adsk.core.ValueInput.createByReal(self.detailThicknes*0.625/2)
        
        CDpoint1 = adsk.core.Point3D.create(self.detailHeight*0.04 , self.detailHeight*0.49)
        CDpoint2 = adsk.core.Point3D.create(self.detailWidth - self.detailHeight*0.04  , self.detailHeight*0.49)
       
        sketch21.sketchCurves.sketchCircles.addByCenterRadius(CDpoint1, self.detailBHoled/8)
        sketch21.sketchCurves.sketchCircles.addByCenterRadius(CDpoint2, self.detailBHoled/8)
        
        sketch21Prof = sketch21.profiles[0]
        sketch21Prof = sketch21.profiles[1]
        
        for i in range(2):
            sketch21ExtInput = extrudes.createInput(sketch21.profiles[i], adsk.fusion.FeatureOperations.JoinFeatureOperation)
            sketch21ExtInput.setDistanceExtent(True, distance12)
            sketch21Ext = extrudes.add(sketch21ExtInput)       
            
            
        
        
        
            ui = None
            try:
                app = adsk.core.Application.get()
                ui = app.userInterface
                product = app.activeProduct
                design = adsk.fusion.Design.cast(product)
                    
                rootComp = design.rootComponent
                    
                sketches = rootComp.sketches 
                    
                    
                
                
                sketch20 = sketches.add(rootComp.xZConstructionPlane)
                distance11 = adsk.core.ValueInput.createByReal(-self.detailHeight*0.06)
                br = 0
                step = 0
                for i in range(2):
                    
                
                    
                    for i in range(4):
                    
                        point1 = adsk.core.Point3D.create(self.detailHeight*0.2 + step ,self.detailThicknes/2,self.detailHeight*0.14 + br)
                        point2 = adsk.core.Point3D.create(self.detailHeight*0.23 + step ,0,self.detailHeight*0.14 + br)
                        point3 = adsk.core.Point3D.create(self.detailHeight*0.33 + step, 0 ,self.detailHeight*0.14 + br)
                        point4 = adsk.core.Point3D.create(self.detailHeight*0.36 + step,self.detailThicknes/2,self.detailHeight*0.14 + br)
                    
                        sketch20.sketchCurves.sketchLines.addByTwoPoints(point1,point2)
                        sketch20.sketchCurves.sketchLines.addByTwoPoints(point2,point3)
                        sketch20.sketchCurves.sketchLines.addByTwoPoints(point3,point4)
                        sketch20.sketchCurves.sketchLines.addByTwoPoints(point4,point1)
                   
                        
                        
                        step = step + (self.detailHeight*0.32)
                    
                    br = br + (self.detailHeight * 0.78)
                    step = 0
                for i in range(8):
                    
                    sketch20ExtInput = extrudes.createInput(sketch20.profiles[i], adsk.fusion.FeatureOperations.CutFeatureOperation)
                    sketch20ExtInput.setDistanceExtent(False, distance11)
                    sketch20Ext = extrudes.add(sketch20ExtInput) 
                    
        
            except:
                if ui:
                    ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
        
       
def run(context):
    try:
        commandDefinitions = ui.commandDefinitions
        #check the command exists or not
        cmdDef = commandDefinitions.itemById('Detail')
        if not cmdDef:
            cmdDef = commandDefinitions.addButtonDefinition('Detail',
                    'Create Detail',
                    'Create a detail.',
                    '') # relative resource file path is specified

        onCommandCreated = DetailCommandCreatedHandler()
        cmdDef.commandCreated.add(onCommandCreated)
        # keep the handler referenced beyond this function
        handlers.append(onCommandCreated)
        inputs = adsk.core.NamedValues.create()
        cmdDef.execute(inputs)

        # prevent this module from being terminate when the script returns, because we are waiting for event handlers to fire
        adsk.autoTerminate(False)
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

