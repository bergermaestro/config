#!/usr/bin/env python3
"""Platform detection utilities for cross-platform dotfiles setup."""

import os
import platform
import subprocess
import sys
from dataclasses import dataclass
from typing import Optional


@dataclass
class Platform:
    """Information about the current platform."""

    os_name: str  # 'macos', 'linux', 'windows'
    distro: Optional[str] = None  # Linux distribution name
    package_manager: Optional[str] = None  # Available package manager
    is_wsl: bool = False


def detect_platform() -> Platform:
    """Detect the current platform and available package managers."""
    system = platform.system().lower()

    if system == "darwin":
        return Platform(
            os_name="macos", package_manager="brew" if _command_exists("brew") else None
        )

    elif system == "linux":
        # Check for WSL environment
        is_wsl = "microsoft" in platform.uname().release.lower()

        # Detect Linux distribution
        distro = _detect_linux_distro()

        # Detect package manager
        package_manager = _detect_package_manager()

        return Platform(
            os_name="linux",
            distro=distro,
            package_manager=package_manager,
            is_wsl=is_wsl,
        )

    elif system == "windows":
        return Platform(
            os_name="windows",
            package_manager="winget" if _command_exists("winget") else None,
        )

    else:
        return Platform(os_name="unknown")


def _detect_linux_distro() -> Optional[str]:
    """Detect Linux distribution."""
    try:
        # Try /etc/os-release first
        with open("/etc/os-release", "r") as f:
            for line in f:
                if line.startswith("ID="):
                    return line.split("=")[1].strip().strip('"')
    except FileNotFoundError:
        pass

    # Fallback methods
    if os.path.exists("/etc/debian_version"):
        return "debian"
    elif os.path.exists("/etc/redhat-release"):
        return "redhat"
    elif os.path.exists("/etc/arch-release"):
        return "arch"

    return None


def _detect_package_manager() -> Optional[str]:
    """Detect available package manager on Linux."""
    managers = ["apt", "pacman", "dnf", "yum", "zypper", "emerge"]

    for manager in managers:
        if _command_exists(manager):
            return manager

    return None


def _command_exists(command: str) -> bool:
    """Check if a command exists in PATH."""
    try:
        subprocess.run(
            ["which", command],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True,
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def print_platform_info() -> None:
    """Print detected platform information."""
    platform_info = detect_platform()

    print(f"OS: {platform_info.os_name}")
    if platform_info.distro:
        print(f"Distribution: {platform_info.distro}")
    if platform_info.package_manager:
        print(f"Package Manager: {platform_info.package_manager}")
    else:
        print("Package Manager: None detected")

    if platform_info.is_wsl:
        print("Environment: WSL")


if __name__ == "__main__":
    print_platform_info()
