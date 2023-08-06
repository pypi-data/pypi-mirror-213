# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['text_emotion']

package_data = \
{'': ['*']}

install_requires = \
['torch>=2.0.1,<3.0.0', 'transformers>=4.30.1,<5.0.0']

extras_require = \
{'translate': ['requests>=2.31.0,<3.0.0',
               'easynmt>=2.0.2,<3.0.0',
               'fasttext>=0.9.2,<0.10.0']}

setup_kwargs = {
    'name': 'text-emotion',
    'version': '0.0.3',
    'description': 'Multilingual Emotion Classification',
    'long_description': '# Text Emotion\n\n# Introduction\n\n### Supported Languages\n\nThe following languages are supported by the finetuned\nxlm-roberta model:\n\n- English\n- French\n- Spanish\n- German\n- Italian\n\nAll other languages are translated to English\nusing the EasyNMT library. If the language is not\nsupported by EasyNMT, then it is not supported.\n\n# Installation\n\nYou can install emotion using:\n\n    $ pip install text-emotion\n\n# Usage\n\n```python\nfrom text_emotion import Detector\n\ndetector = Detector(emotion_language="fr")\n\nprint(detector.detect("Hello, I am so happy!"))\n```\n\n### XLM-Roberta\n\nThe underlying model is xlm-roberta-large. You can test it at:\n\nhttps://huggingface.co/ma2za/xlm-roberta-emotion\n\n### References\n\n[Unsupervised Cross-lingual Representation Learning at Scale](https://aclanthology.org/2020.acl-main.747) (Conneau et\nal., ACL 2020)',
    'author': 'ma2za',
    'author_email': 'mazzapaolo2019@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/ma2za/text-emotion',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
