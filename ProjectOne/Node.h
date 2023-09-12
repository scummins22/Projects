//Seano Cummins spc230001

#ifndef NODE_H
#define NODE_H
#include "Seat.h"

class Node
{
protected:
    Node *nextPtr;
    Node *downPtr;
    Seat seat;
public:
    Node();
    Node(Node *, Node *, Seat);

    Node getNext() const {return *nextPtr;}
    Node getDown() const {return *downPtr;}
    Seat getSeat() const {return seat;}
};
#endif //NODE_H
