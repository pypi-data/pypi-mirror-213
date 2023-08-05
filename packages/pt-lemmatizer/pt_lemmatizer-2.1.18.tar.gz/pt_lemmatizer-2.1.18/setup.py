from setuptools import setup, find_packages
import codecs
import os

VERSION = '2.1.18'
DESCRIPTION = 'A NLP package for Portuguese Lemmatization.'
LONG_DESCRIPTION = '''
This NLP package for Portuguese lemmatization is a powerful and advanced tool that can accurately transform words into their base forms or lemmas, taking into account the specific grammatical rules and variations of the Portuguese language. It is designed to handle various types of text input and supports multiple output formats, making it a versatile tool for applications such as information retrieval, machine translation, sentiment analysis, and text classification. Additionally, the package is customizable and user-friendly, allowing users to specify their own dictionaries and rules for lemmatization and providing features for error correction and word sense disambiguation.
Whether you are a researcher, developer, or linguist working with Portuguese text data, this NLP package can help you save time and improve the accuracy and quality of your analyses. With its advanced algorithms and techniques in NLP, you can trust that this tool will provide high-quality results and make the lemmatization process more efficient.

*_A lemma is a word that stands at the head of a definition in a dictionary._* [Wikipedia](https://simple.wikipedia.org/wiki/Lemma_(linguistics)#:~:text=A%20lemma%20is%20a%20word,you%20find%20in%20the%20dictionary.)
### Example
```
from pt_lemmatizer import Lemmatizer

l = Lemmatizer()
l.lemmatize('apagou')  #all words must be unidecoded and lowercased
>> 'apagar'
l.lemmatize('nasalaram')
>> 'nasalar'

'''

# Setting up
setup(
    name="pt_lemmatizer",
    version=VERSION,
    author="Naomi Lago",
    author_email="<info@naomilago.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['unidecode'],
    keywords=['python', 'portuguese', 'lemmatizer', 'nlp'],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
    package_data={'': ['data/*.txt']},
)
