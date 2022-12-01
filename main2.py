from threading import Thread

from myChrome import MyChrome
from time import sleep

def mainChrome(proxie, sl, type_prx):
    mainDriver = MyChrome()
    driver, ua = mainDriver.OpenChrome(proxie, sl, type_prx)
    return driver, ua

def link(sl):
    driver, ua = mainChrome('45.152.201.100:8000:QTv2Q0:DGboqN', sl, 'user_pass')
    driver.get('https://m.facebook.com/')
    driver.refresh()
    sleep(10)
    driver.close()

    
luong = 2
while True:
    run = []
    for i in range(luong):
        run += [Thread(target=link, args=(i, ))]
    for x in run:
        x.start()
        sleep(0.2)
    for x in run:
        x.join()
