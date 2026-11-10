from collections.abc import Iterator

import pytest

from server import ALERTAS, crear_alerta, obtener_casos, obtener_eventos


@pytest.fixture(autouse=True)
def limpiar_alertas() -> Iterator[None]:
    ALERTAS.clear()
    yield
    ALERTAS.clear()


def test_listar_casos_devuelve_los_tres_casos_y_sus_cantidades() -> None:
    casos = obtener_casos()

    assert casos == [
        {"caso_id": "INC-001", "sistema": "portal_acceso", "cantidad_eventos": 2},
        {"caso_id": "INC-002", "sistema": "portal_acceso", "cantidad_eventos": 6},
        {
            "caso_id": "INC-003",
            "sistema": "panel_administracion",
            "cantidad_eventos": 5,
        },
    ]


def test_consultar_eventos_devuelve_los_seis_eventos_de_inc_002() -> None:
    eventos = obtener_eventos("INC-002")

    assert len(eventos) == 6
    assert {evento["evento"] for evento in eventos} == {"LOGIN_FAILED"}
    assert {evento["usuario"] for evento in eventos} == {"admin"}


def test_consultar_eventos_rechaza_un_caso_inexistente() -> None:
    with pytest.raises(ValueError, match="INC-999.*no existe"):
        obtener_eventos("INC-999")


def test_registrar_alerta_devuelve_confirmacion_y_la_guarda() -> None:
    alerta = crear_alerta(
        "INC-003",
        "alto",
        "Cuatro fallos seguidos de un acceso exitoso; requiere revisión",
    )

    assert alerta == {
        "caso_id": "INC-003",
        "nivel": "alto",
        "motivo": "Cuatro fallos seguidos de un acceso exitoso; requiere revisión",
        "estado": "registrada",
    }
    assert ALERTAS["INC-003"] == alerta


def test_registrar_alerta_rechaza_duplicados() -> None:
    crear_alerta("INC-003", "alto", "Requiere revisión")

    with pytest.raises(ValueError, match="Ya existe una alerta"):
        crear_alerta("INC-003", "medio", "Otra alerta")


def test_registrar_alerta_rechaza_un_caso_inexistente() -> None:
    with pytest.raises(ValueError, match="INC-999.*no existe"):
        crear_alerta("INC-999", "medio", "Intentos repetidos")


@pytest.mark.parametrize("nivel", ["critico", "", None])
def test_registrar_alerta_rechaza_niveles_invalidos(nivel: object) -> None:
    with pytest.raises(ValueError, match="El nivel debe ser"):
        crear_alerta("INC-002", nivel, "Intentos repetidos")  # type: ignore[arg-type]


@pytest.mark.parametrize("motivo", ["", "   ", None])
def test_registrar_alerta_rechaza_motivos_vacios(motivo: object) -> None:
    with pytest.raises(ValueError, match="El motivo no puede estar vacío"):
        crear_alerta("INC-002", "medio", motivo)  # type: ignore[arg-type]


def test_validaciones_fallidas_no_consumen_la_alerta_del_caso() -> None:
    with pytest.raises(ValueError, match="El nivel debe ser"):
        crear_alerta("INC-003", "critico", "Requiere revisión")

    alerta = crear_alerta("INC-003", "alto", "Requiere revisión")

    assert alerta["estado"] == "registrada"
