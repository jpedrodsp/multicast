#include "Debugger.hpp"

int main(int argc, char const *argv[])
{
    auto& d = Debugger::Get();
    d.Log("Starting application.");
    return 0;
}
