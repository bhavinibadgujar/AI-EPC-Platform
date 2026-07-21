$ErrorActionPreference = "Stop"

$baseUrl = $env:AI_EPC_API_URL
if (-not $baseUrl) {
    $baseUrl = "http://localhost:8000"
}

Invoke-RestMethod -Method Post -Uri "$baseUrl/seed/reset"

Write-Host "Demo seed reset complete at $baseUrl"
Write-Host "Sample files:"
Write-Host "  demo/sample_spec.txt"
Write-Host "  demo/sample_vendor_submittal.txt"
Write-Host "  demo/sample_schedule.csv"
