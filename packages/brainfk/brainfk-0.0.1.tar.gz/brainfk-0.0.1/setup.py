from setuptools import setup

VERSION = "0.0.1"
DESCRIPTION = "A Brainfuck interpreter package"
URL="https://github.com/estif0/brainfk"

setup(
    name="brainfk",
    version=VERSION,
    author="Estifanose Sahilu",
    packages=["brainfk"],
    description=DESCRIPTION,
    install_requires=["argparse"],
    author_email="<estifanoswork@gmail.com>",
    entry_points={"console_scripts": ["brainfk = brainfk.interpreter:main"]},
    url=URL,
    keywords=["python", "package", "cli", "interpreter", "brain fuck"],
)
