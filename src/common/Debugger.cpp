#include "Debugger.hpp"
#include <iostream>
#include <chrono>
#include <ctime>

// Global static pointer to ensure a single instance of the class
Debugger* Debugger::Instance = NULL;

// Class constructor
Debugger::Debugger() {
    Log("Instantiated a new debugger object.");
}

// Class destructor
Debugger::~Debugger() {
    Log("Destroying debugger object.");
}

/**
 * Gets singleton instance
 * 
 * @author jpedrodsp
*/
Debugger& Debugger::Get() {
   if (!Instance) {
       Instance = new Debugger();
   }
   return *Instance;
}

/**
 * Log function
 * 
 * @author jpedrodsp
 * @param text Text to log on screen
*/
void Debugger::Log(std::string text) {
    std::cout << "[" << GetTimeString() << "]" << text << std::endl;
}

/**
 * Get actual time function
 * 
 * Retrieves system time, format it and return as a string
 * 
 * @author jpedrodsp
*/
std::string Debugger::GetTimeString() {
    std::string timestring = "";
    auto system_time = std::chrono::system_clock::now();
    std::time_t time = std::chrono::system_clock::to_time_t(system_time);
    timestring = std::ctime(&time);
    //timestring[timestring.length() - 1] = '\0';
    timestring.resize(timestring.length() - 1);
    return timestring;
}