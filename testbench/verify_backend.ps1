# Verify that the Learning Analytics backend is running and responding.
# Run this from any directory after starting the backend (default: http://localhost:8000).
# Usage: .\verify_backend.ps1   or   powershell -File verify_backend.ps1

$baseUrl = "http://localhost:8000"
Write-Host "Checking backend at $baseUrl ..." -ForegroundColor Cyan

try {
    $response = Invoke-RestMethod -Uri $baseUrl -Method Get -ErrorAction Stop
    Write-Host "OK - Backend is running." -ForegroundColor Green
    Write-Host "Response: $($response | ConvertTo-Json -Compress)"
    exit 0
} catch {
    Write-Host "FAIL - Backend did not respond. Is it running on port 8000?" -ForegroundColor Red
    Write-Host $_.Exception.Message
    exit 1
}
