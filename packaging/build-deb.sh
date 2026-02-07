#!/usr/bin/env bash
# =============================================================================
# SimplyConvertFile - .deb Package Builder
# =============================================================================
# Usage: ./packaging/build-deb.sh
#
# Creates a .deb package in the dist/ directory.
# No build tools needed beyond dpkg-deb (pre-installed on Debian/Ubuntu/Mint).
# =============================================================================

set -euo pipefail

# --- Configuration ---
APP_NAME="simplyconvertfile"

# Read version from pyproject.toml (single source of truth)
# Accept override via first argument (used by CI)
if [ -n "${1:-}" ]; then
    APP_VERSION="$1"
else
    APP_VERSION=$(grep -Po '(?<=^version = ")[^"]+' "$(cd "$(dirname "$0")/.." && pwd)/pyproject.toml")
    if [ -z "$APP_VERSION" ]; then
        echo "ERROR: Could not extract version from pyproject.toml" >&2
        exit 1
    fi
fi
ARCH="all"  # Pure Python = architecture-independent
MAINTAINER="thigschuch"
DESCRIPTION="Universal file format converter for Linux"
LONG_DESCRIPTION=" SimplyConvertFile supports 80+ formats including images, videos,
 audio, documents, spreadsheets, presentations, markup, data formats, and
 archives. It provides a GTK 3 graphical interface with single and batch
 conversion, progress tracking, desktop notifications, and intelligent
 format detection."
HOMEPAGE="https://github.com/ThigSchuch/SimplyConvertFile"
PYTHON_VERSION="3"

# --- Paths ---
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
BUILD_DIR="$PROJECT_DIR/dist/deb-build"
PKG_DIR="$BUILD_DIR/${APP_NAME}_${APP_VERSION}_${ARCH}"
DIST_DIR="$PROJECT_DIR/dist"

# Python site-packages path inside the deb (standard Debian location)
PYTHON_SITE="usr/lib/python${PYTHON_VERSION}/dist-packages"

echo "============================================="
echo "  Building ${APP_NAME} v${APP_VERSION} .deb"
echo "============================================="

# --- Clean previous build ---
rm -rf "$BUILD_DIR"
mkdir -p "$DIST_DIR"

# --- Create directory structure ---
echo "[1/6] Creating package structure..."
mkdir -p "$PKG_DIR/DEBIAN"
mkdir -p "$PKG_DIR/$PYTHON_SITE/$APP_NAME"
mkdir -p "$PKG_DIR/usr/bin"
mkdir -p "$PKG_DIR/usr/share/applications"
mkdir -p "$PKG_DIR/usr/share/icons/hicolor/48x48/apps"
mkdir -p "$PKG_DIR/usr/share/doc/$APP_NAME"

# --- Copy application files ---
echo "[2/6] Copying application files..."
cp -r "$PROJECT_DIR/src/$APP_NAME/"* "$PKG_DIR/$PYTHON_SITE/$APP_NAME/"

# Remove __pycache__ and .pyc files
find "$PKG_DIR" -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find "$PKG_DIR" -name "*.pyc" -delete 2>/dev/null || true

# --- Compile translations ---
echo "[2.5/6] Compiling translations..."
PO_DIR="$PKG_DIR/$PYTHON_SITE/$APP_NAME/po"
for po_file in "$PO_DIR"/*.po; do
    [ -f "$po_file" ] || continue
    lang=$(basename "$po_file" .po)
    mkdir -p "$PO_DIR/$lang/LC_MESSAGES"
    msgfmt -o "$PO_DIR/$lang/LC_MESSAGES/$APP_NAME.mo" "$po_file"
done

# --- Create launcher script ---
echo "[3/6] Creating launcher script..."
cat > "$PKG_DIR/usr/bin/$APP_NAME" << 'LAUNCHER'
#!/usr/bin/env python3
"""SimplyConvertFile launcher."""
from simplyconvertfile.main import main
main()
LAUNCHER
chmod 755 "$PKG_DIR/usr/bin/$APP_NAME"

# --- Install desktop file and icon ---
echo "[4/6] Installing desktop integration..."
cp "$PROJECT_DIR/packaging/simplyconvertfile.desktop" \
   "$PKG_DIR/usr/share/applications/$APP_NAME.desktop"

cp "$PROJECT_DIR/src/$APP_NAME/resources/icon.png" \
   "$PKG_DIR/usr/share/icons/hicolor/48x48/apps/$APP_NAME.png"

# --- Create documentation ---
cp "$PROJECT_DIR/README.md" "$PKG_DIR/usr/share/doc/$APP_NAME/"

# --- Calculate installed size (in KB) ---
INSTALLED_SIZE=$(du -sk "$PKG_DIR" | cut -f1)

# --- Create DEBIAN/control ---
echo "[5/6] Creating package metadata..."
cat > "$PKG_DIR/DEBIAN/control" << CONTROL
Package: ${APP_NAME}
Version: ${APP_VERSION}
Section: utils
Priority: optional
Architecture: ${ARCH}
Depends: python3 (>= 3.8), python3-gi, gir1.2-gtk-3.0, libnotify-bin, ffmpeg, imagemagick
Suggests: libreoffice-writer, libreoffice-calc, libreoffice-impress, pandoc, p7zip-full, calibre, poppler-utils, rar, lzop, xz-utils
Installed-Size: ${INSTALLED_SIZE}
Maintainer: ${MAINTAINER}
Homepage: ${HOMEPAGE}
Description: ${DESCRIPTION}
${LONG_DESCRIPTION}
CONTROL

# --- Create DEBIAN/postinst (post-install script) ---
cat > "$PKG_DIR/DEBIAN/postinst" << 'POSTINST'
#!/bin/sh
set -e

# Update icon cache
if command -v gtk-update-icon-cache >/dev/null 2>&1; then
    gtk-update-icon-cache -f -t /usr/share/icons/hicolor/ 2>/dev/null || true
fi

# Update desktop database
if command -v update-desktop-database >/dev/null 2>&1; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

#DEBHELPER#
POSTINST
chmod 755 "$PKG_DIR/DEBIAN/postinst"

# --- Create DEBIAN/postrm (post-removal script) ---
cat > "$PKG_DIR/DEBIAN/postrm" << 'POSTRM'
#!/bin/sh
set -e

# Update icon cache
if command -v gtk-update-icon-cache >/dev/null 2>&1; then
    gtk-update-icon-cache -f -t /usr/share/icons/hicolor/ 2>/dev/null || true
fi

# Update desktop database
if command -v update-desktop-database >/dev/null 2>&1; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

#DEBHELPER#
POSTRM
chmod 755 "$PKG_DIR/DEBIAN/postrm"

# --- Build the .deb ---
echo "[6/6] Building .deb package..."
DEB_FILE="$DIST_DIR/${APP_NAME}_${APP_VERSION}_${ARCH}.deb"
dpkg-deb --build --root-owner-group "$PKG_DIR" "$DEB_FILE"

# --- Cleanup build directory ---
rm -rf "$BUILD_DIR"

echo ""
echo "============================================="
echo "  Package built successfully!"
echo "============================================="
echo ""
echo "  Output: $DEB_FILE"
echo "  Size:   $(du -h "$DEB_FILE" | cut -f1)"
echo ""
echo "  Install:   sudo dpkg -i $DEB_FILE"
echo "  Fix deps:  sudo apt-get install -f"
echo "  Uninstall: sudo apt remove $APP_NAME"
echo ""
