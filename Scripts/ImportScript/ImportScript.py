# Fusion360API Python script
import adsk.core, adsk.fusion, traceback

import urllib.request
import urllib.error
import urllib.parse
import pathlib

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface

        url = "http://195.133.144.86:4200//Half-coupling1.f3d"
        occ = importComponentFromURL(url)

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

# F3D File Only
def importComponentFromURL(url) -> adsk.fusion.Occurrence:
    app = adsk.core.Application.get()
    ui = app.userInterface

    # doc check
    doc :adsk.fusion.FusionDocument = app.activeDocument
    if not doc.dataFile:
        ui.messageBox('Please save the document once.')
        return adsk.fusion.Occurrence.cast(None)

    # get path
    folder = pathlib.Path(__file__).resolve().parent
    parsed = urllib.parse.urlparse(url)
    filename = parsed.path.split('//')[-1]
    dlFile = folder / filename

    # suffix check
    if dlFile.suffix != '.f3d':
        ui.messageBox('F3D File Only')
        return adsk.fusion.Occurrence.cast(None)

    # delete download file
    if dlFile.is_file():
        dlFile.unlink()

    # file download
    try:
        data = urllib.request.urlopen(url).read()
        with open(str(dlFile), mode="wb") as f:
            f.write(data)
    except:
        ui.messageBox(f'File not found in URL\n{url}')
        return adsk.fusion.Occurrence.cast(None)

    # import f3d
    app.executeTextCommand(f'Fusion.ImportComponent {str(dlFile)}')
    app.executeTextCommand(u'NuCommands.CommitCmd')

    # delete download file
    if dlFile.is_file():
        dlFile.unlink()

    des = adsk.fusion.Design.cast(app.activeProduct)
    comp = des.activeComponent
    return comp.occurrences[-1]