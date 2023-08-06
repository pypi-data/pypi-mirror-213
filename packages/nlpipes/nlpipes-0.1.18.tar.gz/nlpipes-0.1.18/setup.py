# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nlpipes',
 'nlpipes.callbacks',
 'nlpipes.configurations',
 'nlpipes.data',
 'nlpipes.layers',
 'nlpipes.losses',
 'nlpipes.metrics',
 'nlpipes.models',
 'nlpipes.optimization',
 'nlpipes.pipelines',
 'nlpipes.trainers']

package_data = \
{'': ['*']}

install_requires = \
['ftfy>=6.1.1,<7.0.0',
 'numpy>=1.21.0,<2.0.0',
 'pandas>=1.3.5,<2.0.0',
 'scipy>=1.7.3,<2.0.0',
 'tensorflow>=2.11.0,<3.0.0',
 'tokenizers>=0.13.0,<0.14.0',
 'tqdm>=4.64.0,<5.0.0',
 'transformers>=4.24.0,<5.0.0']

setup_kwargs = {
    'name': 'nlpipes',
    'version': '0.1.18',
    'description': 'Text Classification with Transformers',
    'long_description': '<!-- PROJECT NAME -->\n<div align="center">\n   <img src="https://ik.imagekit.io/m0ci8dgk4/nlpipes_logo_eSBhzDKCZ.png?updatedAt=1679840445991" alt="nlpipes_logo" title="nlpipes logo">\n  <h2>Text Classification with Transformers</h2>\n</div>\n\n<div align="center">\n    <a href="https://opensource.org/licenses/Apache-2.0">\n       <img alt="Licence" src="https://img.shields.io/badge/License-Apache_2.0-blue.svg">\n    </a>\n     <a href="https://pypi.org/project/nlpipes/">\n       <img alt="PyPi Version" src="https://img.shields.io/pypi/pyversions/nlpipes">\n    </a> \n    <a href="https://pypi.org/project/nlpipes/">\n        <img alt="PyPi Package Version" src="https://img.shields.io/pypi/v/nlpipes">\n    </a>\n    <!--\n    <a href="https://pepy.tech/project/nlpipes/">\n        <img alt="PyPi Downloads" src="https://static.pepy.tech/badge/nlpipes/month">\n    </a>\n    -->\n</div>\n\n<div align="center">\n    <a href=""><strong>Documentation</strong></a>\n    • <a href=""><strong>References</strong></a>\n</div>\n\n\n<div align="center">\n  <img src="https://ik.imagekit.io/m0ci8dgk4/nlpipes_screenshot_q_FDeS4Js.png?updatedAt=1686231419316"\n       alt="nlpipes_screenshot" \n       title="nlpipes screenshot"\n       width="75%"\n       height="75%"\n  >\n</div>\n\n\n## Overview\n\n`NLPipes` is for people unfamiliar with Transformers who want an end to end solution to solve practical text classification problems, including:\n\n* **Single-label classification**: A typical use case is sentiment detection where one want to detect the overall sentiment polarity (e.g., positive, neutral, negative) in a review.\n* **Multi-label classification**: A typical use case is aspect categories detection where one want to detect the multiple aspects mentionned in a review (e.g., product_quality, delivery_time, price, ...).\n* **Aspect-based classification**: A typical use case is aspect based sentiment analysis where one want to detect sentiment polarity associated to each aspect categories mentionned in a review (e.g., product_quality: neutral, delivery_time: negative, price: positive, ...).\n\n`NLPipes` expose a `Model` API that provide a unique and simple abstraction for all the tasks. \nThe library maintain a common usage pattern across models (train, evaluate, predict, save) with\nalso a clear and consistent data structure (python lists as inputs/outputs data).\n\n#### Built with\n`NLPipes` is built with TensorFlow and HuggingFace Transformers:\n* [TensorFlow](https://www.tensorflow.org/): An end-to-end open source deep learning framework\n* [Transformers](https://huggingface.co/transformers/): An general-purpose open-sources library for transformers-based architectures\n\n## Getting Started\n\n#### Installation\n1. Create a virtual environment\n\n ```console\n python3 -m venv nlpipesenv\n source nlpipesenv/bin/activate\n ```\n\n2. Install the package\n\n ```console\n pip install nlpipes\n ```\n \n \n#### Tasks\n\nA model can be trained for a specific task by first loading a backbone model. The train command takes\nat minimum two parameters (X and Y), where X is a list of texts to train on and Y is the \ntraining target.\n\nThe training target expect different formats, depending on what task you want to solve:\n\n\n##### Single Label Classification:\nGive one label name for each sequence of text in `X`:\n\n ```console\n  model = Model("albert-base-v2",\n                task=\'single-label-classification\',\n                all_labels=["NEG", "NEU", "POS"],\n               )\n  \n  X = ["This was bad.", "This was great!"]\n  Y = ["NEG", "POS"]\n  \n  model.train(X, Y)\n ```\n\n##### Multiple Label Classification:\nGive a list of class names for each sequence of text in `X`:\n\n ```console\n  model = Model("albert-base-v2",\n                task=\'multi-label-classification\',\n                all_labels=all_labels,\n                )\n  \n  X = ["I want a refund!",\n       "The bill I got is not correct and I also have technical issues",\n       "All good"]\n  Y = [\n       ["billing"], \n       ["billing", "tech support"],\n       []\n      ]\n      \n  model.train(X, Y)\n ```\n \n ##### Aspect Based Classification:\nGive a list of lists of label lists (pairs) for each given text in `X`:\n\n ```console\n  model = Model("albert-base-v2",\n                task=\'class-label-classification\',\n                all_labels=["NEG", "NEU", "POS"],\n               )\n  \n  X = ["The room was nice.",\n       "The food was great, but the staff was unfriendly.",\n       "The room was horrible, but the waiters were welcoming"]\n  Y = [\n       [["room", "POS"],\n       [["food", "POS"], ["staff", "NEG"]],\n       [["room", "NEG"], ["staff", "POS"]],\n      ]\n      \n  model.train(X, Y)\n ```\n\n\n#### Examples\n\nHere are some examples on open datasets that show how to use `NLPipes` on different tasks:\n\nName|Notebook|Description|Task|Size|Memory|Speed| \n----|-----------|-----|---------|---------|---------|---------|\nGooglePlay Sentiment Detection|Available|Train a model to detect the sentiment polarity from the GooglePlay store |Single label classification|  |  |  \nStackOverflow tags Detection|Available|Train a model to detect tags from the StackOverFlow questions |Multiple label classification|  |  |\nAmazon Aspect Based Sentiment Detection|Available|Train a model to detect the aspect based sentiment polarity on Laptops Amazon reviews |Class label classification|  |  | \n\n\n## Notices\n- `NLPipes` is still in its early stage. The library comes with no warranty and future releases could bring substantial API and behavior changes.\n\n',
    'author': 'Ayhan UYANIK',
    'author_email': 'ayhan.uyanik@renault.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
