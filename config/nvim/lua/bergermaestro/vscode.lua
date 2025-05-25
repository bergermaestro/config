-- VS Code detection utility
local M = {}

-- Check if running in VS Code
function M.is_vscode()
    return vim.g.vscode ~= nil
end

-- Check if running in standalone Neovim
function M.is_standalone()
    return vim.g.vscode == nil
end

return M 
