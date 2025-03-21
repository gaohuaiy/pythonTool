$folderPath = "F:\xeq��Ŀ\xEQ�ۺϰ�汾����\2.0.3"

$files = Get-ChildItem -Path $folderPath -Recurse -File

$hashTable = @{}

foreach ($file in $files) {
    $hash = (Get-FileHash $file.FullName -Algorithm SHA256).Hash
    if ($hashTable.ContainsKey($hash)) {
        # ��ӡ�ظ��ļ���Ϣ
        Write-Host "Duplicate found:"
        Write-Host "  Kept file: $($hashTable[$hash])"
        Write-Host "  Deleted file: $($file.FullName)"
        # ɾ���ظ��ļ�
        #Remove-Item -Path $file.FullName -Force
    } else {
        # ���ļ��Ĺ�ϣֵ��ӵ���ϣ����
        $hashTable[$hash] = $file.FullName
    }
}
