from collections import defaultdict
from glob import glob
import json
import os


def get_licenses(envdir, return_permissive=False):
    filedir = os.path.dirname(__file__)

    with open(os.path.join(filedir, "permissive.txt"), "r") as f:
        permissive = [line.strip() for line in f]
    ignore = [ii.lower() for ii in permissive]

    jsonfiles = glob(os.path.join(envdir, "conda-meta", "*.json"))

    licenses = defaultdict(list)
    for ff in jsonfiles:
        with open(ff, "r") as f:
            packageinfo = json.load(f)
            if "license" in packageinfo:
                licenses[packageinfo["license"]].append(packageinfo["name"])
            else:
                licenses["Unknown"].append(packageinfo["name"])

    if not return_permissive:
        for key in list(licenses.keys()):
            if key.lower() in ignore:
                del licenses[key]

    return dict(licenses)

def main(argv=None):
    import argparse
    
    parser = argparse.ArgumentParser("EnvLicenses")
    parser.add_argument("dir", type=str, help="Directory of a conda environment")
    parser.add_argument("--return-permissive", help="Return also permissive licenses")
    args = parser.parse_args(argv)
    licenses = get_licenses(args.dir, args.return_permissive)
    for key, val in licenses.items():
        print(key)
        print(f"    {val}")

if __name__ == "__main__":
    import sys
    arguments = sys.argv[1:] if len(sys.argv) > 1 else ["-h"]
    main(arguments)