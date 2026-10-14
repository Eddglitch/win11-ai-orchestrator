🎯 **What:** Missing Pester test file for `CoreUtils.psm1` has been addressed. The `Get-GeminiHelp` function previously had no coverage.
📊 **Coverage:** The Pester test suite tests all major argument paths for the `-Topic` argument: 'all', default argument, empty string, 'nav', 'envs', 'mcp' (including matches for 'win' and 'rag'), 'iot', and 'utils'. It also covers case insensitivity by testing inputs like 'NAV' and 'iOt'.
✨ **Result:** Test coverage for `Get-GeminiHelp` went from 0% to nearly 100%, improving stability by safely asserting output behavior using `Mock Write-Host`.
