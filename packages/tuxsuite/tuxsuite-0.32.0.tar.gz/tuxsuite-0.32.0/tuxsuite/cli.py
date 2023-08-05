# -*- coding: utf-8 -*-

import click
from functools import wraps
import json
import os
import sys
import tuxsuite
import tuxsuite.download
import tuxsuite.exceptions
import tuxsuite.gitutils


from tuxsuite.utils import (
    defaults,
    ResultState,
    result_states,
)

info = click.echo


def error(msg):
    raise click.ClickException(msg)


def warning(msg):
    click.echo(msg, err=True)


def no_info(_):
    pass


def quiet_output(quiet):
    global info
    info = no_info if quiet else click.echo


def print_state(state, prefix=""):
    msg = click.style(
        f"{prefix}{state.icon} {state.message}: ", fg=state.cli_color, bold=True
    ) + str(state.build)

    if state.status == "fail" or state.state == "error" or state.warnings:
        warning(msg)
    else:
        info(msg)


def wait_for_object(build_object):
    result = True
    for state in build_object.watch():
        print_state(state)
        if state.status == "fail" or state.state == "error" and state.final:
            result = False
    return result


def key_value(s):
    if "=" not in s:
        error(f"Key Value pair not valid: {s}")
    parts = s.split("=")
    return (parts[0], "=".join(parts[1:]))


def get_make_targets_vars(targets):
    target_list = []
    make_variables = {}
    if targets:
        key_values = [arg for arg in targets if "=" in arg]
        for kv in key_values:
            if kv.count("=") > 1:
                sys.stderr.write(f"Error: invalid KEY=VALUE: {kv}")
                sys.exit(1)
            make_variables = dict((arg.split("=") for arg in key_values))
        target_list = [arg for arg in targets if "=" not in arg]
    return (target_list, make_variables)


def format_result(result_json, tuxapi_tests_url=None):
    state = result_states.get(result_json["state"], None)
    result = result_json["result"]
    result_msg = ""
    if "build_name" in result_json:
        result_msg = (
            f"{result_json['target_arch']} "
            f"({','.join(result_json['kconfig'])}) "
            f"with {result_json['toolchain']} @ {result_json['download_url']}"
        )
    elif "tests" in result_json:
        result_msg = (
            f"[{','.join(result_json['tests'])}] "
            f"{result_json['device']} @ {tuxapi_tests_url}"
        )
    if state is None:
        errors = 0
        warnings = 0

        if result == "pass":
            warnings = result_json.get("warnings_count", 0)
            if warnings == 0:
                icon = "🎉"
                message = "Pass"
                cli_color = "green"
            else:
                icon = "👾"
                cli_color = "yellow"
                if warnings == 1:
                    message = "Pass (1 warning)"
                else:
                    message = "Pass ({} warnings)".format(warnings)
        elif result == "fail":
            icon = "👹"
            cli_color = "bright_red"
            errors = result_json.get("errors_count", 0)
            if errors == 1:
                message = "Fail (1 error)"
            else:
                message = "Fail ({} errors)".format(errors)
            if "tests" in result_json:
                errors = [
                    name
                    for name in result_json["results"]
                    if result_json["results"][name] == "fail"
                ]
                message = "Fail ({})".format(", ".join(errors))
                errors = len(errors)
        else:
            icon = "🔧"
            cli_color = "bright_red"
            message = result_json["status_message"]
        state = ResultState(
            state=state,
            status=result_json["state"],
            final=True,
            message=message,
            icon=icon,
            cli_color=cli_color,
            warnings=warnings,
            errors=errors,
        )
    msg = (
        click.style(f"{state.icon} {state.message}: ", fg=state.cli_color, bold=True)
        + result_msg
    )
    if result == "fail" or result == "error":
        warning(msg)
    else:
        info(msg)


@click.group(name="tuxsuite")
@click.version_option()  # Implement --version
def cli():
    pass


