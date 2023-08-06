from aclib.inputs import Listener, Event

def cbk(e: Event):
    if e.action == e.KEYDOWN:
        print(e.key, e.KEYDOWN, e.stateof('ctrl'))
    if e.key == 'esc':
        print('停止')
        li.stop()
        print('停止')

li = Listener('w', 'esc', 'a', 's', 'd', 'ctrl', callback=cbk).listen()
import time 
time.sleep(5)
print(li._Listener__runningcallback)
li.loop()
