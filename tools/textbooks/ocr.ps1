param([string]$ImgRoot, [string]$OutRoot, [string[]]$Ids)
# Windows.Media.Ocr (ru) over page PNGs -> one UTF-8 text file per book with page markers.
Add-Type -AssemblyName System.Runtime.WindowsRuntime
[void][Windows.Storage.StorageFile, Windows.Storage, ContentType = WindowsRuntime]
[void][Windows.Media.Ocr.OcrEngine, Windows.Foundation, ContentType = WindowsRuntime]
[void][Windows.Graphics.Imaging.BitmapDecoder, Windows.Foundation, ContentType = WindowsRuntime]
[void][Windows.Globalization.Language, Windows.Foundation, ContentType = WindowsRuntime]

$asTask = ([System.WindowsRuntimeSystemExtensions].GetMethods() | Where-Object {
    $_.Name -eq 'AsTask' -and $_.GetParameters().Count -eq 1 -and $_.GetParameters()[0].ParameterType.Name -eq 'IAsyncOperation`1' })[0]
function Await($op, [Type]$t) {
    $task = $asTask.MakeGenericMethod($t).Invoke($null, @($op))
    $task.Wait() | Out-Null
    $task.Result
}

$engine = [Windows.Media.Ocr.OcrEngine]::TryCreateFromLanguage([Windows.Globalization.Language]::new('ru'))
New-Item -ItemType Directory -Force $OutRoot | Out-Null
foreach ($id in $Ids) {
    $dir = Join-Path $ImgRoot $id
    $out = Join-Path $OutRoot "$id.txt"
    if (Test-Path $out) { continue }
    $sb = New-Object System.Text.StringBuilder
    foreach ($f in (Get-ChildItem $dir -Filter 'p*.png' | Sort-Object Name)) {
        $file = Await ([Windows.Storage.StorageFile]::GetFileFromPathAsync($f.FullName)) ([Windows.Storage.StorageFile])
        $stream = Await ($file.OpenAsync([Windows.Storage.FileAccessMode]::Read)) ([Windows.Storage.Streams.IRandomAccessStream])
        $dec = Await ([Windows.Graphics.Imaging.BitmapDecoder]::CreateAsync($stream)) ([Windows.Graphics.Imaging.BitmapDecoder])
        $bmp = Await ($dec.GetSoftwareBitmapAsync()) ([Windows.Graphics.Imaging.SoftwareBitmap])
        $res = Await ($engine.RecognizeAsync($bmp)) ([Windows.Media.Ocr.OcrResult])
        $n = [int]($f.BaseName.Substring(1))
        [void]$sb.Append("`n=== PDF p. $n ===`n")
        foreach ($line in $res.Lines) { [void]$sb.AppendLine($line.Text) }
        $stream.Dispose(); $bmp.Dispose()
    }
    [IO.File]::WriteAllText($out, $sb.ToString(), (New-Object Text.UTF8Encoding($false)))
    "$id done"
}
