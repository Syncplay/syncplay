import glob
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

def arch_checker(path: str) -> bool:
    no_error_found = True
    for bin_to_check in glob.glob(path, recursive=True):
        file_output = run_external_command(["file", bin_to_check], print_output=False)
        if not ("x86_64" in file_output and "arm64" in file_output):
            print(f"Non-universal2 binary found! - {bin_to_check}")
            no_error_found = False
    return no_error_found

def analyze(bundle_path: str) -> None:
    valid = all([arch_checker(f"{bundle_path}/Contents/Frameworks/**/*.dylib"),
                 arch_checker(f"{bundle_path}/Contents/Frameworks/**/*.so"),
                 arch_checker(f"{bundle_path}/Contents/Resources/lib/**/*.dylib"),
                 arch_checker(f"{bundle_path}/Contents/Resources/lib/**/*.so"),
                ])
    if valid:
        print(f"The analyzed bundle '{bundle_path}' is universal2.")
    else:
        raise RuntimeError("The analyzed bundle is NOT universal2!")

def main():
    analyze("Syncplay.app")

if __name__ == "__main__":
    main()
