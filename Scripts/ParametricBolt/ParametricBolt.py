import adsk.core, adsk.fusion, adsk.cam, traceback

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface
        design = app.activeProduct

        S_bolt2 = 0
        d_bolt2 = 0
        m_bolt2 = 0
        D_bolt2 = 0
        l1_bolt2 = 0
        b_bolt2 = 0
        chm_bolt2 = 0
        thr_bolt2 = 0

        data = [('12 mm', '8.0 mm', '5 mm', '5.718 mm', '30 mm', '22 mm', '0.5 mm', '8 mm'),
                 ('14 mm', '10 mm', '6.5 mm', '6 mm', '35 mm', '22 mm', '0.5 mm', '10 mm')
                ]
        keyParam = '8.0 mm'

        for i in range(0, len(data)):
            if data[i][1] == keyParam:
                S_bolt2 = data[i][0]
                d_bolt2 = data[i][1]
                m_bolt2 = data[i][2]
                D_bolt2 = data[i][3]
                l1_bolt2 = data[i][4]
                b_bolt2 = data[i][5]
                chm_bolt2 = data[i][6]
                thr_bolt2 = data[i][7]
                break
        
        S_bolt2Param = design.userParameters.itemByName('S_bolt2')
        S_bolt2Param.expression = S_bolt2

        dParam = design.userParameters.itemByName('d_bolt2')
        dParam.expression = d_bolt2

        m_Param = design.userParameters.itemByName('m_bolt2')
        m_Param.expression = m_bolt2

        D_Param = design.userParameters.itemByName('D_bolt2')
        D_Param.expression = D_bolt2

        l_1Param = design.userParameters.itemByName('l1_bolt2')
        l_1Param.expression = l1_bolt2

        bParam = design.userParameters.itemByName('b_bolt2')
        bParam.expression = b_bolt2

        chmParam = design.userParameters.itemByName('chm_bolt2')
        chmParam.expression = chm_bolt2

        thrParam = design.userParameters.itemByName('thr_bolt2')
        thrParam.expression = thr_bolt2

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
