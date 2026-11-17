$docxPath = "C:\Users\rauna\Downloads\ANTIGRAVITY\FCC Project\INTELLIEMO_Project_Report.docx"
$pdfPath = "C:\Users\rauna\Downloads\ANTIGRAVITY\FCC Project\INTELLIEMO_Project_Report.pdf"

$word = New-Object -ComObject Word.Application
$word.Visible = $false
$word.DisplayAlerts = [Microsoft.Office.Interop.Word.WdAlertLevel]::wdAlertsNone

try {
    $doc = $word.Documents.Open($docxPath)
    $doc.ExportAsFixedFormat($pdfPath, 17) # 17 = wdExportFormatPDF
    $doc.Close([Microsoft.Office.Interop.Word.WdSaveOptions]::wdDoNotSaveChanges)
    Write-Host "PDF successfully generated at: $pdfPath"
}
catch {
    Write-Host "COM Exception: $($_.Exception.Message)"
}
finally {
    $word.Quit()
    [System.Runtime.Interopservices.Marshal]::ReleaseComObject($word) | Out-Null
    [System.GC]::Collect()
    [System.GC]::WaitForPendingFinalizers()
}