def common_options(required):
    def option(*args, **kwargs):
        kw = kwargs.copy()
        kw["required"] = False
        for a in args:
            if a in required:
                kw["required"] = True
        return click.option(*args, **kw)

    options = [
        option("--git-repo", help="Git repository"),
        option("--git-ref", help="Git reference"),
        option("--git-sha", help="Git commit"),
        option(
            "--git-head",
            default=False,
            is_flag=True,
            help="Build the current git HEAD. Overrrides --git-repo and --git-ref",
        ),
        option(
            "--target-arch",
            help="Target architecture [arc|arm|arm64|hexagon|i386|mips|parisc|powerpc|riscv|s390|sh|sparc|x86_64]",
        ),
        option(
            "--kernel-image",
            help="Specify custom kernel image that you wish to build",
        ),
        option(
            "--kconfig",
            multiple=True,
            help="Kernel kconfig arguments (may be specified multiple times)",
        ),
        option(
            "--toolchain",
            help="Toolchain [gcc-8|gcc-9|gcc-10|gcc-11|clang-10|clang-11|clang-12|clang-nightly|clang-android]",
        ),
        option(
            "--build-name",
            help=("User defined string to identify the build"),
        ),
        option(
            "--json-out",
            help="Write json build status out to a named file path",
            type=click.File("w", encoding="utf-8"),
        ),
        option(
            "-d",
            "--download",
            default=False,
            is_flag=True,
            help="Download artifacts after builds finish",
        ),
        option(
            "-o",
            "--output-dir",
            default=".",
            help="Directory where to download artifacts",
        ),
        option(
            "-n",
            "--no-wait",
            default=False,
            is_flag=True,
            help="Don't wait for the builds to finish",
        ),
        option(
            "-q",
            "--quiet",
            default=False,
            is_flag=True,
            help="Supress all informational output; prints only the download URL for the build",
        ),
        option(
            "-s",
            "--show-logs",
            default=False,
            is_flag=True,
            help="Prints build logs to stderr in case of warnings or errors",
        ),
        option(
            "-e",
            "--environment",
            type=key_value,
            multiple=True,
            help="Set environment variables for the build. Format: KEY=VALUE",
        ),
    ]

    def wrapper(f):
        f = wraps(f)(process_git_head(f))
        for opt in options:
            f = opt(f)
        return f

    return wrapper


def process_git_head(f):
    def wrapper(**kw):
        git_head = kw["git_head"]
        if git_head:
            try:
                repo, sha = tuxsuite.gitutils.get_git_head()
                kw["git_repo"] = repo
                kw["git_sha"] = sha
            except Exception as e:
                error(e)
        return f(**kw)

    return wrapper


def show_log(build, download, output_dir):
    if not build.warnings_count and not build.errors_count:
        return
    print("📄 Logs for {}:".format(build), file=sys.stderr)
    sys.stderr.flush()
    if download:
        for line in open(os.path.join(output_dir, build.uid, "build.log")):
            print(line.strip(), file=sys.stderr)
    else:
        tuxsuite.download.download_file(
            os.path.join(build.build_data, "build.log"), sys.stderr.buffer
        )


description = (
    "Positional arguments:\n\n"
    "[KEY=VALUE | target] ...    Make variables to use and targets to build."
    "\n\n"
    "\t\t\t    If no TARGETs are specified, tuxsuite will build "
    f"{' + '.join(defaults.targets)}."
)


