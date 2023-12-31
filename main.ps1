function install_Python() {
    Write-Host "You Dont have python3!"
    ./py.exe 
}
function download_data {
    .env/Scripts/python p.py

}
function install_pakgs {
    .env/Scripts/activate
    .env/Scripts/python -m pip install --upgrade pip
    $reqs = Get-Content('t.txt')
    $envlist = .env/Scripts/python.exe -m pip freeze
    $envlist_n = @()
    for ($i = 0; $i -lt $envlist.Count; $i++) {
        $pkg = $envlist[$i] 
        # -split "=="
        $pkgName = $pkg
        $envlist_n += $pkgName
    }
    for ($i = 0; $i -lt $reqs.Count; $i++) {
        $packg = $reqs[$i]
        # $packg
        if ($packg -in $envlist_n) {
        }
        else {
            "installing " + $packg
            .env/Scripts/pip install $packg
        }
    }   "all dependancies are good"
}
function installpip {
    try {
        .env/Scripts/pip --version
    }
    catch {
        python -m pip install --upgrade pip
    }
}

function mak_env {
    installpip
    pip install --upgrade pip
    pip install virtualenv
    python -m venv .env
    
    install_pakgs
}
function run {
    .env/Scripts/python.exe .\manage.py runserver
    # Start-Process  http://127.0.0.1:8000
    
    
}
function main_run {
    # mak_env
    $error.clear()
    if (!$error) {
        try {
            install_pakgs
            download_data
            run
            # "hellow"
        }
        catch {
            Write-Output "no env yet"
            mak_env
            install_pakgs
            download_data
            run
        }
    }
    $error.clear()

}

# $pyt = python --version


try {
    $pyt = python --version
    if ($pyt.Contains("P")) {
        Write-Host "python version is $pyt"
        main_run
    }
    else {
        
        "you must download python3"
        Start-Process https://www.python.org/downloads/
    }
    
}
catch {
    "nothing good"
}

# $python.GetType() 
