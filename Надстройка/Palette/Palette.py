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
global num

def run(context):
    ui = None

    global num
    num = 0

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

            # url = "http://195.133.144.86:4200//CouplingAssembly.f3d"
            url = "http://195.133.144.86:4200//Couplingv2.f3d"

            doc = app.activeDocument
            if not doc.dataFile:
                ui.messageBox('Пожалуйста, закройте окно и сохраните документ!')
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
                palette = ui.palettes.add('myExport', 'БИБЛИОТЕКА МУФТ', 'index.html', True, True, True, 700, 500)
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
        global num 
        # global 
        try:
            app = adsk.core.Application.get()
            ui  = app.userInterface
            design = app.activeProduct

            htmlArgs = adsk.core.HTMLEventArgs.cast(args)            
            data = json.loads(htmlArgs.data)
            
            if data['action']=='clickOk':
                ui.messageBox('ok!')
                num += 1
                palette = ui.palettes.itemById('myExport')
                if palette :
                    palette.isVisible = False 

            #если был клик, то забираем аргументы и проверяем выбранное исполнение
            if data['action']=='click': 
                args = data['arguments']
                if args['execution'] == 'short': # для коротких концов валов
                    execution = '1'
                if args['execution'] == 'long': # для длинных концов валов
                    execution = '2'

                    #  параметризация для полумуфты 1
                    DHC, LHC, l1HC, l2HC, d2HC, d1HC, dHC, ext_all_HC, B_HC, H_HC, d3HC, d4HC, D2_HC, b1HC, b2HC, R1_HC, R_HC = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
                    dataHC = [# Мкр = 16.0
                              ('80 mm', '25 mm', '8 mm', '2 mm', '25 mm', '11 mm', '18 mm', '1000 mm', '2 mm', '12.8 mm', '8 mm', '9 mm', '55 mm', '1 mm', '0.5 mm', '1 mm', '0.2 mm'),
                              ('80 mm', '32 mm', '8 mm', '2 mm', '25 mm', '12 mm', '20 mm', '1000 mm', '2 mm', '13.8 mm', '8 mm', '9 mm', '55 mm', '1 mm', '0.5 mm', '1 mm', '0.2 mm'),
                              ('80 mm', '32 mm', '8 mm', '2 mm', '25 mm', '14 mm', '22 mm', '1000 mm', '2.5 mm', '16.3 mm', '8 mm', '9 mm', '55 mm', '1 mm', '0.5 mm', '1 mm', '0.2 mm'),
                              ('80 mm', '42 mm', '8 mm', '2 mm', '25 mm', '16 mm', '25 mm', '1000 mm', '2.5 mm', '18.3 mm', '8 mm', '9 mm', '55 mm', '1 mm', '0.5 mm', '1 mm', '0.2 mm'),
                              ('80 mm', '42 mm', '8 mm', '2 mm', '25 mm', '18 mm', '28 mm', '1000 mm', '3 mm', '20.8 mm', '8 mm', '9 mm', '55 mm', '1 mm', '0.5 mm', '1 mm', '0.2 mm'), 
                              # Мкр = 31.5
                              ('90 mm', '42 mm', '10 mm', '2 mm', '30 mm', '19 mm', '30 mm', '1000 mm', '3 mm', '21.8 mm', '8 mm', '9 mm', '60 mm', '1 mm', '0.5 mm', '1 mm', '0.2 mm'),
                              ('90 mm', '52 mm', '10 mm', '2 mm', '30 mm', '20 mm', '32 mm', '1000 mm', '3 mm', '22.8 mm', '8 mm', '9 mm', '60 mm', '1 mm', '0.5 mm', '1 mm', '0.2 mm'),
                              ('90 mm', '52 mm', '10 mm', '2 mm', '30 mm', '22 mm', '35 mm', '1000 mm', '3 mm', '24.8 mm', '8 mm', '9 mm', '60 mm', '1 mm', '0.5 mm', '1 mm', '0.2 mm'),
                              # Мкр = 63.0 
                              ('100 mm', '52 mm', '12 mm', '2 mm', '40 mm', '24 mm', '38 mm', '1000 mm', '4 mm', '27.3 mm', '8 mm', '9 mm', '70 mm', '1 mm', '0.5 mm', '1 mm', '0.2 mm'),
                              ('100 mm', '62 mm', '12 mm', '2 mm', '40 mm', '25 mm', '40 mm', '1000 mm', '4 mm', '28.3 mm', '8 mm', '9 mm', '70 mm', '1 mm', '0.5 mm', '1 mm', '0.2 mm'),
                              ('100 mm', '62 mm', '12 mm', '2 mm', '40 mm', '28 mm', '42 mm', '1000 mm', '4 mm', '31.3 mm', '8 mm', '9 mm', '70 mm', '1 mm', '0.5 mm', '1 mm', '0.2 mm'),
                              # Мкр = 125.0 
                              ('110 mm', '82 mm', '15 mm', '2 mm', '45 mm', '30 mm', '48 mm', '1000 mm', '4 mm', '33.8 mm', '10 mm', '11 mm', '80 mm', '1 mm', '0.5 mm', '1 mm', '0.2 mm'),
                              ('110 mm', '82 mm', '15 mm', '2 mm', '45 mm', '32 mm', '52 mm', '1000 mm', '5 mm', '35.8 mm', '10 mm', '11 mm', '80 mm', '1 mm', '0.5 mm', '1 mm', '0.4 mm'),
                              ('110 mm', '82 mm', '15 mm', '2 mm', '45 mm', '35 mm', '52 mm', '1000 mm', '5 mm', '38.8 mm', '10 mm', '11 mm', '80 mm', '1 mm', '0.5 mm', '1 mm', '0.4 mm'),
                              ('110 mm', '82 mm', '15 mm', '2 mm', '45 mm', '36 mm', '52 mm', '1000 mm', '5 mm', '39.8 mm', '10 mm', '11 mm', '80 mm', '1 mm', '0.5 mm', '1 mm', '0.4 mm'),
                              # Мкр = 160.0
                              ('120 mm', '82 mm', '16 mm', '2 mm', '50 mm', '38 mm', '56 mm', '1000 mm', '5 mm', '41.8 mm', '10 mm', '11 mm', '90 mm', '1 mm', '0.5 mm', '1 mm', '0.4 mm'),
                              # Мкр = 250.0 
                              ('130 mm', '112 mm', '17 mm', '2 mm', '55 mm', '40 mm', '65 mm', '1000 mm', '5 mm', '44.4 mm', '10 mm', '11 mm', '100 mm', '1 mm', '0.5 mm', '1 mm', '0.4 mm'),
                              ('130 mm', '112 mm', '17 mm', '2 mm', '55 mm', '42 mm', '65 mm', '1000 mm', '5 mm', '46.4 mm', '10 mm', '11 mm', '100 mm', '1 mm', '0.5 mm', '1 mm', '0.4 mm'),
                              ('130 mm', '112 mm', '17 mm', '2 mm', '55 mm', '45 mm', '70 mm', '1000 mm', '5 mm', '49.9 mm', '10 mm', '11 mm', '100 mm', '1 mm', '0.5 mm', '1 mm', '0.4 mm'),
                              # Мкр = 400.0
                              ('140 mm', '112 mm', '17 mm', '2 mm', '65 mm', '48 mm', '75 mm', '1000 mm', '7 mm', '52.9 mm', '10 mm', '11 mm', '110 mm', '1.6 mm', '1 mm', '1 mm', '0.4 mm'),
                              ('140 mm', '112 mm', '17 mm', '2 mm', '65 mm', '50 mm', '75 mm', '1000 mm', '7 mm', '54.9 mm', '10 mm', '11 mm', '110 mm', '1.6 mm', '1 mm', '1 mm', '0.4 mm')]

                    keyParamHC = args['key'] +' mm'
                    ui.messageBox('ПОДТВЕРДИТЬ ДЕЙСТВИЕ')

                    for i in range(0, len(dataHC)):
                        if dataHC[i][5] == keyParamHC:
                            DHC = dataHC[i][0]
                            LHC = dataHC[i][1]
                            l1HC = dataHC[i][2]
                            l2HC = dataHC[i][3] 
                            d2HC = dataHC[i][4]
                            d1HC = dataHC[i][5]
                            dHC = dataHC[i][6]
                            ext_all_HC = dataHC[i][7]
                            B_HC = dataHC[i][8]
                            H_HC = dataHC[i][9]
                            d3HC = dataHC[i][10]
                            d4HC = dataHC[i][11] 
                            D2_HC = dataHC[i][12]
                            b1HC = dataHC[i][13]
                            b2HC = dataHC[i][14]  
                            R1_HC = dataHC[i][15]
                            R_HC = dataHC[i][16]
                            break

                    if num == 0:
                        DHCParam = design.userParameters.itemByName('DHC')
                        DHCParam.expression = DHC
                        LHCParam = design.userParameters.itemByName('LHC')
                        LHCParam.expression = LHC
                        l_1HCParam = design.userParameters.itemByName('l1HC')
                        l_1HCParam.expression = l1HC
                        l_2HCParam = design.userParameters.itemByName('l2HC')
                        l_2HCParam.expression = l2HC
                        d_1HCParam = design.userParameters.itemByName('d1HC')
                        d_1HCParam.expression = d1HC
                        dHCParam = design.userParameters.itemByName('dHC')
                        dHCParam.expression = dHC
                        d_2HCParam = design.userParameters.itemByName('d2HC')
                        d_2HCParam.expression = d2HC
                        extHCParam = design.userParameters.itemByName('ext_all_HC')
                        extHCParam.expression = ext_all_HC
                        BHCParam = design.userParameters.itemByName('B_HC')
                        BHCParam.expression = B_HC
                        H_HCParam = design.userParameters.itemByName('H_HC')
                        H_HCParam.expression = H_HC
                        d_3HCParam = design.userParameters.itemByName('d3HC')
                        d_3HCParam.expression = d3HC
                        d_4HCParam = design.userParameters.itemByName('d4HC')
                        d_4HCParam.expression = d4HC
                        D_2HCParam = design.userParameters.itemByName('D2_HC')
                        D_2HCParam.expression = D2_HC
                        b_1HCParam = design.userParameters.itemByName('b1HC')
                        b_1HCParam.expression = b1HC
                        b_2HCParam = design.userParameters.itemByName('b2HC')
                        b_2HCParam.expression = b2HC
                        R_1HCParam = design.userParameters.itemByName('R1_HC')
                        R_1HCParam.expression = R1_HC
                        R_HCParam = design.userParameters.itemByName('R_HC')
                        R_HCParam.expression = R_HC

                    elif num != 0:
                        DHCParam = design.userParameters.itemByName('DHC' + '_' + str(num))
                        DHCParam.expression = DHC
                        LHCParam = design.userParameters.itemByName('LHC' + '_' + str(num))
                        LHCParam.expression = LHC
                        l_1HCParam = design.userParameters.itemByName('l1HC' + '_' + str(num))
                        l_1HCParam.expression = l1HC
                        l_2HCParam = design.userParameters.itemByName('l2HC' + '_' + str(num))
                        l_2HCParam.expression = l2HC
                        d_1HCParam = design.userParameters.itemByName('d1HC' + '_' + str(num))
                        d_1HCParam.expression = d1HC
                        dHCParam = design.userParameters.itemByName('dHC' + '_' + str(num))
                        dHCParam.expression = dHC
                        d_2HCParam = design.userParameters.itemByName('d2HC' + '_' + str(num))
                        d_2HCParam.expression = d2HC
                        extHCParam = design.userParameters.itemByName('ext_all_HC' + '_' + str(num))
                        extHCParam.expression = ext_all_HC
                        BHCParam = design.userParameters.itemByName('B_HC' + '_' + str(num))
                        BHCParam.expression = B_HC
                        H_HCParam = design.userParameters.itemByName('H_HC' + '_' + str(num))
                        H_HCParam.expression = H_HC
                        d_3HCParam = design.userParameters.itemByName('d3HC' + '_' + str(num))
                        d_3HCParam.expression = d3HC
                        d_4HCParam = design.userParameters.itemByName('d4HC' + '_' + str(num))
                        d_4HCParam.expression = d4HC
                        D_2HCParam = design.userParameters.itemByName('D2_HC' + '_' + str(num))
                        D_2HCParam.expression = D2_HC
                        b_1HCParam = design.userParameters.itemByName('b1HC' + '_' + str(num))
                        b_1HCParam.expression = b1HC
                        b_2HCParam = design.userParameters.itemByName('b2HC' + '_' + str(num))
                        b_2HCParam.expression = b2HC
                        R_1HCParam = design.userParameters.itemByName('R1_HC' + '_' + str(num))
                        R_1HCParam.expression = R1_HC
                        R_HCParam = design.userParameters.itemByName('R_HC' + '_' + str(num))
                        R_HCParam.expression = R_HC

                 #  параметризация для полумуфты 1
                    DHC2, LHC2, l1_HC2, l2_HC2, d2_HC2, d1_HC2, dHC2, ext_all_HC2, B_HC2, H_HC2, d3HC2, d4HC2, D2_HC2, b1_HC2, b2_HC2, R1_HC2, R_HC2 = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
                    dataHC2 = [# Мкр = 16.0
                              ('80 mm', '25 mm', '8 mm', '2 mm', '25 mm', '11 mm', '18 mm', '1000 mm', '2 mm', '12.8 mm', '8 mm', '9 mm', '55 mm', '1 mm', '0.5 mm', '1 mm', '0.2 mm'),
                              ('80 mm', '32 mm', '8 mm', '2 mm', '25 mm', '12 mm', '20 mm', '1000 mm', '2 mm', '13.8 mm', '8 mm', '9 mm', '55 mm', '1 mm', '0.5 mm', '1 mm', '0.2 mm'),
                              ('80 mm', '32 mm', '8 mm', '2 mm', '25 mm', '14 mm', '22 mm', '1000 mm', '2.5 mm', '16.3 mm', '8 mm', '9 mm', '55 mm', '1 mm', '0.5 mm', '1 mm', '0.2 mm'),
                              ('80 mm', '42 mm', '8 mm', '2 mm', '25 mm', '16 mm', '25 mm', '1000 mm', '2.5 mm', '18.3 mm', '8 mm', '9 mm', '55 mm', '1 mm', '0.5 mm', '1 mm', '0.2 mm'),
                              ('80 mm', '42 mm', '8 mm', '2 mm', '25 mm', '18 mm', '28 mm', '1000 mm', '3 mm', '20.8 mm', '8 mm', '9 mm', '55 mm', '1 mm', '0.5 mm', '1 mm', '0.2 mm'), 
                              # Мкр = 31.5
                              ('90 mm', '42 mm', '10 mm', '2 mm', '30 mm', '19 mm', '30 mm', '1000 mm', '3 mm', '21.8 mm', '8 mm', '9 mm', '60 mm', '1 mm', '0.5 mm', '1 mm', '0.2 mm'),
                              ('90 mm', '52 mm', '10 mm', '2 mm', '30 mm', '20 mm', '32 mm', '1000 mm', '3 mm', '22.8 mm', '8 mm', '9 mm', '60 mm', '1 mm', '0.5 mm', '1 mm', '0.2 mm'),
                              ('90 mm', '52 mm', '10 mm', '2 mm', '30 mm', '22 mm', '35 mm', '1000 mm', '3 mm', '24.8 mm', '8 mm', '9 mm', '60 mm', '1 mm', '0.5 mm', '1 mm', '0.2 mm'),
                              # Мкр = 63.0 
                              ('100 mm', '52 mm', '12 mm', '2 mm', '40 mm', '24 mm', '38 mm', '1000 mm', '4 mm', '27.3 mm', '8 mm', '9 mm', '70 mm', '1 mm', '0.5 mm', '1 mm', '0.2 mm'),
                              ('100 mm', '62 mm', '12 mm', '2 mm', '40 mm', '25 mm', '40 mm', '1000 mm', '4 mm', '28.3 mm', '8 mm', '9 mm', '70 mm', '1 mm', '0.5 mm', '1 mm', '0.2 mm'),
                              ('100 mm', '62 mm', '12 mm', '2 mm', '40 mm', '28 mm', '42 mm', '1000 mm', '4 mm', '31.3 mm', '8 mm', '9 mm', '70 mm', '1 mm', '0.5 mm', '1 mm', '0.2 mm'),
                              # Мкр = 125.0 
                              ('110 mm', '82 mm', '15 mm', '2 mm', '45 mm', '30 mm', '48 mm', '1000 mm', '4 mm', '33.8 mm', '10 mm', '11 mm', '80 mm', '1 mm', '0.5 mm', '1 mm', '0.2 mm'),
                              ('110 mm', '82 mm', '15 mm', '2 mm', '45 mm', '32 mm', '52 mm', '1000 mm', '5 mm', '35.8 mm', '10 mm', '11 mm', '80 mm', '1 mm', '0.5 mm', '1 mm', '0.4 mm'),
                              ('110 mm', '82 mm', '15 mm', '2 mm', '45 mm', '35 mm', '52 mm', '1000 mm', '5 mm', '38.8 mm', '10 mm', '11 mm', '80 mm', '1 mm', '0.5 mm', '1 mm', '0.4 mm'),
                              ('110 mm', '82 mm', '15 mm', '2 mm', '45 mm', '36 mm', '52 mm', '1000 mm', '5 mm', '39.8 mm', '10 mm', '11 mm', '80 mm', '1 mm', '0.5 mm', '1 mm', '0.4 mm'),
                              # Мкр = 160.0
                              ('120 mm', '82 mm', '16 mm', '2 mm', '50 mm', '38 mm', '56 mm', '1000 mm', '5 mm', '41.8 mm', '10 mm', '11 mm', '90 mm', '1 mm', '0.5 mm', '1 mm', '0.4 mm'),
                              # Мкр = 250.0 
                              ('130 mm', '112 mm', '17 mm', '2 mm', '55 mm', '40 mm', '65 mm', '1000 mm', '5 mm', '44.4 mm', '10 mm', '11 mm', '100 mm', '1 mm', '0.5 mm', '1 mm', '0.4 mm'),
                              ('130 mm', '112 mm', '17 mm', '2 mm', '55 mm', '42 mm', '65 mm', '1000 mm', '5 mm', '46.4 mm', '10 mm', '11 mm', '100 mm', '1 mm', '0.5 mm', '1 mm', '0.4 mm'),
                              ('130 mm', '112 mm', '17 mm', '2 mm', '55 mm', '45 mm', '70 mm', '1000 mm', '5 mm', '49.9 mm', '10 mm', '11 mm', '100 mm', '1 mm', '0.5 mm', '1 mm', '0.4 mm'),
                              # Мкр = 400.0
                              ('140 mm', '112 mm', '17 mm', '2 mm', '65 mm', '48 mm', '75 mm', '1000 mm', '7 mm', '52.9 mm', '10 mm', '11 mm', '110 mm', '1.6 mm', '1 mm', '1 mm', '0.4 mm'),
                              ('140 mm', '112 mm', '17 mm', '2 mm', '65 mm', '50 mm', '75 mm', '1000 mm', '7 mm', '54.9 mm', '10 mm', '11 mm', '110 mm', '1.6 mm', '1 mm', '1 mm', '0.4 mm')]

                    # keyParamHC = args['key'] +' mm'
                    # ui.messageBox('ПОДТВЕРДИТЬ ДЕЙСТВИЕ')
                    for i in range(0, len(dataHC2)):
                        if dataHC2[i][5] == keyParamHC:
                            DHC2 = dataHC2[i][0]
                            LHC2 = dataHC2[i][1]
                            l1_HC2 = dataHC2[i][2]
                            l2_HC2 = dataHC2[i][3] 
                            d2_HC2 = dataHC2[i][4]
                            d1_HC2 = dataHC2[i][5]
                            dHC2 = dataHC2[i][6]
                            ext_all_HC2 = dataHC2[i][7]
                            B_HC2 = dataHC2[i][8]
                            H_HC2 = dataHC2[i][9]
                            d3HC2 = dataHC2[i][10]
                            d4HC2 = dataHC2[i][11] 
                            D2_HC2 = dataHC2[i][12]
                            b1_HC2 = dataHC2[i][13]
                            b2_HC2 = dataHC2[i][14]  
                            R1_HC2 = dataHC2[i][15]
                            R_HC2 = dataHC2[i][16]
                            break

                    if num == 0:
                        DHCParam2 = design.userParameters.itemByName('DHC2')
                        DHCParam2.expression = DHC2
                        LHCParam2 = design.userParameters.itemByName('LHC2')
                        LHCParam2.expression = LHC2
                        l_1HCParam2 = design.userParameters.itemByName('l1_HC2')
                        l_1HCParam2.expression = l1_HC2
                        l_2HCParam2 = design.userParameters.itemByName('l2_HC2')
                        l_2HCParam2.expression = l2_HC2
                        d_1HCParam2 = design.userParameters.itemByName('d1_HC2')
                        d_1HCParam2.expression = d1_HC2
                        dHCParam2 = design.userParameters.itemByName('dHC2')
                        dHCParam2.expression = dHC2
                        d_2HCParam2 = design.userParameters.itemByName('d2_HC2')
                        d_2HCParam2.expression = d2_HC2
                        extHCParam2 = design.userParameters.itemByName('ext_all_HC2')
                        extHCParam2.expression = ext_all_HC2
                        BHCParam2 = design.userParameters.itemByName('B_HC2')
                        BHCParam2.expression = B_HC2
                        H_HCParam2 = design.userParameters.itemByName('H_HC2')
                        H_HCParam2.expression = H_HC2
                        d_3HCParam2 = design.userParameters.itemByName('d3HC2')
                        d_3HCParam2.expression = d3HC2
                        d_4HCParam2 = design.userParameters.itemByName('d4HC2')
                        d_4HCParam2.expression = d4HC2
                        D_2HCParam2 = design.userParameters.itemByName('D2_HC2')
                        D_2HCParam2.expression = D2_HC2
                        b_1HCParam2 = design.userParameters.itemByName('b1_HC2')
                        b_1HCParam2.expression = b1_HC2
                        b_2HCParam2 = design.userParameters.itemByName('b2_HC2')
                        b_2HCParam2.expression = b2HC
                        R_1HCParam2 = design.userParameters.itemByName('R1_HC2')
                        R_1HCParam2.expression = R1_HC2
                        R_HCParam2 = design.userParameters.itemByName('R_HC2')
                        R_HCParam2.expression = R_HC2

                    elif num != 0:
                        DHCParam2 = design.userParameters.itemByName('DHC2' + '_' + str(num))
                        DHCParam2.expression = DHC2
                        LHCParam2 = design.userParameters.itemByName('LHC2' + '_' + str(num))
                        LHCParam2.expression = LHC2
                        l_1HCParam2 = design.userParameters.itemByName('l1_HC2' + '_' + str(num))
                        l_1HCParam2.expression = l1_HC2
                        l_2HCParam2 = design.userParameters.itemByName('l2_HC2' + '_' + str(num))
                        l_2HCParam2.expression = l2_HC2
                        d_1HCParam2 = design.userParameters.itemByName('d1_HC2' + '_' + str(num))
                        d_1HCParam2.expression = d1_HC2
                        dHCParam2 = design.userParameters.itemByName('dHC2' + '_' + str(num))
                        dHCParam2.expression = dHC2
                        d_2HCParam2 = design.userParameters.itemByName('d2_HC2' + '_' + str(num))
                        d_2HCParam2.expression = d2_HC2
                        extHCParam2 = design.userParameters.itemByName('ext_all_HC2' + '_' + str(num))
                        extHCParam2.expression = ext_all_HC2
                        BHCParam2 = design.userParameters.itemByName('B_HC2' + '_' + str(num))
                        BHCParam2.expression = B_HC2
                        H_HCParam2 = design.userParameters.itemByName('H_HC2' + '_' + str(num))
                        H_HCParam2.expression = H_HC2
                        d_3HCParam2 = design.userParameters.itemByName('d3HC2' + '_' + str(num))
                        d_3HCParam2.expression = d3HC2
                        d_4HCParam2 = design.userParameters.itemByName('d4HC2' + '_' + str(num))
                        d_4HCParam2.expression = d4HC2
                        D_2HCParam2 = design.userParameters.itemByName('D2_HC2' + '_' + str(num))
                        D_2HCParam2.expression = D2_HC2
                        b_1HCParam2 = design.userParameters.itemByName('b1_HC2' + '_' + str(num))
                        b_1HCParam2.expression = b1_HC2
                        b_2HCParam2 = design.userParameters.itemByName('b2_HC2' + '_' + str(num))
                        b_2HCParam2.expression = b2HC
                        R_1HCParam2 = design.userParameters.itemByName('R1_HC2' + '_' + str(num))
                        R_1HCParam2.expression = R1_HC2
                        R_HCParam2 = design.userParameters.itemByName('R_HC2' + '_' + str(num))
                        R_HCParam2.expression = R_HC2
     

                    # Параметризация болта ГОСТ 7817 
           
                    dataBolt78 = [('12 mm', '5.5 mm', '35 mm', '29.5 mm', '22.5 mm', '8 mm', '9 mm', '0.4 mm', '1 mm', '5.3 mm', '2 mm', '100 mm'),
                                  ('12 mm', '5.5 mm', '40 mm', '34 mm', '24.5 mm', '8 mm', '9 mm', '0.4 mm', '1 mm', '5.3 mm', '2 mm', '100 mm'),
                                  ('14 mm', '7 mm', '45 mm', '39.5 mm', '27 mm', '10 mm', '11 mm', '0.4 mm', '2.5 mm', '6.7 mm', '2.5 mm', '100 mm'),
                                  ('14 mm', '7 mm', '50 mm', '44.5 mm', '32 mm', '10 mm', '11 mm', '0.4 mm', '2.5 mm', '6.7 mm', '2.5 mm', '100 mm'),
                                  ('17 mm', '8 mm', '60 mm', '53 mm', '40 mm', '12 mm', '13 mm', '0.6 mm', '3.2 mm', '8.1 mm', '3.2 mm', '100 mm'),
                                  ('17 mm', '8 mm', '65 mm', '58 mm', '45 mm', '12 mm', '13 mm', '0.6 mm', '3.2 mm', '8.1 mm', '3.2 mm', '100 mm'),
                                  ('17 mm', '8 mm', '70 mm', '63 mm', '50 mm', '12 mm', '13 mm', '0.6 mm', '3.2 mm', '8.1 mm', '3.2 mm', '100 mm'),
                                  ('22 mm', '12 mm', '80 mm', '71 mm', '53 mm', '16 mm', '17 mm', '0.6 mm', '4 mm', '11.1 mm', '4 mm', '100 mm'), 
                                  ('27 mm', '13 mm', '90 mm', '80 mm', '60 mm', '20 mm', '21 mm', '0.8 mm', '4 mm', '13.8 mm', '4 mm', '100 mm'), 
                                  ('27 mm', '13 mm', '100 mm', '90 mm', '70 mm', '20 mm', '21 mm', '0.8 mm', '4 mm', '13.8 mm', '4 mm', '100 mm'), 
                                  ('32 mm', '15 mm', '110 mm', '99 mm', '67 mm', '24 mm', '25 mm', '0.8 mm', '5 mm', '16.6 mm', '5', '100 mm'), 
                                  ('32 mm', '15 mm', '120 mm', '109 mm', '77 mm', '24 mm', '25 mm', '0.8 mm', '5 mm', '16.6 mm', '5', '100 mm')]

                    keyParamBolt78 = d4HC

                    for i in range(0, len(dataBolt78)):
                        if dataBolt78[i][6] == keyParamBolt78:
                            S_bolt78 = dataBolt78[i][0]
                            m_bolt78 = dataBolt78[i][1]
                            L_bolt78 = dataBolt78[i][2]
                            l1_bolt78 = dataBolt78[i][3]
                            l2_bolt78 = dataBolt78[i][4]
                            d_bolt78 = dataBolt78[i][5]
                            d1_bolt78 = dataBolt78[i][6]
                            R_bolt78 = dataBolt78[i][7]
                            l3_bolt78 = dataBolt78[i][8]
                            d3_bolt78 = dataBolt78[i][9]
                            d4_bolt78 = dataBolt78[i][10]
                            ext_all_bolt = dataBolt78[i][11]
                            break
                    
                    if num == 0:
                        S_boltParam = design.userParameters.itemByName('S_bolt78')
                        S_boltParam.expression = S_bolt78
                        m_BoltParam = design.userParameters.itemByName('m_bolt78')
                        m_BoltParam.expression = m_bolt78
                        LBoltParam = design.userParameters.itemByName('L_bolt78')
                        LBoltParam.expression = L_bolt78
                        l_1BoltParam = design.userParameters.itemByName('l1_bolt78')
                        l_1BoltParam.expression = l1_bolt78
                        l_2BoltParam = design.userParameters.itemByName('l2_bolt78')
                        l_2BoltParam.expression = l2_bolt78
                        dBoltParam = design.userParameters.itemByName('d_bolt78')
                        dBoltParam.expression = d_bolt78
                        d_1BoltParam = design.userParameters.itemByName('d1_bolt78')
                        d_1BoltParam.expression = d1_bolt78
                        R_BoltParam = design.userParameters.itemByName('R_bolt78')
                        R_BoltParam.expression = R_bolt78
                        l_3BoltParam = design.userParameters.itemByName('l3_bolt78')
                        l_3BoltParam.expression = l3_bolt78
                        d_3BoltParam = design.userParameters.itemByName('d3_bolt78')
                        d_3BoltParam.expression = d3_bolt78
                        d_4BoltParam = design.userParameters.itemByName('d4_bolt78')
                        d_4BoltParam.expression = d4_bolt78
                        ext_allBoltParam = design.userParameters.itemByName('ext_all_bolt')
                        ext_allBoltParam.expression = ext_all_bolt
                    
                    elif num != 0: 
                        S_boltParam = design.userParameters.itemByName('S_bolt78' + '_' + str(num))
                        S_boltParam.expression = S_bolt78
                        m_BoltParam = design.userParameters.itemByName('m_bolt78' + '_' + str(num))
                        m_BoltParam.expression = m_bolt78
                        LBoltParam = design.userParameters.itemByName('L_bolt78' + '_' + str(num))
                        LBoltParam.expression = L_bolt78
                        l_1BoltParam = design.userParameters.itemByName('l1_bolt78' + '_' + str(num))
                        l_1BoltParam.expression = l1_bolt78
                        l_2BoltParam = design.userParameters.itemByName('l2_bolt78' + '_' + str(num))
                        l_2BoltParam.expression = l2_bolt78
                        dBoltParam = design.userParameters.itemByName('d_bolt78' + '_' + str(num))
                        dBoltParam.expression = d_bolt78
                        d_1BoltParam = design.userParameters.itemByName('d1_bolt78' + '_' + str(num))
                        d_1BoltParam.expression = d1_bolt78
                        R_BoltParam = design.userParameters.itemByName('R_bolt78' + '_' + str(num))
                        R_BoltParam.expression = R_bolt78
                        l_3BoltParam = design.userParameters.itemByName('l3_bolt78' + '_' + str(num))
                        l_3BoltParam.expression = l3_bolt78
                        d_3BoltParam = design.userParameters.itemByName('d3_bolt78' + '_' + str(num))
                        d_3BoltParam.expression = d3_bolt78
                        d_4BoltParam = design.userParameters.itemByName('d4_bolt78' + '_' + str(num))
                        d_4BoltParam.expression = d4_bolt78
                        ext_allBoltParam = design.userParameters.itemByName('ext_all_bolt' + '_' + str(num))
                        ext_allBoltParam.expression = ext_all_bolt

                  # Параметризация для болта ГОСТ 7796
                    S_bolt77 = 0
                    d_bolt77 = 0
                    m_bolt77 = 0
                    D_bolt77 = 0
                    # R_bolt77 = 0
                    l1_bolt77 = 0
                    b_bolt77 = 0
                    chm_bolt77 = 0
                    # thr_bolt2 = 0

                    dataBolt77 = [('12 mm', '8 mm', '5 mm', '5.718 mm', '30 mm', '22 mm', '0.8 mm'),
                                  ('12 mm', '8 mm', '5 mm', '5.718 mm', '0.1 mm', '35 mm', '22 mm', '0.8 mm'),
                                  ('12 mm', '8 mm', '5 mm', '5.718 mm', '0.1 mm', '40 mm', '22 mm', '0.8 mm'), 
                                  ('14 mm', '10 mm', '6 mm', '6.7 mm', '0.1 mm', '45 mm', '26 mm', '0.92 mm'),
                                  ('14 mm', '10 mm', '6 mm', '6.7 mm', '50 mm', '26 mm', '0.92 mm'),
                                  ('17 mm', '12 mm', '7 mm', '8.1 mm', '60 mm', '30 mm', '1 mm'),
                                  ('17 mm', '12 mm', '7 mm', '8.1 mm', '65 mm', '30 mm', '1 mm'),
                                  ('17 mm', '12 mm', '7 mm', '8.1 mm', '70 mm', '30 mm', '1 mm'),
                                  ('22 mm', '16 mm', '8 mm', '10.5 mm', '80 mm', '38 mm', '1.3 mm'),
                                  ('27 mm', '20 mm', '11 mm', '12.9 mm', '90 mm', '46 mm', '1.5 mm'),
                                  ('27 mm', '20 mm', '11 mm', '12.9 mm', '100 mm', '46 mm', '1.5 mm'),
                                  ('32 mm', '24 mm', '13 mm', '15.3 mm', '110 mm', '54 mm', '1.8 mm'),
                                  ('32 mm', '24 mm', '13 mm', '15.3 mm', '120 mm', '54 mm', '1.8 mm')]

                    keyParamBolt77 = d3HC

                    for i in range(0, len(dataBolt77)):
                        if dataBolt77[i][1] == keyParamBolt77:
                            S_bolt77 = dataBolt77[i][0]
                            d_bolt77 = dataBolt77[i][1]
                            m_bolt77 = dataBolt77[i][2]
                            D_bolt77 = dataBolt77[i][3]
                            # R_bolt77 = dataBolt77[i][4]
                            l1_bolt77 = dataBolt77[i][4]
                            b_bolt77 = dataBolt77[i][5]
                            chm_bolt77 = dataBolt77[i][6]
                            break

                    if num == 0:
                        S_bolt2Param = design.userParameters.itemByName('S_bolt77')
                        S_bolt2Param.expression = S_bolt77
                        dB2Param = design.userParameters.itemByName('d_bolt77')
                        dB2Param.expression = d_bolt77
                        m_B2Param = design.userParameters.itemByName('m_bolt77')
                        m_B2Param.expression = m_bolt77
                        D_B2Param = design.userParameters.itemByName('D_bolt77')
                        D_B2Param.expression = D_bolt77
                        # R_Bolt2Param = design.userParameters.itemByName('R_bolt77')
                        # R_Bolt2Param.expression = R_bolt77
                        l_1B2Param = design.userParameters.itemByName('l1_bolt77')
                        l_1B2Param.expression = l1_bolt77
                        bB2Param = design.userParameters.itemByName('b_bolt77')
                        bB2Param.expression = b_bolt77
                        chmB2Param = design.userParameters.itemByName('chm_bolt77')
                        chmB2Param.expression = chm_bolt77

                    if num != 0:
                        S_bolt2Param = design.userParameters.itemByName('S_bolt77' + '_' + str(num))
                        S_bolt2Param.expression = S_bolt77
                        dB2Param = design.userParameters.itemByName('d_bolt77' + '_' + str(num))
                        dB2Param.expression = d_bolt77
                        m_B2Param = design.userParameters.itemByName('m_bolt77' + '_' + str(num))
                        m_B2Param.expression = m_bolt77
                        D_B2Param = design.userParameters.itemByName('D_bolt77' + '_' + str(num))
                        D_B2Param.expression = D_bolt77
                        # R_Bolt2Param = design.userParameters.itemByName('R_bolt77' + '_' + str(num))
                        # R_Bolt2Param.expression = R_bolt77
                        l_1B2Param = design.userParameters.itemByName('l1_bolt77' + '_' + str(num))
                        l_1B2Param.expression = l1_bolt77
                        bB2Param = design.userParameters.itemByName('b_bolt77' + '_' + str(num))
                        bB2Param.expression = b_bolt77
                        chmB2Param = design.userParameters.itemByName('chm_bolt77' + '_' + str(num))
                        chmB2Param.expression = chm_bolt77
                        
                    # Параметризация гайки 1

                    S_nut = 0
                    d_nut = 0
                    k_nut = 0 
                    ch_nut = 0 
                
                    dataNut = [('12 mm', '8 mm', '6.5 mm', '0.4 mm'),
                               ('14 mm', '10 mm', '8 mm', '0.5 mm'),
                               ('17 mm', '12 mm', '10 mm', '0.55 mm'),
                               ('22 mm', '16 mm', '13 mm', '0.625 mm'),
                               ('27 mm', '20 mm', '16 mm', '0.78 mm'),
                               ('32 mm', '24 mm', '19 mm', '0.94 mm')]

                    keyParamNut = d_bolt78

                    for i in range(0, len(dataNut)):
                        if dataNut[i][1] == keyParamNut:
                            S_nut = dataNut[i][0]
                            d_nut = dataNut[i][1]
                            k_nut = dataNut[i][2]
                            ch_nut = dataNut[i][3]
                            break

                    if num == 0:
                        S_nutParam = design.userParameters.itemByName('S_nut')
                        S_nutParam.expression = S_nut
                        dNutParam = design.userParameters.itemByName('d_nut')
                        dNutParam.expression = d_nut
                        kNutParam = design.userParameters.itemByName('k_nut')
                        kNutParam.expression = k_nut
                        chNutParam = design.userParameters.itemByName('ch_nut')
                        chNutParam.expression = ch_nut

                    elif num != 0:
                        S_nutParam = design.userParameters.itemByName('S_nut' + str(num))
                        S_nutParam.expression = S_nut
                        dNutParam = design.userParameters.itemByName('d_nut' + str(num))
                        dNutParam.expression = d_nut
                        kNutParam = design.userParameters.itemByName('k_nut' + str(num))
                        kNutParam.expression = k_nut
                        chNutParam = design.userParameters.itemByName('ch_nut' + str(num))
                        chNutParam.expression = ch_nut

                   # Параметризация гайки 2
                    
                    S_nut2 = 0
                    d_nut2 = 0
                    k_nut2 = 0 
                    ch_nut2 = 0 
                
                    dataNut2 = [('12 mm', '8 mm', '6.5 mm', '0.4 mm'),
                                 ('14 mm', '10 mm', '8 mm', '0.5 mm'),
                                 ('17 mm', '12 mm', '10 mm', '0.55 mm'),
                                 ('22 mm', '16 mm', '13 mm', '0.625 mm'),
                                 ('27 mm', '20 mm', '16 mm', '0.78 mm'),
                                 ('32 mm', '24 mm', '19 mm', '0.94 mm')]

                    keyParamNut2 = d_bolt77

                    for i in range(0, len(dataNut)):
                        if dataNut2[i][1] == keyParamNut2:
                            S_nut2 = dataNut2[i][0]
                            d_nut2 = dataNut2[i][1]
                            k_nut2 = dataNut2[i][2]
                            ch_nut2 = dataNut2[i][3]
                            break
                    if num == 0:
                        S_nutParam_1 = design.userParameters.itemByName('S_nut2')
                        S_nutParam_1.expression = S_nut2           
                        dNutParam_1 = design.userParameters.itemByName('d_nut2')
                        dNutParam_1.expression = d_nut2
                        kNutParam_1 = design.userParameters.itemByName('k_nut2')
                        kNutParam_1.expression = k_nut2
                        chNutParam_1 = design.userParameters.itemByName('ch_nut2')
                        chNutParam_1.expression = ch_nut2

                    elif num != 0:
                        S_nutParam_1 = design.userParameters.itemByName('S_nut2' + '_' + str(num))
                        S_nutParam_1.expression = S_nut2          
                        dNutParam_1 = design.userParameters.itemByName('d_nut2' + '_' + str(num))
                        dNutParam_1.expression = d_nut2
                        kNutParam_1 = design.userParameters.itemByName('k_nut2' + '_' + str(num))
                        kNutParam_1.expression = k_nut2
                        chNutParam_1 = design.userParameters.itemByName('ch_nut2' + '_' + str(num))
                        chNutParam_1.expression = ch_nut2

                     # Параметризация шайбы 1 
                    d_ws = 0
                    b_ws = 0
                    Dws = 0
                    Sws = 0
                    # angle_ws = 0
                    ext_ws = 0 

                    dataWs = [('8 mm', '2 mm', '10.2 mm', '1.6 mm', '100 mm'),
                              ('10 mm', '2.5 mm', '12.7 mm', '2 mm', '100 mm'),
                              ('12 mm', '3.5 mm', '15.7 mm', '2.5 mm', '100 mm'),
                              ('16 mm', '4.5 mm', '20.8 mm', '3.5 mm', '100 mm'),
                              ('20 mm', '5.5 mm','26 mm', '4.5 mm', '100 mm'),
                              ('24 mm','6.5 mm', '31 mm', '5.5 mm', '100 mm')]

                    keyParamWs = d_bolt77

                    for i in range(0, len(dataWs)):
                        if dataWs[i][0] == keyParamWs:
                            d_ws = dataWs[i][0]
                            b_ws = dataWs[i][1]
                            Dws = dataWs[i][2]
                            Sws = dataWs[i][3]
                            # angle_ws = dataWs[i][4]
                            ext_ws = dataWs[i][4]
                            break

                    if num == 0:
                        dParam = design.userParameters.itemByName('d_ws')
                        dParam.expression = d_ws
                        bParam = design.userParameters.itemByName('b_ws')
                        bParam.expression = b_ws
                        DParam = design.userParameters.itemByName('Dws')
                        DParam.expression = Dws
                        S_Param = design.userParameters.itemByName('Sws')
                        S_Param.expression = Sws
                        # angleParam = design.userParameters.itemByName('angle')
                        # angleParam.expression = angle_ws
                        ext_WParam = design.userParameters.itemByName('ext_ws')
                        ext_WParam.expression = ext_ws

                    elif num != 0:
                        dParam = design.userParameters.itemByName('d_ws' + '_' + str(num))
                        dParam.expression = d_ws
                        bParam = design.userParameters.itemByName('b_ws' + '_' + str(num))
                        bParam.expression = b_ws
                        DParam = design.userParameters.itemByName('Dws' + '_' + str(num))
                        DParam.expression = Dws
                        S_Param = design.userParameters.itemByName('Sws' + '_' + str(num))
                        S_Param.expression = Sws
                        # angleParam = design.userParameters.itemByName('angle' + '_' + str(num))
                        # angleParam.expression = angle_ws
                        ext_WParam = design.userParameters.itemByName('ext_ws' + '_' + str(num))
                        ext_WParam.expression = ext_ws                 

                    # Параметризация шайбы 2 
                    d_ws2 = 0
                    b_ws2 = 0
                    D_ws2 = 0
                    Sws2 = 0
                    # angle_ws2 = 0
                    ext_ws2 = 0 

                    dataWs2 = [('8 mm', '2 mm', '10.2 mm', '1.6 mm', '1000 mm'),
                              ('10 mm', '2.5 mm', '12.7 mm', '2 mm', '1000 mm'),
                              ('12 mm', '3.5 mm', '15.7 mm', '2.5 mm', '1000 mm'),
                              ('16 mm', '4.5 mm', '20.8 mm', '3.5 mm', '1000 mm'),
                              ('20 mm', '5.5 mm','26 mm', '4.5 mm', '1000 mm'),
                              ('24 mm','6.5 mm', '31 mm', '5.5 mm','1000 mm')]

                    keyParamWs2 = d_bolt78

                    for i in range(0, len(dataWs2)):
                        if dataWs2[i][0] == keyParamWs2:
                            d_ws2 = dataWs2[i][0]
                            b_ws2 = dataWs2[i][1]
                            D_ws2 = dataWs2[i][2]
                            Sws2 = dataWs2[i][3]
                            # angle_ws2 = dataWs2[i][4]
                            ext_ws2 = dataWs2[i][4]
                            break

                    if num == 0:
                        dParam = design.userParameters.itemByName('d_ws2')
                        dParam.expression = d_ws2
                        bParam = design.userParameters.itemByName('b_ws2')
                        bParam.expression = b_ws2
                        DParam = design.userParameters.itemByName('D_ws2')
                        DParam.expression = D_ws2
                        S_Param = design.userParameters.itemByName('Sws2')
                        S_Param.expression = Sws2
                        # angleParam = design.userParameters.itemByName('angle2')
                        # angleParam.expression = angle_ws2
                        ext_WParam = design.userParameters.itemByName('ext_ws')
                        ext_WParam.expression = ext_ws2

                    elif num != 0:
                        dParam = design.userParameters.itemByName('d_ws2' + '_' + str(num))
                        dParam.expression = d_ws2
                        bParam = design.userParameters.itemByName('b_ws2' + '_' + str(num))
                        bParam.expression = b_ws2
                        DParam = design.userParameters.itemByName('D_ws2' + '_' + str(num))
                        DParam.expression = D_ws2
                        S_Param = design.userParameters.itemByName('Sws2' + '_' + str(num))
                        S_Param.expression = Sws2
                        # angleParam = design.userParameters.itemByName('angle2' + '_' + str(num))
                        # angleParam.expression = angle_ws2
                        ext_WParam = design.userParameters.itemByName('ext_ws' + '_' + str(num))
                        ext_WParam.expression = ext_ws2    
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
