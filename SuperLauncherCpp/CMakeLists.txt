cmake_minimum_required(VERSION 3.16)
project(SuperLauncher VERSION 2.0.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)
set(CMAKE_AUTOUIC ON)

find_package(Qt6 REQUIRED COMPONENTS
    Core Widgets Gui Network Multimedia
)

set(SOURCES
    src/main.cpp

    # Core
    src/core/Constants.h
    src/core/AppConfig.cpp
    src/core/AppConfig.h
    src/core/Translations.cpp
    src/core/Translations.h
    src/core/PlatformSupport.cpp
    src/core/PlatformSupport.h
    src/core/Utils.h

    # Models
    src/models/Mod.h
    src/models/Modpack.h
    src/models/Server.h
    src/models/User.h
    src/models/Skin.h

    # Network
    src/network/ApiClient.cpp
    src/network/ApiClient.h
    src/network/ModrinthAPI.cpp
    src/network/ModrinthAPI.h
    src/network/CurseForgeAPI.cpp
    src/network/CurseForgeAPI.h

    # Backend
    src/backend/AccountSystem.cpp
    src/backend/AccountSystem.h
    src/backend/BuildsManager.cpp
    src/backend/BuildsManager.h
    src/backend/SkinsManager.cpp
    src/backend/SkinsManager.h
    src/backend/MinecraftLauncher.cpp
    src/backend/MinecraftLauncher.h
    src/backend/ModManager.cpp
    src/backend/ModManager.h
    src/backend/ServerManager.cpp
    src/backend/ServerManager.h
    src/backend/UpdateChecker.cpp
    src/backend/UpdateChecker.h
    src/backend/DiscordRPC.cpp
    src/backend/DiscordRPC.h

    # UI Widgets
    src/ui/widgets/GlassFrame.cpp
    src/ui/widgets/GlassFrame.h
    src/ui/widgets/AnimatedButton.cpp
    src/ui/widgets/AnimatedButton.h
    src/ui/widgets/GradientLabel.cpp
    src/ui/widgets/GradientLabel.h
    src/ui/widgets/SkinWidget.cpp
    src/ui/widgets/SkinWidget.h
    src/ui/widgets/ServerCardWidget.cpp
    src/ui/widgets/ServerCardWidget.h
    src/ui/ModernSidebar.cpp
    src/ui/ModernSidebar.h

    # UI Dialogs
    src/ui/dialogs/LoginDialog.cpp
    src/ui/dialogs/LoginDialog.h
    src/ui/dialogs/CreateServerDialog.cpp
    src/ui/dialogs/CreateServerDialog.h
    src/ui/dialogs/ServerControlDialog.cpp
    src/ui/dialogs/ServerControlDialog.h

    # UI Pages
    src/ui/pages/HomePage.cpp
    src/ui/pages/HomePage.h
    src/ui/pages/AccountPage.cpp
    src/ui/pages/AccountPage.h
    src/ui/pages/ModsPage.cpp
    src/ui/pages/ModsPage.h
    src/ui/pages/BuildsPage.cpp
    src/ui/pages/BuildsPage.h
    src/ui/pages/SkinsPage.cpp
    src/ui/pages/SkinsPage.h
    src/ui/pages/NewsPage.cpp
    src/ui/pages/NewsPage.h
    src/ui/pages/UpdatesPage.cpp
    src/ui/pages/UpdatesPage.h
    src/ui/pages/ServersPage.cpp
    src/ui/pages/ServersPage.h
    src/ui/pages/SettingsPage.cpp
    src/ui/pages/SettingsPage.h
    src/ui/pages/MinecraftPage.cpp
    src/ui/pages/MinecraftPage.h
    src/ui/pages/AIAgentPage.cpp
    src/ui/pages/AIAgentPage.h

    # MainWindow
    src/ui/MainWindow.cpp
    src/ui/MainWindow.h
)

set(RESOURCES
    resources/resources.qrc
)

add_executable(${PROJECT_NAME} ${SOURCES} ${RESOURCES})

target_include_directories(${PROJECT_NAME} PRIVATE
    ${CMAKE_CURRENT_SOURCE_DIR}
)

target_link_libraries(${PROJECT_NAME} PRIVATE
    Qt6::Core
    Qt6::Widgets
    Qt6::Gui
    Qt6::Network
    Qt6::Multimedia
)

if(WIN32)
    set_target_properties(${PROJECT_NAME} PROPERTIES
        WIN32_EXECUTABLE TRUE
    )
endif()
