#!/usr/bin/env python3
"""Tool installation script for cross-platform dotfiles setup."""

import subprocess
import sys
import tomllib
from pathlib import Path
from typing import Dict, List, Optional

from detect_platform import Platform, detect_platform


class ToolInstaller:
    """Handles tool installation across different platforms."""

    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.tools_dir = repo_root / "tools"
        self.platform = detect_platform()

    def install_package_manager(self) -> bool:
        """Install package manager if not present."""
        if self.platform.package_manager:
            print(
                f"✓ Package manager '{self.platform.package_manager}' already installed"
            )
            return True

        if self.platform.os_name == "macos":
            return self._install_homebrew()
        elif self.platform.os_name == "linux":
            print("× No package manager detected. Please install one manually:")
            print("  - Ubuntu/Debian: apt should be pre-installed")
            print("  - Arch: pacman should be pre-installed")
            print("  - Fedora: dnf should be pre-installed")
            return False
        else:
            print(f"× Unsupported platform: {self.platform.os_name}")
            return False

    def _install_homebrew(self) -> bool:
        """Install Homebrew on macOS."""
        print("→ Installing Homebrew...")
        try:
            cmd = '/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"'
            subprocess.run(cmd, shell=True, check=True)

            # Update platform info
            self.platform.package_manager = "brew"
            print("✓ Homebrew installed successfully")
            return True
        except subprocess.CalledProcessError as e:
            print(f"× Failed to install Homebrew: {e}")
            return False

    def install_tools(self, categories: Optional[List[str]] = None) -> bool:
        """Install tools from specified categories."""
        if not self.platform.package_manager:
            print("× No package manager available")
            return False

        if categories is None:
            categories = ["essential"]

        success = True

        for category in categories:
            print(f"\n→ Installing {category} tools...")
            if not self._install_category(category):
                success = False

        return success

    def _install_category(self, category: str) -> bool:
        """Install tools from a specific category."""
        tools = self._get_tools_for_category(category)
        if not tools:
            print(f"× No tools found for category '{category}'")
            return False

        if self.platform.os_name == "macos":
            if isinstance(tools, dict):
                return self._install_macos_tools(tools)
            else:
                print(f"× Invalid tools format for macOS")
                return False
        elif self.platform.os_name == "linux":
            if isinstance(tools, list):
                return self._install_linux_tools(tools)
            else:
                print(f"× Invalid tools format for Linux")
                return False
        else:
            print(f"× Unsupported platform: {self.platform.os_name}")
            return False

    def _get_tools_for_category(self, category: str) -> Optional[Dict | List[str]]:
        """Get tools for a specific category from config files."""
        if self.platform.os_name == "macos":
            config_file = self.tools_dir / "macos.toml"
        elif self.platform.os_name == "linux":
            config_file = self.tools_dir / "linux.toml"
        else:
            return None

        if not config_file.exists():
            print(f"× Config file not found: {config_file}")
            return None

        try:
            with config_file.open("rb") as f:
                config = tomllib.load(f)

            if self.platform.os_name == "macos":
                packages = config.get("packages", {}).get(category, [])
                casks = config.get("casks", {}).get(category, [])
                return {"packages": packages, "casks": casks}
            else:
                packages = config.get("packages", {}).get(category, {})
                return packages.get(self.platform.package_manager, [])

        except Exception as e:
            print(f"× Error reading config file: {e}")
            return None

    def _install_macos_tools(self, tools: Dict) -> bool:
        """Install tools on macOS using Homebrew."""
        success = True

        # Install packages
        packages = tools.get("packages", [])
        if packages:
            print(f"  Installing packages: {', '.join(packages)}")
            if not self._run_brew_install(packages):
                success = False

        # Install casks
        casks = tools.get("casks", [])
        if casks:
            print(f"  Installing casks: {', '.join(casks)}")
            if not self._run_brew_install(casks, cask=True):
                success = False

        return success

    def _install_linux_tools(self, tools: List[str]) -> bool:
        """Install tools on Linux using the detected package manager."""
        if not tools:
            return True

        print(f"  Installing packages: {', '.join(tools)}")

        if self.platform.package_manager == "apt":
            return self._run_apt_install(tools)
        elif self.platform.package_manager == "pacman":
            return self._run_pacman_install(tools)
        elif self.platform.package_manager == "dnf":
            return self._run_dnf_install(tools)
        else:
            print(f"× Unsupported package manager: {self.platform.package_manager}")
            return False

    def _run_brew_install(self, packages: List[str], cask: bool = False) -> bool:
        """Run brew install command."""
        try:
            cmd = ["brew", "install"]
            if cask:
                cmd.append("--cask")
            cmd.extend(packages)

            subprocess.run(cmd, check=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"× Brew install failed: {e}")
            return False

    def _run_apt_install(self, packages: List[str]) -> bool:
        """Run apt install command."""
        try:
            # Update package list first
            subprocess.run(["sudo", "apt", "update"], check=True)

            # Install packages
            cmd = ["sudo", "apt", "install", "-y"] + packages
            subprocess.run(cmd, check=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"× Apt install failed: {e}")
            return False

    def _run_pacman_install(self, packages: List[str]) -> bool:
        """Run pacman install command."""
        try:
            # Update package database
            subprocess.run(["sudo", "pacman", "-Sy"], check=True)

            # Install packages
            cmd = ["sudo", "pacman", "-S", "--noconfirm"] + packages
            subprocess.run(cmd, check=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"× Pacman install failed: {e}")
            return False

    def _run_dnf_install(self, packages: List[str]) -> bool:
        """Run dnf install command."""
        try:
            cmd = ["sudo", "dnf", "install", "-y"] + packages
            subprocess.run(cmd, check=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"× DNF install failed: {e}")
            return False


def main() -> None:
    """Main function for tool installation."""
    if len(sys.argv) < 2:
        print("Usage: python install_tools.py <category1> [category2] ...")
        print("Categories: essential, development, optional")
        sys.exit(1)

    categories = sys.argv[1:]
    repo_root = Path(__file__).parent.parent

    installer = ToolInstaller(repo_root)

    print(f"Platform: {installer.platform.os_name}")
    if installer.platform.distro:
        print(f"Distribution: {installer.platform.distro}")
    print(f"Package Manager: {installer.platform.package_manager or 'None'}")

    # Install package manager if needed
    if not installer.install_package_manager():
        sys.exit(1)

    # Install tools
    if installer.install_tools(categories):
        print("\n✓ Tool installation completed successfully")
    else:
        print("\n× Some tools failed to install")
        sys.exit(1)


if __name__ == "__main__":
    main()
