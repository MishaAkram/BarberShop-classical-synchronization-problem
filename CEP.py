from threading import Semaphore, Thread

n= 2
chairs= 2
semFree= Semaphore(0)
semWakeup= Semaphore(0)
semOnlyOne= Semaphore(1)

def getHairCut():

        print("Customer is getting a haircut")

def balk():

        print("A customer leaves due to non-empty chairs")

def barber():
    global chairs
    while True:
        if chairs==n:
            print("Barber is sleeping")
            semWakeup.acquire()
            print("Barber is awake")
        break

def customer():
    global chairs
    while True:
        if chairs!=0:
            chairs=chairs-1        #customer occupies a chair
            if chairs==n-1:
                print("The first customer is here")
                semWakeup.release()
            semOnlyOne.acquire()
            getHairCut()
            semOnlyOne.release()
            chairs=chairs+1

        else:
            balk()
        break

t2 = Thread(target = barber)
t2.start()
t1 = Thread(target = customer)
t1.start()
t0 = Thread(target = customer)
t0.start()
