import os
import sys
from importlib import import_module
from importlib.metadata import version
from pathlib import Path
from sys import platform
from sys import version as pyversion
from time import monotonic

from rich import print

system = sys.platform
REQUIREMENTS = (
    "appdirs",
    "argcomplete",
    "httpx",
    "InquirerPy",
    "keyring",
    "pydantic",
    "rich",
    "setuptools_scm",
)
HEADING = "yellow"
OK = ":heavy_check_mark:"
BAD = ":x:"

imported = {}

try:
    import appdirs

    imported["appdirs"] = appdirs
except ImportError:
    ...


try:
    import argcomplete

    imported["argcomplete"] = argcomplete
except ImportError:
    ...

try:
    import attrs

    imported["attrs"] = attrs
except ImportError:
    ...

try:
    import httpx

    imported["httpx"] = httpx
except ImportError:
    ...

try:
    import InquirerPy

    imported["InquirerPy"] = InquirerPy
except ImportError:
    ...

try:
    import keyring

    imported["keyring"] = keyring
except ImportError:
    ...

try:
    import pydantic

    imported["pydantic"] = pydantic
except ImportError:
    ...

try:
    import rich

    imported["rich"] = rich
except ImportError:
    ...

try:
    import setuptools_scm

    imported["setuptools_scm"] = setuptools_scm
except ImportError:
    ...


def check_requirements():
    print(f"\n:hammer_and_wrench: [{HEADING}]Requirements check:[/{HEADING}]")
    for req in REQUIREMENTS:
        display = OK if req in imported else BAD
        try:
            v = getattr(imported[req], "__version__", version(req))
            ver = f"[cyan bold]v{v}[/cyan bold]"
        except Exception:
            ver = "n/a"
        print(f"{display} {req} {ver}")


def check_system():
    print(f"\n:computer: [{HEADING}]System information:[/{HEADING}]")
    print(f"Platform: {platform}")
    print(f"Python: {pyversion}")


def check_config_location():
    print(f"\n:file_folder: [{HEADING}]File system access:[/{HEADING}]")

    try:
        path = Path.home()
        if system == "win32":
            path = path / "PacketFabric"
        elif system == "darwin":
            if (config_path := (path / ".config")).exists():
                path = config_path
            else:
                path = path / "Library" / "Application Support"
        else:
            if config_home := os.environ.get("XDG_CONFIG_HOME"):
                path = Path(config_home)
            else:
                path = path / ".config"
        path = path / "pfd"
    except Exception as e:
        print(f"[red]Trouble locating config dir: {path} ({e})[/red]")
    else:
        print(f"Config directory (simple): {path}")

    if "appdirs" in imported:
        config_dir = Path(appdirs.AppDirs("pfd", "PacketFabric").user_config_dir)
        print(f"Config directory (appdirs): {config_dir}")

    try:
        path.mkdir(0o700)
    except Exception as e:
        print(f"Create config file: {BAD} ({e})")
    else:
        print(f"Create config file: {OK}")

    try:
        with open(path / "dummy", "w") as f:
            f.write("Hello, world.")
    except Exception as e:
        print(f"Write to config file: {BAD} ({e})")
    else:
        print(f"Write to config file: {OK}")

    try:
        (path / "dummy").unlink()
    except Exception as e:
        print(f"Remove config file: {BAD} ({e})")
    else:
        print(f"Remove config file: {OK}")

    try:
        path.rmdir()
    except Exception as e:
        print(f"Remove config directory: {BAD} ({e})")
    else:
        print(f"Remove config directory: {OK}")


def check_keypass():
    print(f"\n:lock: [{HEADING}]Keypass storage:[/{HEADING}]")
    if "keyring" not in imported:
        print("[red]keyring not installed. Skipping[/red]")
    else:
        print(f"Backend: [green]{keyring.get_keyring()}[/green]")
        try:
            keyring.set_password("pfctltest", "foo", "bar")
        except Exception as e:
            print(f"Password set: {BAD} ({e})")
        else:
            print(f"Password set: {OK}")

        try:
            check = OK if keyring.get_password("pfctltest", "foo") == "bar" else BAD
        except Exception as e:
            print(f"Password get: {BAD} ({e})")
        else:
            print(f"Password get: {check}")

        try:
            keyring.delete_password("pfctltest", "foo")
        except Exception as e:
            print(f"Password delete: {BAD} ({e})")
        else:
            print(f"Password delete: {OK}")


def check_latency():
    print(f"\n:rocket: [{HEADING}]Latency:[/{HEADING}]")
    if "httpx" not in imported:
        print("[red]HTTPX not installed. Skipping[/red]")
    else:
        time0 = monotonic()
        httpx.get("https://api.packetfabric.com/v2")
        time1 = monotonic()
        length = round(time1 - time0, 2)
        print(f"HTTP rountrip to k8s cluster in {length} seconds")


def main():
    check_system()
    check_requirements()
    check_config_location()
    check_keypass()
    check_latency()


if __name__ == "__main__":
    main()