@cli.command(help=description, short_help="Run a single build.")
@common_options(required=["--target-arch", "--kconfig", "--toolchain"])
@click.argument("targets", metavar="[VAR=VALUE...] [target ...]", nargs=-1)
def build(
    json_out=None,
    quiet=False,
    show_logs=None,
    git_head=False,
    download=False,
    output_dir=None,
    no_wait=False,
    **build_params,
):
    quiet_output(quiet)

    if "targets" in build_params:
        target_list, make_vars = get_make_targets_vars(build_params["targets"])
        build_params["targets"] = target_list
        build_params["make_variables"] = make_vars

    try:
        build = tuxsuite.Build(**build_params)
    except (AssertionError, tuxsuite.exceptions.TuxSuiteError) as e:
        error(e)
    info(
        "Building Linux Kernel {} at {}".format(
            build.git_repo, build.git_ref or build.git_sha
        )
    )
    try:
        build.build()
        info("uid: {}".format(build.uid))
    except tuxsuite.exceptions.BadRequest as e:
        raise (click.ClickException(str(e)))

    build_result = True

    if no_wait:
        format_result(build.status)
    else:
        build_result = wait_for_object(build)

    if json_out:
        json_out.write(json.dumps(build.status, sort_keys=True, indent=4))
    if download:
        tuxsuite.download.download(build, output_dir)
    if show_logs:
        show_log(build, download, output_dir)
    if quiet:
        print(build.build_data)

    if not build_result:
        sys.exit(1)


@cli.command(help=description, short_help="Run a set of builds.")
@click.option("--set-name", required=True, help="Set name")
@click.option("--tux-config", help="Path or a web URL to tuxsuite config file")
@click.argument("targets", metavar="[VAR=VALUE...] [target ...]", nargs=-1)
@common_options(required=[])
def build_set(
    tux_config,
    set_name,
    json_out=None,
    quiet=None,
    show_logs=None,
    git_head=False,
    download=False,
    output_dir=None,
    no_wait=False,
    **build_params,
):
    quiet_output(quiet)

    if "targets" in build_params:
        target_list, make_vars = get_make_targets_vars(build_params["targets"])
        build_params["targets"] = target_list
        build_params["make_variables"] = make_vars

    try:
        build_set_config = tuxsuite.config.BuildSetConfig(set_name, tux_config)
        build_set = tuxsuite.BuildSet(build_set_config.entries, **build_params)
    except (AssertionError, tuxsuite.exceptions.TuxSuiteError) as e:
        error(e)

    info("Building Linux Kernel build set {}".format(set_name))

    try:
        build_set.build()
    except tuxsuite.exceptions.BadRequest as e:
        raise (click.ClickException(str(e)))

    if no_wait:
        build_status_list = []
        for build in build_set.builds:
            format_result(build.status)
            if json_out:
                build_status_list.append(build.status)
        if build_status_list:
            json_out.write(json.dumps(build_status_list, sort_keys=True, indent=4))
        return

    build_set_result = wait_for_object(build_set)

    if json_out:
        json_out.write(json.dumps(build_set.status_list, sort_keys=True, indent=4))

    if download:
        for build in build_set.builds:
            tuxsuite.download.download(build, output_dir)

    if show_logs:
        for build in build_set.builds:
            show_log(build, download, output_dir)

    if quiet:
        for build in build_set.builds:
            print(build.build_data)

    # If any of the builds did not pass, exit with exit code of 1
    if not build_set_result:
        sys.exit(1)


DEVICES = [
    "qemu-arm",
    "qemu-armv5",
    "qemu-armv7",
    "qemu-arm64",
    "qemu-i386",
    "qemu-mips",
    "qemu-mips64",
    "qemu-mips64el",
    "qemu-powerpc",
    "qemu-ppc64",
    "qemu-ppc64le",
    "qemu-riscv",
    "qemu-riscv64",
    "qemu-sparc64",
    "qemu-x86_64",
]
TESTS = [
    "boot",
    "ltp-fcntl-locktests",
    "ltp-fs_bind",
    "ltp-fsx",
    "ltp-nptl",
    "ltp-smoke",
]


