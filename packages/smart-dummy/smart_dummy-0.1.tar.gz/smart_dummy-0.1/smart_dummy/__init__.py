import spacy

try:
    nlp = spacy.load('en_core_web_lg')
except OSError:
    print('Downloading language model for Spacy (this will only happen once)')
    from spacy.cli import download
    download('en_core_web_lg')

from main import get_dummies
__all__ = ['get_dummies']