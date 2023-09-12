//Seano Cummins spc230001
#include "Seat.h"

Seat::Seat()
{
    row = 0;
    seat = 0;
    ticketType = 0;
}

Seat::Seat(int r, char s, char t)
{
    row = r;
    seat = s;
    ticketType = t;
}
