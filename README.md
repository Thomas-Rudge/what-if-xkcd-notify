# What-If XKCD Notification

Receive a [PushBullet](https://www.pushbullet.com) notification when a new [XKCD What-If](http://what-if.xkcd.com/) comic is available.


The script can be called from a batch file like the one below.

```batch
@ECHO OFF
@start pythonw.exe C:\PythonScripts\what-if.py Your_PushBullet_Access_Token
```

You can get your PushBullet access token [here.](https://www.pushbullet.com/#settings/account)