@cli.command(help="Test a kernel", short_help="Test a kernel")
@click.option("--device", help="Device type", required=True, type=click.Choice(DEVICES))
@click.option("--kernel", help="URL of the kernel to test", default="", type=str)
@click.option("--modules", help="URL of the kernel modules", default=None, type=str)
@click.option(
    "--tests",
    help="Comma separated list of tests",
    default="boot",
)
@click.option("--boot-args", help="Extra boot arguments", default=None, type=str)
@click.option("--wait-for", help="Wait for a test uid", default=None, type=str)
@click.option(
    "-n",
    "--no-wait",
    default=False,
    is_flag=True,
    help="Don't wait for tests to finish",
)
@click.option(
    "--json-out",
    help="Write json test status out to a named file path",
    type=click.File("w", encoding="utf-8"),
)
def test(device, kernel, modules, tests, boot_args, wait_for, no_wait, json_out):
    tests = [test for test in tests.split(",") if test]
    invalid_tests = [test for test in tests if test not in TESTS]
    if invalid_tests:
        raise click.ClickException(
            "Invalid tests [{}], only valid tests are: [{}]".format(
                ", ".join(invalid_tests), ", ".join(TESTS)
            )
        )
    tests = [test for test in tests if test != "boot"]
    if wait_for:
        info(
            "Testing build {} on {} with {}".format(
                wait_for, device, ", ".join(["boot"] + tests)
            )
        )
        if kernel:
            raise click.ClickException("--kernel and --wait-for are mutually exclusive")
        if modules:
            raise click.ClickException(
                "--modules and --wait-for are mutually exclusive"
            )
    else:
        info(
            "Testing {} on {} with {}".format(
                kernel, device, ", ".join(["boot"] + tests)
            )
        )

    try:
        test = tuxsuite.Test(
            device=device,
            kernel=kernel,
            modules=modules,
            tests=tests,
            boot_args=boot_args,
            wait_for=wait_for,
        )
    except (AssertionError, tuxsuite.exceptions.TuxSuiteError) as e:
        error(e)

    try:
        test.test()
        info("uid: {}".format(test.uid))
    except tuxsuite.exceptions.BadRequest as e:
        raise (click.ClickException(str(e)))

    test_result = True

    if no_wait:
        format_result(test.status, test.url)
    else:
        test_result = wait_for_object(test)

    if json_out:
        json_out.write(json.dumps(test.status, sort_keys=True, indent=4))

    # If the test did not pass, exit with exit code of 1
    if not test_result:
        sys.exit(1)


@cli.command(help="Run the specified plan file", short_help="Run a plan file.")
@click.option("--name", default=None, help="Set name")
@click.option("--description", default=None, help="Set description")
@click.option("--job-name", default=None, help="Job name")
@click.option("--git-repo", default=None, help="Git repository")
@click.option("--git-ref", default=None, help="Git reference")
@click.option("--git-sha", default=None, help="Git commit")
@click.option(
    "--git-head",
    default=False,
    is_flag=True,
    help="Build the current git HEAD. Overrrides --git-repo and --git-ref",
)
@click.option(
    "-d",
    "--download",
    default=False,
    is_flag=True,
    help="Download artifacts after builds finish",
)
@click.option(
    "-o",
    "--output-dir",
    default=".",
    help="Directory where to download artifacts",
)
@click.option(
    "-s",
    "--show-logs",
    default=False,
    is_flag=True,
    help="Prints build logs to stderr in case of warnings or errors",
)
@click.option(
    "-n",
    "--no-wait",
    default=False,
    is_flag=True,
    help="Don't wait for plan to finish",
)
@click.option(
    "--json-out",
    help="Write json results out to a named file path",
    type=click.File("w", encoding="utf-8"),
)
@click.argument("config")
def plan(
    name,
    description,
    job_name,
    config,
    show_logs=None,
    download=False,
    output_dir=None,
    no_wait=False,
    json_out=None,
    **build_params,
):
    if build_params["git_head"]:
        try:
            repo, sha = tuxsuite.gitutils.get_git_head()
            build_params["git_repo"] = repo
            build_params["git_sha"] = sha
        except Exception as e:
            error(e)
    del build_params["git_head"]

    try:
        plan_config = tuxsuite.config.PlanConfig(name, description, config, job_name)
        if not plan_config.plan:
            warning("Empty plan, skipping")
            return
        plan = tuxsuite.Plan(plan_config, **build_params)
    except (AssertionError, tuxsuite.exceptions.TuxSuiteError) as e:
        error(e)

    info(
        "Running Linux Kernel plan '{}': '{}'".format(
            plan_config.name, plan_config.description
        )
    )

    try:
        plan.submit()
        info("Plan {}/plans/{}\n".format(plan.url, plan.plan))
        info("uid: {}".format(plan.plan))
    except tuxsuite.exceptions.BadRequest as e:
        raise (click.ClickException(str(e)))

    result = True

    if no_wait:
        for build in plan.builds:
            format_result(build.status)
        for test in plan.tests:
            format_result(test.status, plan.url + "/tests/{}".format(test.uid))
    else:
        result = wait_for_object(plan)
        info(f"\nSummary: {plan.url}")
        for build in plan.builds:
            print_state(plan.results["builds"][build.uid], prefix="* ")
            for test in [t for t in plan.tests if t.wait_for == build.uid]:
                print_state(plan.results["tests"][test.uid], prefix="  -> ")
        for test in [t for t in plan.tests if t.wait_for is None]:
            print_state(plan.results["tests"][test.uid], prefix="* ")

    if json_out:
        json_out.write(json.dumps(plan.status, sort_keys=True, indent=4))

    if download:
        for build in plan.builds:
            tuxsuite.download.download(build, output_dir)
    if show_logs:
        for build in plan.builds:
            show_log(build, download, output_dir)

    if not result:
        sys.exit(1)


