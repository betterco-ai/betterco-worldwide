# Redline a new draft against the counterparty's commented copy and answer each of
# their comments (Word COM). Used for Draft 2, 24.09.2026:
#   python scripts/build_docx_source.py
#   powershell -File scripts/to_docx.ps1 -OutDir build
#   powershell -File scripts/redline_docx.ps1
# Verify by accepting all revisions in a copy: the text must equal the clean draft.
param(
    # Original = the counterparty's commented file, copied into build/ (not committed)
    [string]$Original = "$PSScriptRoot\..\build\stp_commented_2026-09-21.docx",
    [string]$Revised  = "$PSScriptRoot\..\build\SEPTEO_RESELLER_AGREEMENT_2026-09-14.docx",
    [string]$Replies  = "$PSScriptRoot\..\docs\SEPTEO_DRAFT2_COMMENT_REPLIES_2026-09-24.json",
    [string]$Out      = "$PSScriptRoot\..\docs\SEPTEO_RESELLER_AGREEMENT_DRAFT2_REDLINE_2026-09-24.docx"
)
$ErrorActionPreference = "Stop"
$data = Get-Content -Raw -Encoding UTF8 $Replies | ConvertFrom-Json

$word = New-Object -ComObject Word.Application
$word.Visible = $false
$word.DisplayAlerts = 0
$word.UserName = "Eckhard Ortwein"
$word.UserInitials = "EO"
try {
    $o = $word.Documents.Open($Original, $false, $true)
    $r = $word.Documents.Open($Revised, $false, $true)
    # CompareDocuments(Original, Revised, Destination=new(2), Granularity=word(1),
    #   CompareFormatting, CompareCaseChanges, CompareWhitespace, CompareTables,
    #   CompareHeaders, CompareFootnotes, CompareTextboxes, CompareFields,
    #   CompareComments, CompareMoves, RevisedAuthor, IgnoreAllComparisonWarnings)
    $d = $word.CompareDocuments($o, $r, 2, 1, $false, $true, $false, $true, $true, $true, $true, $true, $true, $true, "Eckhard Ortwein", $true)
    $o.Close($false); $r.Close($false)

    $n = $d.Comments.Count
    Write-Output ("comments in redline: " + $n + "   revisions: " + $d.Revisions.Count)
    $used = @{}
    $answered = 0
    $orig = @()
    for ($i = 1; $i -le $n; $i++) { $orig += $d.Comments.Item($i) }
    foreach ($c in $orig) {
        $t = $c.Range.Text.Trim()
        $hit = $null
        foreach ($pair in $data.replies) {
            $k = $pair[0]
            if ($used.ContainsKey($k)) { continue }
            if (($k -eq "streichen" -and $t -eq "streichen") -or ($k -ne "streichen" -and $t.StartsWith($k))) { $hit = $pair; break }
        }
        if (-not $hit) { throw ("no reply for comment: " + $t) }
        $used[$hit[0]] = $true
        [void]$c.Replies.Add($c.Scope, $hit[1])
        $answered++
    }
    if ($answered -ne $data.replies.Count) { throw ("answered " + $answered + " of " + $data.replies.Count) }

    # one general comment on the first paragraph
    $first = $d.Paragraphs.Item(1).Range
    [void]$d.Comments.Add($first, $data._general)

    $d.TrackRevisions = $true
    $d.SaveAs2($Out, 16)
    Write-Output ("answered " + $answered + " comments -> " + $Out)
    $d.Close($false)
} finally {
    $word.Quit()
}
