set sh=CreateObject("Wscript.Shell")
sh.Run "python manage.py runserver", 0
WScript.Sleep 120000

set WshShell = WScript.CreateObject("WScript.Shell")
WshShell.Run "taskkill /IM python.exe", 0
WScript.Sleep 2000

set sh=CreateObject("Wscript.Shell")
sh.Run "python manage.py bot", 0
WScript.Sleep 10000

WScript.CreateObject("Wscript.Shell").Run "BackupJson.bat", 1, vbTrue