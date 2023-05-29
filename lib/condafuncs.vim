vim9script

export def SetEnvVariablesWin(env: string, prefix: string)
        # This should be the only function of the plugin that kinda depends on the OS
        # TODO: This is how Windows installs Miniconda: many folders!
        # I expect this to be uniformed to other OS:s in the future
        # C:\Users\yt75534\Miniconda3;
        # C:\Users\yt75534\Miniconda3\Library\mingw-w64\bin;
        # C:\Users\yt75534\Miniconda3\Library\usr\bin;
        # C:\Users\yt75534\Miniconda3\Library\bin;
        # C:\Users\yt75534\Miniconda3\Scripts;
        # C:\Users\yt75534\Miniconda3\bin;

        # C:\Users\yt75534\Miniconda3\envs\myenv;
        # C:\Users\yt75534\Miniconda3\envs\myenv\Library\mingw-w64\bin;
        # C:\Users\yt75534\Miniconda3\envs\myenv\Library\usr\bin;
        # C:\Users\yt75534\Miniconda3\envs\myenv\Library\bin;
        # C:\Users\yt75534\Miniconda3\envs\myenv\Scripts;
        # C:\Users\yt75534\Miniconda3\envs\myenv\bin;
        #
        # Then, you have the following that are always present
        # C:\Users\yt75534\Miniconda3;
        # C:\Users\yt75534\Miniconda3\condabin;
        #
        # Therefore, if C:\Users\yt75534\Miniconda3 is added and removed, you
        # always have a second one.
        #
        # 1) Set environment variables
        g:conda_current_env = env

        $CONDA_DEFAULT_ENV = env
        $CONDA_PROMPT_MODIFIER = $"({env})"

        # Remove old folders
        var path1 = g:conda_current_prefix .. "\\Library\\mingw-w64\\bin"
        var path2 = g:conda_current_prefix .. "\\Library\\usr\\bin"
        var path3 = g:conda_current_prefix .. "\\Library\\bin"
        var path4 = g:conda_current_prefix .. "\\Scripts"
        var path5 = g:conda_current_prefix .. "\\bin"
        var conda_paths = [g:conda_current_prefix, path1, path2, path3, path4, path5]

        var path_lst = split($PATH, ';')
        for path in conda_paths
            remove(path_lst, index(path_lst, path))
        endfor

        # Add new folders
        path1 = prefix .. "\\Library\\mingw-w64\\bin"
        path2 = prefix .. "\\Library\\usr\\bin"
        path3 = prefix .. "\\Library\\bin"
        path4 = prefix .. "\\Scripts"
        path5 = prefix .. "\\bin"
        conda_paths = [prefix, path1, path2, path3, path4, path5]
        path_lst = conda_paths + path_lst
        g:conda_current_prefix = prefix
        $PATH = join(path_lst, ';')

        # 2) Set Vim options
        &pythonthreehome =  g:conda_current_prefix
        &pythonthreedll = g:conda_current_prefix .. "\\python"
        $CONDA_PYTHON_EXE = g:conda_current_prefix .. "\\python"

        # 3) Set internal sys.path
        # TODO The following seems to be independent of the current env in
        # windows, just compare the output of :python3 print(sys.path) from
        # different venv in windows
        #
        # var new_paths = prefix .. "/lib/site-packages"
        # g:sys_path = add(g:conda_py_globals, new_paths)
        # python3 import vim
        # python3 sys.path = vim.eval("g:sys_path")
        # The following don't seem to be needed as Vim use the Unix format for
        # setting environment variables and we already set them.
        # python3 os.environ["CONDA_DEFAULT_ENV"] = vim.eval("g:conda_current_env")
        # python3 os.environ["PATH"] = vim.eval("$PATH")
enddef

export def SetEnvVariables(env: string, prefix: string)
        # This should be the only function of the plugin that kinda depends on the OS

        # 1) Set environment variables
        g:conda_current_env = env

        $CONDA_DEFAULT_ENV = env
        $CONDA_PROMPT_MODIFIER = $"({env})"

        var path_lst = split($PATH, ':')
        var old_path = g:conda_current_prefix .. "/bin"
        var new_path = prefix .. "/bin"
        remove(path_lst, index(path_lst, old_path))
        # Conda's python on top in case of multiple python installations
        path_lst = [new_path] + path_lst

        $PATH = join(path_lst, ':')

        # 2) Set Vim options
        # TODO: the pythonthreedll is wrong.
        &pythonthreehome =  prefix
        &pythonthreedll = prefix .. "/bin/python"
        $CONDA_PYTHON_EXE = prefix .. "/bin/python"

        # 3) Set internal sys.path
        # TODO: check python3 print(sys.path). This is weird and may need a
        # fix.
        # Do something like
        var py_ver_dot = system('python --version')->matchstr('\d\+.\d\+') # e.g. 3.11
        var py_ver_nodot = substitute(py_ver_dot, '\.', '', 'g') # e.g.  311
        # Paths to remove
        var path1 = g:conda_current_prefix .. $"/lib/python{py_ver_nodot}.zip"
        var path2 = g:conda_current_prefix .. $"/lib/python{py_ver_dot}"
        var path3 = g:conda_current_prefix .. $"/lib/python{py_ver_dot}/lib-dynload"
        var path4 = g:conda_current_prefix .. $"/lib/python{py_ver_dot}/site-packages"
        var paths = [path1, path2, path3, path4]
        g:python_sys_path = py3eval('sys.path')

        for path in paths
            remove(g:python_sys_path, index(g:python_sys_path, path))
        endfor

        path1 = prefix .. $"/lib/python{py_ver_nodot}.zip"
        path2 = prefix .. $"/lib/python{py_ver_dot}"
        path3 = prefix .. $"/lib/python{py_ver_dot}/lib-dynload"
        path4 = prefix .. $"/lib/python{py_ver_dot}/site-packages"
        paths = [path1, path2, path3, path4]
        g:python_sys_path = paths + g:python_sys_path

        echom $"g:python_sys_path: {g:python_sys_path}"

        # Add paths
        # OBS! This may not be needed!
        # var new_paths = prefix .. "/lib/site-packages"
        # g:sys_path = add(g:conda_py_globals, new_paths)
        python3 import vim
        python3 sys.path = vim.eval("g:python_sys_path")
        # The following don't seem to be needed as Vim use the Unix format for
        # setting environment variables and we already set them.
        # python3 os.environ["CONDA_DEFAULT_ENV"] = vim.eval("g:conda_current_env")
        # python3 os.environ["PATH"] = vim.eval("$PATH")
        #

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

export def CondaComplete(arglead: string, cmdline: string, cursorPos: number): list<string>
    # This is used in "command -preview=..." in the plugin file.
    return g:conda_envs->filter((_, val) => val =~ $'^{arglead}')
enddef
