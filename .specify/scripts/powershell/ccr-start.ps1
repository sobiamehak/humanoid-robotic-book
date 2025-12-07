<#
.SYNOPSIS
Starts a Claude Code Review (CCR) session.

.DESCRIPTION
This script initializes a Claude Code Review session by setting up the necessary
context and preparing the environment for AI-assisted code review.

.EXAMPLE
PS> .\ccr-start.ps1

Initializes the Claude Code Review session.
#>

param(
    [string]$ProjectRoot = $PSScriptRoot,
    [string]$SessionName = "default"
)

Write-Host "Starting Claude Code Review (CCR) session..." -ForegroundColor Green

# Find the project root by looking for package.json
while ((Test-Path "$ProjectRoot\package.json") -eq $false) {
    $ProjectRoot = Split-Path $ProjectRoot -Parent
    if ($ProjectRoot -eq "" -or $ProjectRoot -eq "/") {
        Write-Error "Could not find project root (directory with package.json)"
        return
    }
}

Write-Host "Project root found: $ProjectRoot" -ForegroundColor Cyan

# Create or update context for the session
$contextFile = Join-Path $ProjectRoot ".claude"
$contextFile = Join-Path $contextFile "session-context.json"
$contextDir = Split-Path $contextFile -Parent

if (!(Test-Path $contextDir)) {
    New-Item -ItemType Directory -Path $contextDir -Force | Out-Null
}

$context = @{
    projectRoot = $ProjectRoot
    sessionName = $SessionName
    startTime = Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ"
    ccrVersion = "1.0.0"
    active = $true
}

$context | ConvertTo-Json | Out-File -FilePath $contextFile -Encoding UTF8

Write-Host "CCR session context created/updated at: $contextFile" -ForegroundColor Cyan

# Check prerequisites
Write-Host "Checking prerequisites..." -ForegroundColor Yellow

# Check if Node.js is available
if (Get-Command node -ErrorAction SilentlyContinue) {
    $nodeVersion = node --version
    Write-Host "Node.js $nodeVersion found" -ForegroundColor Green
} else {
    Write-Warning "Node.js not found. Some functionality may be limited."
}

# Check if Git is available
if (Get-Command git -ErrorAction SilentlyContinue) {
    Write-Host "Git found" -ForegroundColor Green
    $currentBranch = git rev-parse --abbrev-ref HEAD 2>$null
    if ($currentBranch) {
        Write-Host "Current Git branch: $currentBranch" -ForegroundColor Cyan
    }
}
else {
    Write-Warning "Git not found. Version control features will be limited."
}

Write-Host ""
Write-Host "Claude Code Review session initialized successfully!" -ForegroundColor Green
Write-Host "Session: $SessionName" -ForegroundColor Green
Write-Host "Started: $(Get-Date)" -ForegroundColor Green
Write-Host ""
Write-Host "You can now begin your code review session with Claude." -ForegroundColor Yellow
Write-Host "The session context has been saved to .claude/session-context.json" -ForegroundColor Yellow