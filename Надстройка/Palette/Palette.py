import adsk.core, adsk.fusion, adsk.cam, traceback
import urllib.request
import urllib.error
import urllib.parse
import pathlib
import json

handlers = [] 
app = adsk.core.Application.get()
ui  = app.userInterface
global execution

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface

        workSpace = ui.workspaces.itemById('FusionSolidEnvironment')
        tbPanels = workSpace.toolbarPanels
        tbPanel = tbPanels.itemById('NewPanel')
        if tbPanel:
            tbPanel.deleteMe()
        tbPanel = tbPanels.add('NewPanel', 'БИБЛИОТЕКА МУФТ', 'SelectPanel', False)

        cmdDef = ui.commandDefinitions.itemById('NewCommand')
        if cmdDef:
            cmdDef.deleteMe()

            
        cmdDef = ui.commandDefinitions.addButtonDefinition('NewCommand', 'Создать муфту', 'Ввод параметров для соединительных муфт','.//resource')
        tbPanel.controls.addCommand(cmdDef)

        # Запуск плагина 
        sampleCommandCreated = SampleCommandCreatedEventHandler()
        cmdDef.commandCreated.add(sampleCommandCreated)
        handlers.append(sampleCommandCreated)

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))


class SampleCommandCreatedEventHandler(adsk.core.CommandCreatedEventHandler): #Создание событий по нажатию на надстроку
    def __init__(self):
        super().__init__()
    def notify(self, args):
        eventArgs = adsk.core.CommandCreatedEventArgs.cast(args)
        cmd = eventArgs.command

        # Вызывает создание диалогового окна
        onExecute = SampleCommandExecuteHandler()
        cmd.execute.add(onExecute)
        handlers.append(onExecute)

        #Вызывает забирание детали из сервера, кидает в папку, из папки в проект, очищает папку
        onModel = SampleCommandCrateModelHandler()
        cmd.execute.add(onModel)
        handlers.append(onModel)


    # Подгружаем сборку муфты с сервера с предварительным сохранением в папке Temp
class SampleCommandCrateModelHandler(adsk.core.CommandEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):
        try:
            app = adsk.core.Application.get()
            ui  = app.userInterface

            product = app.activeProduct
            design = adsk.fusion.Design.cast(product)
            rootComp = design.rootComponent
            importManager = app.importManager

            url = "http://195.133.144.86:4200//CouplingAssembly.f3d"

            doc = app.activeDocument
            if not doc.dataFile:
                ui.messageBox('Please save the document once.')
                # palette = None
                return adsk.fusion.Occurrence.cast(None)

            # создание папки для файла
            folder = pathlib.Path(r'C:\Temp')
            if not folder.exists():
                folder.mkdir()
            #задание имени для файла по имени на сервере
            parsed = urllib.parse.urlparse(url)
            filename = parsed.path.split('//')[-1]
            dlFile = folder / filename

            # провка расширения файла с сервера
            if dlFile.suffix != '.f3d':
                ui.messageBox('F3D File Only')
                return adsk.fusion.Occurrence.cast(None)

            # если файл если, то удалить
            if dlFile.is_file():
                dlFile.unlink()

            # загрузка файла
            try:
                data = urllib.request.urlopen(url).read()
                with open(str(dlFile), mode="wb") as f:
                    f.write(data)
            except:
                ui.messageBox(f'File not found in URL\n{url}')
                return adsk.fusion.Occurrence.cast(None)

            # импортирование
            archiveOptionsNew = importManager.createFusionArchiveImportOptions(str(dlFile))
            importManager.importToTarget(archiveOptionsNew, rootComp)
            
            # удаление скаченного файла
            if dlFile.is_file():
                dlFile.unlink()

        except:
            ui.messageBox('Command executed failed: {}'.format(traceback.format_exc()))


