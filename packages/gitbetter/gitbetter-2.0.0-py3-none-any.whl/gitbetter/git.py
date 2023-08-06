import shlex
import subprocess
from contextlib import contextmanager
from pathlib import Path
from urllib.parse import urlparse

from pathier import Pathier, Pathish


class Git:
    def __init__(self, capture_stdout: bool = False):
        """If `capture_stdout` is `True`, all functions will return their generated `stdout` as a string.
        Otherwise, the functions return the call's exit code."""
        self.capture_stdout = capture_stdout

    @property
    def capture_stdout(self) -> bool:
        """If `True`, member functions will return the generated `stdout` as a string,
        otherwise they return the command's exit code."""
        return self._capture_stdout

    @capture_stdout.setter
    def capture_stdout(self, should_capture: bool):
        self._capture_stdout = should_capture

    def _run(self, args: list[str]) -> str | int:
        if self._capture_stdout:
            return subprocess.run(args, stdout=subprocess.PIPE, text=True).stdout
        else:
            return subprocess.run(args).returncode

    @contextmanager
    def capture_output(self):
        self.capture_stdout = True
        yield self
        self.capture_stdout = False

    # Seat |===================================================Core===================================================|

    def git(self, command: str) -> str | int:
        """Base function for executing git commands.
        Use this if another function doesn't meet your needs.
        >>> git {command}"""
        args = ["git"] + shlex.split(command)
        return self._run(args)

    # Seat

    def add(self, args: str = "") -> str | int:
        """>>> git add {args}"""
        return self.git(f"add {args}")

    def am(self, args: str = "") -> str | int:
        """>>> git am {args}"""
        return self.git(f"am {args}")

    def annotate(self, args: str = "") -> str | int:
        """>>> git annotate {args}"""
        return self.git(f"annotate {args}")

    def archive(self, args: str = "") -> str | int:
        """>>> git archive {args}"""
        return self.git(f"archive {args}")

    def bisect(self, args: str = "") -> str | int:
        """>>> git bisect {args}"""
        return self.git(f"bisect {args}")

    def blame(self, args: str = "") -> str | int:
        """>>> git blame {args}"""
        return self.git(f"blame {args}")

    def branch(self, args: str = "") -> str | int:
        """>>> git branch {args}"""
        return self.git(f"branch {args}")

    def bugreport(self, args: str = "") -> str | int:
        """>>> git bugreport {args}"""
        return self.git(f"bugreport {args}")

    def bundle(self, args: str = "") -> str | int:
        """>>> git bundle {args}"""
        return self.git(f"bundle {args}")

    def checkout(self, args: str = "") -> str | int:
        """>>> git checkout {args}"""
        return self.git(f"checkout {args}")

    def cherry_pick(self, args: str = "") -> str | int:
        """>>> git cherry-pick {args}"""
        return self.git(f"cherry-pick {args}")

    def citool(self, args: str = "") -> str | int:
        """>>> git citool {args}"""
        return self.git(f"citool {args}")

    def clean(self, args: str = "") -> str | int:
        """>>> git clean {args}"""
        return self.git(f"clean {args}")

    def clone(self, args: str = "") -> str | int:
        """>>> git clone {args}"""
        return self.git(f"clone {args}")

    def commit(self, args: str = "") -> str | int:
        """>>> git commit {args}"""
        return self.git(f"commit {args}")

    def config(self, args: str = "") -> str | int:
        """>>> git config {args}"""
        return self.git(f"config {args}")

    def count_objects(self, args: str = "") -> str | int:
        """>>> git count-objects {args}"""
        return self.git(f"count-objects {args}")

    def describe(self, args: str = "") -> str | int:
        """>>> git describe {args}"""
        return self.git(f"describe {args}")

    def diagnose(self, args: str = "") -> str | int:
        """>>> git diagnose {args}"""
        return self.git(f"diagnose {args}")

    def diff(self, args: str = "") -> str | int:
        """>>> git diff {args}"""
        return self.git(f"diff {args}")

    def difftool(self, args: str = "") -> str | int:
        """>>> git difftool {args}"""
        return self.git(f"difftool {args}")

    def fast_export(self, args: str = "") -> str | int:
        """>>> git fast-export {args}"""
        return self.git(f"fast-export {args}")

    def fast_import(self, args: str = "") -> str | int:
        """>>> git fast-import {args}"""
        return self.git(f"fast-import {args}")

    def fetch(self, args: str = "") -> str | int:
        """>>> git fetch {args}"""
        return self.git(f"fetch {args}")

    def filter_branch(self, args: str = "") -> str | int:
        """>>> git filter-branch {args}"""
        return self.git(f"filter-branch {args}")

    def format_patch(self, args: str = "") -> str | int:
        """>>> git format-patch {args}"""
        return self.git(f"format-patch {args}")

    def fsck(self, args: str = "") -> str | int:
        """>>> git fsck {args}"""
        return self.git(f"fsck {args}")

    def gc(self, args: str = "") -> str | int:
        """>>> git gc {args}"""
        return self.git(f"gc {args}")

    def gitk(self, args: str = "") -> str | int:
        """>>> git gitk {args}"""
        return self.git(f"gitk {args}")

    def gitweb(self, args: str = "") -> str | int:
        """>>> git gitweb {args}"""
        return self.git(f"gitweb {args}")

    def grep(self, args: str = "") -> str | int:
        """>>> git grep {args}"""
        return self.git(f"grep {args}")

    def gui(self, args: str = "") -> str | int:
        """>>> git gui {args}"""
        return self.git(f"gui {args}")

    def help(self, args: str = "") -> str | int:
        """>>> git help {args}"""
        return self.git(f"help {args}")

    def init(self, args: str = "") -> str | int:
        """>>> git init {args}"""
        return self.git(f"init {args}")

    def instaweb(self, args: str = "") -> str | int:
        """>>> git instaweb {args}"""
        return self.git(f"instaweb {args}")

    def log(self, args: str = "") -> str | int:
        """>>> git log {args}"""
        return self.git(f"log {args}")

    def maintenance(self, args: str = "") -> str | int:
        """>>> git maintenance {args}"""
        return self.git(f"maintenance {args}")

    def merge(self, args: str = "") -> str | int:
        """>>> git merge {args}"""
        return self.git(f"merge {args}")

    def merge_tree(self, args: str = "") -> str | int:
        """>>> git merge-tree {args}"""
        return self.git(f"merge-tree {args}")

    def mergetool(self, args: str = "") -> str | int:
        """>>> git mergetool {args}"""
        return self.git(f"mergetool {args}")

    def mv(self, args: str = "") -> str | int:
        """>>> git mv {args}"""
        return self.git(f"mv {args}")

    def notes(self, args: str = "") -> str | int:
        """>>> git notes {args}"""
        return self.git(f"notes {args}")

    def pack_refs(self, args: str = "") -> str | int:
        """>>> git pack-refs {args}"""
        return self.git(f"pack-refs {args}")

    def prune(self, args: str = "") -> str | int:
        """>>> git prune {args}"""
        return self.git(f"prune {args}")

    def pull(self, args: str = "") -> str | int:
        """>>> git pull {args}"""
        return self.git(f"pull {args}")

    def push(self, args: str = "") -> str | int:
        """>>> git push {args}"""
        return self.git(f"push {args}")

    def range_diff(self, args: str = "") -> str | int:
        """>>> git range-diff {args}"""
        return self.git(f"range-diff {args}")

    def rebase(self, args: str = "") -> str | int:
        """>>> git rebase {args}"""
        return self.git(f"rebase {args}")

    def reflog(self, args: str = "") -> str | int:
        """>>> git reflog {args}"""
        return self.git(f"reflog {args}")

    def remote(self, args: str = "") -> str | int:
        """>>> git remote {args}"""
        return self.git(f"remote {args}")

    def repack(self, args: str = "") -> str | int:
        """>>> git repack {args}"""
        return self.git(f"repack {args}")

    def replace(self, args: str = "") -> str | int:
        """>>> git replace {args}"""
        return self.git(f"replace {args}")

    def request_pull(self, args: str = "") -> str | int:
        """>>> git request-pull {args}"""
        return self.git(f"request-pull {args}")

    def rerere(self, args: str = "") -> str | int:
        """>>> git rerere {args}"""
        return self.git(f"rerere {args}")

    def reset(self, args: str = "") -> str | int:
        """>>> git reset {args}"""
        return self.git(f"reset {args}")

    def restore(self, args: str = "") -> str | int:
        """>>> git restore {args}"""
        return self.git(f"restore {args}")

    def revert(self, args: str = "") -> str | int:
        """>>> git revert {args}"""
        return self.git(f"revert {args}")

    def rm(self, args: str = "") -> str | int:
        """>>> git rm {args}"""
        return self.git(f"rm {args}")

    def scalar(self, args: str = "") -> str | int:
        """>>> git scalar {args}"""
        return self.git(f"scalar {args}")

    def shortlog(self, args: str = "") -> str | int:
        """>>> git shortlog {args}"""
        return self.git(f"shortlog {args}")

    def show(self, args: str = "") -> str | int:
        """>>> git show {args}"""
        return self.git(f"show {args}")

    def show_branch(self, args: str = "") -> str | int:
        """>>> git show-branch {args}"""
        return self.git(f"show-branch {args}")

    def sparse_checkout(self, args: str = "") -> str | int:
        """>>> git sparse-checkout {args}"""
        return self.git(f"sparse-checkout {args}")

    def stash(self, args: str = "") -> str | int:
        """>>> git stash {args}"""
        return self.git(f"stash {args}")

    def status(self, args: str = "") -> str | int:
        """>>> git status {args}"""
        return self.git(f"status {args}")

    def submodule(self, args: str = "") -> str | int:
        """>>> git submodule {args}"""
        return self.git(f"submodule {args}")

    def switch(self, args: str = "") -> str | int:
        """>>> git switch {args}"""
        return self.git(f"switch {args}")

    def tag(self, args: str = "") -> str | int:
        """>>> git tag {args}"""
        return self.git(f"tag {args}")

    def verify_commit(self, args: str = "") -> str | int:
        """>>> git verify-commit {args}"""
        return self.git(f"verify-commit {args}")

    def verify_tag(self, args: str = "") -> str | int:
        """>>> git verify-tag {args}"""
        return self.git(f"verify-tag {args}")

    def version(self, args: str = "") -> str | int:
        """>>> git version {args}"""
        return self.git(f"version {args}")

    def whatchanged(self, args: str = "") -> str | int:
        """>>> git whatchanged {args}"""
        return self.git(f"whatchanged {args}")

    def worktree(self, args: str = "") -> str | int:
        """>>> git worktree {args}"""
        return self.git(f"worktree {args}")

    # Seat |=================================================Convenience=================================================|

    @property
    def current_branch(self) -> str:
        """Returns the name of the currently active branch."""
        capturing_output = self.capture_stdout
        current_branch = ""
        with self.capture_output():
            branches = self.branch().splitlines()  # type: ignore
            for branch in branches:
                if branch.startswith("*"):
                    current_branch = branch[2:]
                    break
        self.capture_stdout = capturing_output
        return current_branch

    @property
    def origin_url(self) -> str | int:
        """The remote origin url for this repo
        >>> git remote get-url origin"""
        return self.remote("get-url origin")

    def add_all(self) -> str | int:
        """Stage all modified and untracked files.
        >>> git add ."""
        return self.add(".")

    def add_files(self, files: list[Pathish]) -> str | int:
        """Stage a list of files."""
        args = " ".join([str(file).replace("\\", "/") for file in files])
        return self.add(args)

    def add_remote_url(self, url: str, name: str = "origin") -> str | int:
        """Add remote url to repo.
        >>> git remote add {name} {url}"""
        return self.remote(f"add {name} {url}")

    def amend(self, files: list[Pathish] | None = None) -> str | int:
        """Stage and commit changes to the previous commit.

        If `files` is `None`, all files will be staged.

        >>> git add {files} or git add .
        >>> git commit --amend --no-edit
        """
        return (self.add(files) if files else self.add_all()) + self.commit("--amend --no-edit")  # type: ignore

    def commit_all(self, message: str) -> str | int:
        """Stage and commit all files with `message`.
        >>> git add .
        >>> git commit -m \"{message}\" """
        return self.add_all() + self.commit(f'-m "{message}"')  # type: ignore

    def commit_files(self, files: list[Pathish], message: str) -> str | int:
        """Stage and commit a list of files with commit message `message`.
        >>> git add {files}
        >>> git commit -m \"{message}\" """
        return self.add_files(files) + self.commit(f'-m "{message}"')  # type: ignore

    def create_new_branch(self, branch_name: str) -> str | int:
        """Create and switch to a new branch named with `branch_name`.
        >>> git checkout -b {branch_name} --track"""
        return self.checkout(f"-b {branch_name} --track")

    def delete_branch(self, branch_name: str, local_only: bool = True) -> str | int:
        """Delete `branch_name` from repo.

        #### :params:

        `local_only`: Only delete the local copy of `branch`, otherwise also delete the remote branch on origin and remote-tracking branch.
        >>> git branch --delete {branch_name}

        Then if not `local_only`:
        >>> git push origin --delete {branch_name}
        """
        output = self.branch(f"--delete {branch_name}")
        if not local_only:
            return output + self.push(f"origin --delete {branch_name}")  # type: ignore
        return output

    def initcommit(self, files: list[Pathish] | None = None) -> str | int:
        """Stage and commit `files` with the message `Initial commit`.

        If `files` is not given, all files will be added and committed.
        >>> git add {files} or git add .
        >>> git commit -m "Initial commit" """
        return (self.add_files(files) if files else self.add_all()) + self.commit('-m "Initial commit"')  # type: ignore

    def list_branches(self) -> str | int:
        """>>> git branch -vva"""
        return self.branch("-vva")

    def loggy(self) -> str | int:
        """>>> git log --oneline --name-only --abbrev-commit --graph"""
        return self.log("--oneline --name-only --abbrev-commit --graph")

    def new_repo(self) -> str | int:
        """Initialize a new repo in current directory.
        >>> git init -b main"""
        return self.init("-b main")

    def push_new_branch(self, branch: str) -> str | int:
        """Push a new branch to origin with tracking.
        >>> git push -u origin {branch}"""
        return self.push(f"-u origin {branch}")

    def switch_branch(self, branch_name: str) -> str | int:
        """Switch to the branch specified by `branch_name`.
        >>> git checkout {branch_name}"""
        return self.checkout(branch_name)

    def undo(self) -> str | int:
        """Undo uncommitted changes.
        >>> git checkout ."""
        return self.checkout(".")

    def ignore(self, patterns: list[str]):
        """Add `patterns` to `.gitignore`."""
        gitignore = Pathier(".gitignore")
        if not gitignore.exists():
            gitignore.touch()
        ignores = gitignore.split()
        ignores += [pattern for pattern in patterns if pattern not in ignores]
        gitignore.join(ignores)

    # Seat |===============================Requires GitHub CLI to be installed and configured===============================|

    @property
    def owner(self) -> str:
        return self._owner_reponame().split("/")[0]

    @property
    def repo_name(self) -> str:
        return self._owner_reponame().split("/")[1]

    def _change_visibility(self, visibility: str) -> str | int:
        return self._run(
            [
                "gh",
                "repo",
                "edit",
                f"{self.owner}/{self.repo_name}",
                "--visibility",
                visibility,
            ]
        )

    def _owner_reponame(self) -> str:
        """Returns "owner/repo-name", assuming there's one remote origin url and it's for github."""
        with self.capture_output():
            return urlparse(self.origin_url().strip("\n")).path.strip("/")  # type: ignore

    def create_remote(self, name: str, public: bool = False) -> str | int:
        """Uses GitHub CLI (must be installed and configured) to create a remote GitHub repo.

        #### :params:

        `name`: The name for the repo.

        `public`: Set to `True` to create the repo as public, otherwise it'll be created as private.
        """
        visibility = "--public" if public else "--private"
        return self._run(["gh", "repo", "create", name, visibility])

    def create_remote_from_cwd(self, public: bool = False) -> str | int:
        """Use GitHub CLI (must be installed and configured) to create a remote GitHub repo from
        the current working directory repo and add its url as this repo's remote origin.

        #### :params:

        `public`: Create the GitHub repo as a public repo, default is to create it as private.
        """
        visibility = "public" if public else "private"
        return self._run(
            ["gh", "repo", "create", "--source", ".", f"--{visibility}", "--push"]
        )

    def delete_remote(self) -> str | int:
        """Uses GitHub CLI (must be isntalled and configured) to delete the remote for this repo."""
        return self._run(
            ["gh", "repo", "delete", f"{self.owner}/{self.repo_name}", "--yes"]
        )

    def make_private(self) -> str | int:
        """Uses GitHub CLI (must be installed and configured) to set the repo's visibility to private."""
        return self._change_visibility("private")

    def make_public(self) -> str | int:
        """Uses GitHub CLI (must be installed and configured) to set the repo's visibility to public."""
        return self._change_visibility("public")
