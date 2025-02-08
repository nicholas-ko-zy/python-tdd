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
        # Same test as the one above except that this test takes in a
        # non-empty string
        model = NerModelTestDouble('eng')
        model.returns_doc_ents([])
        ner = NamedEntityClient(model)
        ents = ner.get_ents("Madison is a city in Wisconsin")
        self.assertIsInstance(ents, dict)

    def test_get_ents_given_spacy_PERSON_is_returned_serializes_to_Person(self):
        # Checks for the behaviour that converts uppercase 'PERSON' to 
        # title case 'Person'
        model = NerModelTestDouble('eng')
        # Fake return doc_ents injected into mock model
        doc_ents = [{'text': 'Laurent Fressinet', 'label_':'PERSON'}]
        model.returns_doc_ents(doc_ents)
        ner = NamedEntityClient(model)
        result = ner.get_ents('...')
        expected_result = { 'ents': [{'ent': 'Laurent Fressinet', 
                                     'label': 'Person'}],
                                     # html value left blank because we don't 
                                     # know what it looks like yet.
                                     'html': ""}
        self.assertListEqual(result['ents'], expected_result['ents'])

        # { ents: [{...}],
        #   html: "<span>..."}

    def test_get_ents_given_spacy_NORP_is_returned_serializes_to_Group(self):
        """
        Same NER test but for NORP tag.
        """
        model = NerModelTestDouble('eng')
        doc_ents = [{'text': 'Lithuanian', 'label_':'NORP'}]
        model.returns_doc_ents(doc_ents)
        ner = NamedEntityClient(model)
        result = ner.get_ents('...')
        expected_result = { 'ents': [{'ent': 'Lithuanian', 
                                     'label': 'Group'}],
                                     'html': ""}
        self.assertListEqual(result['ents'], expected_result['ents'])

    def test_get_ents_given_spacy_LOC_is_returned_serializes_to_Location(self):
        """
        Same NER test but for LOC tag.
        """
        model = NerModelTestDouble('eng')
        doc_ents = [{'text': 'the ocean', 'label_':'LOC'}]
        model.returns_doc_ents(doc_ents)
        ner = NamedEntityClient(model)
        result = ner.get_ents('...')
        expected_result = { 'ents': [{'ent': 'the ocean', 
                                     'label': 'Location'}],
                                     'html': ""}
        self.assertListEqual(result['ents'], expected_result['ents'])

    def test_get_ents_given_spacy_LANGUAGE_is_returned_serializes_to_Langauge(self):
        """
        Same NER test but for LOC tag.
        """
        model = NerModelTestDouble('eng')
        doc_ents = [{'text': 'ASL', 'label_':'LANGUAGE'}]
        model.returns_doc_ents(doc_ents)
        ner = NamedEntityClient(model)
        result = ner.get_ents('...')
        expected_result = { 'ents': [{'ent': 'ASL', 
                                     'label': 'Language'}],
                                     'html': ""}
        self.assertListEqual(result['ents'], expected_result['ents'])

    def test_get_ents_given_spacy_GPE_is_returned_serializes_to_GPE(self):
        """
        Same NER test but for GPE tag.
        """
        model = NerModelTestDouble('eng')
        doc_ents = [{'text': 'Australia', 'label_':'GPE'}]
        model.returns_doc_ents(doc_ents)
        ner = NamedEntityClient(model)
        result = ner.get_ents('...')
        expected_result = { 'ents': [{'ent': 'Australia', 
                                     'label': 'Location'}],
                                     'html': ""}
        self.assertListEqual(result['ents'], expected_result['ents'])  

    def test_get_ents_given_multiple_ents_serialises_all(self):
        model = NerModelTestDouble('eng')
        doc_ents = [{'text': 'Australia', 'label_':'GPE'},
                    {'text': 'Judith Polgar', 'label_':'PERSON'}]
        model.returns_doc_ents(doc_ents)
        ner = NamedEntityClient(model)
        result = ner.get_ents('...')
        expected_result = {'ents':
                           [{'ent': 'Australia', 'label':'Location'},
                            {'ent': 'Judith Polgar', 'label':'Person'}],'html': ""}
        self.assertListEqual(result['ents'], expected_result['ents'])
         