#pragma once
#include <string>

/**
 * Program Interface
 * 
 * A program interface that defines a looping program
 */
class IProgram {
public:
    virtual bool Run() = 0;
};