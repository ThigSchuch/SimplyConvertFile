PREFIX ?= /usr
DESTDIR ?=
PYTHON_SITE := $(shell python3 -c "import sysconfig; print(sysconfig.get_paths()['purelib'])")
APP_DIR = $(DESTDIR)$(PYTHON_SITE)/simplyconvertfile
BIN_DIR = $(DESTDIR)$(PREFIX)/bin
DESKTOP_DIR = $(DESTDIR)$(PREFIX)/share/applications
ICON_DIR_48 = $(DESTDIR)$(PREFIX)/share/icons/hicolor/48x48/apps
ICON_DIR_SCALABLE = $(DESTDIR)$(PREFIX)/share/icons/hicolor/scalable/apps

.PHONY: install uninstall install-pip clean compile-po help deb

help: ## Show this help message
	@echo "SimplyConvertFile - Installation targets"
	@echo ""
	@echo "Usage:"
	@echo "  make install        Install system-wide (requires sudo)"
	@echo "  make uninstall      Remove system installation (requires sudo)"
	@echo "  make install-pip    Install via pip (user or venv)"
	@echo "  make deb            Build .deb package"
	@echo "  make clean          Clean build artifacts"
	@echo "  make compile-po     Compile .po translation files to .mo"
	@echo ""

install: ## Install system-wide (requires sudo)
	@echo "Installing SimplyConvertFile..."
	# Install the Python package
	pip3 install --no-deps --prefix=$(DESTDIR)$(PREFIX) .
	# Install desktop file
	install -Dm644 packaging/simplyconvertfile.desktop $(DESKTOP_DIR)/simplyconvertfile.desktop
	# Install icons
	install -Dm644 src/simplyconvertfile/resources/icon.png $(ICON_DIR_48)/simplyconvertfile.png
	# Update icon cache
	-gtk-update-icon-cache -f -t $(DESTDIR)$(PREFIX)/share/icons/hicolor/ 2>/dev/null || true
	# Update desktop database
	-update-desktop-database $(DESKTOP_DIR) 2>/dev/null || true
	@echo "Installation complete!"
	@echo "You can now run 'simplyconvertfile' from the command line or find it in your application menu."

uninstall: ## Remove system installation (requires sudo)
	@echo "Uninstalling SimplyConvertFile..."
	pip3 uninstall -y simplyconvertfile 2>/dev/null || true
	rm -f $(DESKTOP_DIR)/simplyconvertfile.desktop
	rm -f $(ICON_DIR_48)/simplyconvertfile.png
	rm -f $(ICON_DIR_SCALABLE)/simplyconvertfile.svg
	-gtk-update-icon-cache -f -t $(DESTDIR)$(PREFIX)/share/icons/hicolor/ 2>/dev/null || true
	-update-desktop-database $(DESKTOP_DIR) 2>/dev/null || true
	@echo "Uninstallation complete."

install-pip: ## Install via pip (user or venv)
	pip3 install .
	@echo ""
	@echo "Installed via pip. Run 'simplyconvertfile' to launch."
	@echo ""
	@echo "To add desktop integration, copy the .desktop file manually:"
	@echo "  cp packaging/simplyconvertfile.desktop ~/.local/share/applications/"
	@echo "  cp src/simplyconvertfile/resources/icon.png ~/.local/share/icons/hicolor/48x48/apps/simplyconvertfile.png"
	@echo "  gtk-update-icon-cache -f -t ~/.local/share/icons/hicolor/"
	@echo "  update-desktop-database ~/.local/share/applications/"

clean: ## Clean build artifacts
	rm -rf build/ dist/ *.egg-info src/*.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true

compile-po: ## Compile .po translation files to .mo
	@echo "Compiling translation files..."
	@for po in src/simplyconvertfile/po/*.po; do \
		lang=$$(basename "$$po" .po); \
		mkdir -p "src/simplyconvertfile/po/$$lang/LC_MESSAGES"; \
		msgfmt -o "src/simplyconvertfile/po/$$lang/LC_MESSAGES/simplyconvertfile.mo" "$$po"; \
		echo "  Compiled: $$lang"; \
	done
	@echo "All translations compiled."

deb: ## Build .deb package
	@./packaging/build-deb.sh
