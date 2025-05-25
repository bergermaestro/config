#!/usr/bin/env python3
"""
Main installer script for dotfiles setup.

This script orchestrates the installation of tools and configuration files
across macOS and Linux platforms.
"""

import argparse
import sys
from pathlib import Path

# Add scripts directory to path for imports
sys.path.insert(0, str(Path(__file__).parent / "scripts"))

from detect_platform import detect_platform, print_platform_info
from install_tools import ToolInstaller
from setup_configs import ConfigManager


def main() -> None:
    """Main installer function."""
    parser = argparse.ArgumentParser(
        description="Install dotfiles and tools across platforms",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python install.py --all                    # Install everything
  python install.py --tools essential        # Install only essential tools
  python install.py --configs                # Install only config files
  python install.py --tools essential development --configs  # Install tools and configs
  python install.py sync-repo                # Sync configs back to repo
        """,
    )

    # Main actions
    parser.add_argument(
        "action",
        nargs="?",
        choices=["sync-repo"],
        help="Special actions (sync-repo: copy configs back to repository)",
    )

    # Installation options
    parser.add_argument(
        "--all", action="store_true", help="Install everything (tools + configs)"
    )

    parser.add_argument(
        "--tools",
        nargs="*",
        metavar="CATEGORY",
        help="Install tools from specified categories (essential, development, optional)",
    )

    parser.add_argument(
        "--configs", action="store_true", help="Install configuration files"
    )

    # Information options
    parser.add_argument(
        "--platform-info",
        action="store_true",
        help="Show platform information and exit",
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be done without actually doing it",
    )

    args = parser.parse_args()

    # Handle platform info request
    if args.platform_info:
        print_platform_info()
        return

    # Handle sync-repo action
    if args.action == "sync-repo":
        manager = ConfigManager()
        if manager.sync_configs():
            print("✓ Configuration files synced to repository")
        else:
            print("× Failed to sync some configuration files")
            sys.exit(1)
        return

    # Determine what to install
    install_tools = args.all or args.tools is not None
    install_configs = args.all or args.configs

    if not install_tools and not install_configs:
        # Default behavior: install essential tools and configs
        install_tools = True
        install_configs = True
        tool_categories = ["essential"]
    else:
        if args.all:
            # Install all categories when --all is specified
            tool_categories = ["essential", "development", "optional"]
        else:
            tool_categories = args.tools if args.tools is not None else ["essential"]

    # Show what we're going to do
    print("🚀 Dotfiles Installer")
    print("=" * 50)
    print_platform_info()
    print()

    if args.dry_run:
        print("DRY RUN MODE - No changes will be made")
        print()

    if install_tools:
        print(f"→ Will install tools: {', '.join(tool_categories)}")
    if install_configs:
        print("→ Will install configuration files")

    if args.dry_run:
        print("\nDry run completed. Use without --dry-run to actually install.")
        return

    print()

    # Perform installations
    success = True
    repo_root = Path(__file__).parent

    if install_tools:
        print("📦 Installing Tools")
        print("-" * 30)
        installer = ToolInstaller(repo_root)

        # Install package manager if needed
        if not installer.install_package_manager():
            print("× Failed to set up package manager")
            success = False
        else:
            # Install tools
            if not installer.install_tools(tool_categories):
                print("× Failed to install some tools")
                success = False
        print()

    if install_configs:
        print("⚙️  Installing Configuration Files")
        print("-" * 40)
        manager = ConfigManager()

        if not manager.install_configs():
            print("× Failed to install some configuration files")
            success = False
        print()

    # Final status
    if success:
        print("🎉 Installation completed successfully!")
        print()
        print("Next steps:")
        print("1. Restart your terminal or run: source ~/.zshrc")
        print("2. Customize settings.toml with your preferences")
        print("3. Run 'python install.py --configs' again to apply template changes")
    else:
        print("❌ Installation completed with errors")
        sys.exit(1)


if __name__ == "__main__":
    main()
