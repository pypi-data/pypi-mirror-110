import setuptools, glob, os, sys

with open("README.md", "r") as fh:
    readme = fh.read()

version = "0.0.2"
author = "Carlos Osuna"
author_email = "charlie@caosuna.com"
ldct = "text/markdown"
url = "https://gitlab.com/caosuna/ctpros"
dependencies = [
    "itk==4.13.2.post1",
    "lazy-import==0.2.2",
    "mayavi==4.6.2",
    "numpy==1.16.5",
    "pandas==0.25.0",
    "scipy==1.6.0",
    "scikit-image==0.17.2",
    "tqdm==4.48.2",
    "vtk==8.1.2",
]

setuptools.setup(
    name="ctpros",
    version=version,
    author=author,
    author_email=author_email,
    description="Computed Tomography Processing Registration Open Sourced",
    long_description=readme,
    long_description_content_type=ldct,
    url=url,
    packages=setuptools.find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=dependencies,
    python_requires=">=3.7",
    scripts=glob.glob("bin/*"),
)


def write_batch_to_desktop():
    batdir = os.path.join(os.environ["USERPROFILE"], "Desktop", "ctpros.bat")
    python_path = os.path.join(sys.executable, "..")
    activate_path = os.path.join(python_path, "activate")
    log_path = os.path.join(python_path, "ctpros_log.txt")
    # battext = f'@echo off\n{activate_path}\nstart pythonw.exe -m ctpros > logging.txt"'
    battext = f'"{activate_path}" && start pythonw.exe -m ctpros > nul'
    print(f"Generated {batdir}")
    with open(batdir, "w") as bat:
        bat.write(battext)


if "win" in sys.platform:
    write_batch_to_desktop()
