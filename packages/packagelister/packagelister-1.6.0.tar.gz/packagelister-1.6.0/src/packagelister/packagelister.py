import ast
import importlib.metadata
import sys

from pathier import Pathier, Pathish
from printbuddies import ProgBar


def get_packages_from_source(source: str) -> list[str]:
    """Scan `source` and extract the names of imported packages/modules."""
    tree = ast.parse(source)
    packages = []
    for node in ast.walk(tree):
        type_ = type(node)
        package = ""
        if type_ == ast.Import:
            package = node.names[0].name
        elif type_ == ast.ImportFrom:
            package = node.module
        if package:
            if "." in package:
                package = package[: package.find(".")]
            packages.append(package)
    packages = sorted(list(set(packages)))
    return sorted(list(set(packages)))


def remove_builtins(packages: list[str]) -> list[str]:
    """Remove built in packages/modules from a list of package names."""
    builtins = list(sys.stdlib_module_names)
    return filter(lambda x: x not in builtins, packages)


def scan(project_dir: Pathish = None, include_builtins: bool = False) -> dict:
    """Recursively scans a directory for python files to determine
    what packages are in use, as well as the version number if applicable.

    Returns a dictionary where the keys are package names and
    the values are dictionaries with the keys `version` for the version number of the package
    if there is one (None if there isn't) and `files` for a list of the files that import the package.

    :param project_dir: Can be an absolute or relative path to a directory or a single file (.py).
    If it is relative, it will be assumed to be relative to the current working directory.
    If an argument isn't given, the current working directory will be scanned.
    If the path doesn't exist, an empty dictionary is returned."""
    if not project_dir:
        project_dir = Pathier.cwd()
    elif type(project_dir) is str or project_dir.is_file():
        project_dir = Pathier(project_dir)
    if not project_dir.is_absolute():
        project_dir = project_dir.absolute()

    # Raise error if project_dir doesn't exist
    if not project_dir.exists():
        raise FileNotFoundError(
            f"Can't scan directory that doesn't exist: {project_dir}"
        )
    # You can scan a non python file one at a time if you reeeally want to.
    if project_dir.is_file():
        files = [project_dir]
    else:
        files = list(project_dir.rglob("*.py"))

    bar = ProgBar(len(files), width_ratio=0.33)
    used_packages = {}
    for file in files:
        bar.display(suffix=f"Scanning {file.name}")
        source = file.read_text(encoding="utf-8")
        packages = get_packages_from_source(source)
        if not include_builtins:
            packages = remove_builtins(packages)
        for package in packages:
            if file.with_stem(package) not in files:
                if (
                    package in used_packages
                    and str(file) not in used_packages[package]["files"]
                ):
                    used_packages[package]["files"].append(str(file))
                else:
                    try:
                        package_version = importlib.metadata.version(package)
                    except ModuleNotFoundError:
                        package_version = None
                    except Exception as e:
                        print(e)
                        package_version = None
                    used_packages[package] = {
                        "files": [str(file)],
                        "version": package_version,
                    }
    return used_packages
