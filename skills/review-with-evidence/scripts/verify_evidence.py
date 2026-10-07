"""Check local excerpt matching and record structure, not source truth or entailment."""
import argparse
import json
import re
from urllib.parse import urlparse


def validate(data):
    errors = []
    papers = data.get('papers') if isinstance(data, dict) else None
    if not isinstance(papers, list) or not papers:
        return {'ok': False, 'errors': ['papers must be a nonempty array']}
    seen = set()
    for i, paper in enumerate(papers):
        prefix = f'papers[{i}]'
        if not isinstance(paper, dict):
            errors.append(f'{prefix}: must be an object')
            continue
        for key in ('id', 'title', 'source_url', 'abstract_text', 'quote', 'quote_location', 'reason'):
            if not isinstance(paper.get(key), str) or not paper[key].strip():
                errors.append(f'{prefix}: missing/non-string {key}')
        pid = paper.get('id')
        if isinstance(pid, str):
            if pid in seen:
                errors.append(f'{prefix}: duplicate id')
            seen.add(pid)
        authors = paper.get('authors')
        if not isinstance(authors, list) or not authors or any(not isinstance(a, str) or not a.strip() for a in authors):
            errors.append(f'{prefix}: invalid authors')
        year = paper.get('year')
        if isinstance(year, bool) or not isinstance(year, int) or not 1000 <= year <= 9999:
            errors.append(f'{prefix}: invalid year')
        reason = paper.get('reason')
        if isinstance(reason, str) and not 1 <= len(reason.strip()) <= 10:
            errors.append(f'{prefix}: reason must contain 1..10 characters')
        url = paper.get('source_url')
        if isinstance(url, str):
            parsed = urlparse(url)
            if parsed.scheme not in ('http', 'https') or not parsed.netloc:
                errors.append(f'{prefix}: invalid source URL')
        abstract, quote = paper.get('abstract_text'), paper.get('quote')
        if isinstance(abstract, str) and isinstance(quote, str) and quote.strip():
            norm = lambda s: re.sub(r'\s+', ' ', s).strip()
            if norm(quote) not in norm(abstract):
                errors.append(f'{prefix}: quote not found in abstract snapshot')
    return {'ok': not errors, 'errors': errors,
            'scope': 'structure and local text match only; source, sentence boundaries and semantic support require review'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input')
    args = parser.parse_args()
    try:
        with open(args.input, encoding='utf-8') as f:
            result = validate(json.load(f))
    except (ValueError, OSError) as exc:
        result = {'ok': False, 'errors': [str(exc)]}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(0 if result['ok'] else 1)
