$folderPath = "F:\xeq项目\xEQ综合版版本发布\2.0.3"

$files = Get-ChildItem -Path $folderPath -Recurse -File

$hashTable = @{}

foreach ($file in $files) {
    $hash = (Get-FileHash $file.FullName -Algorithm SHA256).Hash
    if ($hashTable.ContainsKey($hash)) {
        Write-Host "Deleting duplicate: $($file.FullName)"
        Remove-Item -Path $file.FullName -Force
    } else {
        $hashTable[$hash] = $file.FullName
    }
}