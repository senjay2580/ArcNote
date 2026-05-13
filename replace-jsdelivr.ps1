# replace-jsdelivr.ps1
# 把 markdown 里的 jsDelivr URL 替换成 raw.githubusercontent.com URL
#
# 用法:
#   .\replace-jsdelivr.ps1 path\to\file.md              # 默认: 输出到 file.raw.md, 不覆盖原文件
#   .\replace-jsdelivr.ps1 path\to\file.md -Overwrite   # 覆盖原文件 (自动加 .bak_<时间戳> 备份)
#   .\replace-jsdelivr.ps1 path\to\file.md -Output other.md  # 指定输出路径

[CmdletBinding()]
param(
    [Parameter(Mandatory=$true, Position=0)]
    [string]$Path,

    [switch]$Overwrite,

    [string]$Output
)

$ErrorActionPreference = "Stop"
$env:HTTPS_PROXY = "http://127.0.0.1:6445"
$env:HTTP_PROXY  = "http://127.0.0.1:6445"

if (-not (Test-Path -LiteralPath $Path)) {
    Write-Host "File not found: $Path" -ForegroundColor Red
    exit 1
}

$filePath = (Resolve-Path -LiteralPath $Path).Path
$content  = Get-Content -Raw -LiteralPath $filePath -Encoding UTF8

$before = ([regex]::Matches($content, 'https://cdn\.jsdelivr\.net/gh/')).Count
if ($before -eq 0) {
    Write-Host "No jsDelivr URLs found in $filePath" -ForegroundColor Yellow
    exit 0
}

$new = $content -replace 'https://cdn\.jsdelivr\.net/gh/([^/]+)/([^/@]+)@([^/]+)/', 'https://raw.githubusercontent.com/$1/$2/$3/'
$leftover = ([regex]::Matches($new, 'https://cdn\.jsdelivr\.net/gh/')).Count
$rawCount = ([regex]::Matches($new, 'https://raw\.githubusercontent\.com/')).Count

# 决定输出路径
if ($Output) {
    $outPath = $Output
} elseif ($Overwrite) {
    $scriptDir  = Split-Path -Parent $PSCommandPath
    $backupRoot = Join-Path $scriptDir "_backups"
    $stamp      = Get-Date -Format "yyyyMMdd_HHmmss"

    # 在 _backups/ 下保留相对路径结构(若文件在脚本目录之外,只用文件名)
    if ($filePath.StartsWith($scriptDir, [StringComparison]::OrdinalIgnoreCase)) {
        $rel = $filePath.Substring($scriptDir.Length).TrimStart('\','/')
    } else {
        $rel = Split-Path -Leaf $filePath
    }
    $bak = Join-Path $backupRoot "$rel.bak_$stamp"
    New-Item -ItemType Directory -Force -Path (Split-Path -Parent $bak) | Out-Null

    Copy-Item -LiteralPath $filePath -Destination $bak -Force
    Write-Host "Backup: $bak" -ForegroundColor Cyan
    $outPath = $filePath
} else {
    $dir  = Split-Path -Parent $filePath
    $base = [System.IO.Path]::GetFileNameWithoutExtension($filePath)
    $ext  = [System.IO.Path]::GetExtension($filePath)
    $outPath = Join-Path $dir "$base.raw$ext"
}

Set-Content -LiteralPath $outPath -Value $new -Encoding UTF8 -NoNewline

Write-Host "Wrote: $outPath" -ForegroundColor Green
Write-Host ("Replaced: {0}  ->  raw URLs total: {1}  (leftover jsDelivr: {2})" -f $before, $rawCount, $leftover) -ForegroundColor Cyan

# 抽样验证 2 张图能否访问
$samples = [regex]::Matches($new, 'https://raw\.githubusercontent\.com/[^\s\)\]\"\<\>]+') |
    ForEach-Object { $_.Value } | Sort-Object -Unique | Select-Object -First 2

if ($samples.Count -gt 0) {
    Write-Host "Sample verification:"
    foreach ($u in $samples) {
        try {
            $r = Invoke-WebRequest -Uri $u -Method Head -TimeoutSec 15 -UseBasicParsing -ErrorAction Stop
            Write-Host ("  [{0}] {1}" -f $r.StatusCode, $u.Substring($u.LastIndexOf('/')+1)) -ForegroundColor Green
        } catch {
            Write-Host ("  [FAIL] {0}" -f $u) -ForegroundColor Red
        }
    }
}
