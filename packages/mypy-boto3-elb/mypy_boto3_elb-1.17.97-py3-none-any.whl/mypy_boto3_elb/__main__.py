import sys


def print_info() -> None:
    print(
        "Type annotations for boto3.ElasticLoadBalancing 1.17.97\n"
        "Version:         1.17.97\n"
        "Builder version: 4.18.3\n"
        "Docs:            https://pypi.org/project/mypy-boto3-elb/\n"
        "Boto3 docs:      https://boto3.amazonaws.com/v1/documentation/api/1.17.97/reference/services/elb.html#ElasticLoadBalancing\n"
        "Other services:  https://pypi.org/project/boto3-stubs/\n"
        "Changelog:       https://github.com/vemel/mypy_boto3_builder/releases"
    )


def print_version() -> None:
    print("1.17.97")


def main() -> None:
    if "--version" in sys.argv:
        return print_version()
    print_info()


if __name__ == "__main__":
    main()
