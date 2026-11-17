$docxPath = "C:\Users\rauna\Downloads\ANTIGRAVITY\FCC Project\INTELLIEMO_Project_Report.docx"
$word = New-Object -ComObject Word.Application
$word.Visible = $false
try {
    $doc = $word.Documents.Open($docxPath)
    $pages = $doc.ComputeStatistics(2) # 2 = wdStatisticPages
    Write-Host "Total Pages: $pages"
    $doc.Close(0)
} finally {
    $word.Quit()
}
