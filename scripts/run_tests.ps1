$ErrorActionPreference = "Stop"

$testTemp = Join-Path ([System.IO.Path]::GetTempPath()) (
    "day13-pytest-" + [guid]::NewGuid().ToString("N")
)
$exitCode = 1

try {
    & python -m pytest -q -p no:cacheprovider "--basetemp=$testTemp" @args
    $exitCode = $LASTEXITCODE
}
finally {
    if (Test-Path -LiteralPath $testTemp) {
        Remove-Item -LiteralPath $testTemp -Recurse -Force -ErrorAction SilentlyContinue
    }
}

exit $exitCode
