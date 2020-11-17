#pragma once
#include <string>

class Debugger {
private:
    static Debugger* Instance;
    Debugger();
    ~Debugger();
    std::string GetTimeString();
public:
    static Debugger& Get();
    void Log(std::string text);
};