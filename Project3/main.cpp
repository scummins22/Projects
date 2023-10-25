//Seano Cummins spc230001

#include <iostream>
#include <string>
#include <fstream>
#include <sstream>
#include "BinTree.h"
#include "Node.h"

using namespace std;

void createBST(const string& filename, BinTree<DVD>&);
void processTransactions(const string& filename, BinTree<DVD>&);
void changeCopies(DVD &, int, bool);

int main()
{
    //prompt user for file names
    string inventoryFileName;
    string transactionFileName;
    cout << "Enter Inventory File Name: " << endl;
    cout << "Enter Transaction Log File Name: " << endl;
    getline(cin, inventoryFileName);
    getline(cin, transactionFileName);

    BinTree<DVD> tree;
    createBST(inventoryFileName, tree);
    processTransactions(transactionFileName, tree);
    tree.inorder();


    return 0;
}
void createBST(const string& filename, BinTree<DVD> &tree)
{
    ifstream input(filename);
    if(input.is_open())
    {
        while(!input.eof())
        {

            string line;
            getline(input, line);

            string title;
            int available, rented;

            istringstream iss(line);
            char delimiter = ',';

            getline(iss, title, delimiter);
            title = title.substr(1, title.length()-2);
            iss >> available;
            iss.ignore(1, delimiter);
            iss >> rented;

            DVD dvd(title, available, rented);

            tree.insert(dvd);
        }
        input.close();
    }
}
void processTransactions(const string& filename, BinTree<DVD>& tree)
{
    ifstream input(filename);
    if (input.is_open())
    {
        string line;
        string transactionType;
        string title;
        int quantity;

        while (getline(input, line))
        {
            istringstream iss(line);
            iss >> transactionType;
            iss.ignore(2); // Consume the opening double quote
            getline(iss, title, '"'); // Read until the closing double quote
            DVD dvdTemp(title, 0, 0);
            DVD* dvd = tree.search(dvdTemp);

            if (transactionType == "rent" || transactionType == "return")
            {
                // Search for the DVD in the tree
                if(dvd)
                {
                    if (transactionType == "rent")
                        changeCopies(*dvd, -1, true);
                    else
                        changeCopies(*dvd, 1, true);
                }

            }
            else if (transactionType == "add" || transactionType == "remove")
            {
                iss.ignore();
                iss >> quantity;

                // Search for the DVD in the tree
                if(dvd)
                {
                    if (transactionType == "add")
                        changeCopies(*dvd, quantity, false);
                    else
                        changeCopies(*dvd, -1*quantity, false);
                    if (dvd->getAvailable() == 0 && dvd->getRented() == 0)
                        tree.remove(*dvd);

                }
                else
                {
                    DVD* newDVD = new DVD(title, quantity, 0);
                    tree.insert(*newDVD);
                }
            }
        }
        input.close();
    }
}


void changeCopies(DVD &dvd, int numCopies, bool rented)
{

    if(rented)
    {
        if(numCopies!=1)
        {
            dvd.setAvailable(dvd.getAvailable()-1);
            dvd.setRented(dvd.getRented()+1);
        }
        else
        {
            dvd.setAvailable(dvd.getAvailable()+1);
            dvd.setRented(dvd.getRented()-1);
        }
    }
    else
    {
        dvd.setAvailable(dvd.getAvailable()+numCopies);
    }
}