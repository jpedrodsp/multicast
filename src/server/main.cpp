#include "../common/Debugger.hpp"
#include "../common/ProgramController.hpp"
#include "ServerProgram.hpp"

int main(int argc, char const *argv[])
{
    Debugger::Get().Log("Starting server application.");
    ProgramController pc = ProgramController();
    ServerProgram sp = ServerProgram();
    pc.Run(sp);
    return 0;
}
