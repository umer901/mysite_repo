#include <iostream>
#include <string>
#include <iomanip>
#include <cmath>
using namespace std;


void drop(int cart[], int id, int total_price, int product[],int answer[],int price[]);
void leave(int cart[], int price[], int product[], int answer[]);
void inventory(int cart[], int id, int total_price, int product[]);
void add(int cart[], int id, int total_price, int product[],int answer[],int price[]);

// for customer

// add function
void add(int cart[], int id, int total_price, int product[],int answer[],int price[])
{
    char check;
    int x;
    int quantity, new_quantity = 0, old_quantity = 0;

// of the
    {
        cout << "enter 0 to exit and 1 to continue shopping" << endl;
        cin >> x;
        if ((x != 0) && (x == 1))
        {
            cout << "ENTER  PRODUCT ID YOU WANT TO ADD FROM 0 to 19" << endl;
            cin >> id;
            cout << "enter the quantity of the product" << endl;
            cin >> quantity;
            // will work till the number the given ids

            cart[id] = cart[id] + quantity; // this would update the quantity (initially set as zero) in the array
            cout << "the quantity of the added product with ID " << id << "  is  " << cart[id] << endl;

            for (int j = 0; j < 20; j++) // to read the updated array for now
            {
                cout << cart[j] << "  ";
            }
            cout << endl;
        }
        else if (x == 0)
        {
            cout << "do you want to drop any product(y/n)" << endl;
            cin >> check;
            if (check == 'y')
            {
                drop(cart, id, total_price, product,answer,price);
            }
            else if (check == 'n')
            {
                inventory(cart, id, total_price, product);
            }
        }

        else
        {
            cout << "ERROR WRONG INPUT";
        }

    } while (x == 1);
}

// drop function
void drop(int cart[], int id, int total_price, int product[],int answer[],int price[])
{
    char check;
    char bill;
    int x;
    int quantity, new_quantity = 0, cart_quantity;

    do
    {
        cout << "enter 0 to exit and 1 to remove products" << endl;
        cin >> x;
        if ((x != 0) && (x == 1))
        {
            cout << "ENTER  PRODUCT ID YOU WANT TO DROP FROM 0 to 19" << endl;
            cin >> id;
            cout << "enter the quantity of the product you want to remove" << endl;
            cin >> quantity;
            // will work till the number the given ids

            cart[id] = cart[id] - quantity; // this would update the quantity (initially set as zero) in the array
            cout << "the quantity of the added product with ID " << id << " now is  " << cart[id] << endl;

            for (int j = 0; j < 20; j++) // to read the updated array for now
            {
                cout << cart[j] << "  ";
            }
            cout << endl;
        }
        else
        {
            cout << "Do you want your bill(y/n)" << endl;
            cin >> check;
            if (check == 'y')
            {
               leave(cart,price, product,answer);
                inventory(cart, id, total_price, product);
            }
            else
                cout << "wrong input" << endl;
        }

    } while (x == 1);
}

void leave(int cart[], int price[], int product[], int answer[])
{
    int quantity, total_price, product_price, id, size = 0;
    int sum = 0;

    for (int i = 0; i < 20; i++) // multipying the arrays to get a new product array

    {
        answer[i] = cart[i] * price[i];
    }

    for (int i = 0; i < 20; i++)
    {
        product[i] = answer[i];
    }

    for (int j = 0; j < 20; j++) // printing the array to see the product array for now
    {
        cout << product[j] << "  ";
    }
    cout << endl;

    for (int k = 0; k < 20; k++)
    {
        total_price = total_price + product[k];
    }
    cout << total_price;
}
void inventory(int cart[], int id, int total_price, int product[])
{

    cout << "__________" << endl;
    cout << "|id |   Quantity   |   ITEM NAME   |  Total(each)                         |" << endl;
    cout << " __________" << endl;
    // to print ids
    cout << "ids" << endl;
    for (int i = 0; i < 20; i++)
    {
        if (cart[i] != 0)
        {
            cout << i << endl;
        }
        else
            cout << "";
    }
    cout << "each quantity" << endl;
    // to print quantity
    for (int v = 0; v < 20; v++)
    {
        if (cart[v] != 0)
        {
            cout << cart[v] << endl;
        }
        else
            cout << "";
    }
    cout << "each price" << endl;
    // to print each price
    for (int m = 0; m < 20; m++)
    {
        if (product[m] != 0)
            cout << product[m] << endl;
        else
            cout << "";
    }
}

int main()

{
    int choice;
    char check;
    cout << "****************************" << endl;
    cout << "                      __________                           **" << endl;
    cout << "*                    | WELCOME TO TIMES SUPERMARKET |                          *" << endl;
    cout << "*                    | ---------------------------- |                          *" << endl;
    cout << "*                    |   A shop that has it all!!   |                          *" << endl;
    cout << "*                    |  ------------------------    |                          *" << endl;
    cout << "*                    |   Timings: 10 am to 2am      |                          *" << endl;
    cout << "*                    |   ---------------------      |                          *" << endl;
    cout << "*                    |__________|                          *" << endl;
    cout << "*                                                                              *" << endl;
    cout << "*                                                                              *" << endl;
    cout << "****************************" << endl;

    cout << "Are you a customer(y/n)" << endl;
    cin >> check;
    if (check == 'y')
    {

        int x, id;

        string milk, bread, eggs, jam, choclate, flour, cake, chips, biscuit, water, juice, sandwitch, icecream, coke, jelly;
        cout << "You can select from the following list" << endl;
        cout << "THE NUMBERS DENOTE THE IDS OF EACH PRODUCT" << endl;
        cout << "0-MILK" << endl;
        cout << "1-MEAT" << endl;
        cout << "2-BREAD" << endl;
        cout << "3-EGGS" << endl;
        cout << "4-JAM" << endl;
        cout << "5-CHOCLATE" << endl;
        cout << "6-FLOUR" << endl;
        cout << "7-CAKE" << endl;
        cout << "8-CHIPS" << endl;
        cout << "9-BISCUIT" << endl;
        cout << "10-WATER" << endl;
        cout << "11-JUICE" << endl;
        cout << "12-SANDWITCH" << endl;
        cout << "13-ICECREAM" << endl;
        cout << "14-COKE" << endl;
        cout << "15-CEREAL" << endl;
        cout << "16-CUPCAKE" << endl;
        cout << "17-REDBULL" << endl;
        cout << "18-NOODLES" << endl;
        cout << "19-SPICES" << endl;
        cout << "20-OIL" << endl;

        int answer[] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
        int total_price;
        int product[20] = {};

        int cart[] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0};                                 // initialising the quantity array to be zero for each product at start
        int price[] = {100, 1000, 12, 300, 40, 100, 2000, 50, 30, 40, 150, 100, 60, 70, 400, 50, 120, 60,40, 600}; // alllocated price of each product

        char operation; // to select the operation customer inputs

        add(cart, id, total_price, product,answer,price);
        for (int i; i < 20; i++)
        {
            cout << cart[i];
        }
        cout << "enter your choice of operation (A to Add),(D to Drop),(B for bill)" << endl;
        cin >> operation;
        switch (operation)
        {
        case 'A':
            add(cart, id, total_price, product);
            break;
        case 'D':
           drop(cart, id, total_price, product);
           break;
        case 'L':leave(cart,price,product,answer);
        break;
       case 'B':
           inventory(cart, id, total_price, product);
           break;

            inventory(cart,id,total_price);
        }
    }

    else if (check == 'n')
    {
    }
    else
        cout << "The given input is wrong" << endl;

    return 0;
}