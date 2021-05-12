import adsk.core, adsk.fusion, adsk.cam, traceback

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface
        
        design = app.activeProduct

        dHC = 0
        DHC = 0
        LHC = 0
        l_1HC = 0
        l_2HC = 0
        d_2HC = 0 
        d_1HC = 0
        ext_all_HC = 0
        B_HC = 0
        H_HC = 0
        d_3HC = 0
        d_4HC = 0 
        D_2HC = 0
        b_1HC = 0
        b_2HC = 0
        R_1HC = 0
        R_HC = 0

        data = [('18 mm', '80 mm', '25 mm', '8 mm', '2 mm', '25 mm', '11 mm', '1000 mm', '2 mm', '12.8 mm', '8.4 mm', '9 mm', '55 mm', '1 mm', '0.5 mm', '1 mm', '0.2 mm'), 
                ('18 mm', '80 mm', '22 mm', '8 mm', '2 mm', '25 mm', '11 mm', '1000 mm', '2 mm', '12.8 mm', '8.4 mm', '9 mm', '55 mm', '1 mm', '0.5 mm', '1 mm', '0.2 mm')]

        keyParam = '25 mm'

        for i in range(0, len(data)):
            if data[i][2] == keyParam:
              dHC = data[i][0]
              DHC = data[i][1]
              LHC = data[i][2]
              l_1HC = data[i][3]
              l_2HC = data[i][4] 
              d_2HC = data[i][5]
              d_1HC = data[i][6]
              ext_all_HC = data[i][7]
              BHC = data[i][8]
              H_HC = data[i][9]
              d_3HC = data[i][10]
              d_4HC = data[i][11] 
              D_2HC = data[i][12]
              b_1HC = data[i][13]
              b_2HC = data[i][14]  
              R_1HC = data[i][15]
              R_HC = data[i][16]
              break
        
        dParam = design.userParameters.itemByName('dHC')
        dParam.expression = dHC

        DParam = design.userParameters.itemByName('DHC')
        DParam.expression = DHC

        LParam = design.userParameters.itemByName('LHC')
        LParam.expression = LHC

        l_1Param = design.userParameters.itemByName('l_1HC')
        l_1Param.expression = l_1HC

        l_2Param = design.userParameters.itemByName('l_2HC')
        l_2Param.expression = l_2HC

        d_1Param = design.userParameters.itemByName('d_1HC')
        d_1Param.expression = d_1HC

        d_2Param = design.userParameters.itemByName('d_2HC')
        d_2Param.expression = d_2HC

        extParam = design.userParameters.itemByName('ext_all_HC')
        extParam.expression = ext_all_HC

        BParam = design.userParameters.itemByName('B_HC')
        BParam.expression = BHC

        H_Param = design.userParameters.itemByName('H_HC')
        H_Param.expression = H_HC

        d_3Param = design.userParameters.itemByName('d_3HC')
        d_3Param.expression = d_3HC

        d_4Param = design.userParameters.itemByName('d_4HC')
        d_4Param.expression = d_4HC

        D_2Param = design.userParameters.itemByName('D_2HC')
        D_2Param.expression = D_2HC

        b_1Param = design.userParameters.itemByName('b_1HC')
        b_1Param.expression = b_1HC

        b_2Param = design.userParameters.itemByName('b_2HC')
        b_2Param.expression = b_2HC

        R_1Param = design.userParameters.itemByName('R_1HC')
        R_1Param.expression = R_1HC

        R_Param = design.userParameters.itemByName('R_HC')
        R_Param.expression = R_HC 
     
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
