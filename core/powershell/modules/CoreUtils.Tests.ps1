# Requires -Version 5.1
# Requires -Modules Pester

Import-Module "$PSScriptRoot/CoreUtils.psm1" -Force

Describe "Get-GeminiHelp" {
    BeforeEach {
        Mock Write-Host {}
    }

    It "Should display all categories when Topic is 'all'" {
        Get-GeminiHelp -Topic "all"
        Assert-MockCalled Write-Host -ParameterFilter { $Object -match "Categorías Disponibles:" } -Times 1 -Exactly
    }

    It "Should display all categories when Topic is empty" {
        Get-GeminiHelp -Topic ""
        Assert-MockCalled Write-Host -ParameterFilter { $Object -match "Categorías Disponibles:" } -Times 1 -Exactly
    }

    It "Should display all categories by default" {
        Get-GeminiHelp
        Assert-MockCalled Write-Host -ParameterFilter { $Object -match "Categorías Disponibles:" } -Times 1 -Exactly
    }

    It "Should display navigation help when Topic is 'nav'" {
        Get-GeminiHelp -Topic "nav"
        Assert-MockCalled Write-Host -ParameterFilter { $Object -match "COMANDOS DE NAVEGACIÓN" } -Times 1 -Exactly
    }

    It "Should display environment help when Topic is 'envs'" {
        Get-GeminiHelp -Topic "envs"
        Assert-MockCalled Write-Host -ParameterFilter { $Object -match "ENTORNOS CONDA" } -Times 1 -Exactly
    }

    It "Should display MCP help when Topic matches 'mcp'" {
        Get-GeminiHelp -Topic "mcp"
        Assert-MockCalled Write-Host -ParameterFilter { $Object -match "HERRAMIENTAS MCP" } -Times 1 -Exactly
    }

    It "Should display MCP help when Topic matches 'win'" {
        Get-GeminiHelp -Topic "win"
        Assert-MockCalled Write-Host -ParameterFilter { $Object -match "HERRAMIENTAS MCP" } -Times 1 -Exactly
    }

    It "Should display MCP help when Topic matches 'rag'" {
        Get-GeminiHelp -Topic "rag"
        Assert-MockCalled Write-Host -ParameterFilter { $Object -match "HERRAMIENTAS MCP" } -Times 1 -Exactly
    }

    It "Should display IoT help when Topic is 'iot'" {
        Get-GeminiHelp -Topic "iot"
        Assert-MockCalled Write-Host -ParameterFilter { $Object -match "CONTROL DE LUCES INTELIGENTES" } -Times 1 -Exactly
    }

    It "Should display utils help when Topic is 'utils'" {
        Get-GeminiHelp -Topic "utils"
        Assert-MockCalled Write-Host -ParameterFilter { $Object -match "UTILIDADES DEL SISTEMA" } -Times 1 -Exactly
    }

    It "Should handle case insensitivity (e.g., 'NAV')" {
        Get-GeminiHelp -Topic "NAV"
        Assert-MockCalled Write-Host -ParameterFilter { $Object -match "COMANDOS DE NAVEGACIÓN" } -Times 1 -Exactly
    }

    It "Should handle case insensitivity (e.g., 'iOt')" {
        Get-GeminiHelp -Topic "iOt"
        Assert-MockCalled Write-Host -ParameterFilter { $Object -match "CONTROL DE LUCES INTELIGENTES" } -Times 1 -Exactly
    }
}
