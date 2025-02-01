import unittest
from ner_client import NamedEntityClient
from test_doubles import NerModelTestDouble

class TestNerClient(unittest.TestCase):

    def test_get_ents_returns_dictionary_given_empty_string_causes_empty_spacy_doc_ents(self):
        # Create a dummy NER model 
        model = NerModelTestDouble('eng')
        model.returns_doc_ents([])
        # Create a NER instance
        ner = NamedEntityClient(model)
        # Assign the entity a variable name "ent"
        ents = ner.get_ents("")
        # Check if the python type is a 'dictionary'
        self.assertIsInstance(ents, dict)
        # You should expect to see a Python dictionary that looks something like
        # { ents: [{...}],
        #   html: "<span>..."}

        # Where,
        # ents : Another dictionary with the entity type (key) and the entity
        # name (value).

        # html: The html code that you will output back to the client facing UI
    def test_get_ents_returns_dictionary_given_nonempty_string_causes_empty_spacy_doc_ents(self):
        model = NerModelTestDouble('eng')
        model.returns_doc_ents([])
        ner = NamedEntityClient(model)
        ents = ner.get_ents("Madison is a city in Wisconsin")
        self.assertIsInstance(ents, dict)
