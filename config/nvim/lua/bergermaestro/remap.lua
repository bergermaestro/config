local vscode = require("bergermaestro.vscode")

print("remap file run")

-- File explorer - only in standalone Neovim
if vscode.is_standalone() then
    vim.keymap.set("n", "<leader>pv", vim.cmd.Ex)
end

-- Move lines up/down in visual mode (works in both environments)
vim.keymap.set("v", "J", ":m '>+1<CR>gv=gv")
vim.keymap.set("v", "K", ":m '>-2<CR>gv=gv")

-- Join lines and keep cursor position
vim.keymap.set("n", "J", "mzJ`z")

--vim.keymap.set("x", "<leader>p", "\"_dP")

-- Yank to system clipboard (works in both environments)
vim.keymap.set("n", "<leader>y", "\"+y")
vim.keymap.set("v", "<leader>y", "\"+y")
vim.keymap.set("n", "<leader>Y", "\"+Y")

-- Disable Q
vim.keymap.set("n", "Q", "<nop>")

-- Format - different behavior for VS Code vs standalone
if vscode.is_vscode() then
    -- In VS Code, use VS Code's format command
    vim.keymap.set("n", "<leader>f", "<Cmd>call VSCodeNotify('editor.action.formatDocument')<CR>")
else
    -- In standalone Neovim, use LSP format
    vim.keymap.set("n", "<leader>f", vim.lsp.buf.format)
end

-- Search and replace current word
vim.keymap.set("n", "<leader>s", [[:%s/\<<C-r><C-w>\>/<C-r><C-w>/gI<Left><Left><Left>]])

-- Window splits (works in both environments)
vim.keymap.set("n", "<C-w>|", "<C-w>v")
vim.keymap.set("n", "<C-w>-", "<C-w>s")

