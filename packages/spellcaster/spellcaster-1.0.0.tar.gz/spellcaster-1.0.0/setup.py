from setuptools import setup
from pathlib import Path

dir = Path(__file__).parent
long_description = (dir / "README.md").read_text()

setup(
  name = "spellcaster",
  version = "1.0.0",
  description = "Take control of Python with ease with the legendary Spellcaster!",
  long_description = long_description,
  long_description_content_type = "text/markdown",
  author = "Omer Drkić",
  author_email = "omerdrkic2501@gmail.com",
  maintainer = "Byte Wraith Technologies",
  url = "https://bytewizarddocs.github.io/spellcaster",
  py_modules = [
    "spellcaster"
  ],
  classifiers = [
    "Development Status :: 5 - Production/Stable",
    "Environment :: Console",
    "Framework :: Jupyter",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: Boost Software License 1.0 (BSL-1.0)",
    "Natural Language :: English",
    "Operating System :: Microsoft",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Topic :: Software Development :: Interpreters",
    "Topic :: Software Development :: Libraries",
    "Typing :: Typed"
  ],
  license = "Boost Software License 1.0",
  install_requires = [
    "keyboard"
  ],
  python_requires = ">=3.11"
)