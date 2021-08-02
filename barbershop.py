from threading import Thread
import threading
import time
import random
barber_wakeup = 1  # 1 means customer can wakeup barber , 0 means customers cannot wakeup barber
a= threading.Semaphore(0)
b= threading.Semaphore(0)
c= threading.Semaphore(2)  # for Mutual Exclusion
d= threading.Semaphore(2)  # for Mutual Exclusion

chair_total =int(input("enter the number of chairs" ))
chair_used  =int(input("enter the number of chair used" ))
barber_Chair=True

print("chair_Total",chair_total)
print("chair_Used",chair_used)
print("barber_chair",barber_Chair)
barber_sleep=0


def customer():
    global chair_used
    while chair_used<=chair_total:
        if(barber_Chair==True and chair_used<chair_total):
            chair_used+=1
            b.release()
            print("%s released lock"%(threading.current_thread().name))
            print("semaphore b value",b._value)
            time.sleep(5)
            print("chairs used",chair_used)
        elif (chair_used==chair_total and barber_Chair==True):
            c.release()
            print("%s released lock"%(threading.current_thread().name))
            print("semaphore c value",c._value)
            balk()
            d.release()
            print("%s released lock"%(threading.current_thread().name))
            print("semaphore d value",d._value)
            break
def cutHair():
    global barber_Chair
    if(barber_Chair==True):
        print("barbers chair is occupied")
    elif(barber_Chair==False):
        print("barbers chair is empty")

def gethairCut():
    global chair_used
    global barber_Chair
    a.acquire()
    print("%s released lock"%(threading.current_thread().name))
    print("semaphore a value",a._value)
    barber_Chair=True
    if(barber_Chair==True and chair_used==0):
        pass
    else:
        print("barbars chair s status")
    d.acquire()
    b.acquire()
    if (chair_used==0):
        pass
    else:
        chair_used-=1
    print("%s aquired lock"%(threading.current_thread().name))
    print("semaphore d value",d._value)
    print("semaphore bvalue",b._value)
    print("chair used",chair_used)
    customer()
def barber():
    if(chair_used!=0 and barber_Chair==False):
        barber_sleep=0
        cutHair()
    elif(barber_Chair==True):
        pass
    elif(barber_Chair==False and chair_used==0):
        barber_sleep=1
        print("barber has gone to sleep")
def balk():
    c.acquire()
    print("%s aquired lock"%(threading.current_thread().name))
    print("semaphore c value",c._value)
    if(chair_used==0):
        pass
    elif(chair_used==chair_total):
        time.sleep(1)
        print("unattended customer has left")


def main():
    t1=threading.Thread(target=customer)
    t2=threading.Thread(target=gethairCut)
    t3=threading.Thread(target=cutHair)
    t4=threading.Thread(target=barber)
    t5=threading.Thread(target=balk)
    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t5.start()
    t1.join()
    t2.join()
    t3.join()
    t4.join()
    t5.join()

    print("all threads done Exiting")
main()
