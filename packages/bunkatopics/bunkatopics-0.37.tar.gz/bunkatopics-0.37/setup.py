# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bunkatopics',
 'bunkatopics.bunka_logger',
 'bunkatopics.functions',
 'bunkatopics.visualisation']

package_data = \
{'': ['*']}

install_requires = \
['black>=23.3.0,<24.0.0',
 'gensim>=4.3.1,<5.0.0',
 'hdbscan>=0.8.29,<0.9.0',
 'instructorembedding>=1.0.1,<2.0.0',
 'ipywidgets>=8.0.6,<9.0.0',
 'jupyterlab>=4.0.1,<5.0.0',
 'kneed>=0.8.3,<0.9.0',
 'langchain>=0.0.188,<0.0.189',
 'loguru>=0.7.0,<0.8.0',
 'matplotlib>=3.7.1,<4.0.0',
 'numba>=0.57.0,<0.58.0',
 'pandas>=2.0.2,<3.0.0',
 'plotly>=5.14.1,<6.0.0',
 'pytest>=7.3.2,<8.0.0',
 'sentence-transformers>=2.2.2,<3.0.0',
 'statsmodels>=0.14.0,<0.15.0',
 'textacy>=0.13.0,<0.14.0',
 'umap-learn>=0.5.3,<0.6.0']

setup_kwargs = {
    'name': 'bunkatopics',
    'version': '0.37',
    'description': 'Topic Modeling using Transformers and advanced visualization',
    'long_description': '[![PyPI - Python](https://img.shields.io/badge/python-v3.9+-blue.svg)](https://pypi.org/project/bertopic/)\n[![PyPI - PyPi](https://img.shields.io/pypi/v/bunkatopics)](https://pypi.org/project/bunkatopics/)\n\n# Bunkatopics\n\n<img src="images/logo.png" width="35%" height="35%" align="right" />\n\nBunkatopics is a Topic Modeling Visualisation Method that leverages Transformers from HuggingFace through langchain. It is built with the same philosophy as [BERTopic](https://github.com/MaartenGr/BERTopic) but goes deeper in the visualization to help users grasp quickly and intuitively the content of thousands of text.\nIt also allows for a supervised visual representation by letting the user create continnums with natural language.\n\n## Installation\n\nFirst, create a new virtual environment using pyenv\n\n```bash\npyenv virtualenv 3.9 bunkatopics_env\n```\n\nActivate the environment\n\n```bash\npyenv activate bunkatopics_env\n```\n\nThen Install the Bunkatopics package:\n\n```bash\npip install bunkatopics\n```\n\nInstall the spacy tokenizer model for english:\n\n```bash\npython -m spacy download en_core_web_sm\n```\n\n## Contributing\n\nAny contribution is more than welcome\n\n```bash\npip install poetry\ngit clone https://github.com/charlesdedampierre/BunkaTopics.git\ncd BunkaTopics\n\n# Create the environment from the .lock file. \npoetry install # This will install all packages in the .lock file inside a virtual environmnet\n\n# Start the environment\npoetry shell\n```\n\n## Getting Started\n\n| Name  | Link  |\n|---|---|\n| Visual Topic Modeling With Bunkatopics  | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1DtPrI82TYepWLoc4RwuQnOqMJb0eWT_t?usp=sharing)  |\n\n## Quick Start\n\nWe start by extracting topics from the well-known 20 newsgroups dataset containing English documents:\n\n```python\nfrom bunkatopics import bunkatopics\nfrom sklearn.datasets import fetch_20newsgroups\nimport random\n \nfull_docs = fetch_20newsgroups(subset=\'all\',  remove=(\'headers\', \'footers\', \'quotes\'))[\'data\']\nfull_docs_random = random.sample(full_docs, 1000)\n\n```\n\nYou can the load any model from langchain. Some of them might be large, please check the langchain [documentation](https://python.langchain.com/en/latest/reference/modules/embeddings.html)\n\nIf you want to start with a small model:\n\n```python\nfrom langchain.embeddings import HuggingFaceEmbeddings\n\nembedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")\n\nbunka = Bunka(model_hf=embedding_model)\n\nbunka.fit(full_docs)\ndf_topics = bunka.get_topics(n_clusters = 20)\n```\n\nIf you want a bigger LLM Like [Instructor](https://github.com/HKUNLP/instructor-embedding)\n\n```python\nfrom langchain.embeddings import HuggingFaceInstructEmbeddings\n\nembedding_model = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-large",\n                                                embed_instruction="Embed the documents for visualisation of Topic Modeling on a map : ")\n\nbunka = Bunka(model_hf=embedding_model)\n\nbunka.fit(full_docs)\ndf_topics = bunka.get_topics(n_clusters = 20)\n```\n\nThen, we can visualize\n\n```python\ntopic_fig = bunka.visualize_topics( width=800, height=800)\ntopic_fig\n...\n```\n\nThe map display the different texts on a 2-Dimensional unsupervised scale. Every region of the map is a topic described by its most specific terms.\n\n<img src="images/newsmap.png" width="70%" height="70%" align="center" />\n\n```python\n\nbourdieu_fig = bunka.visualize_bourdieu(x_left_words=["past"],\n                                        x_right_words=["future", "futuristic"],\n                                        y_top_words=["politics", "Government"],\n                                        y_bottom_words=["cultural phenomenons"],\n                                        height=2000,\n                                        width=2000)\n```  \n\nThe power of this visualisation is to constrain the axis by creating continuums and looking how the data distribute over these continuums. The inspiration is coming from the French sociologist Bourdieu, who projected items on [2 Dimensional maps](https://www.politika.io/en/notice/multiple-correspondence-analysis).\n\n<img src="images/bourdieu.png" width="70%" height="70%" align="center" />\n\n## Multilanguage\n\nThe package use Spacy to extract meaningfull terms for the topic represenation.\n\nIf you wish to change language to french, first, download the corresponding spacy model:\n\n```bash\npython -m spacy download fr_core_news_lg\n```\n\n```python\nfrom langchain.embeddings import HuggingFaceEmbeddings\n\nembedding_model = HuggingFaceEmbeddings(model_name="distiluse-base-multilingual-cased-v2")\n\nbunka = Bunka(model_hf=embedding_model, language = \'fr_core_news_lg\')\n\nbunka.fit(full_docs)\ndf_topics = bunka.get_topics(n_clusters = 20)\n```  \n\n## Functionality\n\nHere are all the things you can do with Bunkatopics\n\n### Common\n\nBelow, you will find an overview of common functions in BERTopic.\n\n| Method | Code  |\n|-----------------------|---|\n| Fit the model    |  `.fit(docs)` |\n| Fit the model and get the topics  |  `.fit_transform(docs)` |\n| Acces the topics   | `.get_topics(n_clusters=10)`  |\n| Access the top documents per topic    |  `.get_top_documents()` |\n| Access the distribution of topics   |  `.get_topic_repartition()` |\n| Visualize the topics on a Map |  `.visualize_topics()` |\n| Visualize the topics on Natural Language Supervised axis | `.visualize_bourdieu()` |\n| Access the Coherence of Topics |  `.get_topic_coherence()` |\n| Get the closest documents to your search | `.search(\'politics\')` |\n\n### Attributes\n\nYou can access several attributes\n\n| Attribute | Description |\n|------------------------|---------------------------------------------------------------------------------------------|\n| `.docs`               | The documents stores as a Document pydantic model |\n| `.topics` | The Topics stored as a Topic pydantic model. |\n',
    'author': 'Charles De Dampierre',
    'author_email': 'charlesdedampierre@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
