# CoreUtils.psm1 - Gemini CLI Core Commands v4.1
# Location: $env:DEV_HOME\Config\PowerShell\modules\CoreUtils.psm1

function Global:Get-GeminiHelp {
    param([string]$Topic = "all")
    Write-Host "`n📖 MANUAL RÁPIDO GEMINI CLI" -ForegroundColor Cyan
    Write-Host "════════════════════════════" -ForegroundColor DarkGray
    $t = $Topic.ToLower()

    if ($t -eq "all" -or $t -eq "") {
        Write-Host "Categorías Disponibles:" -ForegroundColor White
        Write-Host "  • nav    :: Navegación rápida (dev, uhome...)" -ForegroundColor Gray
        Write-Host "  • envs   :: Entornos Conda (rag, auto, script...)" -ForegroundColor Gray
        Write-Host "  • mcp    :: Herramientas WinMCP y RAG" -ForegroundColor Gray
        Write-Host "  • iot    :: Control de Luces Inteligentes" -ForegroundColor Gray
        Write-Host "  • utils  :: Utilidades del Sistema" -ForegroundColor Gray
        Write-Host "`nUso: 'ghelp [categoría]'" -ForegroundColor Yellow
    }
    elseif ($t -eq "nav") {
        Write-Host "📍 COMANDOS DE NAVEGACIÓN" -ForegroundColor White
        Write-Host "  dev    :: Ir a $env:DEV_HOME" -ForegroundColor Gray
        Write-Host "  ghome  :: Ir a .gemini" -ForegroundColor Gray
        Write-Host "  uhome  :: Ir a Usuario" -ForegroundColor Gray
    }
    elseif ($t -eq "envs") {
        Write-Host "🐍 ENTORNOS CONDA" -ForegroundColor White
        Write-Host "  rag    :: Activar entorno RAG-System" -ForegroundColor Gray
        Write-Host "  auto   :: Activar entorno N8N" -ForegroundColor Gray
        Write-Host "  script :: Activar entorno Scripts" -ForegroundColor Gray
    }
    elseif ($t -match "mcp|win|rag") {
        Write-Host "🔧 HERRAMIENTAS MCP (Nativas v2.2)" -ForegroundColor White
        Write-Host "`n  Windows MCP (Prefijo 'win-')" -ForegroundColor Cyan
        Write-Host "    win-spy   :: Inspeccionar elementos UI" -ForegroundColor Gray
        Write-Host "    win-click :: Ejecutar clic programado" -ForegroundColor Gray
        Write-Host "`n  RAG System (Prefijo 'rag-')" -ForegroundColor Cyan
        Write-Host "    rag-q     :: Consulta rápida RAG" -ForegroundColor Gray
        Write-Host "    rag-gui   :: Lanzar dashboard visual de RAG" -ForegroundColor Gray
    }
    elseif ($t -eq "iot") {
        Write-Host "💡 CONTROL DE LUCES INTELIGENTES (Magic Home)" -ForegroundColor White
        
        Write-Host "`n  Comandos Grupales (Toda la casa)" -ForegroundColor Cyan
        Write-Host "    luces-on / luces-off     :: Control total" -ForegroundColor Gray
        Write-Host "    luces-color R G B        :: Color uniforme (ej: luces-color 0 255 255)" -ForegroundColor Gray
        Write-Host "    luces-brillo %           :: Intensidad global (1-100)" -ForegroundColor Gray

        Write-Host "`n  Automatización & Tiempo" -ForegroundColor Cyan
        Write-Host "    set-time-[foco] 'HH:mm'  :: Encender a una hora (ej: set-time-sala '20:00')" -ForegroundColor Gray
        Write-Host "    set-time-[foco] 'HH:mm' -action 'off' :: Apagar a una hora" -ForegroundColor Gray
        Write-Host "    dash / focos             :: Dashboards (Limpia pantalla / Append)" -ForegroundColor Gray

        Write-Host "`n  💡 IDEAS DE USO CREATIVO" -ForegroundColor Yellow
        Write-Host "    1. Modo Cine    : luces-brillo 10; azul-sala" -ForegroundColor DarkGray
        Write-Host "    2. Alarma Visual: set-time-recamara '07:00'; blanco-recamara" -ForegroundColor DarkGray
        Write-Host "    3. Concentración: luces-color 255 150 50; luces-brillo 40" -ForegroundColor DarkGray
        Write-Host "    4. Notificación : rojo-sala; Start-Sleep 2; blanco-sala" -ForegroundColor DarkGray
    }
    elseif ($t -eq "utils") {
        Write-Host "🛠 UTILIDADES DEL SISTEMA" -ForegroundColor White
        Write-Host "`n  Introspección & Estado" -ForegroundColor Cyan
        Write-Host "    devinfo         :: Dashboard resumen (RAM, IP, Versiones)" -ForegroundColor Gray
        Write-Host "    dev-audit       :: Auditoría técnica (Módulos, Alias, Env)" -ForegroundColor Gray
        Write-Host "    dev-audit -Full :: Desglose completo de funciones internas" -ForegroundColor DarkGray
        Write-Host "`n  Mantenimiento" -ForegroundColor Cyan
        Write-Host "    refresh         :: Recargar perfil y LIMPIAR pantalla" -ForegroundColor Gray
        Write-Host "    dash            :: Desplegar dashboard completo" -ForegroundColor Gray
        Write-Host "`n  Seguridad (Advanced)" -ForegroundColor Cyan
        Write-Host "    Net-SmartEye    :: Auditor de conexiones y procesos" -ForegroundColor Gray
        Write-Host "    Net-DeepAudit   :: Análisis forense de tráfico de red" -ForegroundColor Gray
    }
}

Export-ModuleMember -Function Get-GeminiHelp
$aliasContent
