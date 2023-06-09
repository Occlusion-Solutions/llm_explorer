import re
import sys
import glob
from setuptools import find_packages, setup

if sys.version_info < (3, 6):
    print("Error: llm_explorer does not support this version of Python.")
    print("Please upgrade to Python 3.6 or higher.")
    sys.exit(1)

try:
    from setuptools import find_namespace_packages

    find_namespace_packages()
except ImportError:
    # the user has a downlevel version of setuptools.
    print("Error: llm_explorer requires setuptools v40.1.0 or higher.")
    print(
        'Please upgrade setuptools with "pip install --upgrade setuptools" '
        "and try again"
    )
    sys.exit(1)

version = "#{PKG_VAR_SETUP}#"
package_name = "llm_explorer"

package_env = re.sub(r"[^a-zA-Z]", "", version)

if "PKGVARSETUP" in package_env:
    version = "0.0.9"

package_env = re.sub(r"[^a-zA-Z]", "", version)

# Check if any letters were found
if len(package_env) > 0:
    package_name += f"_{package_env}"


with open("requirements.txt") as f:
    required = f.read().splitlines()


def prepare_data_files(directory, extensions):
    files = []
    for ext in extensions:
        files.extend(glob.glob(f'{directory}/*.{ext}'))
    return files


data_files_structure = [
    ('llm_explorer', prepare_data_files('llm_explorer', ['csv', 'sql', 'txt', 'md', 'html', 'css', 'json', 'yaml', 'faiss', 'pkl'])),
]

print(package_name, version)
setup(
    name=package_name,
    version=version,
    author="Carlos D. Escobar-Valbuena",
    author_email="carlosdavidescobar@gmail.com",
    description="A Lakehouse LLM Explorer. Wrapper for spark, databricks and langchain processes",
    long_description=open("README.md", "r").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    include_package_data=True,
    setup_requires=["setuptools", "wheel"],
    tests_require=["pytest"],
    python_requires=">=3.10",
    nstall_requires=required,
    test_suite="tests",
    zip_safe=False,
    url="https://github.com/Occlusion-Solutions/llm_explorer.git",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.10",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    install_requires=required,
    package_data={
        "llm_explorer": ["*.json", "*.yaml", "*.sql", "*.csv", "*.txt", "*.md", "*.html", "*.css", "*.pkl", "*.faiss"],
    },
    data_files=data_files_structure,
    py_modules=['main'],
    entry_points={
        "console_scripts": [
            "llm_explorer=main:main",
        ],
    },
)
