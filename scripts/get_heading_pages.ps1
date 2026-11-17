$docxPath = "C:\Users\rauna\Downloads\ANTIGRAVITY\FCC Project\INTELLIEMO_Project_Report.docx"
$word = New-Object -ComObject Word.Application
$word.Visible = $false
try {
    $doc = $word.Documents.Open($docxPath)
    foreach ($p in $doc.Paragraphs) {
        $text = $p.Range.Text.Trim()
        if ($text -match "^(1\.|2\.|3\.|4\.|5\.|Index)") {
            $page = $p.Range.Information(3) # 3 = wdActiveEndPageNumber
            Write-Host "$text -> Page $page"
        }
    }
    $doc.Close(0)
} finally {
    $word.Quit()
}
