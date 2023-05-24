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

# --------------------------------------------------------
# API

import autoload "../lib/condafuncs.vim"

if !exists(":CondaChangeEnv")
    command CondaChangeEnv call <SID>condafuncs.CondaChangeEnv()
endif

if !exists(":CondaActivate")
    command -nargs=? CondaActivate
                \ call <SID>condafuncs.CondaActivateUser(<f-args>)
endif

# CondaChangeEnv()
# CondaActivateUser("myenv")
