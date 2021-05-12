import adsk.core, adsk.fusion, adsk.cam, traceback

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface

        design = app.activeProduct
        # rootComp = design.rootComponent
        
        S_nut = 0
        d_nut = 0
        k_nut = 0 
        ch_nut = 0 
    
        data = [('12.0 mm', '8.0 mm', '6.5 mm', '0.5 mm'), 
                ('14 mm', '10 mm', '8 mm', '0.5 mm'), 
                ('16.0 mm', '12.0 mm', '10.0 mm', '0.5 mm')]

        keyParam = '8.0 mm'

        for i in range(0, len(data)):
            if data[i][1] == keyParam:
                S_nut = data[i][0]
                d_nut = data[i][1]
                k_nut = data[i][2]
                ch_nut = data[i][3]
                break

        S_Param = design.userParameters.itemByName('S_nut')
        S_Param.expression = S_nut
        S_Param.deleteMe()

        dParam = design.userParameters.itemByName('d_nut')
        dParam.expression = d_nut

        kParam = design.userParameters.itemByName('k_nut')
        kParam.expression = k_nut

        chParam = design.userParameters.itemByName('ch_nut')
        chParam.expression = ch_nut

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
