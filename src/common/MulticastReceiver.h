#pragma once
#include <functional>

class MulticastReceiver {
private:
    std::function<void(std::string& multicastText)> OnMulticastMessageReceived;
public:
    void Initialize();
    void Listen();
    void Close();
};
