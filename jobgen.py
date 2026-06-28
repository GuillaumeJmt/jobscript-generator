#!/usr/bin/env python3
"""
jobgen.py - Slurm jobscript generator for scientific HPC workflows.

Usage:
    python3 jobgen.py --soft nwchem --input mol.nw --mem 32G --time 24h --cpus 8
    python3 jobgen.py --soft gaussian --input mol.gjf --mem 64G --time 48h --cpus 16
    python3 jobgen.py --soft python_ml --input train.py --mem 16G --time 12h --cpus 4
"""

import argparse
import sys
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

DEFAULTS = {
    "nwchem":     {"version": "7.3.0", "partition": "batch", "cpus": "8",  "mem": "32G", "time": "24:00:00"},
    "gaussian":   {"version": "16-C.02", "partition": "batch", "cpus": "16", "mem": "64G", "time": "48:00:00"},
    "python_ml":  {"version": "3.11",  "partition": "batch", "cpus": "4",  "mem": "16G", "time": "12:00:00"},
}

def parse_time(time_str):
    """Convert 24h or 24:00:00 to Slurm format HH:MM:SS."""
    if ":" in time_str:
        return time_str
    if time_str.endswith("h"):
        hours = int(time_str[:-1])
        return f"{hours:02d}:00:00"
    if time_str.endswith("m"):
        mins = int(time_str[:-1])
        return f"00:{mins:02d}:00"
    return time_str

def main():
    parser = argparse.ArgumentParser(
        description="Generate Slurm jobscripts for scientific HPC workflows"
    )
    parser.add_argument("--soft",      required=True, choices=list(DEFAULTS.keys()),
                        help="Software to run")
    parser.add_argument("--input",     required=True, help="Input file")
    parser.add_argument("--output",    help="Output file (default: input.log)")
    parser.add_argument("--mem",       help="Memory (e.g. 32G)")
    parser.add_argument("--time",      help="Walltime (e.g. 24h or 24:00:00)")
    parser.add_argument("--cpus",      help="CPUs per task")
    parser.add_argument("--partition", help="Slurm partition")
    parser.add_argument("--version",   help="Software version")
    parser.add_argument("--out",       help="Output jobscript filename")

    args = parser.parse_args()

    defaults = DEFAULTS[args.soft]

    input_path = Path(args.input)
    output_file = args.output or input_path.stem + ".log"
    job_name = input_path.stem

    context = {
        "job_name":   job_name,
        "input_file": args.input,
        "output_file": output_file,
        "cpus":       args.cpus      or defaults["cpus"],
        "mem":        args.mem       or defaults["mem"],
        "time":       parse_time(args.time or defaults["time"]),
        "partition":  args.partition or defaults["partition"],
        "version":    args.version   or defaults["version"],
    }

    templates_dir = Path(__file__).parent / "templates"
    env = Environment(loader=FileSystemLoader(str(templates_dir)))
    template = env.get_template(f"{args.soft}.sh.j2")
    jobscript = template.render(**context)

    outfile = args.out or f"{job_name}_{args.soft}.sh"
    with open(outfile, "w") as f:
        f.write(jobscript)

    print(f"Generated: {outfile}")
    print(f"  Software:  {args.soft} {context['version']}")
    print(f"  CPUs:      {context['cpus']}")
    print(f"  Memory:    {context['mem']}")
    print(f"  Walltime:  {context['time']}")
    print(f"  Partition: {context['partition']}")
    print(f"Submit with: sbatch {outfile}")

if __name__ == "__main__":
    main()
