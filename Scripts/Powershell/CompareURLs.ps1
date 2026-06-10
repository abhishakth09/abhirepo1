# Load the files into variables
$master = Get-Content -Path "C:\Users\ADasari\Downloads\Master SAN.txt"
$inactive = Get-Content -Path "C:\Users\ADasari\Downloads\Inactive SAN.txt"

# Clean up any accidental trailing spaces or empty lines
$master = $master | Where-Object { $_.Trim() -ne "" } | ForEach-Object { $_.Trim() }
$inactive = $inactive | Where-Object { $_.Trim() -ne "" } | ForEach-Object { $_.Trim() }

# Process and compare
$results = foreach ($url in $inactive) {
    if ($master -contains $url) {
        [PSCustomObject]@{
            URL    = $url
            Status = "Found in Master"
        }
    } else {
        [PSCustomObject]@{
            URL    = $url
            Status = "NOT in Master"
        }
    }
}

# Output the results neatly to the console
$results | Format-Table -AutoSize