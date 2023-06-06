vim9script

export def SetEnvVariablesWin(env: string, prefix: string)
    # This should be the only function of the plugin that kinda depends on the
    # OS
    # This is how Windows installs Miniconda: many folders!
    # I expect this to be uniformed to other OS:s in the future
    # This is 'base'
    # C:\Users\yt75534\Miniconda3;
    # C:\Users\yt75534\Miniconda3\Library\mingw-w64\bin;
    # C:\Users\yt75534\Miniconda3\Library\usr\bin;
    # C:\Users\yt75534\Miniconda3\Library\bin;
    # C:\Users\yt75534\Miniconda3\Scripts;
    # C:\Users\yt75534\Miniconda3\bin;

    # This is 'myenv'
    # C:\Users\yt75534\Miniconda3\envs\myenv;
    # C:\Users\yt75534\Miniconda3\envs\myenv\Library\mingw-w64\bin;
    # C:\Users\yt75534\Miniconda3\envs\myenv\Library\usr\bin;
    # C:\Users\yt75534\Miniconda3\envs\myenv\Library\bin;
    # C:\Users\yt75534\Miniconda3\envs\myenv\Scripts;
    # C:\Users\yt75534\Miniconda3\envs\myenv\bin;
    #
    # Then, you have the following that shall be always present
    # C:\Users\yt75534\Miniconda3\condabin;
    #
    # 1) Set environment variables -------------------------------------
    g:conda_current_env = env

    $CONDA_DEFAULT_ENV = env
    $CONDA_PROMPT_MODIFIER = $"({env})"

    # Remove old paths
    var path_lst = split($PATH, ';')
    var path_lst_cleaned = path_lst
                \->filter('stridx(v:val, g:conda_current_prefix) != 0')

    # Add new paths
    var path1 = prefix .. "\\Library\\mingw-w64\\bin"
    var path2 = prefix .. "\\Library\\usr\\bin"
    var path3 = prefix .. "\\Library\\bin"
    var path4 = prefix .. "\\Scripts"
    var path5 = prefix .. "\\bin"
    var path6 = "" # This is /condabin for conda command
    # Check if /condabin disappeared
    if index(path_lst_cleaned, g:conda_base_prefix .. "\\condabin") == -1
        path6 = g:conda_base_prefix .. "\\condabin"
    endif
    var conda_paths = [prefix, path1, path2, path3, path4, path5, path6]
    path_lst = conda_paths + path_lst_cleaned
    $PATH = join(path_lst, ';')
    $CONDA_PYTHON_EXE = prefix .. "\\bin\\python.exe"

    # 2) Set Vim options ----------------------------------------------
    # var py_ver_dot = system('python --version')
    var py_ver_dot = system($CONDA_PYTHON_EXE .. ' --version')
                \->matchstr('\d\+.\d\+') # e.g. 3.11
    var py_ver_nodot = substitute(py_ver_dot, '\.', '', 'g') # e.g.  311
    &pythonthreehome =  prefix
    &pythonthreedll = prefix .. $"\\python{py_ver_nodot}.dll"


    # 3) Set vim internal sys.path ------------------------------------
    # Remove previous env paths
    # TODO: Not sure if
    # 'C:\Users\yt75534\AppData\Roaming\Python\Python310\site-packages',
    # shall be actually removed.
    g:python_sys_path = py3eval('sys.path')
    g:python_sys_path_cleaned = g:python_sys_path
                \->filter('stridx(v:val, g:conda_current_prefix) != 0')

    # Define new paths
    var sys_path1 = prefix .. $"\\python{py_ver_nodot}.zip"
    var sys_path2 = prefix .. "\\DLLs"
    var sys_path3 = prefix .. "\\lib"
    var sys_path4 = prefix .. "\\lib\\site-packages"
    var sys_path5 = prefix .. "\\lib\\site-packages\\win32"
    var sys_path6 = prefix .. "\\lib\\site-packages\\win32\\lib"
    var sys_path7 = prefix .. "\\lib\\site-packages\\Pythonwin"
    var sys_paths = [prefix, sys_path1, sys_path2, sys_path3,
                \ sys_path4, sys_path5, sys_path6, sys_path7]
    g:python_sys_path = sys_paths + g:python_sys_path_cleaned

    # Add paths to sys.path
    python3 import vim
    python3 sys.path = vim.eval("g:python_sys_path")

    # Refresh variables
    g:conda_current_prefix = prefix
