# Path: C:\ProgramasGodMode\ClaudeCode-Dashboard\Configure-ClaudeCode-AuthorizedDirectories.ps1
# Persistent additional directories for Claude Code; no permission bypass is enabled.
$ErrorActionPreference = 'Stop'
$settingsPath = Join-Path $env:USERPROFILE '.claude\settings.json'
if (-not (Test-Path -LiteralPath $settingsPath)) {
    New-Item -ItemType Directory -Path (Split-Path -Parent $settingsPath) -Force | Out-Null
    [System.IO.File]::WriteAllText($settingsPath, '{}', (New-Object System.Text.UTF8Encoding($false)))
}
# Explicit UTF-8 avoids corrupting non-ASCII Windows profile names in Windows PowerShell 5.1.
$settings = [System.IO.File]::ReadAllText($settingsPath, [System.Text.Encoding]::UTF8) | ConvertFrom-Json
if ($null -eq $settings.permissions) {
    $settings | Add-Member -NotePropertyName permissions -NotePropertyValue ([pscustomobject]@{}) -Force
}
$approved = @(
    'C:\AI',
    'C:\AndreOS-Memory',
    'C:\AndreOS-Memory-LEGACY-2026-10-07',
    'C:\CloneZIP',
    'C:\DevopGodMode',
    'C:\DevopsGodMode',
    'C:\Lords Mobile PC',
    'C:\Programas',
    'C:\ProgramasGodMode',
    'C:\ProgramData',
    'C:\ProjectFlux',
    'C:\ProjectMind',
    'C:\Projects',
    'C:\WinClean',
    'C:\Program Files (x86)'
)
$userHome = $env:USERPROFILE
$approved += @(
    (Join-Path $userHome 'OneDrive'),
    (Join-Path $userHome 'Documents'),
    (Join-Path $userHome 'Os Meus Documentos'),
    (Join-Path $userHome 'Downloads'),
    (Join-Path $userHome 'Music'),
    (Join-Path $userHome 'Videos'),
    (Join-Path $userHome '3D Objects'),
    (Join-Path $userHome 'Contacts'),
    (Join-Path $userHome 'Favorites'),
    (Join-Path $userHome 'Links'),
    (Join-Path $userHome 'Saved Games'),
    (Join-Path $userHome 'Searches'),
    (Join-Path $userHome 'Modelos'),
    [Environment]::GetFolderPath('Desktop'),
    [Environment]::GetFolderPath('MyDocuments'),
    [Environment]::GetFolderPath('MyPictures'),
    [Environment]::GetFolderPath('MyMusic'),
    [Environment]::GetFolderPath('MyVideos'),
    (Join-Path $userHome 'OneDrive\Ambiente de Trabalho'),
    (Join-Path $userHome 'OneDrive\Documentos'),
    (Join-Path $userHome 'OneDrive\Imagens'),
    (Join-Path $userHome 'OneDrive\Transferências'),
    (Join-Path $userHome 'OneDrive\Anexos'),
    (Join-Path $userHome 'OneDrive\Vídeos')
)
$approved = @($approved | Where-Object { $_ -and (Test-Path -LiteralPath $_ -PathType Container) } | ForEach-Object { ([string]$_).TrimEnd('\') } | Sort-Object -Unique)
$existing = @()
if ($settings.permissions.PSObject.Properties.Name -contains 'additionalDirectories' -and $settings.permissions.additionalDirectories) {
    $excludedDirectory = Join-Path 'C:\' 'Program Files'
    # Rebuild this feature's profile paths from the live Windows profile to avoid duplicates or encoding variants.
    # Preserve unrelated additional directories outside C:\Users.
    $existing = @($settings.permissions.additionalDirectories | Where-Object { $_ -ine $excludedDirectory -and $_ -notlike 'C:\Users\*' })
}
$merged = @($existing + $approved | Where-Object { $_ } | Sort-Object -Unique)
$backup = "$settingsPath.backup-$(Get-Date -Format 'yyyyMMdd-HHmmss')"
Copy-Item -LiteralPath $settingsPath -Destination $backup -Force
$settings.permissions | Add-Member -NotePropertyName additionalDirectories -NotePropertyValue $merged -Force
$json = $settings | ConvertTo-Json -Depth 100
[System.IO.File]::WriteAllText($settingsPath, $json, (New-Object System.Text.UTF8Encoding($false)))
Write-Output "Settings updated: $settingsPath"
Write-Output "Backup created: $backup"
Write-Output "Authorized existing directories: $($approved.Count)"
$approved | ForEach-Object { Write-Output "AUTHORIZED | $_" }
Write-Output "Global permission mode and bypass settings were not changed."
