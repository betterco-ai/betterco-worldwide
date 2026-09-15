# Convert the Word-friendly HTML built by build_docx_source.py into .docx,
# using the locally installed Word via COM. No pandoc, no python-docx, and
# nothing installed into the shared Python.
#
#   python scripts/build_docx_source.py
#   powershell -ExecutionPolicy Bypass -File scripts/to_docx.ps1
#
# Track changes is switched ON in the saved file so the counterparty's edits
# are recorded as revisions without them having to remember to enable it.

param(
    [string]$BuildDir = "$PSScriptRoot\..\build",
    [string]$OutDir   = "$PSScriptRoot\..\docs"
)

$ErrorActionPreference = "Stop"
$wdFormatXMLDocument = 16

$BuildDir = (Resolve-Path $BuildDir).Path
$OutDir   = (Resolve-Path $OutDir).Path

$files = Get-ChildItem -Path $BuildDir -Filter *.docx.html
if (-not $files) { throw "no *.docx.html in $BuildDir - run build_docx_source.py first" }

$word = New-Object -ComObject Word.Application
$word.Visible = $false
$word.DisplayAlerts = 0

try {
    foreach ($f in $files) {
        $target = Join-Path $OutDir ($f.Name -replace '\.docx\.html$', '.docx')
        Write-Output ("converting " + $f.Name)

        $doc = $word.Documents.Open($f.FullName, $false, $true)   # ReadOnly source

        # A4, sane margins - Word defaults to Letter from an HTML source
        $doc.PageSetup.PageWidth  = $word.CentimetersToPoints(21.0)
        $doc.PageSetup.PageHeight = $word.CentimetersToPoints(29.7)
        $doc.PageSetup.TopMargin    = $word.CentimetersToPoints(2.0)
        $doc.PageSetup.BottomMargin = $word.CentimetersToPoints(2.0)
        $doc.PageSetup.LeftMargin   = $word.CentimetersToPoints(2.2)
        $doc.PageSetup.RightMargin  = $word.CentimetersToPoints(2.2)

        # record the counterparty's edits as revisions by default
        # SaveAs with [ref] fails on Windows PowerShell 5.1 ("psobject cannot be
        # converted to Object"); SaveAs2 takes plain arguments.
        $doc.SaveAs2([string]$target, [int]$wdFormatXMLDocument)

        # TrackRevisions set before SaveAs is lost, because the source is opened
        # read-only. Set it on the saved document and save again.
        $doc.TrackRevisions = $true
        $doc.Save()

        $pages = $doc.ComputeStatistics(2)   # wdStatisticPages
        $words = $doc.ComputeStatistics(0)   # wdStatisticWords
        Write-Output ("  -> " + (Split-Path $target -Leaf) + "  pages=$pages words=$words track-changes=on")
        $doc.Close($false)
    }
}
finally {
    $word.Quit()
    [System.Runtime.InteropServices.Marshal]::ReleaseComObject($word) | Out-Null
}
