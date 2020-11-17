#pragma once
#include "../common/IProgram.hpp"

/**
 * Server Program
 */
class ServerProgram : public IProgram {
private:
public:
    ServerProgram();
    bool Run();
};