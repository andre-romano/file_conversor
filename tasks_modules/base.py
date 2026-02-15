# tasks_modules\base.py

import os
import platform

from pathlib import Path

from invoke.tasks import task  # pyright: ignore[reportUnknownVariableType]

# user provided
from tasks_modules import locales
from tasks_modules._config import *


WINDOWS = (platform.system() == "Windows")
LINUX = (platform.system() == "Linux")
MACOS = (platform.system() == "Darwin")


@task
def mkdirs(_: InvokeContext):
    dirs = [
        "build",
        "dist",
        f"{CACHE_DIR}",
        "docs",
        "deps",
        "htmlcov",
    ]
    for dir in dirs:
        Path(dir).mkdir(parents=True, exist_ok=True)
        if not Path(dir).exists():
            raise RuntimeError(f"Cannot create dir '{dir}'")


@task
def clean_logs(_: InvokeContext):
    remove_path_pattern(f"**/*.log")
    remove_path_pattern(f"**/*.log.*")


@task(pre=[mkdirs])  # pyright: ignore[reportUntypedFunctionDecorator]
def clean_build(_: InvokeContext):
    remove_path_pattern(f"build/*")


@task(pre=[mkdirs])  # pyright: ignore[reportUntypedFunctionDecorator]
def clean_dist(_: InvokeContext):
    remove_path_pattern(f"dist/*")


@task(pre=[mkdirs])  # pyright: ignore[reportUntypedFunctionDecorator]
def clean_cache(_: InvokeContext):
    remove_path_pattern(f"{CACHE_DIR}/*")


@task(pre=[mkdirs])  # pyright: ignore[reportUntypedFunctionDecorator]
def clean_htmlcov(_: InvokeContext):
    remove_path_pattern(f"htmlcov/*")


@task(pre=[mkdirs])  # pyright: ignore[reportUntypedFunctionDecorator]
def clean_docs(_: InvokeContext):
    remove_path_pattern(f"docs/*")


@task(pre=[mkdirs])  # pyright: ignore[reportUntypedFunctionDecorator]
def clean_deps(_: InvokeContext):
    remove_path_pattern(f"deps/*")


@task(pre=[mkdirs])  # pyright: ignore[reportUntypedFunctionDecorator]
def clean_changelog(_: InvokeContext):
    remove_path_pattern(f"CHANGELOG.md")
    remove_path_pattern(f"RELEASE_NOTES.md")


@task(pre=[mkdirs])  # pyright: ignore[reportUntypedFunctionDecorator]
def clean_requirements(_: InvokeContext):
    remove_path_pattern(f"requirements.txt")
    remove_path_pattern(f"requirements-*.txt")


@task(pre=[clean_logs,
           clean_build,
           clean_dist,
           clean_cache,
           clean_htmlcov,
           clean_docs,
           clean_deps,
           clean_changelog,
           ])  # pyright: ignore[reportUntypedFunctionDecorator]
def clean(_: InvokeContext):
    pass


@task
def licenses(c: InvokeContext):
    print("[bold]Generating THIRD_PARTY_LICENSES.md licenses report ... [/]")
    third_party_licenses_file = Path("THIRD_PARTY_LICENSES.md")
    third_party_licenses_file.unlink(missing_ok=True)
    result = c.run(" ".join([
        "pdm",
        "run",
        "pip-licenses",
        "--format=markdown",
        "--with-authors",
        "--with-urls",
        # "--with-license-file",
        f"--output-file={third_party_licenses_file}",
    ]))
    assert (result is not None) and (result.return_code == 0)
    assert third_party_licenses_file.exists()
    git_commit_push(c, third_party_licenses_file, message=f"ci: third party licenses file for {GIT_RELEASE}")
    print("[bold]Generating THIRD_PARTY_LICENSES.md licenses report ... [/][bold green]OK[/]")


@task(pre=[clean_requirements,])  # pyright: ignore[reportUntypedFunctionDecorator]
def requirements(c: InvokeContext):
    def get_pdm_export_cmd(group: str):
        group_opts: list[str]
        requirements_file: Path
        if group == "prod":
            group_opts, requirements_file = ["--prod"], Path("requirements.txt")
        elif group == "dev":
            group_opts, requirements_file = ["--dev"], Path("requirements-dev.txt")
        else:
            group_opts, requirements_file = ["-G", group], Path(f"requirements-{group}.txt")
        return [
            "pdm",
            "export",
            "-f", "requirements",
            "--without-hashes",
            *group_opts,
            "-o", str(requirements_file),
        ]

    print("[bold]Generating requirements.txt files ... [/]")
    for group, deps in get_dependencies_dict().items():
        print(f"    Exporting group {group} ({len(deps)} dependencies) ...")
        result = c.run(" ".join(get_pdm_export_cmd(group)))
        assert (result is not None) and (result.return_code == 0)
    print("[bold]Generating requirements.txt files ... [/][bold green]OK[/]")


@task(pre=[clean_deps,])  # pyright: ignore[reportUntypedFunctionDecorator]
def deps(c: InvokeContext):
    print("[bold]Checking for circular dependencies ... [/]")
    result = c.run(" ".join([
        "pdm",
        "run",
        "pydeps",
        "src/file_conversor/__main__.py",
        "--show-cycles",
        "--no-show",
        # "--no-output",
        "-o", "deps/dependencies.svg",
        "-T", "svg",
    ]))
    assert (result is not None) and (result.return_code == 0)
    print("[bold]Checking for circular dependencies ... [/][bold green]OK[/]")


