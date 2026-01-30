include upstream.sh
export

cf_source_dir := lucid_browser-$(version)-$(release)
ff_source_tarball := firefox-$(version).source.tar.xz

debs := python3 python3-dev python3-pip p7zip-full golang-go msitools wget aria2 libsqlite3-dev
rpms := python3 python3-devel p7zip golang msitools wget aria2 sqlite-devel
pacman := python python-pip p7zip go msitools wget aria2 sqlite

.PHONY: help fetch setup setup-minimal clean set-target distclean build package \
        build-launcher check-arch revert edits run bootstrap mozbootstrap dir \
        package-linux package-macos package-windows vcredist_arch patch unpatch \
        workspace check-arg edit-cfg ff-dbg tests update-ubo-assets generate-assets-car

help:
	@echo "Available targets:"
	@echo "  fetch           - Fetch the Firefox source code"
	@echo "  setup           - Setup Lucid Empire & local git repo for development"
	@echo "  bootstrap       - Set up build environment"
	@echo "  mozbootstrap    - Sets up mach"
	@echo "  dir             - Prepare Lucid Empire source directory with BUILD_TARGET"
	@echo "  revert          - Kill all working changes"
	@echo "  edits           - Lucid Empire developer UI"
	@echo "  build-launcher  - Build launcher"
	@echo "  clean           - Remove build artifacts"
	@echo "  distclean       - Remove everything including downloads"
	@echo "  build           - Build Lucid Empire"
	@echo "  set-target      - Change the build target with BUILD_TARGET"
	@echo "  package-linux   - Package Lucid Empire for Linux"
	@echo "  package-macos   - Package Lucid Empire for macOS"
	@echo "  package-windows - Package Lucid Empire for Windows"
	@echo "  run             - Run Lucid Empire"
	@echo "  edit-cfg        - Edit lucid_browser.cfg"
	@echo "  ff-dbg          - Setup vanilla Firefox with minimal patches"
	@echo "  patch           - Apply a patch"
	@echo "  unpatch         - Remove a patch"
	@echo "  workspace       - Sets the workspace to a patch, assuming its applied"
	@echo "  tests           - Runs the Playwright tests"
	@echo "  update-ubo-assets - Update the uBOAssets.json file"

_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
$(eval $(_ARGS):;@:)

fetch:
	# Fetching private patches...
	@if [ -d "patches/private" ]; then \
		echo "Found patches/private. Skipping private patches fetch..."; \
	else \
		if [ -z "$$CAMOUFOX_PASSWD" ]; then \
			echo "CAMOUFOX_PASSWD environment variable not set. Skipping private patches..."; \
		else \
			echo "Fetching private patches..."; \
			mkdir -p patches/closedsrc; \
			if ! aria2c --dry-run "https://lucid_browser.com/pipeline/rev-$(closedsrc_rev).7z" 2>/dev/null; then \
				echo "No private patches found for this version"; \
				exit 1; \
			else \
				aria2c -o rev-$(closedsrc_rev).7z "https://lucid_browser.com/pipeline/rev-$(closedsrc_rev).7z" && \
				7z x -p"$$CAMOUFOX_PASSWD" rev-$(closedsrc_rev).7z -o./patches/closedsrc && \
				rm rev-$(closedsrc_rev).7z; \
			fi; \
		fi; \
	fi
	# Fetching the Firefox source tarball...
	aria2c -x16 -s16 -k1M -o $(ff_source_tarball) "https://archive.mozilla.org/pub/firefox/releases/$(version)/source/firefox-$(version).source.tar.xz"; \