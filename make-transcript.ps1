# Define log directory
$logDir = "C:\Users\missk\Williope\kelvin-stardate\logs"

# Ensure directory exists
if (-not (Test-Path $logDir)) {
    New-Item -ItemType Directory -Path $logDir | Out-Null
}

# Capture start time
$startTime = Get-Date
$startStamp = $startTime.ToString("yyyy-MM-dd_HH-mm-ss")

# Temporary transcript path
$tempLog = Join-Path $logDir "terminal_log_${startStamp}_IN_PROGRESS.txt"

# Start transcript
Start-Transcript -Path $tempLog -Append
