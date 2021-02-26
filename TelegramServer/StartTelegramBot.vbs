set sh=CreateObject("Wscript.Shell")
sh.Run "python manage.py runserver", 0
sh.Run "python manage.py bot", 0
WScript.CreateObject("Wscript.Shell").Run "BuckupJson.bat", 1, vbTrue



