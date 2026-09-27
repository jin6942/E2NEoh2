param([Parameter(Mandatory=$true)][string]$InputDocx,
      [Parameter(Mandatory=$true)][string]$OutputPdf)
$ErrorActionPreference = 'Stop'
$sourcePath = (Resolve-Path -LiteralPath $InputDocx).Path
$pdfPath = [System.IO.Path]::GetFullPath($OutputPdf)
if ([System.IO.Path]::GetExtension($sourcePath) -ne '.docx') { throw 'Expected DOCX input' }
if ([System.IO.Path]::GetExtension($pdfPath) -ne '.pdf') { throw 'Expected PDF output' }
$outputDirectory = [System.IO.Path]::GetDirectoryName($pdfPath)
[System.IO.Directory]::CreateDirectory($outputDirectory) | Out-Null
$sourceHash = (Get-FileHash -LiteralPath $sourcePath -Algorithm SHA256).Hash
$wordApp = $null
$openedDocument = $null
try {
    Write-Output 'Creating private Word renderer'
    $wordApp = New-Object -ComObject Word.Application
    $wordApp.Visible = $false
    $wordApp.DisplayAlerts = 0
    $wordApp.AutomationSecurity = 3
    Write-Output 'Opening source read-only'
    $openedDocument = $wordApp.Documents.Open($sourcePath, $false, $true, $false)
    Write-Output 'Exporting PDF'
    $openedDocument.Repaginate()
    $openedDocument.ExportAsFixedFormat($pdfPath, 17)
    $pages = $openedDocument.ComputeStatistics(2)
    $wordVersion = $wordApp.Version
    $openedDocument.Close(0)
    [System.Runtime.InteropServices.Marshal]::FinalReleaseComObject($openedDocument) | Out-Null
    $openedDocument = $null
    if ((Get-FileHash -LiteralPath $sourcePath -Algorithm SHA256).Hash -ne $sourceHash) {
        throw 'Read-only source hash changed'
    }
    $renderReport = @{ renderer='Microsoft Word'; version=$wordVersion; pages=$pages;
       pdf=$pdfPath; source_sha256=$sourceHash; source_unchanged=$true }
} finally {
    try {
        if ($null -ne $openedDocument) {
            try { $openedDocument.Close(0) }
            finally { [System.Runtime.InteropServices.Marshal]::FinalReleaseComObject($openedDocument) | Out-Null }
        }
    } finally {
        if ($null -ne $wordApp) {
            # The optional COM parameter rejects Quit(0) on Windows PowerShell 5.1.
            # This private application has already closed its read-only document.
            try { $wordApp.Quit() }
            finally { [System.Runtime.InteropServices.Marshal]::FinalReleaseComObject($wordApp) | Out-Null }
        }
    }
}
# A successful report is emitted only after the private application has closed.
$renderReport | ConvertTo-Json
