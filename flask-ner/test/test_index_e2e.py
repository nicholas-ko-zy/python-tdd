import unittest
# import webdriver, which is a automation package for Firefox
from selenium import webdriver
from selenium.webdriver.common.by import By

# You have to run the Flask App in another terminal in
# order for this test to work 

class E2ETests(unittest.TestCase):
    
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.get('http://localhost:5000')

    def tearDown(self):
        self.driver.quit()

    def test_browser_title_contains_app_name(self):
        self.assertIn('Named Entity', self.driver.title)

    def test_page_heading_is_named_entity_finder(self):
        heading = self._find("heading").text
        self.assertEqual("Named Entity Finder", heading)

    def test_page_has_input_for_text(self):
        input_element = self._find('input-text')
        self.assertIsNotNone(input_element)

    def test_page_has_button_for_submitting_text(self):
        submit_button = self._find('find-button')
        self.assertIsNotNone(submit_button)

    def test_page_has_ner_table(self):
        input_element = self._find('input-text')
        submit_button = self._find('find-button')
        input_element.send_keys('France and Germany share a border in Europe')
        submit_button.click()
        table = self._find('ner-table')
        self.assertIsNotNone(table)

    def _find(self, val):
        attribute_of_interest = f"[data-test-id='{val}']"
        input_element = self.driver.find_element(By.CSS_SELECTOR, attribute_of_interest)
        return input_element