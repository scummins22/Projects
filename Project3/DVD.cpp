//Seano Cummins spc230001

#include "DVD.h"
#include <iostream>
#include <iomanip>

DVD::DVD()
{
    title = "";
    available = 0;
    rented = 0;
}

DVD::DVD(std::string t, int a, int r)
{
    title = t;
    available = a;
    rented = r;
}

std::ostream& operator<<(std::ostream &output, const DVD &obj)
{
    output << std::left << std::setw(35) << obj.title
           << std::setw(10) << obj.available
           << std::setw(10) << obj.rented;
    return output;
}
bool DVD::operator==(const DVD &obj) {
    return title == obj.title;
}
bool DVD::operator<(const DVD &obj) {
    return title < obj.title;
}

bool DVD::operator>(const DVD &obj) {
    return title > obj.title;
}