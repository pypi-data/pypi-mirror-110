import sys


def print_info() -> None:
    print(
        "Type annotations for botocore 1.20.98\n"
        "Version:         1.20.98\n"
        "Builder version: 4.18.3\n"
        "Docs:            https://pypi.org/project/boto3-stubs/\n"
        "Changelog:       https://github.com/vemel/mypy_boto3_builder/releases"
    )


def print_version() -> None:
    print("1.20.98")


def main() -> None:
    if "--version" in sys.argv:
        return print_version()
    print_info()


if __name__ == "__main__":
    main()
