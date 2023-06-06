vim9script noclear

# Activate conda environments inside Vim.
# Maintainer:	Ubaldo Tiberi
# GetLatestVimScripts: 6074 1 :AutoInstall: outline.vim
# License: BSD3-Clause.

if !has('vim9script') ||  v:version < 900
    # Needs Vim version 9.0 and above
    echo "You need at least Vim 9.0"
    finish
endif

if exists('g:conda_loaded')
    finish
endif
g:conda_loaded = true

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
    # g:conda_current_env = g:conda_info["active_prefix_name"]
    g:conda_current_env = $CONDA_DEFAULT_ENV
endif

if !exists('g:conda_current_prefix')
    # This also may be redundant
    # g:conda_current_prefix =  g:conda_info["active_prefix"]
    # TODO: Does the following holds for Windows? It should...
    if $CONDA_DEFAULT_ENV ==# "base"
        g:conda_current_prefix = $CONDA_PREFIX
    else
        g:conda_current_prefix = $CONDA_PREFIX .. "/envs/" .. $CONDA_DEFAULT_ENV
    endif
endif

if !exists('g:conda_prefixes') && !exists('g:conda_envs')
    g:conda_prefixes = g:conda_info["envs"]
    g:conda_envs = []
    for env in g:conda_prefixes
        add(g:conda_envs, fnamemodify(env, ":t"))
    endfor
endif

# ---------------------------------------------------
# Init
import autoload "../lib/condafuncs.vim"

if has('win32')
    condafuncs.SetEnvVariablesWin(g:conda_current_env, g:conda_current_prefix)
else
    condafuncs.SetEnvVariables(g:conda_current_env, g:conda_current_prefix)
endif

# --------------------------------------------------------
# API
if !exists(":CondaActivate")
    command -nargs=? -complete=customlist,condafuncs.CondaComplete
                \ CondaActivate call <SID>condafuncs.CondaActivate(<f-args>)
endif