@task(pre=[clean_htmlcov, locales.build])   # pyright: ignore[reportUntypedFunctionDecorator, reportUnknownMemberType]
def tests(c: InvokeContext, app: str = f"python -m {PROJECT_NAME}"):
    print("[bold] Running self tests ... [/]")
    cmd = f"pdm run {app} --self-test"
    print(f"    [italic]$ {cmd}[/]")
    result = c.run(cmd)
    assert (result is not None) and (result.return_code == 0)
    print("[bold] Running self tests ... [/][bold green]OK[/]")


# @task(pre=[clean_uml,])
# def uml(c:InvokeContext):
#     print("[bold] Generating uml/ ... [/]")
#     c.run("pdm run pyreverse -A --filter-mode=ALL --colorized -d uml/ -o jpg src/")
#     if not Path("uml/classes.jpg").exists():
#         raise RuntimeError("UML PyReverse - Empty dist/classes.jpg")
#     c.run("pdm run pydeps src/ --noshow --reverse -Tpng -o uml/dependencies.png")
#     if not Path("uml/dependencies.png").exists():
#         raise RuntimeError("UML PyDeps - Empty dist/dependencies.png")
#     print("[bold] Generating uml/ ... [/][bold green]OK[/]")

@task
def check(c: InvokeContext, exe: str | Path = ""):
    exe = exe if exe else PROJECT_NAME
    print(f"[bold] Checking app '{exe}' ... [/]")
    app_exe = shutil.which(exe)
    if not app_exe:
        raise RuntimeError(f"'{exe}' not found in PATH")
    print(f"[bold] Found:[/] '{app_exe}'")

    print(f"[bold] Checking version ...")
    result = c.run(f'"{app_exe}" -V')
    assert result is not None and result.return_code == 0
    if PROJECT_VERSION not in result.stdout:
        raise RuntimeError(f"'{exe}' version mismatch. Expected: '{PROJECT_VERSION}'.")

    # run self tests
    tests(c, app=f'"{app_exe}"')
    print(f"[bold] Checking app '{exe}' ... [/][bold green]OK[/]")


@task
def pylint(c: InvokeContext):
    print("[bold] Running pylint ... [/]")
    for module in ["src", "tests", "tasks_modules"]:
        print(f"    Running pylint for module '{module}' ...")
        result = c.run(" ".join([
            "pdm",
            "run",
            "pylint",
            "-j", "0",
            module,
        ]))
        assert (result is not None) and (result.return_code == 0)
        print(f"    Running pylint for module '{module}' ... [/][bold green]OK[/]")
    print("[bold] Running pylint ... [/][bold green]OK[/]")


@task
def ruff(c: InvokeContext):
    print("[bold] Running linter ... [/]")
    result = c.run(" ".join([
        "pdm",
        "run",
        "ruff",
        "check",
        "--no-fix",
        "--config", "./pyproject.toml",
        "src",
        "tests",
        "tasks_modules",
    ]))
    assert (result is not None) and (result.return_code == 0)
    print("[bold] Running linter ... [/][bold green]OK[/]")


@task(pre=[ruff, pylint])  # pyright: ignore[reportUntypedFunctionDecorator]
def lint(c: InvokeContext):
    """Run all linters and code quality checks."""


@task(pre=[clean_logs])  # pyright: ignore[reportUntypedFunctionDecorator]
def importtime(c: InvokeContext):
    # self, cumulative, module_name
    modules_data: list[tuple[float, float, str]] = []
    print(f"[bold] Measuring import time for app ... [/]")
    for module in ["cli"]:
        import_time_log = Path(f"import_time_{module}.log")
        import_time_log.unlink(missing_ok=True)

        result = c.run(f'pdm run python -X importtime -m {PROJECT_NAME}.{module}', hide=True, warn=True)
        assert result is not None

        import_time_log.write_text(result.stderr)
        if not import_time_log.exists():
            raise RuntimeError("Import time log file not created")

        # parse data
        for line in import_time_log.read_text().splitlines():
            try:
                # parse line
                line_parsed = line.replace("import time:", "").strip()
                time_self, time_cumulative, module_name = line_parsed.split("|")
                time_self, time_cumulative, module_name = int(time_self.strip()), int(time_cumulative.strip()), module_name.strip()
                time_self, time_cumulative = round(time_self / 1000, 2), round(time_cumulative / 1000, 2)  # convert to ms
                if (
                    re.match(rf"^.*\.", module_name) and
                    not re.match(rf"^{PROJECT_NAME}\.{module}$", module_name)
                ):
                    continue
                modules_data.append((time_self, time_cumulative, module_name))
            except Exception:
                """ ignore parsing errors """

        # sort and get top 10
        modules_data.sort(key=lambda x: x[1], reverse=True)
        modules_data = modules_data[:10]
        print()
        print(f"[bold] Top 10 imported modules for '{module}': [/]")
        for time_self, time_cumulative, module_name in modules_data:
            print(f"    cumulative={time_cumulative:>8.2f} ms,   self={time_self:>6.2f} ms,   module={module_name}")

    print()
    print(f"[bold] Measuring import time for app ... [/][bold green]OK[/]")


@task
def is_admin(_: InvokeContext):
    print(f"[bold] Checking for admin rights ... [/]")
    if WINDOWS:
        try:
            import ctypes
            if ctypes.windll.shell32.IsUserAnAdmin():  # pyright: ignore[reportAttributeAccessIssue]
                return
        except:
            """ If any error occurs (e.g., due to missing permissions), we assume the user is not admin. """
    elif os.geteuid() == 0:   # pyright: ignore[reportAttributeAccessIssue, reportUnknownMemberType]
        return
    raise RuntimeError("User is not admin")
