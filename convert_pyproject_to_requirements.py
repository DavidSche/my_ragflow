#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import toml
from pathlib import Path


def convert_pyproject_to_requirements(pyproject_path: str, requirements_path: str):
    """
    Convert dependencies in pyproject.toml to a requirements.txt file.

    Args:
        pyproject_path (str): Path to the pyproject.toml file.
        requirements_path (str): Path to save the requirements.txt file.
    """
    pyproject_file = Path(pyproject_path)
    requirements_file = Path(requirements_path)

    if not pyproject_file.exists():
        raise FileNotFoundError(f"The file {pyproject_path} does not exist.")

    # Load the pyproject.toml file
    pyproject_data = toml.load(pyproject_file)

    # Extract dependencies
    try:
        dependencies = pyproject_data["tool"]["poetry"]["dependencies"]
    except KeyError:
        raise ValueError("Dependencies not found in pyproject.toml under [tool.poetry.dependencies]")

    # Exclude the Python version
    requirements = []
    for package, version in dependencies.items():
        if package.lower() == "python":
            continue
        if isinstance(version, dict):
            # Handle optional dependencies with extras
            extras = version.get("extras", [])
            version_str = version.get("version", "")
            extra_str = f"[{','.join(extras)}]" if extras else ""
            requirements.append(f"{package}{extra_str}{version_str}")
        else:
            requirements.append(f"{package}=={version}" if version else package)

    # Write to requirements.txt
    with requirements_file.open("w") as f:
        f.write("\n".join(requirements))

    print(f"Requirements written to {requirements_path}")


# Example usage
if __name__ == "__main__":
    pyproject_path = "pyproject.toml"
    requirements_path = "requirements.txt"
    convert_pyproject_to_requirements(pyproject_path, requirements_path)
