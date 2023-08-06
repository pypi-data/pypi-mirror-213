# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['lentille', 'lentille.embedders.vision', 'lentille.utils']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.24.3,<2.0.0', 'onnxruntime>=1.14.1,<2.0.0', 'pillow>=9.5.0,<10.0.0']

setup_kwargs = {
    'name': 'lentille',
    'version': '0.2.0',
    'description': '',
    'long_description': '# Lentille\nLibrary that wraps various embedders. For now it only wraps a Resnet50 model.\n\n## Installation\n``` bash\npip install lentille\n```\n\n## Example usage\n``` python\nfrom lentille import Resnet50Embedder\n\nembedder = Resnet50Embedder.from_file(\n    "resnet50-v1-12-int8.onnx" # ONNX model from: https://github.com/onnx/models/tree/main/vision/classification/resnet\n)\n\nprint(embedder.classify("cat.jpg"))\n```\n',
    'author': 'Alex',
    'author_email': '46456279+the-alex-b@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
