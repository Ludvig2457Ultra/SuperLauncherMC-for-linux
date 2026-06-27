#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
BUILD_DIR="$ROOT_DIR/build"
DIST_DIR="$ROOT_DIR/dist"
PYTHON_PKG_DIR="$ROOT_DIR/SuperLauncher"
CPP_DIR="$ROOT_DIR/SuperLauncherCpp"

print_step() { echo -e "\n\033[1;34m==>\033[0m \033[1m$1\033[0m"; }
print_ok()   { echo -e "  \033[1;32m[\xE2\x9C\x93]\033[0m $1"; }
print_skip() { echo -e "  \033[1;33m[\xe2\x86\x92]\033[0m $1"; }

detect_distro() {
    if [ -f /etc/os-release ]; then
        . /etc/os-release
        DISTRO_ID="$ID"
        DISTRO_LIKE="$ID_LIKE"
    elif command -v lsb_release &>/dev/null; then
        DISTRO_ID="$(lsb_release -si | tr '[:upper:]' '[:lower:]')"
    else
        DISTRO_ID="unknown"
    fi
    echo "$DISTRO_ID"
}

install_deps() {
    local distro
    distro=$(detect_distro)
    print_step "Installing dependencies for: $distro"

    case "$distro" in
        arch|manjaro|endeavouros)
            sudo pacman -S --noconfirm --needed \
                python python-pip python-pyqt6 python-requests \
                python-packaging python-pillow python-tqdm \
                qt6-base cmake gcc make
            pip install --user pypresence
            ;;
        ubuntu|debian|linuxmint|pop|elementary|zorin)
            sudo apt-get update -qq
            sudo apt-get install -y -qq \
                python3 python3-pip python3-pyqt6 python3-requests \
                python3-packaging python3-pil python3-tqdm \
                qt6-base-dev cmake g++ make
            pip install --user pypresence
            ;;
        fedora)
            sudo dnf install -y \
                python3 python3-pip python3-qt6 python3-requests \
                python3-packaging python3-pillow python3-tqdm \
                qt6-qtbase-devel cmake gcc-c++ make
            pip install --user pypresence
            ;;
        *)
            echo "Unsupported distro: $distro"
            echo "Please install manually: Python 3.10+, PyQt6, requests, Pillow, tqdm, packaging, pypresence"
            ;;
    esac
}

build_python_package() {
    print_step "Building Python package (SuperLauncher)"

    cd "$ROOT_DIR"

    if [ -d "$PYTHON_PKG_DIR" ]; then
        pip install --user -e "$ROOT_DIR"
        print_ok "Python package installed in editable mode"
    else
        print_skip "Python package directory not found, skipping"
    fi
}

build_cpp_component() {
    print_step "Building C++ component (SuperLauncherCpp)"

    if [ ! -d "$CPP_DIR" ]; then
        print_skip "C++ directory not found, skipping"
        return
    fi

    if [ ! -f "$CPP_DIR/CMakeLists.txt" ]; then
        print_skip "No CMakeLists.txt found, skipping"
        return
    fi

    mkdir -p "$CPP_DIR/build"
    cd "$CPP_DIR/build"

    cmake .. -DCMAKE_BUILD_TYPE=Release
    cmake --build . --parallel "$(nproc)"

    if [ -f "SuperLauncher" ]; then
        mkdir -p "$DIST_DIR"
        cp SuperLauncher "$DIST_DIR/"
        print_ok "C++ binary built: $DIST_DIR/SuperLauncher"
    fi
}

build_pyinstaller() {
    print_step "Building standalone executable with PyInstaller"

    cd "$ROOT_DIR"

    if [ ! -f "superlauncher.spec" ]; then
        print_skip "superlauncher.spec not found, skipping"
        return
    fi

    if command -v pyinstaller &>/dev/null; then
        pyinstaller --clean superlauncher.spec
        if [ -f "dist/superlauncher" ]; then
            print_ok "Standalone executable: dist/superlauncher"
        fi
    else
        echo "PyInstaller not installed. Install with: pip install pyinstaller"
        print_skip "Skipping PyInstaller build"
    fi
}

create_desktop_entry() {
    print_step "Creating .desktop entry"

    local app_id="superlauncher"
    local desktop_file="$HOME/.local/share/applications/${app_id}.desktop"

    mkdir -p "$HOME/.local/share/applications"
    mkdir -p "$HOME/.local/share/icons/hicolor/256x256/apps"

    cat > "$desktop_file" << EOF
[Desktop Entry]
Type=Application
Name=SuperLauncher
Comment=Minecraft launcher with mod support and server management
Exec=superlauncher
Icon=$app_id
Terminal=false
Categories=Game;Utility;
EOF

    if [ -f "$ROOT_DIR/assets/icon.png" ]; then
        cp "$ROOT_DIR/assets/icon.png" "$HOME/.local/share/icons/hicolor/256x256/apps/${app_id}.png"
    elif [ -f "$ROOT_DIR/SuperLauncher/assets/icons/icon.png" ]; then
        cp "$ROOT_DIR/SuperLauncher/assets/icons/icon.png" "$HOME/.local/share/icons/hicolor/256x256/apps/${app_id}.png"
    fi

    print_ok "Desktop entry created: $desktop_file"
}

clean() {
    print_step "Cleaning build artifacts"
    rm -rf "$ROOT_DIR/build" "$ROOT_DIR/dist" "$ROOT_DIR/__pycache__"
    rm -rf "$PYTHON_PKG_DIR"/**/__pycache__
    rm -rf "$ROOT_DIR/"*.egg-info
    rm -rf "$ROOT_DIR/.eggs"
    find "$ROOT_DIR" -name "*.pyc" -delete
    find "$ROOT_DIR" -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
    print_ok "Cleaned"
}

usage() {
    echo "Usage: $0 [OPTIONS]"
    echo "Options:"
    echo "  all         Build everything (default)"
    echo "  deps        Install system dependencies"
    echo "  python      Build/install Python package only"
    echo "  cpp         Build C++ component only"
    echo "  pyinstaller Build standalone executable with PyInstaller"
    echo "  desktop     Create .desktop entry"
    echo "  clean       Remove build artifacts"
    echo "  help        Show this help"
}

main() {
    local cmd="${1:-all}"

    case "$cmd" in
        all)
            install_deps
            build_python_package
            build_cpp_component
            create_desktop_entry
            print_step "Build complete!"
            echo "Run: superlauncher"
            ;;
        deps)
            install_deps
            ;;
        python)
            build_python_package
            ;;
        cpp)
            build_cpp_component
            ;;
        pyinstaller)
            build_pyinstaller
            ;;
        desktop)
            create_desktop_entry
            ;;
        clean)
            clean
            ;;
        help|--help|-h)
            usage
            ;;
        *)
            echo "Unknown command: $cmd"
            usage
            exit 1
            ;;
    esac
}

main "$@"
