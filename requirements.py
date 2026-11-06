try:
    import toml
except ImportError:
    raise SystemExit("Please install toml module to run this script.")

def generate_requirements():
    # Load pyproject.toml
    with open("pyproject.toml", "r") as f:
        pyproject = toml.load(f)

    # Extract dependencies
    project = pyproject.get("project", {})
    dependencies = project.get("dependencies", [])
    optional_dependencies = project.get("optional-dependencies", {}).get("gui", [])

    # Write requirements.txt
    with open("requirements.txt", "w") as req_file:
        for dep in dependencies:
            req_file.write("{}\n".format(dep))

    # Write requirements-gui.txt
    with open("requirements-gui.txt", "w") as gui_req_file:
        for dep in dependencies:
            gui_req_file.write("{}\n".format(dep))
        for dep in optional_dependencies:
            gui_req_file.write("{}\n".format(dep))

    print("Generated requirements.txt and requirements-gui.txt")

if __name__ == "__main__":
    generate_requirements()