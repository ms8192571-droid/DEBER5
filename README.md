# Deber 5 — MCP Detective

Servidor MCP de Python para consultar casos simulados y registrar alertas en memoria. Las instrucciones de instalación, pruebas y conexión en VS Code están en [respuestas.md](respuestas.md).

## Inicio rápido

```powershell
python -m pip install -r mcp-detective/requirements.txt
python -m pytest mcp-detective -q
mcp dev mcp-detective/server.py
```

Los casos son datos ficticios. El directorio `evidencias/` documenta las capturas reales que deben adjuntarse antes de entregar.
