"""Check saved integrated/split artifacts and actual internal Word/PDF receipts.

This module never generates or approves review evidence. A matching receipt is
only evidence supplied by the actual renderer/reviewer; semantic and visual
review remain mandatory in verify_split_release.
"""
import json
from pathlib import Path


def check_split_evidence(manifest, reports, files, base='.'):
    from verify_release import digest, canonical_hash, pdf_pages
    from review_coverage import _unique_json
    from split_book import verify_split, VOLUME_KINDS

    base = Path(base).resolve()
    errors, pending, protected = [], [], set()
    bindings, page_map, boundaries, deliveries, docx_files = {}, [], [], [], []
    volume_rows, pdf_rows, render_rows = [], [], []

    def fail(code, detail):
        errors.append({'code': code, 'detail': str(detail)})

    def wait(code, detail):
        pending.append({'code': code, 'detail': str(detail)})

    def result():
        return {'errors': errors, 'pending': pending, 'protected_paths': sorted(protected),
                'bindings': bindings, 'pages': len(page_map) if page_map else None,
                'page_map': page_map, 'boundaries': boundaries, 'delivery_files': deliveries,
                'docx_files': docx_files}

    def load(ref, name, suffix=None, as_json=False):
        if not isinstance(ref, dict) or not isinstance(ref.get('path'), str) or not ref['path'].strip():
            wait('SPLIT_EVIDENCE_MISSING', name)
            return None
        try:
            path = Path(ref['path'])
            path = (path if path.is_absolute() else base / path).resolve()
            protected.add(str(path))
            if suffix and path.suffix.lower() != suffix:
                raise ValueError(name + ': expected ' + suffix)
            if not path.is_file():
                wait('SPLIT_EVIDENCE_MISSING', str(path)); return None
            raw = path.read_bytes()
            if ref.get('sha256') != digest(raw):
                fail('SPLIT_EVIDENCE_STALE', name); return None
            value = json.loads(raw.decode('utf-8-sig'), object_pairs_hook=_unique_json) if as_json else raw
            if as_json and not isinstance(value, dict):
                raise ValueError(name + ': JSON object required')
            return path, value, digest(raw)
        except (OSError, ValueError, UnicodeError) as exc:
            fail('SPLIT_EVIDENCE_INVALID', name + ': ' + str(exc)); return None

    if not isinstance(manifest, dict):
        wait('SPLIT_MANIFEST_MISSING', 'Current splitter manifest is required')
        return result()
    try:
        match = verify_split(manifest, base)
        protected.update(match.get('protected_paths', []))
        if match.get('status') != 'SPLIT_CONTENT_MATCH':
            fail('SPLIT_CONTENT_MISMATCH', match.get('errors', match.get('status')))
    except (OSError, ValueError, TypeError, KeyError, AttributeError) as exc:
        fail('SPLIT_CONTENT_MISMATCH', exc)
    for manifest_name, artifact_name in [('source_docx', 'docx'), ('plan', 'plan')]:
        reference = manifest.get(manifest_name)
        if (not files.get(artifact_name) or
                not isinstance(reference, dict) or reference.get('sha256') != files[artifact_name][2]):
            fail('SPLIT_INPUT_MISMATCH', manifest_name + ': current full input is required')
    volumes = manifest.get('volumes', [])
    if (not isinstance(volumes, list) or any(not isinstance(v, dict) for v in volumes) or
            [v.get('kind') for v in volumes] != list(VOLUME_KINDS)):
        fail('SPLIT_VOLUME_ORDER', 'Exactly five ordered split volumes are required')
        return result()
    integrated = manifest.get('integrated_docx')
    if not isinstance(integrated, dict):
        wait('SPLIT_INTEGRATED_COPY_MISSING', 'The delivered integrated copy must be declared')
        return result()
    rows = [dict(integrated, kind='integrated')] + volumes
    docs = {}
    for row in rows:
        kind = row['kind']
        item = load(row, kind + '/docx', '.docx')
        if item:
            if row.get('filename') != item[0].name:
                fail('SPLIT_FILENAME_MISMATCH', kind)
            docs[kind] = item
            docx_files.append({'kind': kind, 'path': str(item[0]), 'sha256': item[2]})
            volume_rows.append({'kind': kind, 'sha256': item[2]})
    if len({v['path'] for v in docx_files}) != len(docx_files):
        fail('SPLIT_ARTIFACT_ALIAS', 'Six delivered DOCX files must have distinct paths')
    if docs.get('integrated') and files.get('docx') and docs['integrated'][2] != files['docx'][2]:
        fail('SPLIT_INTEGRATED_COPY_CHANGED', 'The integrated copy must be byte-identical')
    delivery_zip = load(manifest.get('delivery_zip'), 'delivery ZIP', '.zip')
    if delivery_zip:
        bindings['delivery_zip_sha256'] = delivery_zip[2]
        deliveries.append({'kind': 'delivery_zip', 'path': str(delivery_zip[0]), 'sha256': delivery_zip[2]})

    supplied = reports.get('split_word_renders', [])
    if (not isinstance(supplied, list) or any(not isinstance(row, dict) for row in supplied) or
            [row.get('kind') for row in supplied] != list(VOLUME_KINDS)):
        wait('SPLIT_WORD_RENDERS_MISSING', 'Five ordered {kind,pdf,receipt} references required')
        return result()
    render_specs = [{'kind': 'integrated',
                     'pdf': {'path': str(files['pdf'][0]), 'sha256': files['pdf'][2]} if files.get('pdf') else {},
                     'receipt': reports.get('word_render')}] + supplied
    seen_pdf_paths = set()
    for spec in render_specs:
        kind = spec['kind']
        pdf = load(spec.get('pdf'), kind + '/pdf', '.pdf')
        receipt = load(spec.get('receipt'), kind + '/Word receipt', '.json', True)
        docx = docs.get(kind)
        if pdf:
            if pdf[0] in seen_pdf_paths:
                fail('SPLIT_PDF_ALIAS', 'Each volume requires its actual distinct PDF')
            seen_pdf_paths.add(pdf[0])
        if not all((pdf, receipt, docx)):
            continue
        row = receipt[1]
        if row.get('renderer') != 'Microsoft Word' or row.get('status') != 'PASS':
            wait('SPLIT_WORD_NOT_PERFORMED', kind)
        for key in ('version', 'execution_id'):
            if not isinstance(row.get(key), str) or not row[key].strip():
                fail('SPLIT_WORD_DETAIL_MISSING', kind + '/' + key)
        try:
            count = pdf_pages(pdf[0])
        except RuntimeError as exc:
            wait('SPLIT_PDF_CHECK_UNAVAILABLE', str(exc)); continue
        except Exception as exc:
            fail('SPLIT_PDF_INVALID', kind + ': ' + str(exc)); continue
        if (type(count) is not int or count < 1 or type(row.get('pages')) is not int or
                row['pages'] != count or row.get('source_unchanged') is not True or
                row.get('source_sha256') != docx[2] or row.get('pdf_sha256') != pdf[2]):
            fail('SPLIT_WORD_RENDER_MISMATCH', kind)
            continue
        start = len(page_map) + 1
        for local_page in range(1, count + 1):
            page_map.append({'page': len(page_map) + 1, 'kind': kind, 'volume_page': local_page,
                             'docx_sha256': docx[2], 'pdf_sha256': pdf[2]})
        boundaries.extend([[page, page + 1] for page in range(start, start + count - 1)])
        pdf_rows.append({'kind': kind, 'sha256': pdf[2]})
        render_rows.append({'kind': kind, 'sha256': receipt[2]})
    if len(volume_rows) == 6:
        bindings['volume_set_sha256'] = canonical_hash(volume_rows)
    if len(pdf_rows) == 6 and len(render_rows) == 6:
        bindings.update(pdf_set_sha256=canonical_hash(pdf_rows),
                        word_renders_sha256=canonical_hash(render_rows),
                        word_page_map_sha256=canonical_hash(page_map))
    return result()
