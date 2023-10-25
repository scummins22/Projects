//Seano Cummins spc230001

#ifndef NODE_H
#define NODE_H
#include <iostream>
#include "DVD.h"

template <typename T>
class Node {
public:
    // Members
    Node* left;
    Node* right;
    T data;

    // Constructors
    Node() {left = nullptr; right = nullptr;};
    Node(const T &d) {left = nullptr; right = nullptr; data = d;}; // NOLINT(*-explicit-constructor)

    // data accessor
    T getData() const {return data;};
    Node* getLeft() const {return left;};
    Node* getRight() const {return right;};
    // data mutator
    void setData(const T& obj) {this->data = obj;};
    void setLeft(Node* node){left = node;};
    void setRight(Node* node){right = node;};

    friend std::ostream& operator<<(std::ostream& output, const Node& obj) {
        output << obj.data;
        return output;
    }
    // Overloaded comparison operators
    bool operator<(const Node& rhs) {return data < rhs.data;};
    bool operator>(const Node& rhs) {return data > rhs.data;};
};

#endif