import spacy

class NamedEntityClient:
    def __init__(self, model):
        self.model = model

    def get_ents(self, sentence):
        doc = self.model(sentence)
        entities = [{ 'ent': ent.text, 'label': self.map_label(ent.label_)} for ent in doc.ents]
        return {'ents': entities, 'html': ''}
 
    # A static method is a method that belongs to a class rather than an
    # instance of a class. The static methods do not require instantiation. 
    @staticmethod  
    def map_label(label):
        label_map = {
            'PERSON'  : 'Person',
            'NORP'    : 'Group',
            'LOC'     : 'Location',
            'GPE'     : 'Location',
            'LANGUAGE': 'Language'
        }
        # The get method returns the value of the assoc. key in the dict.
        return label_map.get(label)
    