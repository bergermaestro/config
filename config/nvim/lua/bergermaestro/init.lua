local vscode = require("bergermaestro.vscode")

-- Always load basic settings and remaps
require("bergermaestro.set")
require("bergermaestro.remap")

-- Load VS Code specific remaps when in VS Code
if vscode.is_vscode() then
    require("bergermaestro.vscode_remap")
end

-- Only load plugins and their configurations in standalone Neovim
if vscode.is_standalone() then
    require("bergermaestro.packer")
end
