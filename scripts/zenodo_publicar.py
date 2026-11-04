#!/usr/bin/env python3
"""Publicación del artifact en Zenodo mediante la API REST (Semana 5).

Flujo en tres pasos, para que el DOI quede escrito en el README *antes* de archivar:

    python3 scripts/zenodo_publicar.py reservar          # crea el borrador y reserva el DOI
    # ... escribir el DOI reservado en README/CITATION.cff, commit, tag v1.0.0 y generar el zip ...
    python3 scripts/zenodo_publicar.py subir artifact-v1.0.0.zip
    python3 scripts/zenodo_publicar.py publicar          # irreversible: pide confirmación

Otros comandos: `estado` (muestra el borrador guardado).

El token personal (permisos deposit:write y deposit:actions) se lee de la variable de entorno
ZENODO_TOKEN o del archivo ~/.zenodo_token. Nunca se guarda en el repositorio.
Los metadatos se toman de .zenodo.json. El identificador del borrador se guarda en
.zenodo_deposito.json (ignorado por git). Con ZENODO_URL=https://sandbox.zenodo.org se
puede ensayar en el entorno de pruebas de Zenodo.

Solo usa la biblioteca estándar de Python.
"""
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
BASE = os.environ.get("ZENODO_URL", "https://zenodo.org").rstrip("/")
ESTADO = RAIZ / ".zenodo_deposito.json"
METADATOS = RAIZ / ".zenodo.json"


def leer_token():
    """Obtiene el token desde ZENODO_TOKEN o ~/.zenodo_token."""
    token = os.environ.get("ZENODO_TOKEN", "").strip()
    if not token:
        archivo = Path.home() / ".zenodo_token"
        if archivo.exists():
            token = archivo.read_text(encoding="utf-8").strip()
    if not token:
        sys.exit("Falta el token: defina ZENODO_TOKEN o cree ~/.zenodo_token")
    return token


def peticion(metodo, url, datos=None, binario=None):
    """Realiza una petición autenticada y devuelve la respuesta JSON."""
    cabeceras = {"Authorization": f"Bearer {leer_token()}", "Accept": "application/json"}
    cuerpo = None
    if datos is not None:
        cuerpo = json.dumps(datos).encode("utf-8")
        cabeceras["Content-Type"] = "application/json"
    elif binario is not None:
        cuerpo = binario
        cabeceras["Content-Type"] = "application/octet-stream"
    req = urllib.request.Request(url, data=cuerpo, headers=cabeceras, method=metodo)
    try:
        with urllib.request.urlopen(req, timeout=300) as resp:
            texto = resp.read().decode("utf-8")
            return json.loads(texto) if texto else {}
    except urllib.error.HTTPError as err:
        sys.exit(f"Error HTTP {err.code} en {metodo} {url}:\n{err.read().decode('utf-8', 'replace')}")


def guardar_estado(dep):
    ESTADO.write_text(json.dumps({
        "id": dep["id"],
        "doi": dep["metadata"].get("prereserve_doi", {}).get("doi"),
        "bucket": dep["links"]["bucket"],
        "html": dep["links"]["html"],
    }, indent=2) + "\n", encoding="utf-8")


def cargar_estado():
    if not ESTADO.exists():
        sys.exit("No hay borrador: ejecute primero `reservar`.")
    return json.loads(ESTADO.read_text(encoding="utf-8"))


def reservar():
    """Crea el borrador con los metadatos de .zenodo.json y reserva el DOI."""
    if ESTADO.exists():
        sys.exit(f"Ya existe un borrador ({ESTADO.name}); use `estado`.")
    metadatos = json.loads(METADATOS.read_text(encoding="utf-8"))
    metadatos["prereserve_doi"] = True
    dep = peticion("POST", f"{BASE}/api/deposit/depositions", {"metadata": metadatos})
    guardar_estado(dep)
    estado = cargar_estado()
    print(f"Borrador creado: {estado['html']}")
    print(f"DOI reservado:   {estado['doi']}")
    print(f"Registro final:  {BASE}/records/{estado['id']}")


def subir(ruta_zip):
    """Sube (o reemplaza) el archivo del artifact en el borrador."""
    estado = cargar_estado()
    ruta = Path(ruta_zip)
    dep = peticion("GET", f"{BASE}/api/deposit/depositions/{estado['id']}")
    for archivo in dep.get("files", []):
        if archivo["filename"] == ruta.name:
            peticion("DELETE", archivo["links"]["self"])
    res = peticion("PUT", f"{estado['bucket']}/{ruta.name}", binario=ruta.read_bytes())
    print(f"Subido {ruta.name}: {res.get('size')} bytes, checksum {res.get('checksum')}")


def mostrar_estado():
    estado = cargar_estado()
    dep = peticion("GET", f"{BASE}/api/deposit/depositions/{estado['id']}")
    print(f"Título:  {dep['metadata'].get('title')}")
    print(f"Estado:  {dep.get('state')} · publicado: {dep.get('submitted')}")
    print(f"DOI:     {estado['doi']}")
    print(f"Enlace:  {dep['links']['html']}")
    for archivo in dep.get("files", []):
        print(f"Archivo: {archivo['filename']} ({archivo['filesize']} bytes, md5 {archivo['checksum']})")


def publicar():
    """Publica el borrador. En Zenodo esto es irreversible."""
    estado = cargar_estado()
    if "--si" not in sys.argv:
        resp = input(f"Publicar {estado['doi']} en {BASE}? Es irreversible [escriba 'si']: ")
        if resp.strip().lower() != "si":
            sys.exit("Cancelado.")
    dep = peticion("POST", f"{BASE}/api/deposit/depositions/{estado['id']}/actions/publish")
    print(f"Publicado: {dep['links'].get('record_html', dep['links']['html'])}")
    print(f"DOI: {dep.get('doi')}")


if __name__ == "__main__":
    comando = sys.argv[1] if len(sys.argv) > 1 else ""
    if comando == "reservar":
        reservar()
    elif comando == "subir" and len(sys.argv) > 2:
        subir(sys.argv[2])
    elif comando == "estado":
        mostrar_estado()
    elif comando == "publicar":
        publicar()
    else:
        sys.exit(__doc__)