@cli.command(help="Fetch results", short_help="Fetch results")
@click.option("--build", help="UID of the build to fetch result", default="", type=str)
@click.option("--test", help="UID of the test to fetch result", default="", type=str)
@click.option("--plan", help="UID of the plan to fetch result", default="", type=str)
@click.option(
    "--from-json",
    help="Read status input from named json file path",
    type=click.File("r", encoding="utf-8"),
)
@click.option(
    "--json-out",
    help="Write json results out to a named file path",
    type=click.File("w", encoding="utf-8"),
)
def results(build, test, plan, from_json, json_out):
    result_json = {}
    try:
        results = tuxsuite.Results()
    except (AssertionError, tuxsuite.exceptions.TuxSuiteError) as e:
        error(e)

    try:
        if from_json:
            data = json.loads(from_json.read())
            if "builds" in data and "tests" in data:
                plan = data["builds"][list(data["builds"].keys())[0]]["plan"]
            elif "build_name" in data:
                build = data["uid"]
            elif "tests" in data:
                test = data["uid"]
            elif isinstance(data, list):
                result_json = []
                for res in data:
                    results.uid = res["uid"]
                    build_result = results.get_build()
                    format_result(build_result)
                    if json_out:
                        result_json.append(build_result)
        elif not any([build, test, plan]):  # get all results with no options
            result_json, tuxapi_tests_url = results.get_all()
            for key in result_json.keys():
                info(f"{key.capitalize()}:")
                for result in result_json[key].get("results", None):
                    if key == "plans":
                        info(f"{result['uid']}: {result['name']} {result['project']}")
                    else:
                        format_result(result, tuxapi_tests_url)
                info("\n")
        if build:
            results.uid = build
            result_json = results.get_build()
            format_result(result_json)
        if test:
            results.uid = test
            result_json, tuxapi_tests_url = results.get_test()
            format_result(result_json, tuxapi_tests_url)
        if plan:
            results.uid = plan
            result_json, tuxapi_tests_url = results.get_plan()
            for result in result_json["builds"].keys():
                format_result(result_json["builds"][result])
            for result in result_json["tests"].keys():
                format_result(
                    result_json["tests"][result],
                    tuxapi_tests_url + "/{}".format(result),
                )
    except tuxsuite.exceptions.URLNotFound as e:
        raise (click.ClickException(str(e)))

    if json_out:
        json_out.write(json.dumps(result_json, sort_keys=True, indent=4))


def main():
    cli.main(prog_name="tuxsuite")
