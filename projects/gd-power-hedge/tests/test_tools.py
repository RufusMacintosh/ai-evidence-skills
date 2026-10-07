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
power = load('skills/gd-power-hedge/scripts/analyze_coverage.py')

class PowerTests(unittest.TestCase):

    def setUp(self):
        self.data = {'region': '广东', 'subject': '售电公司', 'unit': 'MWh', 'as_of': '2026-10-06', 'period': '2026-11', 'rows': [{'slot': 'peak', 'load_mwh': 100, 'contract_mwh': 50}, {'slot': 'valley', 'load_mwh': 100, 'contract_mwh': 150}]}

    def test_total_masks_mismatch(self):
        result = power.analyze(self.data)
        self.assertEqual(result['forecast_coverage_ratio'], 1)
        self.assertEqual(result['total_shortfall_mwh'], 50)
        self.assertEqual(result['total_surplus_mwh'], 50)
        self.assertEqual(result['signing_rule_check']['status'], 'pending_verification')

    def test_duplicate_slot(self):
        self.data['rows'].append(copy.deepcopy(self.data['rows'][0]))
        with self.assertRaises(ValueError):
            power.analyze(self.data)

    def test_invalid_numeric(self):
        for val in (True, float('nan'), -1, '100'):
            self.data['rows'][0]['load_mwh'] = val
            with self.assertRaises(ValueError):
                power.analyze(self.data)

    def test_zero_load_surplus(self):
        self.data['rows'] = [{'slot': 'zero', 'load_mwh': 0, 'contract_mwh': 10}]
        result = power.analyze(self.data)
        self.assertIsNone(result['forecast_coverage_ratio'])
        self.assertEqual(result['total_surplus_mwh'], 10)

    def test_rule_separate_denominator_and_expiry(self):
        rule = {'verified': True, 'region': '广东', 'subject': '售电公司', 'period': '2026-11', 'effective_from': '2026-01-01', 'effective_to': '2026-12-31', 'source_url': 'https://example.invalid/synthetic-rule', 'clause': 'Synthetic clause', 'numerator_basis': 'synthetic eligible contracts', 'denominator_basis': 'synthetic historical load', 'numerator_mwh': 200, 'denominator_mwh': 1000, 'min_ratio': 0.5}
        self.data['signing_rule'] = rule
        result = power.analyze(self.data)['signing_rule_check']
        self.assertEqual(result['status'], 'below_supplied_threshold')
        self.assertEqual(result['additional_numerator_mwh'], 300)
        rule['effective_to'] = '2025-12-31'
        self.assertEqual(power.analyze(self.data)['signing_rule_check']['status'], 'pending_verification')

    def test_wrong_region_rule(self):
        self.data['signing_rule'] = {'region': '山东'}
        self.assertEqual(power.analyze(self.data)['signing_rule_check']['status'], 'pending_verification')
if __name__ == '__main__':
    unittest.main()
