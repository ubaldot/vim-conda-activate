vim9script noclear

# Activate conda environments inside Vim.
# Maintainer:	Ubaldo Tiberi
# GetLatestVimScripts: 6068 1 :AutoInstall: outline.vim
# License: Vim license

if !has('vim9script') ||  v:version < 900
  # Needs Vim version 9.0 and above
  echo "You need at least Vim 9.0"
  finish
endif

if exists('g:conda_loaded')
    finish
endif
g:conda_loaded = true

# The commented line should not be needed.
# python3 if vim.eval('expand("<sfile>:p:h")') not in sys.path: sys.path.append(vim.eval('expand("<sfile>:p:h")'))
g:conda_py_globals = py3eval('sys.path')

# Initialize Conda info.
if !exists('g:conda_info')
    g:conda_info = json_decode(system('conda info --json'))
endif

if !exists('g:conda_base_prefix')
    g:conda_base_prefix = g:conda_info["conda_prefix"]
    # This syntax appear to work both on Windows and Linux/OSX.
    # This should be where conda command is located.
    $CONDA_PREFIX = g:conda_base_prefix
endif

if !exists('g:conda_current_env')
    # This may be redundant with $CONDA_DEFAULT_ENV
    g:conda_current_env = g:conda_info["active_prefix_name"]
endif

if !exists('g:conda_current_prefix')
    # This also may be redundant
    g:conda_current_prefix =  g:conda_info["active_prefix"]
endif

if !exists('g:conda_prefixes') && !exists('g:conda_envs')
    g:conda_prefixes = g:conda_info["envs"]
    g:conda_envs = []
    for env in g:conda_prefixes
        add(g:conda_envs, fnamemodify(env, ":t"))
    endfor
endif


# --------------------------------------------------------
# API
import autoload "../lib/condafuncs.vim"

if !exists(":CondaActivate")
    command -nargs=? -complete=customlist,condafuncs.CondaComplete
            \ CondaActivate call <SID>condafuncs.CondaActivate(<f-args>)
endif
