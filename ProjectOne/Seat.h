//Seano Cummins spc230001

//header guard
#ifndef SEAT_H
#define SEAT_H

class Seat
{
//protected member variables
protected:
    int row;
    char seat;
    char ticketType;

public:
    //constructors
    Seat();
    Seat(int, char, char);

    // accessors
    int getRow() const {return row;}
    char getSeat() const {return seat;}
    char getTicketType() const {return ticketType;}

    //mutators
    void setRow(int r) {row = r;}
    void setSeat(char s){seat = s;}
    void setTicketType(char t){ticketType = t;}
};

#endif //SEAT_H
