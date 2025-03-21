$folderPath = "F:\xeq项目\xEQ综合版版本发布\2.0.3"

$files = Get-ChildItem -Path $folderPath -Recurse -File

$hashTable = @{}

foreach ($file in $files) {
    $hash = (Get-FileHash $file.FullName -Algorithm SHA256).Hash
    if ($hashTable.ContainsKey($hash)) {
        # 打印重复文件信息
        Write-Host "Duplicate found:"
        Write-Host "  Kept file: $($hashTable[$hash])"
        Write-Host "  Deleted file: $($file.FullName)"
        # 删除重复文件
        #Remove-Item -Path $file.FullName -Force
    } else {
        # 将文件的哈希值添加到哈希表中
        $hashTable[$hash] = $file.FullName
    }
}
