"""Registra las características del entorno de ejecución del experimento.

Funciona en Linux, macOS y Windows (solo usa la biblioteca estándar de Python).

Uso: python scripts/collect_env.py <salida.md> [motor: docker|podman] [tag]
"""

import datetime
import os
import platform
import shlex
import shutil
import subprocess
import sys
from pathlib import Path

IMAGENES = {
    "cpp": "g++ --version | head -n1; echo 'Flags: -O2 -std=c++17 -ffp-contract=off'; cat /etc/os-release | grep PRETTY",
    "go": "go version; cat /etc/os-release | grep PRETTY",
    "java": "java -version 2>&1; echo 'JVM flags: -Xms1g -Xmx1g'",
    "python": "python --version; cat /etc/os-release | grep PRETTY",
    "analysis": "python --version; pip freeze | grep -Ei 'numpy|pandas|scipy|statsmodels|matplotlib'",
}


def salida(cmd):
    """Devuelve la salida (stdout + stderr) de un comando, o '(no disponible)'."""
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
        return (r.stdout + r.stderr).strip() or "(no disponible)"
    except OSError:
        return "(no disponible)"


def leer(ruta):
    try:
        return Path(ruta).read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def procesador():
    if sys.platform.startswith("linux"):
        for linea in leer("/proc/cpuinfo").splitlines():
            if linea.startswith("model name"):
                return linea.split(":", 1)[1].strip()
    elif sys.platform == "win32":
        try:
            import winreg
            clave = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                                   r"HARDWARE\DESCRIPTION\System\CentralProcessor\0")
            return winreg.QueryValueEx(clave, "ProcessorNameString")[0].strip()
        except OSError:
            pass
    elif sys.platform == "darwin":
        return salida(["sysctl", "-n", "machdep.cpu.brand_string"])
    return platform.processor() or "n/d"


def ram_total():
    """RAM total en GiB."""
    try:
        if sys.platform.startswith("linux"):
            for linea in leer("/proc/meminfo").splitlines():
                if linea.startswith("MemTotal:"):
                    return f"{int(linea.split()[1]) / 1024**2:.1f} GiB"
        elif sys.platform == "win32":
            import ctypes

            class MEMORYSTATUSEX(ctypes.Structure):
                _fields_ = [("dwLength", ctypes.c_ulong), ("dwMemoryLoad", ctypes.c_ulong),
                            ("ullTotalPhys", ctypes.c_ulonglong), ("ullAvailPhys", ctypes.c_ulonglong),
                            ("ullTotalPageFile", ctypes.c_ulonglong), ("ullAvailPageFile", ctypes.c_ulonglong),
                            ("ullTotalVirtual", ctypes.c_ulonglong), ("ullAvailVirtual", ctypes.c_ulonglong),
                            ("ullAvailExtendedVirtual", ctypes.c_ulonglong)]

            estado = MEMORYSTATUSEX()
            estado.dwLength = ctypes.sizeof(MEMORYSTATUSEX)
            ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(estado))
            return f"{estado.ullTotalPhys / 1024**3:.1f} GiB"
        elif sys.platform == "darwin":
            return f"{int(salida(['sysctl', '-n', 'hw.memsize'])) / 1024**3:.1f} GiB"
    except (ValueError, OSError, AttributeError):
        pass
    return "n/d"


def sistema_operativo():
    for linea in leer("/etc/os-release").splitlines():
        if linea.startswith("PRETTY_NAME="):
            return linea.split("=", 1)[1].strip('"')
    return platform.platform()


def main() -> int:
    destino = Path(sys.argv[1] if len(sys.argv) > 1 else "results/environment/environment.md")
    motor = shlex.split(sys.argv[2] if len(sys.argv) > 2 else "docker")
    tag = sys.argv[3] if len(sys.argv) > 3 else "1.0"
    destino.parent.mkdir(parents=True, exist_ok=True)

    gobernador = leer("/sys/devices/system/cpu/cpu0/cpufreq/scaling_governor").strip() or "n/d"
    ahora = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    L = [
        "# Entorno de ejecución", "",
        f"Registrado: {ahora}", "",
        "## Host", "", "```",
        f"Procesador:        {procesador()}",
        f"Núcleos lógicos:   {os.cpu_count()}",
        f"Arquitectura:      {platform.machine()}",
        f"RAM total:         {ram_total()}",
        f"Sistema operativo: {sistema_operativo()}",
        f"Kernel:            {platform.release()} ({platform.version()})",
        f"Gobernador CPU:    {gobernador}",
        f"Motor contenedores: {salida(motor + ['--version'])}",
        "```", "",
    ]
    if shutil.which("lscpu"):
        claves = ("Model name", "Socket", "Core", "Thread", "CPU(s)", "L1d", "L2", "L3",
                  "CPU max MHz", "CPU min MHz")
        detalle = [l for l in salida(["lscpu"]).splitlines() if l.startswith(claves)]
        L += ["```"] + detalle + ["```", ""]

    L += ["## Imágenes y versiones de lenguajes", ""]
    for lang, comando in IMAGENES.items():
        imagen = f"matmul-{lang}:{tag}"
        r = subprocess.run(motor + ["image", "inspect", "--format", "{{.Id}}", imagen],
                           capture_output=True, text=True)
        id_imagen = r.stdout.strip() if r.returncode == 0 else "no construida"
        L += [f"### {imagen}", "", "```", f"Image ID: {id_imagen}"]
        if r.returncode == 0:
            L.append(salida(motor + ["run", "--rm", "--entrypoint", "sh", imagen, "-c", comando]))
        L += ["```", ""]

    destino.write_text("\n".join(L), encoding="utf-8", newline="\n")
    print(f"Entorno registrado en {destino}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
