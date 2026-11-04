#!/usr/bin/env python3
"""Descarga un artifact publicado en Zenodo para la evaluación cruzada (Semana 5).

Uso:
    python3 scripts/descargar_zenodo.py <URL o DOI o id del registro> <carpeta destino>

Ejemplos:
    python3 scripts/descargar_zenodo.py https://zenodo.org/records/1234567 ../eval-companero
    python3 scripts/descargar_zenodo.py 10.5281/zenodo.1234567 ../eval-companero

Qué hace (y qué NO hace):
- Consulta la API pública de Zenodo (sin token), descarga cada archivo del registro,
  verifica su checksum MD5 y descomprime los .zip/.tar.gz en <destino>/contenido/.
- Guarda los metadatos del registro en <destino>/zenodo_registro.json y un resumen en
  <destino>/DESCARGA.md (fecha, DOI, archivos, checksums), útil como evidencia en la
  plantilla docs/evaluacion-cruzada/PLANTILLA_EVALUACION.md.
- NO ejecuta nada del artifact descargado: se trata como datos no confiables hasta leerlo.
- La carpeta destino debe estar vacía o no existir, y debe quedar FUERA de este repositorio.

Solo usa la biblioteca estándar de Python.
"""
import datetime
import hashlib
import json
import re
import sys
import tarfile
import time
import urllib.request
import zipfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent


def id_registro(texto):
    """Extrae el número de registro de una URL, DOI o id."""
    m = re.search(r"(?:records?/|zenodo\.)(\d+)", texto) or re.fullmatch(r"\s*(\d+)\s*", texto)
    if not m:
        sys.exit(f"No se reconoce un registro de Zenodo en: {texto}")
    return m.group(1)


def obtener_json(url):
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=120) as resp:
        return json.loads(resp.read().decode("utf-8"))


def descargar(url, ruta, intentos=4):
    """Descarga con reintentos (Zenodo puede responder 5xx de forma transitoria)."""
    for i in range(1, intentos + 1):
        try:
            urllib.request.urlretrieve(url, ruta)
            return
        except Exception as err:  # noqa: BLE001 - se informa y se reintenta
            if i == intentos:
                sys.exit(f"No se pudo descargar {url}: {err}")
            print(f"  intento {i} falló ({err}); reintentando en {5 * i} s...")
            time.sleep(5 * i)


def extraer_seguro(archivo, destino):
    """Descomprime rechazando rutas absolutas o con '..' (path traversal)."""
    destino = destino.resolve()
    sufijo = archivo.name.lower()
    if sufijo.endswith(".zip") and zipfile.is_zipfile(archivo):
        with zipfile.ZipFile(archivo) as z:
            for nombre in z.namelist():
                if not (destino / nombre).resolve().is_relative_to(destino):
                    sys.exit(f"Ruta insegura en el zip: {nombre}")
            z.extractall(destino)
            for info in z.infolist():  # conserva el bit de ejecución de los scripts
                modo = info.external_attr >> 16
                if modo and not info.is_dir():
                    (destino / info.filename).chmod(modo & 0o755)
        return True
    if sufijo.endswith((".tar.gz", ".tgz", ".tar")) and tarfile.is_tarfile(archivo):
        with tarfile.open(archivo) as t:
            t.extractall(destino, filter="data")
        return True
    return False


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    rid = id_registro(sys.argv[1])
    destino = Path(sys.argv[2]).resolve()
    if destino.is_relative_to(RAIZ):
        sys.exit("La carpeta destino debe estar fuera de este repositorio.")
    if destino.exists() and any(destino.iterdir()):
        sys.exit(f"La carpeta destino no está vacía: {destino}")
    (destino / "descargas").mkdir(parents=True, exist_ok=True)

    registro = obtener_json(f"https://zenodo.org/api/records/{rid}")
    (destino / "zenodo_registro.json").write_text(
        json.dumps(registro, indent=2, ensure_ascii=False), encoding="utf-8")
    meta = registro.get("metadata", {})
    autores = ", ".join(c.get("name", "") for c in meta.get("creators", []))
    print(f"Registro {rid}: {meta.get('title')}\nAutores: {autores}\nDOI: {registro.get('doi')}")

    filas = []
    archivos = registro.get("files", [])
    if not archivos:
        sys.exit("El registro no tiene archivos públicos (¿acceso restringido o embargo?).")
    for f in archivos:
        nombre = Path(f["key"]).name
        ruta = destino / "descargas" / nombre
        print(f"Descargando {nombre} ({f.get('size', 0)} bytes)...")
        descargar(f["links"]["self"], ruta)
        algoritmo, _, esperado = f.get("checksum", "md5:").partition(":")
        obtenido = hashlib.new(algoritmo or "md5", ruta.read_bytes()).hexdigest()
        ok = obtenido == esperado
        print(f"  checksum {algoritmo}: {'OK' if ok else 'NO COINCIDE'}")
        extraido = extraer_seguro(ruta, destino / "contenido")
        filas.append(f"| `{nombre}` | {f.get('size', 0)} | `{obtenido}` | {'sí' if ok else '**NO**'} | {'sí' if extraido else 'no'} |")

    ahora = datetime.datetime.now().astimezone().isoformat(timespec="seconds")
    (destino / "DESCARGA.md").write_text("\n".join([
        f"# Descarga del artifact desde Zenodo",
        "",
        f"- Fecha: {ahora}",
        f"- Registro: https://zenodo.org/records/{rid}",
        f"- DOI: {registro.get('doi')}",
        f"- Título: {meta.get('title')}",
        f"- Autores: {autores}",
        f"- Versión: {meta.get('version', '—')} · publicado: {meta.get('publication_date', '—')}",
        f"- Licencia: {(meta.get('license') or {}).get('id', '—')}",
        "",
        "| Archivo | Bytes | Checksum | ¿Coincide con Zenodo? | ¿Descomprimido? |",
        "|---|---|---|---|---|",
        *filas,
        "",
    ]), encoding="utf-8")
    print(f"\nListo. Contenido en {destino / 'contenido'}; resumen en {destino / 'DESCARGA.md'}")
    print("Lea el README del artifact antes de ejecutar cualquier comando.")


if __name__ == "__main__":
    main()
