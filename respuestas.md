# Deber 5 — MCP Detective

## Arquitectura

El LLM interpreta la solicitud y propone una herramienta. El host (Copilot en VS Code) presenta la solicitud al cliente MCP; el cliente descubre la herramienta, envía sus argumentos y devuelve el resultado al agente. El servidor MCP ejecuta el código Python, consulta los casos y valida antes de registrar alertas. El modelo no ejecuta directamente las funciones del servidor.

## Evidencia

`INC-003` contiene cuatro intentos fallidos consecutivos seguidos de un acceso exitoso para `admin`, desde la misma IP y en minutos consecutivos. Ese patrón justifica revisar la actividad, pero los eventos por sí solos no identifican quién operó la cuenta ni demuestran que el acceso fuera no autorizado.

## Validación

El servidor rechaza `INC-999`, niveles fuera de `bajo`, `medio` y `alto`, motivos vacíos y alertas duplicadas. La validación ocurre en el servidor porque los argumentos propuestos por un modelo no son confiables y también pueden llegar de otros clientes MCP.

## Agente y ejecución

- Agente usado: Copilot en VS Code.
- La conexión por stdio se verificó con un cliente MCP: descubrió las tres herramientas y completó D1–D7. La prueba interactiva con el host en una sesión nueva de VS Code y su captura `evidencias/agente_tools.png` siguen pendientes.
- Ejecuta `mcp dev mcp-detective/server.py` para repetir las pruebas en MCP Inspector. No se incluyen capturas simuladas.

## Instrucciones

Desde la raíz del repositorio, con Python 3.11 o superior:

```powershell
python -m pip install -r mcp-detective/requirements.txt
python -m pytest mcp-detective -q
mcp dev mcp-detective/server.py
```

Para conectar el servidor en VS Code, agrega esta configuración a `.vscode/mcp.json` del workspace:

```json
{
  "servers": {
    "mcp-detective": {
      "type": "stdio",
      "command": "python",
      "args": ["${workspaceFolder}/mcp-detective/server.py"]
    }
  }
}
```

Inicia o reinicia el servidor desde VS Code y verifica que aparezcan `listar_casos`, `consultar_eventos` y `registrar_alerta`. No se requieren tokens ni credenciales.

El servidor solo utiliza los datos simulados de `casos.json`; las alertas viven en memoria y se pierden al reiniciarlo.
