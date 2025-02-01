# Introduction

I am tracking the tutorial from this video: ["TDD Full Course (Learn Test Driven Development with Python)"](https://www.youtube.com/watch?v=eAPmXQ0dC7Q) by Wes Doyle.

## 3 Rules of TDD

1. Write a failing test first.

2. Write just enough test to fail.

3. Write just enough code to pass.

To run a set of tests, run this in your terminal:
```
# Run in your terminal
python3 -m pytest
```

Remark: Look up SOLID principles for OOP.

## Learning Point: Dependency Inversion Principle

(Timestamp: 23:14 - 25:27) At this time, Doyle shows a live coding example 
of the "Dependency Inversion Principle". From Wiki: It's summarised as a emphasis on depending on abstractions not concretes. I've copied out the example below from the `ner_client.py` file.

```python
# Before
import spacy

class NamedEntityClient:
    def __init__(self):
        # Initialise ner instance with a SpaCy model, as specified below
        self.model = spacy.load("en_core_web_sm")

    def get_ents(self, sentence):
        doc = self.model(sentence)
        return {}
```

Issue: Here there is a tight coupling of 'spaCy' existing in the first place anytime we create an instance of `NamedEntityClient`. You're loading the language model into memory. Now this is not flexible, because what if you want to load another language model or you may think it's kinda pointless to load a spacy model just to test for the existence of `NamedEntityClient`.

What does it look like to exercise the 'Dependency Inversion Principle'? Instead of having `NamedEntityClient` depend on some detail like `"en_core_web_sm"`, it should depend on an abstraction that gets passed to it. Here's what the after code looks like:

```python
# After
import spacy

class NamedEntityClient:
    def __init__(self, model):
        # Initialise ner instance with a spaCy model, as specified below
        self.model = model

    def get_ents(self, sentence):
        doc = self.model(sentence)
        return {}
```

The difference here is that we still get to preserve the functionality of the `get_ents` method. You can still pass a sentence to the model to generate some output. But now, instead of straightaway instantiating the specific model you want to use when you create a fresh instance of `NamedEntityClient`, you sort of push the responsibility of specifying your model to a 'higher' level of abstraction. You do this by adding a `model` argument to the initialisation method. Of course this decision will influence the way your test cases are written. The test case will need a placeholder `model` variable. 

```python
class TestNerClient(unittest.TestCase):

    def test_get_ents_returns_dictionary_given_empty_string(self):
        # Create a dummy NER model 
        model = NerModelTestDouble('eng') # <- Change was made here
        # Create a NER instance
        ner = NamedEntityClient(model)
        # Assign the entity a variable name "ent"
        ents = ner.get_ents("")
        # Check if the python type is a 'dictionary'
        self.assertIsInstance(ents, dict)
#...
```
Doyle: When testing, we want something that behaves like the `spaCy` model but we don't want to load the whole thing.

Remark to self: You can also look into what mocks, spies are in relation to 'Dependency Inversion Principle'. Is creating a dummy model above a mock? 

## Lesson: Creating a mock for the Ner model

(Timestamp 26:56 - )

Rationale: Since we are using a mock up in our test for Ner, we need to actually create a class to represent the mock up. We do that in the file `test_doubles.py`. Our mock-up can't be made up since it's supposed to have the subset (not necessarily proper subset) of behaviours that the actual `spaCy` model has. One thing to check out is what kind of attributes does the model output give. In our case, the model output is of type `<class 'spacy.tokens.doc.Doc'>` and has a attribute (no parentheses) `ents`. From there, we observe that `ents` has two attributes - `text` and `label` respectively. See screenshot below.

![types and attributes of model](/screenshot_img/ent_attributes.png)

Remark to self: Check out ways of automating mocks in `pytest-mock` and `monkey-patch`.

## Lesson: Command to run a single test

```
pytest test/test_ner_client.py::TestNerClient::test_get_ents_returns_dictionary_given_empty_string_causes_empty_spacy_doc_ents 
```
^ Hint: You can use tab completion along the way. Remember to use the double-colons `::` after the `.py` file. First `::` to specify the class name and the second one to specify the test name.

(Stopped at 38:40)
