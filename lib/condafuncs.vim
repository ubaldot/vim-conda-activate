vim9script

def SetEnvVariables(env: string, prefix: string)
        # This should be the only function of the plugin that kinda depends on the OS

        # 1) Set environment variables
        g:conda_current_env = env

        $CONDA_DEFAULT_ENV = env
        $CONDA_PROMPT_MODIFIER = $"({env})"

        var path_lst = split($PATH, ':')
        remove(path_lst, index(path_lst, g:conda_current_prefix .. "/bin"))
        add(path_lst, prefix .. "/bin")
        g:conda_current_prefix = prefix
        $PATH = join(path_lst, ':')

        # 2) Set Vim options
        &pythonthreehome = fnamemodify(trim(system("which python")), ":h:h")
        &pythonthreedll = trim(system("which python"))

        # 3) Set internal sys.path
        var new_paths = prefix .. "/lib/site-packages"
        g:sys_path = add(g:conda_py_globals, new_paths)
        python3 import vim
        python3 sys.path = vim.eval("g:sys_path")
        # The following don't seem to be needed as Vim use the Unix format for
        # setting environment variables and we already set them.
        # python3 os.environ["CONDA_DEFAULT_ENV"] = vim.eval("g:conda_current_env")
        # python3 os.environ["PATH"] = vim.eval("$PATH")
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
    else
        SetEnvVariables(env, prefixes[env])
    endif
enddef

def CondaActivatePopupCallback(id: number, env_idx: number)
    # Callback of the popup menu.
    var target_prefix = g:conda_prefixes[env_idx - 1]
    var target_env = fnamemodify(target_prefix, ":t")
    SetEnvVariables(target_env, target_prefix)
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
    return g:conda_envs->filter((_, val) => val =~ $'^{arglead}')
enddef
