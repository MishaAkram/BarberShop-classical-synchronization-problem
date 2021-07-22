#include <stdio.h>
#include <unistd.h>
#include <pthread.h>
#include <semaphore.h>

#define TRUE 1
#define FALSE 0

// Maximum number of chairs
#define MAX_CHAIR 5
// Maximum number of customers
#define MAX_CUSTOMERS 20

// define p, v operation
#define p(x) sem_wait(&x)
#define v(x) sem_post(&x)

// chair
int chair;
// Barber and customer semaphore
sem_t baber, customers;
// Mutually exclusive semaphore protection critical area (ie chair)
pthread_mutex_t chair_mutex;

// Initialize the number of chairs and semaphore
int init()
{
    chair = MAX_CHAIR;
    return (sem_init(&baber, 0, 1) || sem_init(&customers, 0, 0));
}

// Barber thread function
void* _baber(void *arg)
{
    printf("the baber shop opens...\n\n");
    while (TRUE)
    {
        p(customers); // try to serve a customer, otherwise sleep
        // printf("baber wake up...\n");
        pthread_mutex_lock(&chair_mutex);
        ++chair;    // A customer goes to get a haircut and vacates a chair
        printf("the baber is working on one...\nso the chair left : %d\n", chair);
        pthread_mutex_unlock(&chair_mutex);
        v(baber);   // The barber finished one
        printf("the baber has done one!\n");
        sleep(2);
    }
}

// Customer thread function
void* _customer(void *arg)
{
    int * id_p = (int *)arg;
    int id = *id_p;

    printf("customer #%d comes...\n", id);

    pthread_mutex_lock(&chair_mutex); // want a chair
    if(chair > 0) {   // There are empty chairs
        --chair;
        v(customers); // Add a new customer
        printf("the chair left : %d\n", chair);
        pthread_mutex_unlock(&chair_mutex);
        p(baber);     //Waiting for the barber
        printf("customer #%d is getting a hair cut...\n", id);
        sleep(1);
    }
    else
    {
        pthread_mutex_unlock(&chair_mutex); // release the lock
        printf("customer #%d left...\n", id);
    }
}

int main()
{
    if(init()) {
        printf("initialize semaphore error!\n");
        return 0;
    }

    pthread_t baber_tid;
    pthread_t customers_tid[MAX_CUSTOMERS];

    pthread_attr_t attr;
    pthread_attr_init(&attr);

    pthread_create(&baber_tid, &attr, _baber, NULL);

    for (int i = 0; i < MAX_CUSTOMERS; ++i) {
        pthread_create(&customers_tid[i], &attr, _customer, (void *)&i);
        sleep(1);
    }

    pthread_join(baber_tid, NULL);
    for (int i = 0; i < MAX_CUSTOMERS; ++i)
        pthread_join(customers_tid[i], NULL);

    return 0;
}