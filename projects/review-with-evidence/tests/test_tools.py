import copy
import importlib.util
from pathlib import Path
import unittest
ROOT = Path(__file__).resolve().parents[1]

def load(rel):
    spec = importlib.util.spec_from_file_location(rel.split('/')[-1][:-3], ROOT / rel)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module
evidence = load('skills/review-with-evidence/scripts/verify_evidence.py')

class EvidenceTests(unittest.TestCase):

    def setUp(self):
        self.data = {'papers': [{'id': 'synthetic-1', 'title': 'Synthetic example', 'authors': ['Example'], 'year': 2026, 'source_url': 'https://example.invalid/paper', 'abstract_text': 'This is synthetic evidence. Results depend on context.', 'quote': 'Results depend on context.', 'quote_location': 'Abstract sentence 2', 'reason': '说明适用边界'}]}

    def test_valid_local_match(self):
        self.assertTrue(evidence.validate(self.data)['ok'])

    def test_fabricated_quote(self):
        self.data['papers'][0]['quote'] = 'The method always works.'
        self.assertFalse(evidence.validate(self.data)['ok'])

    def test_reason_limit(self):
        self.data['papers'][0]['reason'] = '一' * 11
        self.assertFalse(evidence.validate(self.data)['ok'])

    def test_duplicate(self):
        self.data['papers'].append(copy.deepcopy(self.data['papers'][0]))
        self.assertFalse(evidence.validate(self.data)['ok'])
if __name__ == '__main__':
    unittest.main()
