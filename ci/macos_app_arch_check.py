import os
import subprocess

from typing import List

def run_external_command(command: List[str], print_output: bool = True) -> str:
    """Wrapper to ease the use of calling external programs"""
    process = subprocess.Popen(command, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output, _ = process.communicate()
    ret = process.wait()
    if (output and print_output) or ret != 0:
        print(output)
    if ret != 0:
        raise RuntimeError("Command returned non-zero exit code %s!" % ret)
    return output

def analyze(bundle_path: str) -> None:
    if not os.path.isdir(bundle_path):
        raise RuntimeError("The application bundle was not found: {}".format(bundle_path))

    binaries = []
    for root, directories, filenames in os.walk(bundle_path):
        for filename in filenames:
            path = os.path.join(root, filename)
            file_output = run_external_command(["file", path], print_output=False)
            if "Mach-O" not in file_output:
                continue
            architectures = run_external_command(["lipo", "-archs", path], print_output=False).split()
            if not {"x86_64", "arm64"}.issubset(architectures):
                raise RuntimeError("Non-universal2 binary found: {}".format(path))
            binaries.append(path)

    if not binaries:
        raise RuntimeError("No Mach-O binaries found in the application bundle: {}".format(bundle_path))
    print("Verified {} universal2 binaries in '{}'.".format(len(binaries), bundle_path))

def main():
    analyze("dist/Syncplay.app")

if __name__ == "__main__":
    main()
