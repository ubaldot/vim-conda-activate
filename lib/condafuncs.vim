vim9script

def GetCondaInfoDict(): dict<any>
    var conda_info_str = system('conda info --json')
    return json_decode(conda_info_str)
enddef

# We made global variables to easy debugging if something goes wrong.
def UpdateCondaInfo()
    if !exists('g:conda_info')
        g:conda_info = GetCondaInfoDict()
    endif
    if !exists('g:conda_base_prefix')
        g:conda_base_prefix = g:conda_info["conda_prefix"]
        # TODO Win, Linux, OSX
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
    if !exists('g:conda_envs')
        g:conda_envs = g:conda_info["envs"]
    endif
enddef

def CondaActivateUser(env: string)
    UpdateCondaInfo()

    var prefixes = {}
    var key = ""
    for prefix in g:conda_envs
        key = fnamemodify(prefix, ":t")
        prefixes[key] = prefix
    endfor

    if index(keys(prefixes), env) == -1
        echo $"{env} environment not found."
    else
        SetEnvVariables(env, prefixes[env])
    endif
enddef

def SetEnvVariables(env: string, prefix: string)
        # This should be the only part of the script that depends on the OS
        #
        # 1) Set environment variables
        g:conda_current_env = env

        # TODO Win, Linux, OSX
        $CONDA_DEFAULT_ENV = env
        $CONDA_PROMPT_MODIFIER = $"({env})"

        # Adjust $PATH
        var bin = ""
        if has("win32")
            bin = "\\bin"
        else
            bin = "/bin"
        endif

        var path_lst = split($PATH, ':')
        remove(path_lst, index(path_lst, g:conda_current_prefix .. bin))
        add(path_lst, prefix .. bin)
        g:conda_current_prefix = prefix

        # TODO Win, Linux, OSX
        $PATH = join(path_lst, ':')

        # 2) Set Vim options
        &pythonthreehome = fnamemodify(trim(system("which python")), ":h:h")
        &pythonthreedll = trim(system("which python"))

        # 3) Set internal sys.path
        # TODO Win. Linux, Os
        var new_paths = prefix .. "/lib/site-packages"
        g:sys_path = add(g:conda_py_globals, new_paths)
        python3 import vim
        python3 sys.path = vim.eval("g:sys_path")
        # The following don't seem to be needed.
        # python3 os.environ["CONDA_DEFAULT_ENV"] = vim.eval("g:conda_current_env")
        # python3 os.environ["PATH"] = vim.eval("$PATH")
enddef


def CondaActivateCallback(id: number, env_idx: number)
    # Callback of the popup menu.
    var target_prefix = g:conda_envs[env_idx - 1]
    var target_env = fnamemodify(target_prefix, ":t")
    SetEnvVariables(target_env, target_prefix)
enddef


def CondaChangeEnv()
    # Selection through popup menu
    UpdateCondaInfo()
    # Names to be displayed in the popup menu
    var env_short_names = []
    for env in g:conda_envs
        add(env_short_names, fnamemodify(env, ":t"))
    endfor

    # Actual popup menu
    popup_menu(env_short_names,
        {'title': " envs ",
        'borderchars': ['─', '│', '─', '│', '╭', '╮', '╯', '╰'],
        'callback': CondaActivateCallback,
})
enddef
