# Собирает панель проекта: читает STATUS.md, notes.json и git, пишет out/index.html с данными внутри.
# Запуск: powershell -ExecutionPolicy Bypass -File tools/dashboard/build.ps1
$ErrorActionPreference = 'Stop'
[Console]::OutputEncoding = [Text.Encoding]::UTF8
$repo = (Resolve-Path "$PSScriptRoot\..\..").Path
$utf8 = New-Object System.Text.UTF8Encoding($false)

$notes = [IO.File]::ReadAllText("$PSScriptRoot\notes.json", $utf8) | ConvertFrom-Json
$statusLines = [IO.File]::ReadAllLines("$repo\STATUS.md", $utf8)
$files = @(git -C $repo -c core.quotepath=false ls-files)

$tasks = @()
$decisions = @()
$inDecisions = $false
$decisionsWord = -join [char[]](0x0420, 0x0435, 0x0448, 0x0435, 0x043D, 0x0438, 0x044F)
foreach ($line in $statusLines) {
    if ($line -match '^\|\s*\[(T\d+)\s+([^\]]+)\]\(([^)]+)\)\s*\|(.*)$') {
        $cells = $Matches[4] -split '\|'
        $tasks += [ordered]@{
            id = $Matches[1]; title = $Matches[2].Trim(); prompt = $Matches[3]
            status = $cells[0].Trim(); result = $cells[1].Trim(); notes = $cells[2].Trim()
        }
    }
    # Heading word built from char codes: PowerShell 5.1 reads BOM-less scripts as ANSI.
    if ($line -match '^## ') { $inDecisions = $line.Contains($decisionsWord) }
    elseif ($inDecisions -and $line -match '^- \[( |x|X)\] (.+)$') {
        $decisions += [ordered]@{ done = ($Matches[1] -ne ' '); text = $Matches[2].Trim() }
    }
}

$deliverables = @()
foreach ($d in $notes.deliverables) {
    $item = [ordered]@{ task = $d.task; label = $d.label; note = $d.note }
    if ($d.path) {
        $item.state = $(if ($files -contains $d.path) { 'yes' } else { 'no' })
        $item.link = $d.path
    } elseif ($d.prefix) {
        $n = @($files | Where-Object { $_.StartsWith($d.prefix) }).Count
        $item.state = $(if ($n -gt 0) { 'yes' } else { 'no' })
        $item.count = $n
        $item.link = $d.prefix
    } else {
        $item.state = 'no'
    }
    if ($item.state -eq 'yes') { $item.note = $null }
    $deliverables += $item
}

$mediaExt = '\.(png|jpe?g|webp|gif|svg|mp4|webm)$'
# One copy per identical file (same git blob); prefer the deliverables/ copy.
$seen = @{}
$media = @(git -C $repo -c core.quotepath=false ls-files -s | ForEach-Object {
    $parts = $_ -split "`t", 2
    [pscustomobject]@{ hash = ($parts[0] -split ' ')[1]; path = $parts[1] }
} | Where-Object { $_.path -match $mediaExt } |
    Sort-Object @{ Expression = { -not $_.path.StartsWith('deliverables/') } }, path |
    Where-Object { if ($seen.ContainsKey($_.hash)) { $false } else { $seen[$_.hash] = $true; $true } } |
    ForEach-Object { $_.path })

$commits = @(git -C $repo log -12 --date=short "--format=%h%x1f%ad%x1f%s" | ForEach-Object {
    $p = $_ -split [char]0x1f
    [ordered]@{ hash = $p[0]; date = $p[1]; subject = $p[2] }
})

$data = [ordered]@{
    generated = (Get-Date -Format 'yyyy-MM-dd HH:mm')
    head = (git -C $repo rev-parse --short HEAD)
    start = $notes.start
    tasks = $tasks
    decisions = $decisions
    deliverables = $deliverables
    gaps = @($notes.gaps)
    connections = @($notes.connections)
    files = $files
    media = $media
    commits = $commits
}
$json = ($data | ConvertTo-Json -Depth 6) -replace '</', '<\/'
$template = [IO.File]::ReadAllText("$PSScriptRoot\template.html", $utf8)
$out = "$PSScriptRoot\out"
New-Item -ItemType Directory -Force $out | Out-Null
[IO.File]::WriteAllText("$out\index.html", $template.Replace('/*DATA*/null', $json), $utf8)
"OK: $($tasks.Count) tasks, $($decisions.Count) decisions, $($files.Count) files, $($media.Count) media -> $out\index.html"
if ($media.Count) { 'Media to publish next to the page:'; $media }
