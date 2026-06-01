# Stop all backends
# Usage: .\stop-all.ps1

Write-Host "== Stopping background jobs ==" -ForegroundColor Yellow

$jobs = Get-Job
if ($jobs.Count -eq 0) {
    Write-Host "  No running jobs"
} else {
    foreach ($job in $jobs) {
        Write-Host "  Stopping $($job.Name) (Job $($job.Id))"
        Stop-Job -Id $job.Id
        Remove-Job -Id $job.Id
    }
}

Write-Host ''
Write-Host '== Cleaning up ports ==' -ForegroundColor Yellow
$ports = @(8006, 8005, 8002, 8003, 8000, 8010)
foreach ($port in $ports) {
    $pid_line = netstat -ano 2>$null | Select-String ":$port.*LISTENING"
    if ($pid_line) {
        $proc_id = ($pid_line -split '\s+')[-1]
        Write-Host "  Port $port -> PID $proc_id, killing" -ForegroundColor Red
        Stop-Process -Id $proc_id -Force -ErrorAction SilentlyContinue
    }
}

Write-Host ''
Write-Host '== All stopped ==' -ForegroundColor Green
