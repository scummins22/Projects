//Seano Cummins spc230001

#ifndef BINTREE_H
#define BINTREE_H
#include "Node.h"

template <typename T>
class BinTree {
private:
    Node<T>* root;

    Node<T>* insertRecur(Node<T>* curNode, T& data) {
        if (!curNode)
            return new Node<T>(data);

        if (data < curNode->getData())
            curNode->setLeft(insertRecur(curNode->getLeft(), data));
        else
            curNode->setRight(insertRecur(curNode->getRight(), data));

        return curNode;
    }

    void inorderRecur(Node<T>* curNode) {
        if (curNode == nullptr)
            return;
        inorderRecur(curNode->getLeft());
        std::cout << *curNode << std::endl;
        inorderRecur(curNode->getRight());
    }

    T* searchRecur(Node<T>* curNode, T& data) {
        if (curNode == nullptr) {
            return nullptr; // Node not found
        }

        if (data == curNode->getData())
            return &(curNode->data); // Node found, return a pointer to its data

        if (data < curNode->getData()) {
            return searchRecur(curNode->getLeft(), data);
        } else {
            return searchRecur(curNode->getRight(), data);
        }
    }

    T* removeRecur(Node<T>* curNode,  T& data) {
        if (curNode == nullptr) {
            return nullptr; // Node not found
        }

        if (data < curNode->getData()) {
            return removeRecur(curNode->getLeft(), data);
        } else if (data > curNode->getData()) {
            return removeRecur(curNode->getRight(), data);
        } else {
            // Node found, handle different cases
            T* removedData = new T(curNode->getData());
            Node<T>* temp = curNode;

            if (curNode->getLeft() == nullptr && curNode->getRight() == nullptr) {
                curNode = nullptr;
            } else if (curNode->getLeft() == nullptr) {
                curNode = curNode->getRight();
            } else if (curNode->getRight() == nullptr) {
                curNode = curNode->getLeft();
            } else {
                Node<T>* successor = findMinNode(curNode->getRight());
                curNode->setData(successor->getData());
                removeRecur(curNode->getRight(), successor->getData());
            }

            delete temp;
            return removedData;
        }
    }

public:
    // Constructor
    BinTree() : root(nullptr) {}

    // Insert
    void insert(T& data) {
        root = insertRecur(root, data);
    }

    // Search
    T* search(T& data) {
        return searchRecur(root, data);
    }
    T* remove(T& data) {
        return removeRecur(root, data);
    }
    // Display the tree
    void inorder() {
        inorderRecur(root);
    }
};

#endif