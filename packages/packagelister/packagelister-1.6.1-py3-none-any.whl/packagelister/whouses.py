import argparse

from pathier import Pathier

from packagelister import scan


def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "package",
        type=str,
        help=""" Scan the current working directory for project folders that use this package.""",
    )

    parser.add_argument(
        "-i",
        "--ignore",
        nargs="*",
        default=["pkgs", "envs"],
        type=str,
        help=""" Ignore these folders. """,
    )
    args = parser.parse_args()

    return args


def find(root: Pathier, package: str, ignore: list[str] = []) -> list[str]:
    """Find what sub-folders of `root`, excluding those in `ignore`, have files that use `package`."""
    package_users = []
    for project in root.iterdir():
        if project.is_dir() and project.stem not in ignore:
            if package in scan(project):
                package_users.append(project.stem)
    return package_users


def main(args: argparse.Namespace = None):
    if not args:
        args = get_args()
    package_users = find(Pathier.cwd(), args.package, args.ignore)
    print(f"The following folders have files that use {args.package}:")
    print(*package_users, sep="\n")


if __name__ == "__main__":
    main(get_args())
