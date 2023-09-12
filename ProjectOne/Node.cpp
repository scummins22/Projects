//Seano Cummins spc230001
#include "Node.h"

Node::Node()
{
    nextPtr = nullptr;
    downPtr = nullptr;
    seat;
}
Node::Node(Node *n, Node *d, Seat s)
{
    nextPtr = n;
    downPtr = d;
    seat = s;
}