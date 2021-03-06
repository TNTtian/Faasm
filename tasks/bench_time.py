from decimal import Decimal
from os import makedirs
from os.path import join, exists
from subprocess import call
from tempfile import NamedTemporaryFile

from invoke import task

from tasks.util.env import PROJ_ROOT, BENCHMARK_BUILD, RESULT_DIR, set_benchmark_env

TIME_BINARY = "/usr/bin/time"
OUTPUT_FILE = join(RESULT_DIR, "runtime-bench-time.csv")


@task
def bench_time(ctx):
    if not exists(RESULT_DIR):
        makedirs(RESULT_DIR)

    benches = [
        ("faasm", join(BENCHMARK_BUILD, "bin", "bench_time"), 10000),
        ("docker", "./bin/docker_noop_time.sh", 10),
        ("thread", join(BENCHMARK_BUILD, "bin", "thread_bench_time"), 10000),
    ]

    csv_out = open(OUTPUT_FILE, "w")
    csv_out.write(
        "Runtime,Measure,Value,Iterations,ValuePerIteration\n")

    for bench_name, cmd, iterations in benches:
        _do_cpu_cycles(bench_name, cmd, iterations, csv_out)
        _do_time(bench_name, cmd, iterations, csv_out)


def _exec_cmd(cmd_str):
    print(cmd_str)
    set_benchmark_env()
    ret_code = call(cmd_str, shell=True, cwd=PROJ_ROOT)

    if ret_code != 0:
        raise RuntimeError("Command failed: {}".format(ret_code))


def _do_cpu_cycles(runtime_name, cmd, iterations, csv_out):
    # Build the command with output to temp file
    out_file = NamedTemporaryFile()
    cmd = [
        "perf", "stat", "-x, -e cycles,instructions -a",
        "-o", out_file.name,
        cmd,
        str(iterations),
    ]

    cmd_str = " ".join(cmd)
    _exec_cmd(cmd_str)

    # Parse output from perf file
    with open(out_file.name, "r") as fh:
        for perf_line in fh:
            perf_line = perf_line.strip()
            if not perf_line or perf_line.startswith("#"):
                continue

            parts = perf_line.split(",")
            metric = parts[2]
            value = parts[0]

            if metric == "cycles":
                # Amortize over iterations
                value = Decimal(value) / iterations
                csv_out.write("{},{},{},{},{}\n".format(
                    runtime_name,
                    "cpu_cycles",
                    value,
                    iterations,
                    Decimal(value) / iterations,
                ))

    csv_out.flush()


def _do_time(runtime_name, cmd, iterations, csv_out):
    # Build the command with output to temp file
    out_file = NamedTemporaryFile()
    cmd = [
        TIME_BINARY,
        "-v",
        "-o", out_file.name,
        cmd,
        str(iterations),
    ]

    cmd_str = " ".join(cmd)
    _exec_cmd(cmd_str)

    # Parse time stats as dictionary (looking for elapsed wall time)
    time_stats = dict()
    with open(out_file.name, "r") as fh:
        for time_line in fh:
            if not time_line:
                continue

            time_line = time_line.strip()

            # Wall clock time is messed up as it has colons in the string as well as for the separator
            # Assume format of mm:ss.ss
            if time_line.startswith("Elapsed (wall"):
                # Extract the label
                label = ":".join(time_line.split(":")[:-2])

                # Parse into seconds
                minute_str, seconds_str = time_line.split(":")[-2:]
                value = (Decimal(minute_str) * 60) + Decimal(seconds_str)
            else:
                label, value = time_line.split(":")
                value = value.strip()

            time_stats[label.strip()] = value

    # Check return code
    if time_stats["Exit status"] != "0":
        raise RuntimeError("Time command failed. Time stats: {}".format(time_stats))

    # Map time labels to output labels
    label = "Elapsed (wall clock) time (h:mm:ss or m:ss)"
    value = time_stats[label]
    csv_out.write("{},{},{},{},{}\n".format(
        runtime_name,
        "elapsed_seconds",
        value,
        iterations,
        Decimal(value) / iterations,
    ))

    csv_out.flush()
