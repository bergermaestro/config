-- VS Code specific remaps
local vscode = require("bergermaestro.vscode")

-- Only load these remaps in VS Code
if not vscode.is_vscode() then
    return
end

-- File navigation
vim.keymap.set("n", "<leader>pf", "<Cmd>call VSCodeNotify('workbench.action.quickOpen')<CR>")
vim.keymap.set("n", "<leader>ps", "<Cmd>call VSCodeNotify('workbench.action.findInFiles')<CR>")

-- File explorer
vim.keymap.set("n", "<leader>pv", "<Cmd>call VSCodeNotify('workbench.view.explorer')<CR>")

-- Git
vim.keymap.set("n", "<leader>gs", "<Cmd>call VSCodeNotify('workbench.view.scm')<CR>")

-- Terminal
vim.keymap.set("n", "<leader>t", "<Cmd>call VSCodeNotify('workbench.action.terminal.toggleTerminal')<CR>")

-- Command palette
vim.keymap.set("n", "<leader>:", "<Cmd>call VSCodeNotify('workbench.action.showCommands')<CR>")

-- Go to definition/references
vim.keymap.set("n", "gd", "<Cmd>call VSCodeNotify('editor.action.revealDefinition')<CR>")
vim.keymap.set("n", "gr", "<Cmd>call VSCodeNotify('editor.action.goToReferences')<CR>")

-- Rename symbol
vim.keymap.set("n", "<leader>rn", "<Cmd>call VSCodeNotify('editor.action.rename')<CR>")

-- Show hover
vim.keymap.set("n", "K", "<Cmd>call VSCodeNotify('editor.action.showHover')<CR>")

-- Navigate between problems
vim.keymap.set("n", "[d", "<Cmd>call VSCodeNotify('editor.action.marker.prevInFiles')<CR>")
vim.keymap.set("n", "]d", "<Cmd>call VSCodeNotify('editor.action.marker.nextInFiles')<CR>")

-- Code actions
vim.keymap.set("n", "<leader>ca", "<Cmd>call VSCodeNotify('editor.action.quickFix')<CR>")

-- Fold/unfold
vim.keymap.set("n", "za", "<Cmd>call VSCodeNotify('editor.toggleFold')<CR>")
vim.keymap.set("n", "zR", "<Cmd>call VSCodeNotify('editor.unfoldAll')<CR>")
vim.keymap.set("n", "zM", "<Cmd>call VSCodeNotify('editor.foldAll')<CR>")

-- Cursor Chat (In progress)
vim.keymap.set("v", "<leader>cc", "<Cmd>call VSCodeNotifyVisual('composer.sendToAgent', 1)<CR>")
vim.keymap.set("n", "<leader>cc", "<Cmd>call VSCodeNotify('composer.sendToAgent')<CR>")
vim.keymap.set("v", "<leader>ca", "<Cmd>call VSCodeNotifyVisual('composer.sendToAgent', 1)<CR>")
vim.keymap.set("n", "<leader>ca", "<Cmd>call VSCodeNotify('composer.sendToAgent')<CR>")
vim.keymap.set("n", "<leader>ch", "<Cmd>call VSCodeNotify('composer.startComposerPrompt')<CR>")
vim.keymap.set("v", "<leader>cq", "<Cmd>call VSCodeNotifyVisual('cursor.quickQuestion', 1)<CR>")
vim.keymap.set("n", "<leader>cq", "<Cmd>call VSCodeNotify('cursor.quickQuestion')<CR>")
