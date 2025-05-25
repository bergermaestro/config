# Dotfiles Management System

A cross-platform dotfiles management system that handles tool installation and configuration file deployment across macOS and Linux.

## Features

- 🚀 **Cross-platform**: Works on macOS and Linux
- 📦 **Tool Installation**: Automatically installs development tools via package managers
- ⚙️ **Config Management**: Deploys and templates configuration files
- 🎯 **Modular**: Install tools and configs separately or together
- 🔧 **Templating**: Support for templated config files with variable substitution
- 🔄 **Bidirectional Sync**: Sync changes back to the repository

## Quick Start

### Fresh Machine Setup

```bash
# Clone the repository
git clone <your-repo-url> ~/.dotfiles
cd ~/.dotfiles

# Install everything (tools + configs)
python install.py --all
```

### Selective Installation

```bash
# Install only essential tools
python install.py --tools essential

# Install tools and configs
python install.py --tools essential development --configs

# Install only configuration files
python install.py --configs
```

## Project Structure

```
dotfiles/
├── install.py              # Main installer script
├── scripts/                # Installation scripts
│   ├── detect_platform.py  # Platform detection
│   ├── install_tools.py    # Tool installation
│   └── setup_configs.py    # Config file management
├── tools/                  # Tool definitions
│   ├── common.toml         # Cross-platform tools
│   ├── macos.toml          # macOS-specific tools
│   └── linux.toml         # Linux-specific tools
├── config/                 # Configuration files
│   ├── zsh/               # Zsh configuration
│   ├── git/               # Git configuration
│   ├── nvim/              # Neovim configuration
│   └── ...                # Other app configs
├── settings.toml           # Template variables
└── README.md              # This file
```

## Configuration

### Settings File (`settings.toml`)

The `settings.toml` file contains variables that can be used in templated configuration files:

```toml
[user]
name = "Your Name"
email = "your.email@example.com"

[colors]
primary = "#007acc"
background = "#1e1e1e"

[fonts]
mono = "FiraCode Nerd Font"
size = "12"
```

### Using Templates

Configuration files marked as `templated=True` can use these variables:

```bash
# In a config file
font_family $mono
font_size $size
background $background
```

## Tool Categories

### Essential

Basic tools needed for development:

- git, curl, wget, tmux, zsh, neovim, htop, tree, jq, ripgrep, fd, bat, exa

### Development

Programming languages and development tools:

- python3, nodejs, npm, rust, go, docker, docker-compose

### Optional

Nice-to-have tools:

- fzf, zoxide, starship, lazygit, bottom, dust, procs

## Platform Support

### macOS

- **Package Manager**: Homebrew (auto-installed if missing)
- **Packages**: Homebrew formulas
- **GUI Apps**: Homebrew casks (fonts, applications)

### Linux

- **Package Managers**: apt, pacman, dnf, yum (auto-detected)
- **Distributions**: Ubuntu, Debian, Arch, Fedora, CentOS
- **Special Environments**: WSL

## Commands

### Installation

```bash
# Install everything
python install.py --all

# Install specific tool categories
python install.py --tools essential development

# Install only configs
python install.py --configs

# Dry run (see what would be installed)
python install.py --all --dry-run
```

### Maintenance

```bash
# Sync configs back to repository
python install.py sync-repo

# Show platform information
python install.py --platform-info

# Update tools (re-run installation)
python install.py --tools essential development
```

### Individual Scripts

```bash
# Platform detection
python scripts/detect_platform.py

# Install tools only
python scripts/install_tools.py essential development

# Manage configs only
python scripts/setup_configs.py install
python scripts/setup_configs.py sync
```

## Adding New Tools

### 1. Edit Tool Configuration Files

Add tools to the appropriate files in the `tools/` directory:

**For cross-platform tools** (`tools/common.toml`):

```toml
[essential]
tools = ["git", "curl", "new-tool"]
```

**For macOS** (`tools/macos.toml`):

```toml
[packages.essential]
essential = ["git", "curl", "new-tool"]

[casks.essential]
essential = ["font-fira-code-nerd-font"]
```

**For Linux** (`tools/linux.toml`):

```toml
[packages.essential]
apt = ["git", "curl", "new-tool"]
pacman = ["git", "curl", "new-tool"]
```

### 2. Test Installation

```bash
python install.py --tools essential --dry-run
```

## Adding New Config Files

### 1. Add Config Mapping

Edit `scripts/setup_configs.py` and add your config to the appropriate section:

```python
config_files = [
    # Existing configs...
    Config.home(".config/myapp/config.toml", "myapp/config.toml"),
    Config.home(".config/myapp/theme.toml", "myapp/theme.toml", templated=True),
]
```

### 2. Create Config Files

Add your configuration files to the `config/` directory:

```
config/
└── myapp/
    ├── config.toml
    └── theme.toml
```

### 3. Test Deployment

```bash
python install.py --configs --dry-run
```

## Customization

### Personal Settings

1. Edit `settings.toml` with your personal information
2. Customize tool lists in `tools/*.toml` files
3. Add/remove config files in `scripts/setup_configs.py`
4. Modify config files in the `config/` directory

### Platform-Specific Configs

The system automatically detects your platform and only installs relevant configurations. You can add platform-specific logic in `scripts/setup_configs.py`.

## Troubleshooting

### Common Issues

**Python version**: Requires Python 3.11+ for `tomllib` support

```bash
python --version  # Should be 3.11+
```

**Package manager not found**:

```bash
python install.py --platform-info  # Check detected package manager
```

**Permission errors**: Some tools may require sudo access

```bash
# On Linux, ensure your user can use sudo
sudo -v
```

**Config file conflicts**: Existing configs are backed up with `.backup` extension

### Debug Mode

Use `--dry-run` to see what would be installed without making changes:

```bash
python install.py --all --dry-run
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add your changes
4. Test on your platform
5. Submit a pull request

## License

[Add your license here]
