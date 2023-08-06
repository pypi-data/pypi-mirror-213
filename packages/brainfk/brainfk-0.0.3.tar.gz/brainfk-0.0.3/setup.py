from setuptools import setup

VERSION = "0.0.3"
DESCRIPTION = "A Brainfuck interpreter package"
with open("README.md", "r") as fh:
    LONG_DESCRIPTION = fh.read()

setup(
    name="brainfk",
    version=VERSION,
    author="Estifanose Sahilu",
    packages=["brainfk"],
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/plain",
    install_requires=["argparse"],
    author_email="<estifanoswork@gmail.com>",
    entry_points={"console_scripts": ["brainfk = brainfk.interpreter:main"]},
    url="https://github.com/estif0/brainfk",
    keywords=["python", "package", "cli", "interpreter", "brainfuck"],
)
