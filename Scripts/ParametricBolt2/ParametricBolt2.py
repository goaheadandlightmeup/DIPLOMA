import adsk.core, adsk.fusion, adsk.cam, traceback

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface

        design = app.activeProduct

        S_bolt = 0
        m_bolt = 0
        L_bolt = 0
        l1_bolt = 0
        l2_bolt = 0
        d_bolt = 0
        d1_bolt = 0
        R_bolt = 0
        l3_bolt = 0
        d3_bolt = 0
        d4_bolt = 0
        ext_all_bolt = 0

        data = [('12 mm', '5 mm', '35 mm', '29.5 mm', '20.5 mm', '8 mm', '9 mm', '0.2 mm', '1 mm', '5.3 mm', '2 mm', '100 mm'),
                ('14 mm', '6.5 mm', '35 mm', '29.5 mm', '20.5 mm', '9 mm', '10 mm', '0.2 mm', '1 mm', '5.3 mm', '2 mm', '100 mm')]

        keyParam = '8 mm'

        for i in range(0, len(data)):
            if data[i][5] == keyParam:
                S_bolt = data[i][0]
                m_bolt = data[i][1]
                L_bolt = data[i][2]
                l1_bolt = data[i][3]
                l2_bolt = data[i][4]
                d_bolt = data[i][5]
                d1_bolt = data[i][6]
                R_bolt = data[i][7]
                l3_bolt = data[i][8]
                d3_bolt = data[i][9]
                d4_bolt= data[i][10]
                ext_all_bolt = data[i][11]
                break

        S_boltParam = design.userParameters.itemByName('S_bolt')
        S_boltParam.expression = S_bolt

        m_Param = design.userParameters.itemByName('m_bolt')
        m_Param.expression = m_bolt

        LParam = design.userParameters.itemByName('L_bolt')
        LParam.expression = L_bolt

        l_1Param = design.userParameters.itemByName('l1_bolt')
        l_1Param.expression = l1_bolt

        l_2Param = design.userParameters.itemByName('l2_bolt')
        l_2Param.expression = l2_bolt

        dParam = design.userParameters.itemByName('d_bolt')
        dParam.expression = d_bolt

        d_1Param = design.userParameters.itemByName('d1_bolt')
        d_1Param.expression = d1_bolt

        R_Param = design.userParameters.itemByName('R_bolt')
        R_Param.expression = R_bolt

        l_3Param = design.userParameters.itemByName('l3_bolt')
        l_3Param.expression = l3_bolt

        d_3Param = design.userParameters.itemByName('d3_bolt')
        d_3Param.expression = d3_bolt

        d_4Param = design.userParameters.itemByName('d4_bolt')
        d_4Param.expression = d4_bolt

        ext_allParam = design.userParameters.itemByName('ext_all_bolt')
        ext_allParam.expression = ext_all_bolt

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
