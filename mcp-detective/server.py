import json
from copy import deepcopy
from pathlib import Path
from typing import Any

from mcp.server import MCPServer


mcp = MCPServer("MCP Detective")
CASOS_PATH = Path(__file__).resolve().with_name("casos.json")

with CASOS_PATH.open(encoding="utf-8") as casos_file:
    CASOS: dict[str, dict[str, Any]] = json.load(casos_file)

ALERTAS: dict[str, dict[str, str]] = {}
NIVELES_VALIDOS = {"bajo", "medio", "alto"}


def obtener_casos() -> list[dict]:
    """Devuelve el identificador, sistema y cantidad de eventos de cada caso."""
    return [
        {
            "caso_id": caso_id,
            "sistema": caso["sistema"],
            "cantidad_eventos": len(caso["eventos"]),
        }
        for caso_id, caso in CASOS.items()
    ]


def obtener_eventos(caso_id: str) -> list[dict]:
    """Devuelve una copia de los eventos de un caso existente."""
    if not isinstance(caso_id, str) or caso_id not in CASOS:
        raise ValueError(f"El caso '{caso_id}' no existe.")
    return deepcopy(CASOS[caso_id]["eventos"])


def crear_alerta(caso_id: str, nivel: str, motivo: str) -> dict[str, str]:
    """Valida y registra en memoria una única alerta por caso."""
    if not isinstance(caso_id, str) or caso_id not in CASOS:
        raise ValueError(f"El caso '{caso_id}' no existe.")
    if not isinstance(nivel, str) or nivel not in NIVELES_VALIDOS:
        raise ValueError("El nivel debe ser 'bajo', 'medio' o 'alto'.")
    if not isinstance(motivo, str) or not motivo.strip():
        raise ValueError("El motivo no puede estar vacío.")
    if caso_id in ALERTAS:
        raise ValueError(f"Ya existe una alerta registrada para el caso '{caso_id}'.")

    alerta = {
        "caso_id": caso_id,
        "nivel": nivel,
        "motivo": motivo,
        "estado": "registrada",
    }
    ALERTAS[caso_id] = alerta
    return alerta.copy()


@mcp.tool()
def listar_casos() -> list[dict]:
    """Lista los casos disponibles, su sistema y la cantidad de eventos."""
    return obtener_casos()


@mcp.tool()
def consultar_eventos(caso_id: str) -> list[dict]:
    """Consulta los eventos exactos de un caso; falla si el caso no existe."""
    return obtener_eventos(caso_id)


@mcp.tool()
def registrar_alerta(caso_id: str, nivel: str, motivo: str) -> dict[str, str]:
    """Registra en memoria una alerta validada, como máximo una por caso."""
    return crear_alerta(caso_id, nivel, motivo)


if __name__ == "__main__":
    mcp.run(transport="stdio")
