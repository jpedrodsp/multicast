#include "Debugger.hpp"
#include "ProgramController.hpp"

bool ProgramController::Run(IProgram& program) {
    return program.Run();
}