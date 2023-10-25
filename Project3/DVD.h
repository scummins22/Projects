//Seano Cummins spc230001

#ifndef DVD_H
#define DVD_H

#include <string>

class DVD
{
private:
//private member variables
    std::string title;
    int available;
    int rented;

public:
    //constructors
    DVD();
    DVD(std::string, int, int);

    //mutator methods to change private member variables
    void setTitle(std::string t){title = t;};
    void setAvailable(int a){available = a;};
    void setRented(int r){ rented = r;};

    //accessor methods to get private member variables
    std::string getTitle() const {return title;};
    int getAvailable() const {return available;};
    int getRented() const {return  rented;};

    //overloaded insertion operator
    friend std::ostream& operator<<(std::ostream&, const DVD&);

    //overloaded relational operator
    bool operator==(const DVD&);
    bool operator<(const DVD&);
    bool operator>(const DVD&);
};


#endif