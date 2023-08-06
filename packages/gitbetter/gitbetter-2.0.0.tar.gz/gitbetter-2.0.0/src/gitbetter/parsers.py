from argshell import ArgShellParser


def new_remote_parser() -> ArgShellParser:
    parser = ArgShellParser()
    parser.add_argument(
        "--public",
        action="store_true",
        help=""" Set the new remote visibility as public. Defaults to private. """,
    )
    return parser


def commit_files_parser() -> ArgShellParser:
    parser = ArgShellParser()
    parser.add_argument(
        "files", type=str, nargs="*", help=""" List of files to stage and commit. """
    )
    parser.add_argument(
        "-m",
        "--message",
        type=str,
        required=True,
        help=""" The commit message to use. """,
    )
    return parser


def add_files_parser() -> ArgShellParser:
    parser = ArgShellParser()
    parser.add_argument(
        "files",
        type=str,
        nargs="*",
        default=None,
        help=""" List of files to stage and commit. 
        If not given, all files will be added.""",
    )
    return parser


def delete_branch_parser() -> ArgShellParser:
    parser = ArgShellParser()
    parser.add_argument(
        "branch", type=str, help=""" The name of the branch to delete. """
    )
    parser.add_argument(
        "-r",
        "--remote",
        action="store_true",
        help=""" Delete the remote and remote-tracking branches along with the local branch.
        By default only the local branch is deleted.""",
    )
    return parser
