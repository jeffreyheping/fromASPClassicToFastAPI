# Start all backends with one command
# Usage: .\start-all.ps1
# Stop:  .\stop-all.ps1

$condaPath = "C:\Users\jeffr\anaconda3"
if (-not (Test-Path "$condaPath\Scripts\conda.exe")) {
    Write-Host "ERROR: Anaconda not found at $condaPath" -ForegroundColor Red
    exit 1
}

# Init conda for current session
& "$condaPath\Scripts\conda.exe" shell.powershell hook | Out-String | Invoke-Expression
conda activate base

$projects = @(
    @{Name="app-6"; Port=8006; App="app-6.main:app";      WorkDir=""},
    @{Name="app-5"; Port=8005; App="app-5.main:app";      WorkDir=""},
    @{Name="app-2"; Port=8002; App="app-2.main:app";      WorkDir=""},
    @{Name="app-1"; Port=8003; App="app-1.main:app";      WorkDir=""},
    @{Name="app"  ; Port=8000; App="app.main:app";        WorkDir=""},
    @{Name="app+1"; Port=8010; App="main:app";            WorkDir="app+1\backend"}
)

Write-Host "== Cleaning up ports ==" -ForegroundColor Yellow
foreach ($p in $projects) {
    $pid_line = netstat -ano 2>$null | Select-String ":$($p.Port).*LISTENING"
    if ($pid_line) {
        $proc_id = ($pid_line -split '\s+')[-1]
        Write-Host "  Port $($p.Port) in use by PID $proc_id, killing..." -ForegroundColor Red
        Stop-Process -Id $proc_id -Force -ErrorAction SilentlyContinue
    }
}

Write-Host ''
Write-Host "== Starting all backends ==" -ForegroundColor Green
foreach ($p in $projects) {
    $job = Start-Job -Name $p.Name -ScriptBlock {
        param($name, $port, $app, $condaPath, $workDir)
        $env:PATH = "$condaPath;$condaPath\Scripts;$condaPath\Library\bin;$env:PATH"
        Set-Location $workDir
        & "$condaPath\python.exe" -m uvicorn $app --host 0.0.0.0 --port $port --reload 2>&1 |
            ForEach-Object { "[$name] $_" }
    } -ArgumentList $p.Name, $p.Port, $p.App, $condaPath, (Join-Path (Get-Location) $p.WorkDir)

    Write-Host "  $($p.Name) -> http://localhost:$($p.Port)  (Job $($job.Id))"
}

Write-Host ''
Write-Host '== All backends started ==' -ForegroundColor Green
Write-Host 'Frontend (start separately):'
Write-Host '  app+1: cd app+1\frontend; npm run dev'
Write-Host ''
Write-Host 'View logs:  Receive-Job -Id <JobId>'
Write-Host 'Stop all:   .\stop-all.ps1'
Write-Host ''
Write-Host 'Ctrl+C does NOT stop background jobs. Use stop-all.ps1.'
