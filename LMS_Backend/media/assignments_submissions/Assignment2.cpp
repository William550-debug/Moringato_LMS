#include <iostream>
#include <string>
using namespace std;

// Stack class definition
class Stack {
private:
    string* arr;     // Array to hold stack elements
    int top;         // Index of the top element
    int capacity;    // Maximum number of elements in the stack

public:
    // Constructor to initialize the stack
    Stack(int size) {
        arr = new string[size]; // Allocate memory for stack
        capacity = size;
        top = -1; // Initialize top to -1 indicating stack is empty
    }

    // Destructor to free allocated memory
    ~Stack() {
        delete[] arr; // Free the allocated memory
    }

    // Function to add an element to the stack
    void push(string value) {
        if (top == capacity - 1) { // Check if stack is full
            cout << "Stack overflow! Cannot push \"" << value << "\".\n";
            return;
        }
        arr[++top] = value; // Increment top and add the new value
        cout << "Pushed \"" << value << "\" onto the stack.\n";
    }

    // Function to remove the top element from the stack
    string pop() {
        if (isEmpty()) { // Check if stack is empty
            cout << "Stack underflow! Cannot pop from an empty stack.\n";
            return ""; // Return an empty string if stack is empty
        }
        return arr[top--]; // Return the top value and decrement top
    }

    // Function to return the top element without removing it
    string peek() {
        if (isEmpty()) { // Check if stack is empty
            cout << "Stack is empty! No top element.\n";
            return ""; // Return an empty string if stack is empty
        }
        return arr[top]; // Return the top value
    }

    // Function to check if the stack is empty
    bool isEmpty() {
        return top == -1; // Return true if top is -1
    }

    // Function to get the current size of the stack
    int size() {
        return top + 1; // Return the number of elements in the stack
    }
};

// Main program to test the stack operations
int main() {
    Stack stack(5); // Create a stack of capacity 5

    // Push strings onto the stack
    stack.push("Hello");
    stack.push("World");
    stack.push("C++");
    stack.push("Stack");
    stack.push("Implementation");

    // Attempt to push an additional string (should show overflow)
    stack.push("Extra"); 

    // Peek at the top element
    cout << "Top element: \"" << stack.peek() << "\"\n";

    // Pop elements from the stack
    cout << "Popped: \"" << stack.pop() << "\"\n";
    cout << "Popped: \"" << stack.pop() << "\"\n";

    // Show the current top element after popping
    cout << "Top element after popping: \"" << stack.peek() << "\"\n";

    // Pop remaining elements
    while (!stack.isEmpty()) {
        cout << "Popped: \"" << stack.pop() << "\"\n";
    }

    // Attempt to pop from an empty stack (should show underflow)
    stack.pop();

    return 0;
}