#include "ServerProgram.hpp"
#include <thread>
#include "../common/Debugger.hpp"

ServerProgram::ServerProgram() {

}

bool ServerProgram::Run() {
    const auto sleepMsgTime = std::chrono::seconds(30);
    while (true)
    {
        std::this_thread::sleep_for(sleepMsgTime);
        Debugger::Get().Log("Server is running and sleeping...");
    }
    return true;
}