class SampleCommandExecuteHandler(adsk.core.CommandEventHandler): #создание диалогового окна и ожидание действия в HTML
    def __init__(self):
        super().__init__()
    def notify(self, args):
        try:
            app = adsk.core.Application.get()
            ui  = app.userInterface

            palette = ui.palettes.itemById('myExport')

            if not palette:
                palette = ui.palettes.add('myExport', 'БИБЛИОТЕКА МУФТ', 'index.html', True, True, True, 800, 600)
                palette.dockingState = adsk.core.PaletteDockingStates.PaletteDockStateRight

                #должен быть запуск параметризации после нажатия на кнопку
                onHTMLEvent = MyHTMLEventHandler()
                palette.incomingFromHTML.add(onHTMLEvent)   
                handlers.append(onHTMLEvent)

            else: 
                palette.isVisible = True
        except:
            ui.messageBox('Command executed failed: {}'.format(traceback.format_exc()))


class MyHTMLEventHandler(adsk.core.HTMLEventHandler): #По нажатию кнопки проверяется нажатое и меняются параметры у сборки
    def __init__(self):
        super().__init__()
    def notify(self, args):
        global execution
        try:
            app = adsk.core.Application.get()
            ui  = app.userInterface
            design = app.activeProduct

            htmlArgs = adsk.core.HTMLEventArgs.cast(args)            
            data = json.loads(htmlArgs.data)
                
            #если был клик, то забираем аргументы и проверяем выбранное исполнение
            if data['action']=='click': 
                args = data['arguments']
                if args['execution'] == 'short': #если короткий и цилиндр
                    execution = '1'
                if args['execution'] == 'long': #если короткий и цилиндр
                    execution = '2'
                    ui.messageBox(args['key'] +' mm')

                      #  параметризация для полумуфты 1
                    DHC = 0
                    LHC = 0
                    l_1HC = 0
                    l_2HC = 0
                    d_2HC = 0 
                    d_1HC = 0
                    dHC = 0
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

                    dataHC = [('80 mm', '25 mm', '8 mm', '2 mm', '25 mm', '11 mm', '18 mm', '1000 mm', '2 mm', '12.8 mm', '8 mm', '9 mm', '55 mm', '1 mm', '0.5 mm', '1 mm', '0.2 mm'),
                              ('80 mm', '32 mm', '8 mm', '2 mm', '25 mm', '12 mm', '20 mm', '1000 mm', '2 mm', '13.8 mm', '8 mm', '9 mm', '55 mm', '1 mm', '0.5 mm', '1 mm', '0.2 mm'),
                              ('80 mm', '32 mm', '8 mm', '2 mm', '25 mm', '14 mm', '22 mm', '1000 mm', '2.5 mm', '16.3 mm', '8 mm', '9 mm', '55 mm', '1 mm', '0.5 mm', '1 mm', '0.2 mm'),
                              ('80 mm', '42 mm', '8 mm', '2 mm', '25 mm', '16 mm', '25 mm', '1000 mm', '2.5 mm', '18.3 mm', '8 mm', '9 mm', '55 mm', '1 mm', '0.5 mm', '1 mm', '0.2 mm'),
                              ('80 mm', '42 mm', '8 mm', '2 mm', '25 mm', '18 mm', '28 mm', '1000 mm', '3 mm', '20.8 mm', '8 mm', '9 mm', '55 mm', '1 mm', '0.5 mm', '1 mm', '0.2 mm')]

                    keyParamHC = args['key'] +' mm'

                    for i in range(0, len(dataHC)):
                        if dataHC[i][5] == keyParamHC:
                            DHC = dataHC[i][0]
                            LHC = dataHC[i][1]
                            l_1HC = dataHC[i][2]
                            l_2HC = dataHC[i][3] 
                            d_2HC = dataHC[i][4]
                            d_1HC = dataHC[i][5]
                            dHC = dataHC[i][6]
                            ext_all_HC = dataHC[i][7]
                            BHC = dataHC[i][8]
                            H_HC = dataHC[i][9]
                            d_3HC = dataHC[i][10]
                            d_4HC = dataHC[i][11] 
                            D_2HC = dataHC[i][12]
                            b_1HC = dataHC[i][13]
                            b_2HC = dataHC[i][14]  
                            R_1HC = dataHC[i][15]
                            R_HC = dataHC[i][16]
                            break
        
                    DHCParam = design.userParameters.itemByName('DHC')
                    DHCParam.expression = DHC

                    LHCParam = design.userParameters.itemByName('LHC')
                    LHCParam.expression = LHC

                    l_1HCParam = design.userParameters.itemByName('l_1HC')
                    l_1HCParam.expression = l_1HC

                    l_2HCParam = design.userParameters.itemByName('l_2HC')
                    l_2HCParam.expression = l_2HC

                    d_1HCParam = design.userParameters.itemByName('d_1HC')
                    d_1HCParam.expression = d_1HC

                    dHCParam = design.userParameters.itemByName('dHC')
                    dHCParam.expression = dHC

                    d_2HCParam = design.userParameters.itemByName('d_2HC')
                    d_2HCParam.expression = d_2HC

                    extHCParam = design.userParameters.itemByName('ext_all_HC')
                    extHCParam.expression = ext_all_HC

                    BHCParam = design.userParameters.itemByName('B_HC')
                    BHCParam.expression = BHC

                    H_HCParam = design.userParameters.itemByName('H_HC')
                    H_HCParam.expression = H_HC

                    d_3HCParam = design.userParameters.itemByName('d_3HC')
                    d_3HCParam.expression = d_3HC

                    d_4HCParam = design.userParameters.itemByName('d_4HC')
                    d_4HCParam.expression = d_4HC

                    D_2HCParam = design.userParameters.itemByName('D_2HC')
                    D_2HCParam.expression = D_2HC

                    b_1HCParam = design.userParameters.itemByName('b_1HC')
                    b_1HCParam.expression = b_1HC

                    b_2HCParam = design.userParameters.itemByName('b_2HC')
                    b_2HCParam.expression = b_2HC

                    R_1HCParam = design.userParameters.itemByName('R_1HC')
                    R_1HCParam.expression = R_1HC

                    R_HCParam = design.userParameters.itemByName('R_HC')
                    R_HCParam.expression = R_HC 

            #  параметризация для полумуфты 2
                    DHC_1 = 0
                    LHC_1 = 0
                    l_1HC_1 = 0
                    l_2H_1 = 0
                    d_2HC_1 = 0 
                    d_1HC_1 = 0
                    dHC_1 = 0
                    ext_all_HC_1 = 0
                    B_HC_1 = 0
                    H_HC_1 = 0
                    d_3HC_1 = 0
                    d_4HC_1 = 0 
                    D_2HC_1 = 0
                    b_1HC_1 = 0
                    b_2HC_1 = 0
                    R_1HC_1 = 0
                    R_HC_1 = 0

                    dataHC2 = [('80 mm', '25 mm', '8 mm', '2 mm', '25 mm', '11 mm', '18 mm', '1000 mm', '2 mm', '12.8 mm', '8 mm', '9 mm', '55 mm', '1 mm', '0.5 mm', '1 mm', '0.2 mm'),
                               ('80 mm', '32 mm', '8 mm', '2 mm', '25 mm', '12 mm', '20 mm', '1000 mm', '2 mm', '13.8 mm', '8 mm', '9 mm', '55 mm', '1 mm', '0.5 mm', '1 mm', '0.2 mm'),
                               ('80 mm', '32 mm', '8 mm', '2 mm', '25 mm', '14 mm', '22 mm', '1000 mm', '2.5 mm', '16.3 mm', '8 mm', '9 mm', '55 mm', '1 mm', '0.5 mm', '1 mm', '0.2 mm'),
                               ('80 mm', '42 mm', '8 mm', '2 mm', '25 mm', '16 mm', '25 mm', '1000 mm', '2.5 mm', '18.3 mm', '8 mm', '9 mm', '55 mm', '1 mm', '0.5 mm', '1 mm', '0.2 mm'),
                               ('80 mm', '42 mm', '8 mm', '2 mm', '25 mm', '18 mm', '28 mm', '1000 mm', '3 mm', '20.8 mm', '8 mm', '9 mm', '55 mm', '1 mm', '0.5 mm', '1 mm', '0.2 mm')
                            ]

                    # keyParamHC2 = '11 mm'

                    for i in range(0, len(dataHC2)):
                        if dataHC2[i][5] == keyParamHC:
                            DHC_1 = dataHC2[i][0]
                            LHC_1 = dataHC2[i][1]
                            l_1HC_1 = dataHC2[i][2]
                            l_2HC_1 = dataHC2[i][3] 
                            d_2HC_1 = dataHC2[i][4]
                            d_1HC_1 = dataHC2[i][5]
                            dHC_1 = dataHC2[i][6]
                            ext_all_HC_1 = dataHC2[i][7]
                            BHC_1 = dataHC2[i][8]
                            H_HC_1 = dataHC2[i][9]
                            d_3HC_1 = dataHC2[i][10]
                            d_4HC_1 = dataHC2[i][11] 
                            D_2HC_1 = dataHC2[i][12]
                            b_1HC_1 = dataHC2[i][13]
                            b_2HC_1 = dataHC2[i][14]  
                            R_1HC_1 = dataHC2[i][15]
                            R_HC_1 = dataHC2[i][16]
                            break
                    
                    DHCParam_1 = design.userParameters.itemByName('DHC_1')
                    DHCParam_1.expression = DHC_1

                    LHCParam_1 = design.userParameters.itemByName('LHC_1')
                    LHCParam_1.expression = LHC_1

                    l_1HCParam_1 = design.userParameters.itemByName('l_1HC_1')
                    l_1HCParam_1.expression = l_1HC_1

                    l_2HCParam_1 = design.userParameters.itemByName('l_2HC_1')
                    l_2HCParam_1.expression = l_2HC_1

                    d_1HCParam_1 = design.userParameters.itemByName('d_1HC_1')
                    d_1HCParam_1.expression = d_1HC_1

                    d_2HCParam_1 = design.userParameters.itemByName('d_2HC_1')
                    d_2HCParam_1.expression = d_2HC_1

                    dHCParam_1 = design.userParameters.itemByName('dHC_1')
                    dHCParam_1.expression = dHC_1

                    extHCParam_1 = design.userParameters.itemByName('ext_all_HC_1')
                    extHCParam_1.expression = ext_all_HC_1

                    BHCParam_1 = design.userParameters.itemByName('B_HC_1')
                    BHCParam_1.expression = BHC_1

                    H_HCParam_1 = design.userParameters.itemByName('H_HC_1')
                    H_HCParam_1.expression = H_HC_1

                    d_3HCParam_1 = design.userParameters.itemByName('d_3HC_1')
                    d_3HCParam_1.expression = d_3HC_1

                    d_4HCParam_1 = design.userParameters.itemByName('d_4HC_1')
                    d_4HCParam.expression = d_4HC_1

                    D_2HCParam_1 = design.userParameters.itemByName('D_2HC_1')
                    D_2HCParam_1.expression = D_2HC_1

                    b_1HCParam_1 = design.userParameters.itemByName('b_1HC_1')
                    b_1HCParam_1.expression = b_1HC_1

                    b_2HCParam_1 = design.userParameters.itemByName('b_2HC_1')
                    b_2HCParam_1.expression = b_2HC_1

                    R_1HCParam_1 = design.userParameters.itemByName('R_1HC_1')
                    R_1HCParam.expression = R_1HC_1

                    R_HCParam_1 = design.userParameters.itemByName('R_HC_1')
                    R_HCParam_1.expression = R_HC_1


                    # Параметризация болта ГОСТ 7817 
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

                    dataBolt = [('12 mm', '5 mm', '35 mm', '29.5 mm', '22.5 mm', '8 mm', '9 mm', '0.2 mm', '1 mm', '5.3 mm', '2 mm', '100 mm'),
                                ('14 mm', '6.5 mm', '35 mm', '29.5 mm', '22.5 mm', '9 mm', '10 mm', '0.2 mm', '1 mm', '5.3 mm', '2 mm', '100 mm')] 

                    keyParamBolt = d_4HC

                    for i in range(0, len(dataBolt)):
                        if dataBolt[i][5] == keyParamBolt:
                            S_bolt = dataBolt[i][0]
                            m_bolt = dataBolt[i][1]
                            L_bolt = dataBolt[i][2]
                            l1_bolt = dataBolt[i][3]
                            l2_bolt = dataBolt[i][4]
                            d_bolt = dataBolt[i][5]
                            d1_bolt = dataBolt[i][6]
                            R_bolt = dataBolt[i][7]
                            l3_bolt = dataBolt[i][8]
                            d3_bolt = dataBolt[i][9]
                            d4_bolt= dataBolt[i][10]
                            ext_all_bolt = dataBolt[i][11]
                            break

                    S_boltParam = design.userParameters.itemByName('S_bolt')
                    S_boltParam.expression = S_bolt

                    m_BoltParam = design.userParameters.itemByName('m_bolt')
                    m_BoltParam.expression = m_bolt

                    LBoltParam = design.userParameters.itemByName('L_bolt')
                    LBoltParam.expression = L_bolt

                    l_1BoltParam = design.userParameters.itemByName('l1_bolt')
                    l_1BoltParam.expression = l1_bolt

                    l_2BoltParam = design.userParameters.itemByName('l2_bolt')
                    l_2BoltParam.expression = l2_bolt

                    dBoltParam = design.userParameters.itemByName('d_bolt')
                    dBoltParam.expression = d_bolt

                    d_1BoltParam = design.userParameters.itemByName('d1_bolt')
                    d_1BoltParam.expression = d1_bolt

                    R_BoltParam = design.userParameters.itemByName('R_bolt')
                    R_BoltParam.expression = R_bolt

                    l_3BoltParam = design.userParameters.itemByName('l3_bolt')
                    l_3BoltParam.expression = l3_bolt

                    d_3BoltParam = design.userParameters.itemByName('d3_bolt')
                    d_3BoltParam.expression = d3_bolt

                    d_4BoltParam = design.userParameters.itemByName('d4_bolt')
                    d_4BoltParam.expression = d4_bolt

                    ext_allBoltParam = design.userParameters.itemByName('ext_all_bolt')
                    ext_allBoltParam.expression = ext_all_bolt

                    # Параметризация для болта ГОСТ 7796
                    S_bolt2 = 0
                    d_bolt2 = 0
                    m_bolt2 = 0
                    D_bolt2 = 0
                    R_bolt = 0
                    l1_bolt2 = 0
                    b_bolt2 = 0
                    chm_bolt2 = 0
                    thr_bolt2 = 0

                    dataBolt2 = [('12 mm', '8 mm', '5 mm', '5.718 mm', '0.2 mm', '30 mm', '22 mm', '0.5 mm', '8 mm'),
                                ('14 mm', '10 mm', '6 mm', '6 mm', '0.2 mm', '30 mm', '22 mm', '0.5 mm', '10 mm'),
                                ('14 mm', '10 mm', '6 mm', '6 mm', '0.2 mm', '30 mm', '22 mm', '0.5 mm', '10 mm'),
                                ('17 mm', '12 mm', '7 mm', '8.1 mm', '0.2 mm', '30 mm', '22 mm', '0.5 mm', '12 mm'),
                                ('20 mm', '12 mm', '7 mm', '8.1 mm', '0.2 mm', '30 mm', '22 mm', '0.5 mm', '12 mm')
                                ]

                    keyParamBolt2 = d_3HC

                    for i in range(0, len(dataBolt2)):
                        if dataBolt2[i][1] == keyParamBolt2:
                            S_bolt2 = dataBolt2[i][0]
                            d_bolt2 = dataBolt2[i][1]
                            m_bolt2 = dataBolt2[i][2]
                            D_bolt2 = dataBolt2[i][3]
                            R_bolt = dataBolt2[i][4]
                            l1_bolt2 = dataBolt2[i][5]
                            b_bolt2 = dataBolt2[i][6]
                            chm_bolt2 = dataBolt2[i][7]
                            thr_bolt2 = dataBolt2[i][8]
                            break
                    
                    S_bolt2Param = design.userParameters.itemByName('S_bolt2')
                    S_bolt2Param.expression = S_bolt2

                    dB2Param = design.userParameters.itemByName('d_bolt2')
                    dB2Param.expression = d_bolt2

                    m_B2Param = design.userParameters.itemByName('m_bolt2')
                    m_B2Param.expression = m_bolt2

                    D_B2Param = design.userParameters.itemByName('D_bolt2')
                    D_B2Param.expression = D_bolt2

                    R_Bolt2Param = design.userParameters.itemByName('R_bolt')
                    R_Bolt2Param.expression = R_bolt

                    l_1B2Param = design.userParameters.itemByName('l1_bolt2')
                    l_1B2Param.expression = l1_bolt2

                    bB2Param = design.userParameters.itemByName('b_bolt2')
                    bB2Param.expression = b_bolt2

                    chmB2Param = design.userParameters.itemByName('chm_bolt2')
                    chmB2Param.expression = chm_bolt2

                    thrB2Param = design.userParameters.itemByName('thr_bolt2')
                    thrB2Param.expression = thr_bolt2

            #         # Параметризация гайки 1

            #         S_nut = 0
            #         d_nut = 0
            #         k_nut = 0 
            #         ch_nut = 0 
                
            #         dataNut = [('12 mm', '8 mm', '6.5 mm', '0.5 mm'),
            #                    ('14 mm', '10 mm', '8 mm', '0.5 mm'),
            #                    ('17 mm', '12 mm', '10 mm', '0.5 mm'),
            #                    ('22 mm', '16 mm', '13 mm', '0.5 mm'),
            #                    ('27 mm', '20 mm', '16 mm', '0.5 mm'),
            #                    ('32 mm', '24 mm', '19 mm', '0.5 mm')]

            #         keyParamNut = d_bolt

            #         for i in range(0, len(dataNut)):
            #             if dataNut[i][1] == keyParamNut:
            #                 S_nut = dataNut[i][0]
            #                 d_nut = dataNut[i][1]
            #                 k_nut = dataNut[i][2]
            #                 ch_nut = dataNut[i][3]
            #                 break

            #         S_nutParam = design.userParameters.itemByName('S_nut')
            #         S_nutParam.expression = S_nut
                
            #         dNutParam = design.userParameters.itemByName('d_nut')
            #         dNutParam.expression = d_nut

            #         kNutParam = design.userParameters.itemByName('k_nut')
            #         kNutParam.expression = k_nut

            #         chNutParam = design.userParameters.itemByName('ch_nut')
            #         chNutParam.expression = ch_nut

            #         # Параметризация гайки 2
                    
            #         S_nut_1 = 0
            #         d_nut_1 = 0
            #         k_nut_1 = 0 
            #         ch_nut_1 = 0 
                
            #         dataNut_1 = [('12 mm', '8 mm', '6.5 mm', '0.5 mm'),
            #                      ('14 mm', '10 mm', '8 mm', '0.5 mm'),
            #                      ('17 mm', '12 mm', '10 mm', '0.5 mm'),
            #                      ('22 mm', '16 mm', '13 mm', '0.5 mm'),
            #                      ('27 mm', '20 mm', '16 mm', '0.5 mm'),
            #                      ('32 mm', '24 mm', '19 mm', '0.5 mm')]

            #         keyParamNut_1 = d_bolt2

            #         for i in range(0, len(dataNut)):
            #             if dataNut_1[i][1] == keyParamNut:
            #                 S_nut_1 = dataNut[i][0]
            #                 d_nut_1= dataNut[i][1]
            #                 k_nut_1 = dataNut[i][2]
            #                 ch_nut_1 = dataNut[i][3]
            #                 break

            #         S_nutParam_1 = design.userParameters.itemByName('S_nut')
            #         S_nutParam_1.expression = S_nut_1
                
            #         dNutParam_1 = design.userParameters.itemByName('d_nut_1')
            #         dNutParam_1.expression = d_nut_1

            #         kNutParam_1 = design.userParameters.itemByName('k_nut_1')
            #         kNutParam_1.expression = k_nut_1

            #         chNutParam_1 = design.userParameters.itemByName('ch_nut_1')
            #         chNutParam_1.expression = ch_nut_1

            #         # Параметризация шайбы 1 
            #         d = 0
            #         b = 0
            #         D = 0
            #         S_ = 0
            #         angle = 0
            #         ext_w = 0 

            #         dataWs = [('8 mm', '2 mm', '10.2 mm', '1.6 mm', '77.78', '1000 mm'),
            #                   ('10.2 mm', '2.5 mm', '12.7 mm', '2 mm', '77.78' '1000 mm')]

            #         keyParamWs = d_bolt

            #         for i in range(0, len(dataWs)):
            #             if dataWs[i][0] == keyParamWs:
            #                 d = dataWs[i][0]
            #                 b = dataWs[i][1]
            #                 D = dataWs[i][2]
            #                 S_ = dataWs[i][3]
            #                 angle = dataWs[i][4]
            #                 ext_w = dataWs[i][5]
            #                 break

            #         dParam = design.userParameters.itemByName('d')
            #         dParam.expression = d

            #         bParam = design.userParameters.itemByName('b')
            #         bParam.expression = b

            #         DParam = design.userParameters.itemByName('D')
            #         DParam.expression = D

            #         S_Param = design.userParameters.itemByName('S_')
            #         S_Param.expression = S_

            #         angleParam = design.userParameters.itemByName('angle')
            #         angleParam.expression = angle

            #         ext_WParam = design.userParameters.itemByName('ext_w')
            #         ext_WParam.expression = ext_w

            #         # Параметризация шайбы 2 

            #         d_1 = 0 
            #         b_1 = 0
            #         D_1 = 0
            #         S__1 = 0
            #         angle_1 = 0
            #         ext_w_1 = 0 

            #         dataWs2 = [('8 mm', '2 mm', '10.2 mm', '1.6 mm', '77.78', '1000 mm'),
            #                    ('10.2 mm', '2.5 mm', '12.7 mm', '2 mm', '77.78' '1000 mm')]

            #         keyParamWs2 = d_bolt2

            #         for i in range(0, len(dataWs2)):
            #             if dataWs2[i][0] == keyParamWs:
            #                 d_1 = dataWs[i][0]
            #                 b_1 = dataWs[i][1]
            #                 D_1 = dataWs[i][2]
            #                 S__1 = dataWs[i][3]
            #                 angle_1 = dataWs[i][4]
            #                 ext_w_1 = dataWs[i][5]
            #                 break

            #         dParam_1 = design.userParameters.itemByName('d_1')
            #         dParam_1.expression = d_1

            #         bParam_1 = design.userParameters.itemByName('b_1')
            #         bParam_1.expression = b_1

            #         DParam_1 = design.userParameters.itemByName('D_1')
            #         DParam_1.expression = D_1

            #         S_Param_1 = design.userParameters.itemByName('S__1')
            #         S_Param_1.expression = S__1

            #         angleParam_1 = design.userParameters.itemByName('angle_1')
            #         angleParam_1.expression = angle_1

            #         ext_WParam_1 = design.userParameters.itemByName('ext_w_1')
            #         ext_WParam_1.expression = ext_w_1


                # if args['shaftend'] == 'long' and args['shafthole'] == 'cylindrical': #если длинный и цилиндр
                #     execution = '2'
                # if args['shaftend'] == 'short' and args['shafthole'] == 'conical': #если короткий и конус
                #     execution = '3'
                # if args['shaftend'] == 'long' and args['shafthole'] == 'conical': #если длинный и конус
                #     execution = '4'

        except:
            if ui:
                ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

def stop(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface
        workSpace = ui.workspaces.itemById('FusionSolidEnvironment')
        tbPanels = workSpace.toolbarPanels
        tbPanel = tbPanels.itemById('NewPanel')
        if tbPanel:
            tbPanel.deleteMe()
        palette = ui.palettes.itemById('myExport')
        if palette:
            palette.deleteMe()

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
