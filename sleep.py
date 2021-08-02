import threading
import time

# Haircut start signal
ready = threading.Semaphore(0)
# Haircut end semaphore
finish = threading.Semaphore(0)
# Mutually exclusive semaphore
mutex = threading.Lock()
# Initial number of haircuts
wait_customer = 0
# Waiting chairs are mutually exclusive
wchair = threading.Lock()
# Barber chairs are mutually exclusive
barchair = threading.Lock()
# Number of chairs
#CHAIRS = 6
# serial number
counter = 0
# Waiting queue
wchair_list = []
#
in_cut = 0
def customer():
    # Customer Process
    global wait_customer, CHAIRS, mutex, wchair, finish, barchair, ready, counter, in_cut
    time.sleep(2)
    # Enter the critical area, modify the number of people waiting
    mutex.acquire()
    if wait_customer <= CHAIRS:
        wait_customer += 1
        counter += 1
        print('Customer {} is coming'.format(counter))
        wchair_list.append(counter)
        print('The current number of customers is:', wait_customer)
        print('The waiting queue is:', wchair_list)
        mutex.release()
        # Wait for the chair resource to be available
        wchair.acquire()
        # Waiting for haircut
        barchair.acquire()
        # You can have a haircut and release the waiting chair resources
        try:
            in_cut = wchair_list.pop(0)
        except:
            pass
        wchair.release()
        print('Customer {} sat in the barber chair'.format(in_cut))
        print('The remaining waiting queue is:', wchair_list)
        # Send a signal to the barber
        ready.release()
        # Waiting for haircut
        finish.acquire()
        # Release barber chair resources
        print('The customer{} left the barber chair and walked out of the store happily! '.format(in_cut))
        barchair.release()
        # Modify the number of customers
        mutex.acquire()
        wait_customer -= 1
        mutex.release()
    else:
        counter += 1
        print('Customer {} is coming'.format(counter))
        print('The waiting number is full, there are no seats, the customer {}leaves'.format(counter))
        mutex.release()


def barber():
    # Barber process
    print('The barber shop is open! ')
    print('--------------------------')
    global wait_customer, CHAIRS, mutex, ready, finish
    while True:
        if wait_customer == 0:
            print('No customers, sleep! ')
            time.sleep(1)
        # Waiting for the customer to make a request
        ready.acquire()
        cut_hair()
        # Haircut finished
        finish.release()

def cut_hair():
    print('The barber is getting a haircut! ')
    time.sleep(2)
    print('The haircut is over! ', end=' ')

if __name__=='__main__':
    CHAIRS = int(input('Please enter the number of chairs waiting for customers in the barber shop:'))
    t1 = threading.Thread(target=barber)
    t1.start()
    t1.join(1)
    while True:
        try:
            time.sleep(0.5)
            t2 = threading.Thread(target=customer)
            t2.start()
            t2.join(1)
        except:
            print('error! ')
