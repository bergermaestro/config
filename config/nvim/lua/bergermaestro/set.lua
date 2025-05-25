local vscode = require("bergermaestro.vscode")

-- Always set leader key
vim.g.mapleader = " "

-- Key sequence timeout settings
vim.opt.timeoutlen = 1000  -- Time to wait for a mapped sequence to complete (ms)
vim.opt.ttimeoutlen = 10   -- Time to wait for a key code sequence to complete (ms)

-- Settings that work in both environments
vim.opt.tabstop = 4
vim.opt.softtabstop = 4
vim.opt.shiftwidth = 4
vim.opt.expandtab = false
vim.opt.smartindent = true

-- Settings only for standalone Neovim
if vscode.is_standalone() then
    vim.opt.nu = true
    vim.opt.relativenumber = true
    vim.opt.wrap = false
    vim.opt.hlsearch = false
    vim.opt.incsearch = true
    vim.opt.termguicolors = true
end
