#!/usr/bin/env python
# coding: utf-8
from logger import logger
import sys
import os
import commands
import json
import requests
from threading import Thread

__version__ = '0.2.1'
__author__ = 'Huang xiongbiao(billo@qq.com)'


def run_GUI():
    check_root()
    Thread(target=check_update, args=()).start()
    check_system()
    try:
        stat, terminalId = commands.getstatusoutput('xdotool getactivewindow')
        from GUI import TickeysApp
        if stat == 0:
            TickeysApp(terminalId).run()
        else:
            TickeysApp().run()

    except Exception, e:
        logger.info("Run GUI Fail, use CLI instead..Fail msg:%s" % str(e))
        run_CLI()


def run_CLI():
    check_root()
    Thread(target=check_update, args=()).start()
    check_system()
    from CLI import CLI
    CLI().cmdloop()


def check_root():
    logger.info("Root checking...")
    if os.getegid() != 0:
        logger.info("This program must be run as root..")
        sys.exit(0)
    logger.info("Root checking success. You have the root permission")
    logger.debug("File path:" + os.path.dirname(__file__))


def check_update():
    try:
        logger.info("Version checking...")
        r = requests.get("http://billbill.sinaapp.com/tickeys")
        returnInfor = json.loads(r.text)
        # print returnInfor
        if returnInfor["version"] <= __version__:
            logger.debug("Version checking success. It is the latest version...")
            return
        else:
            # show update notify
            import pynotify
            pynotify.init('Tickeys')
            title = '<h2>Tickeys</h2>'
            body = '<span style="color: #00B8CB; font-size:15px">Tickeys</span>有可用的<span style="color: #FF4500">更新：</span>\n 版本：%s \n 内容：%s' % (returnInfor["version"], returnInfor["update"])
            iconfile = os.getcwd() + '/tickeys.png'
            notify = pynotify.Notification(title, body, iconfile)
            notify.show()
    except Exception, e:
        logger.error("Version checking fail:" + str(e))


def check_system():
    systems = ['Linux', 'SunOS', 'FreeBSD', 'Unix', 'OpenBSD', 'NetBSD']
    try:
        logger.info("System checking...")
        import platform
        system_name = platform.system()
        if system_name not in systems:
            logger.error("System %s is not supported." % system_name)
            sys.exit(0)
        else:
            logger.info("System checking success. Your system is supported")
    except Exception, e:
        logger.error("System checking fail:" + str(e))
        sys.exit(0)


def print_help_msg():
    print "Tickeys will run GUI by default"
    print "Usage: -c     ---CLI mode"
    print "       -g     ---GUI mode"


def main():
    logger.debug("Tickeys start........")
    if len(sys.argv) == 1:
        run_GUI()
    elif len(sys.argv) == 2:
        if sys.argv[1] == '-g':
            del sys.argv[1]  # otherwise kivy would regard it as option
            run_GUI()
        elif sys.argv[1] == '-c':
            run_CLI()
        else:
            print_help_msg()
    else:
        print_help_msg()

if __name__ == '__main__':
    main()