enddef

export def SetEnvVariables(env: string, prefix: string)

    # 1) Set environment variables ----------------------------
    g:conda_current_env = env

    $CONDA_DEFAULT_ENV = env
    $CONDA_PROMPT_MODIFIER = $"({env})"

    # Remove old path (g:conda_current_prefix)
    var path_lst = split($PATH, ':')
    # The following filtering may not be needed because for MacOSX and Linux
    # conda creates only ONE folder and not 200000 like in Windows.
    # You could simply cherry-pick
    #
    #   var old_path = g:conda_current_prefix .. "/bin"
    #   remove(path_lst, index(path_lst, old_path))
    #
    # and use path_lst = [new_path] + path_lst_cleaned
    var path_lst_cleaned = path_lst
                \->filter('stridx(v:val, g:conda_current_prefix) != 0')

    # Add new path (prefix)
    var new_path = prefix .. "/bin"
    # Conda's python on top in case of multiple python installations
    path_lst = [new_path] + path_lst_cleaned
    $PATH = join(path_lst, ':')
    $CONDA_PYTHON_EXE = prefix .. "/bin/python"


    # 2) Set Vim options -----------------------------------
    # var py_ver_dot = system('python --version')
    var py_ver_dot = system($CONDA_PYTHON_EXE .. ' --version')
                \->matchstr('\d\+.\d\+') # e.g. 3.11
    var py_ver_nodot = substitute(py_ver_dot, '\.', '', 'g') # e.g.  311
    &pythonthreehome =  prefix
    &pythonthreedll = prefix .. $"/lib/libpython{py_ver_dot}.dylib"


    # 3) Set internal sys.path -----------------------------------
    # Paths to remove
    #
    g:python_sys_path = py3eval('sys.path')
    g:python_sys_path_cleaned = g:python_sys_path
                \->filter('stridx(v:val, g:conda_current_prefix) != 0')

    # Paths to add
    var path1 = prefix .. $"/lib/python{py_ver_nodot}.zip"
    var path2 = prefix .. $"/lib/python{py_ver_dot}"
    var path3 = prefix .. $"/lib/python{py_ver_dot}/lib-dynload"
    var path4 = prefix .. $"/lib/python{py_ver_dot}/site-packages"
    var paths = [path1, path2, path3, path4]
    g:python_sys_path = paths + g:python_sys_path_cleaned

    # Add paths
    python3 import vim
    python3 sys.path = vim.eval("g:python_sys_path")

    # Refresh variables
    g:conda_current_prefix = prefix
enddef

def CondaActivateUser(env: string)
    var prefixes = {}
    var key = ""
    for prefix in g:conda_prefixes
        key = fnamemodify(prefix, ":t")
        prefixes[key] = prefix
    endfor

    if index(keys(prefixes), env) == -1
        echo $"{env} environment not found."
    elseif has('win32')
        SetEnvVariablesWin(env, prefixes[env])
    else
        SetEnvVariables(env, prefixes[env])
    endif
enddef

def CondaActivatePopupCallback(id: number, env_idx: number)
    # Callback of the popup menu.
    var target_prefix = g:conda_prefixes[env_idx - 1]
    var target_env = fnamemodify(target_prefix, ":t")
    if has('win32')
        SetEnvVariablesWin(target_env, target_prefix)
    else
        SetEnvVariables(target_env, target_prefix)
    endif
enddef


def CondaActivatePopup()
    # Actual popup menu
    popup_menu(g:conda_envs,
        {'title': " envs ",
            'borderchars': ['─', '│', '─', '│', '╭', '╮', '╯', '╰'],
            'callback': CondaActivatePopupCallback,
        })
enddef


export def CondaActivate(...env: list<string>)
    if empty(env)
        CondaActivatePopup()
    else
        CondaActivateUser(env[0])
    endif
enddef

export def CondaComplete(arglead: string, cmdline: string, cursorPos: number):
            \ list<string>
    # This is used in "command -preview=..." in the plugin file.
    return g:conda_envs->filter((_, val) => val =~ $'^{arglead}')
enddef
