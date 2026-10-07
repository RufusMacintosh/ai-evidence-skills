"""Compute forecast coverage; no official Guangdong settlement or source verification."""
import argparse
import json
import math
from datetime import date
from urllib.parse import urlparse


def number(value, name, positive=False):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise ValueError(f'{name}: must be a finite number')
    if value < 0 or (positive and value == 0):
        raise ValueError(f'{name}: invalid sign/zero')
    return value


def analyze(data):
    if not isinstance(data, dict):
        raise ValueError('input must be an object')
    if data.get('region') != '广东' or data.get('subject') != '售电公司' or data.get('unit') != 'MWh':
        raise ValueError('expected 广东/售电公司/MWh')
    as_of = date.fromisoformat(data['as_of'])
    if not isinstance(data.get('period'), str) or not data['period'].strip():
        raise ValueError('period required')
    if not isinstance(data.get('rows'), list) or not data['rows']:
        raise ValueError('rows must be a nonempty array')
    rows, seen = [], set()
    for row in data['rows']:
        if not isinstance(row, dict) or not isinstance(row.get('slot'), str) or not row['slot'].strip():
            raise ValueError('invalid row/slot')
        if row['slot'] in seen:
            raise ValueError('duplicate slot')
        seen.add(row['slot'])
        load = number(row.get('load_mwh'), 'load_mwh')
        contract = number(row.get('contract_mwh'), 'contract_mwh')
        exposure = load - contract
        rows.append({'slot': row['slot'], 'load_mwh': load, 'contract_mwh': contract,
                     'coverage_ratio': contract / load if load else None,
                     'exposure_mwh': exposure,
                     'shortfall_mwh': max(exposure, 0), 'surplus_mwh': max(-exposure, 0)})
    load = sum(r['load_mwh'] for r in rows)
    contract = sum(r['contract_mwh'] for r in rows)
    rule_result = {'status': 'pending_verification', 'reason': 'no verified applicable rule supplied'}
    rule = data.get('signing_rule')
    if rule is not None:
        reasons = []
        if not isinstance(rule, dict):
            raise ValueError('signing_rule must be an object')
        if rule.get('verified') is not True:
            reasons.append('rule not marked manually verified')
        for key in ('region', 'subject', 'period'):
            if rule.get(key) != data[key]:
                reasons.append(f'rule {key} mismatch')
        try:
            start, end = date.fromisoformat(rule['effective_from']), date.fromisoformat(rule['effective_to'])
            if start > end or not start <= as_of <= end:
                reasons.append('rule outside supplied effective interval')
        except (KeyError, TypeError, ValueError):
            reasons.append('invalid or missing effective dates')
        for key in ('source_url', 'clause', 'numerator_basis', 'denominator_basis'):
            if not isinstance(rule.get(key), str) or not rule[key].strip():
                reasons.append(f'missing {key}')
        url = urlparse(rule.get('source_url', '') if isinstance(rule.get('source_url'), str) else '')
        if url.scheme not in ('http', 'https') or not url.netloc:
            reasons.append('invalid source URL')
        try:
            numerator = number(rule.get('numerator_mwh'), 'numerator_mwh')
            denominator = number(rule.get('denominator_mwh'), 'denominator_mwh', positive=True)
            threshold = number(rule.get('min_ratio'), 'min_ratio')
            if threshold > 1:
                raise ValueError('min_ratio must be <= 1')
        except ValueError as exc:
            reasons.append(str(exc))
        if reasons:
            rule_result = {'status': 'pending_verification', 'reasons': reasons}
        else:
            ratio = numerator / denominator
            rule_result = {'status': 'matches_supplied_threshold' if ratio >= threshold else 'below_supplied_threshold',
                           'ratio': ratio, 'min_ratio': threshold,
                           'additional_numerator_mwh': max(denominator * threshold - numerator, 0),
                           'source_url': rule['source_url'], 'clause': rule['clause'],
                           'scope': 'arithmetic against user-supplied manually verified record; not official verification'}
    return {'unit': 'MWh', 'period': data['period'], 'total_load_mwh': load,
            'total_contract_mwh': contract, 'forecast_coverage_ratio': contract / load if load else None,
            'total_shortfall_mwh': sum(r['shortfall_mwh'] for r in rows),
            'total_surplus_mwh': sum(r['surplus_mwh'] for r in rows),
            'rows': rows, 'signing_rule_check': rule_result,
            'limitations': ['No price forecast, optimization, settlement or profit calculation.',
                            'Caller must verify interval alignment, completeness and official rule applicability.']}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input')
    args = parser.parse_args()
    try:
        with open(args.input, encoding='utf-8') as f:
            result = analyze(json.load(f))
    except (KeyError, TypeError, ValueError, OSError) as exc:
        print(json.dumps({'error': str(exc)}, ensure_ascii=False))
        raise SystemExit(1)
    print(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False))
