---
layout: default
title: Installation
parent: Getting Started
nav_order: 1
---

# Installation
{: .no_toc }

## Table of Contents
{: .no_toc .text-delta }

1. TOC
{:toc}

---

## Via APT Repository (recommended)

Add the SimplyConvertFile APT repository to get automatic updates via `apt upgrade`:

```bash
# Import the signing key
curl -fsSL https://thigschuch.github.io/SimplyConvertFile/gpg.key | sudo gpg --dearmor -o /usr/share/keyrings/simplyconvertfile.gpg

# Add the repository
echo "deb [signed-by=/usr/share/keyrings/simplyconvertfile.gpg] https://thigschuch.github.io/SimplyConvertFile/ stable main" | sudo tee /etc/apt/sources.list.d/simplyconvertfile.list

# Install
sudo apt update && sudo apt install simplyconvertfile
```

To update later:

```bash
sudo apt update && sudo apt upgrade
```

## Via .deb Package

Download the latest `.deb` from the [Releases page](https://github.com/ThigSchuch/SimplyConvertFile/releases) and install:

```bash
sudo dpkg -i simplyconvertfile_*.deb
sudo apt-get install -f  # install dependencies if needed
```

## Via pip

```bash
pip install .
```

Then optionally add desktop integration:

```bash
cp packaging/simplyconvertfile.desktop ~/.local/share/applications/
cp src/simplyconvertfile/resources/icon.png ~/.local/share/icons/hicolor/48x48/apps/simplyconvertfile.png
gtk-update-icon-cache -f -t ~/.local/share/icons/hicolor/
update-desktop-database ~/.local/share/applications/
```

## System-wide Install

```bash
sudo make install
```

## Build .deb Package

```bash
make deb
```

## Uninstall

```bash
sudo make uninstall
# or
pip uninstall simplyconvertfile
```

## Nemo File Manager Integration

If you use the Cinnamon desktop, you can integrate SimplyConvertFile into Nemo's context menu.

**If installed from source / pip** (the `packaging/` directory is available):

```bash
cp packaging/simplyconvertfile.nemo_action ~/.local/share/nemo/actions/
```

**If installed via APT or .deb**:

```bash
mkdir -p ~/.local/share/nemo/actions
curl -fsSL https://raw.githubusercontent.com/ThigSchuch/SimplyConvertFile/main/packaging/simplyconvertfile.nemo_action -o ~/.local/share/nemo/actions/simplyconvertfile.nemo_action
```

## Verification

After installation, run `simplyconvertfile` from the terminal or find it in your application menu.
