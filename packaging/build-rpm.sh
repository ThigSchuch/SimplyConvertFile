#!/usr/bin/env bash
# =============================================================================
# SimplyConvertFile - RPM Package Builder
# =============================================================================
# Usage: ./packaging/build-rpm.sh
#
# Creates an RPM package in the dist/ directory using FPM.
# Requires fpm (gem install fpm) and gettext for translations.
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
ARCH="noarch"  # Pure Python = architecture-independent
MAINTAINER="thigschuch"
DESCRIPTION="Universal file format converter for Linux"
LONG_DESCRIPTION="SimplyConvertFile supports 80+ formats including images, videos,
audio, documents, spreadsheets, presentations, markup, data formats, and
archives. It provides a GTK 3 graphical interface with single and batch
conversion, progress tracking, desktop notifications, and intelligent
format detection."
HOMEPAGE="https://github.com/ThigSchuch/SimplyConvertFile"
PYTHON_VERSION="3"

# --- Paths ---
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
BUILD_DIR="$PROJECT_DIR/dist/rpm-build"
PKG_DIR="$BUILD_DIR/${APP_NAME}-${APP_VERSION}"
DIST_DIR="$PROJECT_DIR/dist"

# Python site-packages path inside the rpm (standard location)
PYTHON_SITE="usr/lib/python${PYTHON_VERSION}/site-packages"

echo "============================================="
echo "  Building ${APP_NAME} v${APP_VERSION} RPM"
echo "============================================="

# --- Clean previous build ---
rm -rf "$BUILD_DIR"
mkdir -p "$DIST_DIR"

# --- Create directory structure ---
echo "[1/5] Creating package structure..."
mkdir -p "$PKG_DIR/$PYTHON_SITE/$APP_NAME"
mkdir -p "$PKG_DIR/usr/bin"
mkdir -p "$PKG_DIR/usr/share/applications"
mkdir -p "$PKG_DIR/usr/share/icons/hicolor/48x48/apps"
mkdir -p "$PKG_DIR/usr/share/doc/$APP_NAME"

# --- Copy application files ---
echo "[2/5] Copying application files..."
cp -r "$PROJECT_DIR/src/$APP_NAME/"* "$PKG_DIR/$PYTHON_SITE/$APP_NAME/"

# Remove __pycache__ and .pyc files
find "$PKG_DIR" -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find "$PKG_DIR" -name "*.pyc" -delete 2>/dev/null || true

# --- Compile translations ---
echo "[2.5/5] Compiling translations..."
PO_DIR="$PKG_DIR/$PYTHON_SITE/$APP_NAME/po"
for po_file in "$PO_DIR"/*.po; do
    [ -f "$po_file" ] || continue
    lang=$(basename "$po_file" .po)
    mkdir -p "$PO_DIR/$lang/LC_MESSAGES"
    msgfmt -o "$PO_DIR/$lang/LC_MESSAGES/$APP_NAME.mo" "$po_file"
done

# --- Create launcher script ---
echo "[3/5] Creating launcher script..."
cat > "$PKG_DIR/usr/bin/$APP_NAME" << 'LAUNCHER'
#!/usr/bin/env python3
"""SimplyConvertFile launcher."""
from simplyconvertfile.main import main
main()
LAUNCHER
chmod 755 "$PKG_DIR/usr/bin/$APP_NAME"

# --- Install desktop file and icon ---
echo "[4/5] Installing desktop integration..."
cp "$PROJECT_DIR/packaging/simplyconvertfile.desktop" \
   "$PKG_DIR/usr/share/applications/$APP_NAME.desktop"

cp "$PROJECT_DIR/src/$APP_NAME/resources/icon.png" \
   "$PKG_DIR/usr/share/icons/hicolor/48x48/apps/$APP_NAME.png"

# --- Create documentation ---
cp "$PROJECT_DIR/README.md" "$PKG_DIR/usr/share/doc/$APP_NAME/"

# --- Build the RPM using FPM ---
echo "[5/5] Building RPM package..."
RPM_FILE="$DIST_DIR/${APP_NAME}-${APP_VERSION}-1.${ARCH}.rpm"

fpm -s dir -t rpm \
    -n "$APP_NAME" \
    -v "$APP_VERSION" \
    -a "$ARCH" \
    --iteration 1 \
    --description "$DESCRIPTION" \
    --url "$HOMEPAGE" \
    --maintainer "$MAINTAINER" \
    --license "GPL-3.0-or-later" \
    --depends "python3 >= 3.8" \
    --depends "python3-gobject" \
    --depends "gtk3" \
    --depends "libnotify" \
    --depends "ffmpeg" \
    --depends "ImageMagick" \
    --provides "$APP_NAME" \
    --after-install "$SCRIPT_DIR/rpm-postinst.sh" \
    --after-remove "$SCRIPT_DIR/rpm-postrm.sh" \
    -C "$PKG_DIR" \
    -p "$RPM_FILE" \
    .

# --- Cleanup build directory ---
rm -rf "$BUILD_DIR"

echo ""
echo "============================================="
echo "  Package built successfully!"
echo "============================================="
echo ""
echo "  Output: $RPM_FILE"
echo "  Size:   $(du -h "$RPM_FILE" | cut -f1)"
echo ""
echo "  Install:   sudo rpm -i $RPM_FILE"
echo "  Uninstall: sudo rpm -e $APP_NAME"
echo ""