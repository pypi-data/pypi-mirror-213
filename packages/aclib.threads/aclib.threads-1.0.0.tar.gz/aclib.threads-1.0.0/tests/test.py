from aclib import threads
from aclib.winlib import winapi
from time import sleep
Thread = threads.Thread

print(Thread.main_thread())
# def func(a):
#     while True:
#         print('i am printing')
#         sleep(1)

# t = threads.Thread(func, (1,))
# print('创建了', t)
# print(t.ident, t.isrunning, t.time)

# sleep(1)
# t.start()
# print('启动')
# print(t.ident, t.isrunning, t.time)
# sleep(1)
# print(t.ident, t.isrunning, t.time)

# sleep(1.5)
# t.pause()
# print('暂停')
# print(t.ident, t.isrunning, t.time)
# sleep(1)
# print(t.ident, t.isrunning, t.time)

# sleep(5)
# t.resume()
# print('恢复')
# print(t.ident, t.isrunning, t.time)
# sleep(1)
# print(t.ident, t.isrunning, t.time)

# sleep(5)
# t.kill()
# print('杀死')
# print(t.ident, t.isrunning, t.time)
# sleep(1)
# print(t.ident, t.isrunning, t.time)

# print('join')
# t.join()
# print(t.ident, t.isrunning, t.time)
