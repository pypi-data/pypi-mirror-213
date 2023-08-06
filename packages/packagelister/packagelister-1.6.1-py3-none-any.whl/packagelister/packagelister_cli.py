import argparse

from pathier import Pathier

from packagelister import scan

""" These are packages whose name doesn't match their `pip install` name.
When `packagelister` is generating a requirements file, these substitutions will be made."""

pipmappings = {"speech_recognition": "SpeechRecognition"}


def main():
    def get_args() -> argparse.Namespace:
        parser = argparse.ArgumentParser()

        parser.add_argument(
            "project_path",
            nargs="?",
            type=str,
            default=None,
            help=""" The project directory path to scan. """,
        )

        parser.add_argument(
            "-s",
            "--show_files",
            action="store_true",
            help=""" Show which files imported each of the packages. """,
        )

        parser.add_argument(
            "-g",
            "--generate_requirements",
            action="store_true",
            help=""" Generate a requirements.txt file in --project_path. """,
        )

        parser.add_argument(
            "-v",
            "--versions",
            type=str,
            default=None,
            choices=["==", "<", "<=", ">", ">=", "~="],
            help=""" When generating a requirements.txt file, include the versions of the packages using this relation.
            (You may need to put quotes around some of the options.)""",
        )

        parser.add_argument(
            "-i",
            "--include_builtins",
            action="store_true",
            help=""" Include built in standard library modules. """,
        )

        args = parser.parse_args()

        if not args.project_path:
            args.project_path = Pathier.cwd()
        else:
            args.project_path = Pathier(args.project_path)
        if not args.project_path.is_absolute():
            args.project_path = args.project_path.absolute()

        return args

    args = get_args()
    packages = scan(args.project_path, args.include_builtins)
    packages.pop(args.project_path.stem, None)
    if args.generate_requirements:
        req_path = args.project_path / "requirements.txt"
        requirements = "\n".join(
            f"{package}{args.versions}{packages[package]['version']}"
            if args.versions
            else f"{package}"
            if packages[package]["version"]
            else package
            for package in sorted(packages)
        )
        for mapping in pipmappings:
            requirements = requirements.replace(mapping, pipmappings[mapping])
        req_path.write_text(requirements)
    packages = {
        f"{package}=={packages[package]['version']}": packages[package]["files"]
        for package in sorted(packages)
    }

    if args.show_files:
        longest_key = max(len(package) for package in packages)
        packages = [
            f"{package}{' '*(longest_key-len(package)+4)}{', '.join(str(Pathier(file).relative_to(args.project_path)) for file in packages[package])}"
            for package in packages
        ]

    print(f"Packages used in {args.project_path.stem}:")
    print(
        *packages,
        sep="\n",
    )


if __name__ == "__main__":
    main()
