#include "../common/Debugger.hpp"

int main(int argc, char const *argv[])
{
    auto& d = Debugger::Get();
    d.Log("Starting server application.");
    return 0;
}
