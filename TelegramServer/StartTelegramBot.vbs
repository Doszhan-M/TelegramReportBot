set sh=CreateObject("Wscript.Shell")
sh.Run "python manage.py runserver", 0
sh.Run "python manage.py bot", 0
sh.Run "python manage.py dumpdata --format=json > server > data_buckap.json", 0


