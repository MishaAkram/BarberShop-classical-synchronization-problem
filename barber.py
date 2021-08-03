from threading import Thread
import threading
import time
import random
barber_wakeup = 1  # 1 means customer can wakeup barber , 0 means customers cannot wakeup barber
customers_sem = threading.Semaphore(0)
barber_sem = threading.Semaphore(0)
mutex = threading.Semaphore(1)  # for Mutual Exclusion


class BarberShop:
    # Try to get access to the waiting room chairs or Enter in CS
    # if waiting room is not fulled then customer can sit on chair

    waiting_customers = []

    def __init__(self, barber, total_chairs):
        self.barber = barber
        self.total_chairs = total_chairs
        print("Total seats: ", total_chairs)

    def startBarberThread(self):
        t_barber = Thread(target=self.barber_working_in_barber_room)
        t_barber.start()

    def barber_shop_entry(self, customer):
        print("\nCustomer {} is entering in the shop and looking for empty seats" .format(customer))
        mutex.acquire()
        if len(self.waiting_customers) < self.total_chairs:
            print("\nCustomer {} founds an empty chair" .format(customer))
            self.waiting_customers.append(customer)
            global barber_wakeup
            while barber_wakeup:
                # barber gets a wakeup call by customer
                customers_sem.release()
                # 1st customer will come
                print("\nCustomer {} wakesup the barber" .format(customer))
                barber_wakeup = 0  # now no customer can wakeup the baber before barber goes to sleep
            print("Customer {} sits on waiting chair" .format(customer))
            mutex.release()  # customer after sitting on waiting seat is releasing the lock
            print("\nCustomer {} is waiting to be called by barber" .format(customer))
            barber_sem.acquire()
            Customer.get_hair_cut(self, customer)
            # customer is having haircut
            # if waiting room is full
            # As no seat is empty so leaving the CS
        else:
            mutex.release()
            Customer.balk(self, customer)

    def barber_working_in_barber_room(self):
        while True:
            # if there are no customer to be served in waiting room
            if len(self.waiting_customers) == 0:
                global barber_wakeup
                print("Barber is sleeping and waiting for customer to wake up")

                # now customer can wakeup barber
                barber_wakeup = 1
                customers_sem.acquire()
                # barber sleep if there is no customer
                # if customers are waiting in the room
                if len(self.waiting_customers) > 0:
                    mutex.acquire()
                    # Barber saw the customer so he locked the barber's chair (CS)
                    # Barber calls the customer
                    cust = self.waiting_customers[0]
                    print("\nBarber calls {} for haircut" .format(cust))
                    del self.waiting_customers[0]
                    barber_sem.release()  # barber is now ready to work
                    mutex.release()  # Barber unlock the barber's chair so customer can sit on the chair
                    self.barber.cut_hair(cust)  # (Cut hair here.)


class Barber:
    def cut_hair(self, customer):
        for i in range(0, 3):
            print("\nBarber is cutting hair of {}." .format(customer))
            time.sleep(2)
        print("\n{} is done so leaving barber shop" .format(customer))


class Customer:
    def __init__(self, name):
        self.name = name

    def get_hair_cut(self, customer):
        for i in range(0, 3):
            print("\nCutomer {} is having haircut" .format(customer))
            time.sleep(2)

    def balk(self, customer):
        print("\nWaiting Room is full. Customer {} leaves shop without hair cutting" .format(customer))
if __name__ == '__main__':
    customers_list = []
    barber = Barber()
    barberShop = BarberShop(barber,  2)  # 1 Seat
    barberShop.startBarberThread()          # 1 customers are entering
    customers_list.append(Customer('Misha Akram'))
    customers_list.append(Customer('Iqra Irfan'))
    customers_list.append(Customer('Firdous Riaz'))
    customers_list.append(Customer('Soniya Shafi'))
    while len(customers_list) > 0:
        c = customers_list.pop()
        # running customer threads here
        t = threading.Thread(target=barberShop.barber_shop_entry, args=(c.name,))
        # customers are entering in shop after random seconds from 1 to 5
        time.sleep(random.randint(1, 5))
        t.start()


