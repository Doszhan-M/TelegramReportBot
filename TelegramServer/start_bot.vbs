set WshShell = WScript.CreateObject("WScript.Shell")
WshShell.Run "taskkill /IM python.exe", 0
WScript.Sleep 2000

set sh=CreateObject("Wscript.Shell")
WScript.Sleep 1000
sh.Run "python manage.py bot", 0
WScript.Sleep 4000




