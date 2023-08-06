#!/usr/bin/env python
#   -*- coding: utf-8 -*-

from setuptools import setup
from setuptools.command.install import install as _install

class install(_install):
    def pre_install_script(self):
        pass

    def post_install_script(self):
        pass

    def run(self):
        self.pre_install_script()

        _install.run(self)

        self.post_install_script()

if __name__ == '__main__':
    setup(
        name = 'text-animator',
        version = '0.1.0',
        description = 'A simple text animator',
        long_description = '[![complexity](https://img.shields.io/badge/complexity-A-brightgreen)](https://radon.readthedocs.io/en/latest/api.html#module-radon.complexity)\n[![vulnerabilities](https://img.shields.io/badge/vulnerabilities-None-brightgreen)](https://pypi.org/project/bandit/)\n[![PyPI version](https://badge.fury.io/py/text-animator.svg)](https://badge.fury.io/py/text-animator)\n[![python](https://img.shields.io/badge/python-3.7%20%7C%203.8%20%7C%203.9%20%7C%203.10-teal)](https://www.python.org/downloads/)\n# text-animator\n\nA simple text animator.\n\nThs is a subclass of the `Animation` abstract class and uses the `Animator` class to display the animated text to the terminal; both classes are defined in the [ascii-animator](https://pypi.org/project/ascii-animator/0.1.6/) package. \n\n\n### Installation\n```bash\npip install text_animator\n```\n\n### Usage\n\n#### [example1](https://github.com/soda480/text-animator/blob/main/examples/example1.py)\n\nAnimate some text and display characters from left to right (default).\n\n<details><summary>Code</summary>\n\n```Python\nfrom text_animator import TextAnimation\ntext = """This is the text\n    that we want to animate\n    let\'s see how well\n    this works ..."""\nTextAnimation(text)()\n```\n\n</details>\n\n![example1](https://github.com/soda480/text-animator/blob/main/docs/images/example1.gif?raw=true)\n\n#### [example2](https://github.com/soda480/text-animator/blob/main/examples/example2.py)\n\nAnimate some text and display characters from right to left.\n\n<details><summary>Code</summary>\n\n```Python\nfrom text_animator import TextAnimation, Effect\ntext = """This is the text\n    that we want to animate\n    let\'s see how well\n    this works ..."""\nTextAnimation(text, effect=Effect.RIGHT_TO_LEFT)()\n```\n\n</details>\n\n![example2](https://github.com/soda480/text-animator/blob/main/docs/images/example2.gif?raw=true)\n\n#### [example3](https://github.com/soda480/text-animator/blob/main/examples/example3.py)\n\nAnimate some text and display characters at random.\n\n<details><summary>Code</summary>\n\n```Python\nfrom text_animator import TextAnimation, Effect\ntext = """This is the text\n    that we want to animate\n    let\'s see how well\n    this works ..."""\nTextAnimation(text, effect=Effect.RANDOM)()\n```\n\n</details>\n\n![example3](https://github.com/soda480/text-animator/blob/main/docs/images/example3.gif?raw=true)\n\n#### [example4](https://github.com/soda480/text-animator/blob/main/examples/example4.py)\n\nAnimate some text and display characters from left to right then surround text with a border. A border can be customized with top|bottom|left|right margins as well as top|bottom|left|right padding, default for all margins and padding is 1.  Margins define the space outside the border, and padding define the space between the border and text.\n\n<details><summary>Code</summary>\n\n```Python\nfrom text_animator import TextAnimation, Effect, Border\ntext = """This is the text\n    that we want to animate\n    let\'s see how well\n    this works ..."""\nTextAnimation(text, border=Border(lm=0, tm=0, bm=0, tp=0, bp=0))()\n```\n\n</details>\n\n![example4](https://github.com/soda480/text-animator/blob/main/docs/images/example4.gif?raw=true)\n\n### Development\n\nClone the repository and ensure the latest version of Docker is installed on your development server.\n\nBuild the Docker image:\n```bash\ndocker image build \\\n-t \\\ntext-animator:latest .\n```\n\nRun the Docker container:\n```bash\ndocker container run \\\n--rm \\\n-it \\\n-v $PWD:/code \\\ntext-animator:latest \\\nbash\n```\n\nExecute the build:\n```sh\npyb -X\n```\n',
        long_description_content_type = 'text/markdown',
        classifiers = [
            'Programming Language :: Python',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
            'Programming Language :: Python :: 3.9',
            'Programming Language :: Python :: 3.10'
        ],
        keywords = '',

        author = 'Emilio Reyes',
        author_email = 'soda480@gmail.com',
        maintainer = '',
        maintainer_email = '',

        license = 'Apache License, Version 2.0',

        url = 'https://github.com/soda480/text-animator',
        project_urls = {},

        scripts = [],
        packages = ['text_animator'],
        namespace_packages = [],
        py_modules = [],
        entry_points = {},
        data_files = [],
        package_data = {},
        install_requires = ['ascii_animator'],
        dependency_links = [],
        zip_safe = True,
        cmdclass = {'install': install},
        python_requires = '',
        obsoletes = [],
    )
