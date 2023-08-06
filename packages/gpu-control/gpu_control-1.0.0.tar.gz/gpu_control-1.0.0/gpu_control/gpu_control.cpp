#include "gpu_control.h"
#include <iostream>

#ifdef _WIN32
    #include <windows.h>

    typedef int (*nvmlInitFunc)();
    typedef int (*nvmlShutdownFunc)();
    typedef int (*nvmlDeviceGetHandleByIndexFunc)(unsigned int, void**);
    typedef int (*nvmlDeviceGetTemperatureFunc)(void*, int, unsigned int*);
    typedef int (*nvmlDeviceSetFanSpeedFunc)(void*, unsigned int, unsigned int);
    typedef int (*nvmlDeviceGetFanSpeedFunc)(void*, unsigned int*);

    HMODULE nvmlLibrary = nullptr;

    template <typename T>
    T loadNvmlSymbol(const char* symbolName) {
        T symbol = reinterpret_cast<T>(GetProcAddress(nvmlLibrary, symbolName));
        if (!symbol) {
            std::cerr << "Failed to load symbol: " << symbolName << std::endl;
            FreeLibrary(nvmlLibrary);
            nvmlLibrary = nullptr;
        }
        return symbol;
    }

    void initializeNvmlLibrary() {
        if (!nvmlLibrary) {
            nvmlLibrary = LoadLibraryA("nvml.dll");  // Use LoadLibraryA for ANSI string
            if (!nvmlLibrary) {
                std::cerr << "Failed to load NVML library" << std::endl;
            }
        }
    }

    void releaseNvmlLibrary() {
        if (nvmlLibrary) {
            FreeLibrary(nvmlLibrary);
            nvmlLibrary = nullptr;
        }
    }
#else
    #include <nvml.h>

    typedef nvmlReturn_t (*nvmlInitFunc)();
    typedef nvmlReturn_t (*nvmlShutdownFunc)();
    typedef nvmlReturn_t (*nvmlDeviceGetHandleByIndexFunc)(unsigned int, nvmlDevice_t*);
    typedef nvmlReturn_t (*nvmlDeviceGetTemperatureFunc)(nvmlDevice_t, nvmlTemperatureSensors_t, unsigned int*);
    typedef nvmlReturn_t (*nvmlDeviceSetFanSpeedFunc)(nvmlDevice_t, unsigned int, unsigned int);
    typedef nvmlReturn_t (*nvmlDeviceGetFanSpeedFunc)(nvmlDevice_t, unsigned int*);

    void* nvmlLibrary = nullptr;

    template <typename T>
    T loadNvmlSymbol(const char* symbolName) {
        void* symbol = dlsym(nvmlLibrary, symbolName);
        if (!symbol) {
            std::cerr << "Failed to load symbol: " << symbolName << std::endl;
            dlclose(nvmlLibrary);
            nvmlLibrary = nullptr;
        }
        return reinterpret_cast<T>(symbol);
    }

    void initializeNvmlLibrary() {
        if (!nvmlLibrary) {
            nvmlLibrary = dlopen("libnvidia-ml.so.1", RTLD_LAZY);
            if (!nvmlLibrary) {
                std::cerr << "Failed to load NVML library: " << dlerror() << std::endl;
            }
        }
    }

    void releaseNvmlLibrary() {
        if (nvmlLibrary) {
            dlclose(nvmlLibrary);
            nvmlLibrary = nullptr;
        }
    }
#endif

typedef void* nvmlDevice_t;
#define NVML_TEMPERATURE_GPU 0
typedef int nvmlReturn_t;
#define NVML_SUCCESS 0

