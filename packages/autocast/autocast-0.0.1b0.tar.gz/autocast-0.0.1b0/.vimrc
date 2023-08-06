" ale configs
let g:ale_linters = {'python': ['mypy', 'ruff']}

let g:ale_fixers = {}
let g:ale_fixers.python = ['black', 'ruff']

nnoremap <F12> :ALEFix<CR>
