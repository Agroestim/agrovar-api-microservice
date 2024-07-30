function Invoke-Venv() {
    Write-Host "Trying to invoke a Python Virtual Environment" -ForegroundColor White -BackgroundColor Blue

    # Check if exist an active virtual env.
    if ($env:VIRTUAL_ENV) {
        [System.Media.SystemSounds]::Asterisk.Play()
        Write-Host "Already exist an active virtual env" -ForegroundColor White -BackgroundColor Blue
        exit 1
    }

    # Check if exist any virtual environment directore over the path.
    if (!(Test-Path -Path "./venv")) {
        Write-Host "No venv path found" -ForegroundColor White -BackgroundColor Red
        exit 1
    }

    # Execute the venv activate script.
    .(Get-ChildItem -Path ".\venv\Scripts\Activate.ps1")
}