int get_temperature() {
    initializeNvmlLibrary();
    if (!nvmlLibrary) {
        std::cerr << "NVML library not loaded" << std::endl;
        return -1;
    }

    nvmlInitFunc nvmlInit = loadNvmlSymbol<nvmlInitFunc>("nvmlInit");
    nvmlShutdownFunc nvmlShutdown = loadNvmlSymbol<nvmlShutdownFunc>("nvmlShutdown");
    nvmlDeviceGetHandleByIndexFunc nvmlDeviceGetHandleByIndex =
        loadNvmlSymbol<nvmlDeviceGetHandleByIndexFunc>("nvmlDeviceGetHandleByIndex");
    nvmlDeviceGetTemperatureFunc nvmlDeviceGetTemperature =
        loadNvmlSymbol<nvmlDeviceGetTemperatureFunc>("nvmlDeviceGetTemperature");
    if (!nvmlInit || !nvmlShutdown || !nvmlDeviceGetHandleByIndex || !nvmlDeviceGetTemperature) {
        return -1;
    }

    nvmlInit();
    nvmlDevice_t device;
    nvmlDeviceGetHandleByIndex(0, &device);

    unsigned int temp;
    nvmlDeviceGetTemperature(device, NVML_TEMPERATURE_GPU, &temp);

    nvmlShutdown();

    return static_cast<int>(temp);
}

int set_fan_speed(unsigned int speed) {
    initializeNvmlLibrary();
    if (!nvmlLibrary) {
        std::cerr << "NVML library not loaded" << std::endl;
        return -1;
    }

    nvmlInitFunc nvmlInit = loadNvmlSymbol<nvmlInitFunc>("nvmlInit");
    nvmlShutdownFunc nvmlShutdown = loadNvmlSymbol<nvmlShutdownFunc>("nvmlShutdown");
    nvmlDeviceGetHandleByIndexFunc nvmlDeviceGetHandleByIndex =
        loadNvmlSymbol<nvmlDeviceGetHandleByIndexFunc>("nvmlDeviceGetHandleByIndex");
    nvmlDeviceSetFanSpeedFunc nvmlDeviceSetFanSpeed =
        loadNvmlSymbol<nvmlDeviceSetFanSpeedFunc>("nvmlDeviceSetFanSpeed_v2");
    if (!nvmlInit || !nvmlShutdown || !nvmlDeviceGetHandleByIndex || !nvmlDeviceSetFanSpeed) {
        return -1;
    }

    nvmlInit();
    nvmlDevice_t device;
    nvmlDeviceGetHandleByIndex(0, &device);

    nvmlReturn_t result = nvmlDeviceSetFanSpeed(device, 0, speed);

    if (result != NVML_SUCCESS) {
        std::cerr << "Failed to set fan speed: " << result << std::endl;
    }

    nvmlShutdown();

    return (result == NVML_SUCCESS) ? 0 : -1;
}

int get_fan_speed() {
    initializeNvmlLibrary();
    if (!nvmlLibrary) {
        std::cerr << "NVML library not loaded" << std::endl;
        return -1;
    }

    nvmlInitFunc nvmlInit = loadNvmlSymbol<nvmlInitFunc>("nvmlInit");
    nvmlShutdownFunc nvmlShutdown = loadNvmlSymbol<nvmlShutdownFunc>("nvmlShutdown");
    nvmlDeviceGetHandleByIndexFunc nvmlDeviceGetHandleByIndex =
        loadNvmlSymbol<nvmlDeviceGetHandleByIndexFunc>("nvmlDeviceGetHandleByIndex");
    nvmlDeviceGetFanSpeedFunc nvmlDeviceGetFanSpeed =
        loadNvmlSymbol<nvmlDeviceGetFanSpeedFunc>("nvmlDeviceGetFanSpeed");
    if (!nvmlInit || !nvmlShutdown || !nvmlDeviceGetHandleByIndex || !nvmlDeviceGetFanSpeed) {
        return -1;
    }

    nvmlInit();
    nvmlDevice_t device;
    nvmlDeviceGetHandleByIndex(0, &device);

    unsigned int speed;
    nvmlDeviceGetFanSpeed(device, &speed);

    nvmlShutdown();

    return static_cast<int>(speed);
}
