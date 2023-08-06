"""
firstRun
===============================================================================

This script is executed when the app runs for the first time.
"""
import os
import wx

theme = {
    "AUI_DOCKART_BACKGROUND_COLOUR": 0x5EBB00,
    "AUI_DOCKART_SASH_SIZE": 0x000004,
    "AUI_DOCKART_SASH_COLOUR": 0x204000,
    "AUI_DOCKART_CAPTION_SIZE": 0x000012,
    "AUI_DOCKART_INACTIVE_CAPTION_COLOUR": 0x295300,
    "AUI_DOCKART_INACTIVE_CAPTION_TEXT_COLOUR": 0xF9FFF2,
    "AUI_DOCKART_PANE_BORDER_SIZE": 0x000001,
    "AUI_DOCKART_PANE_BUTTON_SIZE": 0x00000E,
    "AUI_DOCKART_BORDER_COLOUR": 0x79DD00,
}

newScriptCode = """
import os
import wx

scriptName = wx.GetTextFromUser(
    "Enter name for new script", "Create New Script", "My New Script"
)
if scriptName:
    if not scriptName.endswith(".py"):
        scriptName += ".py"
    macroFolder = os.path.join(app.privateDataDir, "Macro")
    scriptPath = os.path.join(macroFolder, scriptName)
    if os.path.isfile(scriptPath):
        wx.LogError(f'Script "{scriptName}" already exists')
    else:
        with open(scriptPath, "w") as newScript:
            newScript.write("\\n# new workbench script\\n")
        app.TopWindow.scriptsMenu.rebuild()
        OpenDocument(scriptPath)
"""


def makeScripts():
    app = wx.GetApp()
    scriptsFolder = os.path.join(app.privateDataDir, "Macro")
    newScriptPath = os.path.join(scriptsFolder, "-- New Script --.py")
    if os.path.isfile(newScriptPath):
        return
    if not os.path.isdir(scriptsFolder):
        os.makedirs(scriptsFolder)
    with open(newScriptPath, "w", encoding="utf-8") as newScript:
        newScript.write(newScriptCode)


def setTheme():
    app = wx.GetApp()
    config = app.config
    config.SetPath("/Window/Panels/")
    for name, value in theme.items():
        config.WriteInt(name, value)

def setExternalTools():
    app = wx.GetApp()
    config = app.config
    config.SetPath("/Application/")
    externalTools = config.Read("ExternalTools")
    if externalTools:
        return
    config.Write("ExternalTools", "[{'name': 'FontTools Documentation', 'cmd': 'https://fonttools.readthedocs.io/en/latest/', 'folder': ''}]")


def main():
    setTheme()
    setExternalTools()
    makeScripts()


if __name__ == "__main__":
    main()
    del setTheme
    del setExternalTools
    del makeScripts
    del newScriptCode
    del theme
