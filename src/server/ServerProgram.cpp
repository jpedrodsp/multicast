#include "ServerProgram.hpp"
#include <thread>
#include "../common/Debugger.hpp"
#include "../common/MulticastTransmitter.h"

ServerProgram::ServerProgram() {

}

bool ServerProgram::Run() {
    const auto sleepMsgTime = std::chrono::seconds(30);
    while (true)
    {
        Debugger::Get().Log("Server is running...");
        Debugger::Get().Log("Running Multicast listen test!");
        MulticastTransmitter::Test();
        std::this_thread::sleep_for(sleepMsgTime);
    }
    return true;
}