import os
import re
import subprocess
import sys
import pathlib
from repo_cloner.yml_reader import read_repos_list

_help_arguments = ["--help", "-h"]
_repo_file_arguments = ["--repo_file", "-rf"]
_script_name_without_extension = __file__[:-3]
_version_arguments = ["--version", "-v"]


def _print_help():
    print("Usage: repo-cloner [--help][-h]/[--repo_file]/[-rf]/[--version][-v]")
    print("--help, -h: prints this message")
    print("--repo_file, -rf: .yml file with list of repositories to clone")
    print("--version, -v: prints version of the package")


def _verify_yml_extension(filename):
    if pathlib.Path(filename).suffix == ".yml":
        return True
    return False


def _get_version():
    filename = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),"__init__.py"))
    with open(filename, "rt") as version_file:
        init_file = version_file.read()
        version = re.search(r"__version__ = '([0-9a-z.-]+)'", init_file).group(1)
        return version


def is_git_repository(repo):
    if isinstance(repo, str):
        if repo.find("https://") != -1 or repo.find("git@") != -1:
            return True
        return False
    return False


def clone_repository(repo_link, path="."):
    print("Cloning: {} into: {}".format(repo_link, path))
    clone_repo = subprocess.run(["git", "clone", repo_link, path])
    print("The exit code was: {}".format(str(clone_repo.returncode)))


def clone_repositories(repos, repo_paths=["."]):
    for repo in repos:
        if is_git_repository(repo):
            repo_name = repo.split("/")[-1]
            repo_name = repo_name[:-4]
            path = os.path.join(repo_paths[-1], repo_name)
            clone_repository(repo, path)
            continue

        if repo_paths[-1] == ".":
            repo_paths.append(repo)
        else:
            repo_paths.append(os.path.join(repo_paths[-1], repo))
        try:
            os.mkdir(repo_paths[-1])
        except FileExistsError:
            print("{} already exist".format(repo_paths[-1]))
        clone_repositories(repos[repo], repo_paths.copy())
        repo_paths = repo_paths[:-1]


def execute_arguments(args):
    if len(args) <= 1:
        _print_help()
        return

    for h in _help_arguments:
        if h in args:
            _print_help()
            return

    for arg in args[1:]:
        if arg in _repo_file_arguments:
            file_index = args.index(arg)+1
            if file_index >= len(args):
                print("Error: missing repo .yml file argument")
                _print_help()
                return
            if args[file_index] not in _help_arguments \
                    and args[file_index] not in _repo_file_arguments \
                    and _verify_yml_extension(args[file_index]) == False:
                print("Error: bad argument for --repo_file: {}".format(args[file_index]))
                _print_help()
                return
            clone_repositories(read_repos_list(args[file_index]))
            return
        if arg in _version_arguments:
            print("repo-cloner version: {}".format(_get_version()))
        else:
            _print_help()
            return


def main():
    execute_arguments(sys.argv)


if __name__ == "__main__":
    main()
