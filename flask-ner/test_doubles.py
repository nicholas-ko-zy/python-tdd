class NerModelTestDouble:
    """
    Test double for spaCy NLP model
    """
    def __init__(self, model):
        self.model = model

    def returns_doc_ents(self, ents):
        # Specify what entity your model returns in the argument of this 
        # method. i.e. for an empty string input, you can specify an
        # empty list as the ents
        self.ents = ents

    def __call__(self, sent):
        return DocTestDouble(sent, self.ents)


class DocTestDouble:
    """
    Test double for docs, which is the variable assigned to the
    output of the nlp model as in:
    doc = nlp("string")
    """
    def __init__(self, sent, ents):
        # A Span is the data structure of
        # [('Madison', 'PERSON'), ('Wisconsin', 'GPE')]
        # In our mockup, we use list comprehension to reverse engineer
        # [(ent.text, ent.label_) for ent in doc.ents]
        self.ents = [SpanTestDouble(ent['text'], ent['label_']) for ent in ents]

    # optional patch_method
    def patch_method(self, attr, return_value):
        """
        A method to control the attribute of a DocTestDouble instance.
        """
        def patched(): return return_value
        setattr(self, attr, patched)
        return self

class SpanTestDouble:
    """
    Test double for spaCy Span
    """
    def __init__(self, text, label):
        self.text = text
        self.label_ = label
