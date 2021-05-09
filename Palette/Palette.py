#Author-
#Description-

import adsk.core, adsk.fusion, adsk.cam, traceback
import urllib.request
import urllib.error
import urllib.parse
import pathlib
import json

handlers = [] #события все
app = adsk.core.Application.get()
ui  = app.userInterface

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
        tbPanel = tbPanels.add('NewPanel', 'Муфты', 'SelectPanel', False)

        cmdDef = ui.commandDefinitions.itemById('NewCommand')
        if cmdDef:
            cmdDef.deleteMe()

            
        cmdDef = ui.commandDefinitions.addButtonDefinition('NewCommand', 'Создать муфту', 'Ввод параметров для соединительных муфт','.//resource')
        tbPanel.controls.addCommand(cmdDef)

        ui.messageBox('Добавлена надстройка для соединительных муфт')

        #Событие по нажатию на надстройку
        sampleCommandCreated = SampleCommandCreatedEventHandler()
        cmdDef.commandCreated.add(sampleCommandCreated)
        handlers.append(sampleCommandCreated)

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))


class MyHTMLEventHandler(adsk.core.HTMLEventHandler): #По нажатию кнопки запускается
    def __init__(self):
        super().__init__()
    def notify(self, args):
        try:
            app = adsk.core.Application.get()
            ui  = app.userInterface

            htmlArgs = adsk.core.HTMLEventArgs.cast(args)            
            data = json.loads(htmlArgs.data)
                
            if data['action']=='click': #если был клик, то забираем аргументы
                args = data['arguments']
                ui.messageBox(args['shaftend'])

        except:
            if ui:
                ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))




class SampleCommandCreatedEventHandler(adsk.core.CommandCreatedEventHandler): #Обработчик событий для команды Создано событие.
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

            # url = "http://195.133.144.86:4200//Half-coupling1.f3d"
            url = "http://195.133.144.86:4200//AssemblyCoupling.f3d"

            doc = app.activeDocument
            if not doc.dataFile:
                ui.messageBox('Please save the document once.')
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


class SampleCommandExecuteHandler(adsk.core.CommandEventHandler): #Обработчик события для команды Выполненное событие.
    def __init__(self):
        super().__init__()
    def notify(self, args):
        try:
            app = adsk.core.Application.get()
            ui  = app.userInterface

            palette = ui.palettes.itemById('myExport')

            if not palette:
                palette = ui.palettes.add('myExport', 'Муфты', 'index.html', True, True, True, 600, 400)
                palette.dockingState = adsk.core.PaletteDockingStates.PaletteDockStateRight

                #должен быть запуск параметризации после нажатия на кнопку
                onHTMLEvent = MyHTMLEventHandler()
                palette.incomingFromHTML.add(onHTMLEvent)   
                handlers.append(onHTMLEvent)

            else: 
                palette.isVisible = True
        except:
            ui.messageBox('Command executed failed: {}'.format(traceback.format_exc()))

def stop(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface
        ui.messageBox('Надстройка удалена')
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
