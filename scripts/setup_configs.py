#!/usr/bin/env python3
"""Config file setup script for dotfiles management."""

import shutil
import sys
import tomllib
from dataclasses import dataclass
from pathlib import Path
from string import Template
from typing import Self

from detect_platform import detect_platform


@dataclass
class Config:
    """Configuration file or directory mapping."""

    host: Path  # relative to home directory
    repo: Path  # relative to `config` directory
    templated: bool
    is_directory: bool = False

    @classmethod
    def home(
        cls: type[Self],
        host: str,
        repo: str,
        templated: bool = False,
        is_directory: bool = False,
    ) -> Self:
        """Create config mapping relative to home directory."""
        host_root = Path.home()
        config_root = Path(__file__).parent.parent / "config"

        return cls(
            host=host_root / host,
            repo=config_root / repo,
            templated=templated,
            is_directory=is_directory,
        )


def get_config_files() -> list[Config]:
    """Get list of config files to manage."""
    platform = detect_platform()

    config_files = [
        # Zsh
        Config.home(".zshrc", "zsh/zshrc"),
        Config.home(".zsh_aliases", "zsh/aliases"),
        # Git
        Config.home(".config/git/config", "git/config"),
        # Starship
        Config.home(".config/starship/starship.toml", "starship/starship.toml"),
        # Neovim - copy entire directory structure
        Config.home(".config/nvim", "nvim", is_directory=True),
    ]

    # Add platform-specific configs
    if platform.os_name == "linux":
        config_files.extend(
            [
                # SSH (Linux only, macOS handles this differently)
                Config.home(".ssh/config", "ssh/config"),
                Config.home(".ssh/authorized_keys", "ssh/authorized_keys"),
                # Less
                Config.home(".lesskey", "less/lesskey"),
                # Htop
                Config.home(".config/htop/htoprc", "htop/htoprc"),
                # Curl
                Config.home(".config/curlrc", "curl/curlrc"),
                # Postgres
                Config.home(".psqlrc", "postgres/psqlrc"),
            ]
        )

    return config_files


class ConfigManager:
    """Manages dotfiles configuration."""

    def __init__(self):
        self.repo_root = Path(__file__).parent.parent
        self.settings = self._load_settings()

    def _load_settings(self) -> dict[str, str]:
        """Load settings from settings.toml."""
        settings_path = self.repo_root / "settings.toml"

        if not settings_path.exists():
            print(f"× Settings file not found: {settings_path}")
            return {}

        try:
            with settings_path.open("rb") as settings_file:
                settings = tomllib.load(settings_file)

            # Flatten nested settings
            flat_settings = {}
            for section, values in settings.items():
                if isinstance(values, dict):
                    for key, value in values.items():
                        flat_settings[f"{section}_{key}"] = str(value)
                        flat_settings[key] = str(value)  # Also allow direct access
                else:
                    flat_settings[section] = str(values)

            # Add builtin variables
            flat_settings["home"] = str(Path.home())
            flat_settings["repo"] = str(self.repo_root)

            return flat_settings

        except Exception as e:
            print(f"× Error loading settings: {e}")
            return {}

    def install_configs(self) -> bool:
        """Install config files to their target locations."""
        print("→ Installing configuration files...")

        success = True
        config_files = get_config_files()

        for config in config_files:
            if not self._install_config(config):
                success = False

        return success

    def sync_configs(self) -> bool:
        """Sync config files back to the repository."""
        print("→ Syncing configuration files back to repository...")

        success = True
        config_files = get_config_files()

        for config in config_files:
            if not self._sync_config(config):
                success = False

        return success

    def _install_config(self, config: Config) -> bool:
        """Install a single config file or directory."""
        if not config.repo.exists():
            print(f"× Source not found: {config.repo}")
            return False

        print(f"  {config.repo} → {config.host}")

        try:
            if config.is_directory:
                # Handle directory copying
                if config.host.exists():
                    # Create backup of existing directory
                    backup_path = config.host.with_suffix(".backup")
                    if backup_path.exists():
                        shutil.rmtree(backup_path)
                    shutil.move(config.host, backup_path)
                    print(f"    (backed up to {backup_path})")

                # Copy entire directory tree
                shutil.copytree(config.repo, config.host)

            else:
                # Handle file copying (existing logic)
                # Create parent directories
                config.host.parent.mkdir(parents=True, exist_ok=True)

                # Create backup if file exists
                if config.host.exists():
                    backup_path = config.host.with_suffix(
                        config.host.suffix + ".backup"
                    )
                    shutil.copy2(config.host, backup_path)
                    print(f"    (backed up to {backup_path})")

                # Load and process file
                with config.repo.open("r") as repo_file:
                    content = repo_file.read()

                # Apply templating if needed
                if config.templated:
                    template = Template(content)
                    content = template.safe_substitute(**self.settings)

                # Write to target location
                with config.host.open("w") as host_file:
                    host_file.write(content)

            return True

        except Exception as e:
            print(f"× Failed to install {config.repo}: {e}")
            return False

    def _sync_config(self, config: Config) -> bool:
        """Sync a single config file or directory back to repository."""
        if not config.host.exists():
            print(f"× Host not found: {config.host}")
            return False

        print(f"  {config.host} → {config.repo}")

        try:
            if config.is_directory:
                # Handle directory syncing
                if config.repo.exists():
                    shutil.rmtree(config.repo)

                # Create parent directories
                config.repo.parent.mkdir(parents=True, exist_ok=True)

                # Copy entire directory tree
                shutil.copytree(config.host, config.repo)

            else:
                # Handle file syncing (existing logic)
                # Create parent directories
                config.repo.parent.mkdir(parents=True, exist_ok=True)

                # Copy file back
                shutil.copy2(config.host, config.repo)

            return True

        except Exception as e:
            print(f"× Failed to sync {config.host}: {e}")
            return False


def main() -> None:
    """Main function for config management."""
    if len(sys.argv) < 2:
        print("Usage: python setup_configs.py <install|sync>")
        sys.exit(1)

    action = sys.argv[1]
    manager = ConfigManager()

    if action == "install":
        if manager.install_configs():
            print("✓ Configuration files installed successfully")
        else:
            print("× Some configuration files failed to install")
            sys.exit(1)

    elif action == "sync":
        if manager.sync_configs():
            print("✓ Configuration files synced successfully")
        else:
            print("× Some configuration files failed to sync")
            sys.exit(1)

    else:
        print(f"× Unknown action: {action}")
        print("Usage: python setup_configs.py <install|sync>")
        sys.exit(1)


if __name__ == "__main__":
    main()
