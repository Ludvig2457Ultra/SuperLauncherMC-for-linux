# Maintainer: ludvig2457 <ludvig2457@archlinux.org>

pkgname=superlauncher
pkgver=2.0.0
pkgrel=1
pkgdesc="Minecraft launcher with mod support and server management"
arch=('any')
url="https://github.com/Ludvig2457Ultra/SuperLauncherMC-for-linux"
license=('GPL3')
depends=(
    'python'
    'python-pyqt6'
    'python-requests'
    'python-pillow'
    'python-pypresence'
)
    'python-cryptography: encrypted storage'
    'python-psutil: system resource monitoring'
    'python-pyjwt: JWT authentication'
    'python-minecraft-launcher-lib: Minecraft version management'
    'tk: Pillow TK support'
    'jdk17-openjdk: run Minecraft Java Edition'
)
source=("${pkgname}-${pkgver}.tar.gz")
sha256sums=('SKIP')

package() {
    cd "${srcdir}/${pkgname}-${pkgver}"

    # Install the main script
    install -Dm755 superlauncher.py "$pkgdir/usr/share/superlauncher/superlauncher.py"

    # Create wrapper
    mkdir -p "$pkgdir/usr/bin"
    cat > "$pkgdir/usr/bin/superlauncher" << 'EOF'
#!/usr/bin/env bash
exec python3 /usr/share/superlauncher/superlauncher.py "$@"
EOF
    chmod +x "$pkgdir/usr/bin/superlauncher"

    # Desktop entry
    install -Dm644 superlauncher.desktop \
        "$pkgdir/usr/share/applications/superlauncher.desktop"

    # Icon
    install -Dm644 assets/icon.png \
        "$pkgdir/usr/share/icons/hicolor/256x256/apps/superlauncher.png"

    # Copy assets to launcher directory
    cp -r assets "$pkgdir/usr/share/superlauncher/assets"
}
