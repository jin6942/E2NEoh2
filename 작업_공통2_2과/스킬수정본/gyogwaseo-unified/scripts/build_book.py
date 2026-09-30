"""Build or advance one cumulative DOCX from the common manuscript.

Writes an exclusive new plan/report, updates only changed approved blocks, and
checks the actual saved text and formatting. Success is BUILT_NOT_FINAL: Word
visual inspection and independent content review remain verify_release inputs.
"""
import argparse
from contextlib import ExitStack
from copy import deepcopy
import hashlib
import json
import os
from pathlib import Path
import uuid

from book_plan import compile_plan
from check_saved_docx import check, extract
from master_docx import RoleBank, write
from saved_format import canonical_hash


def file_hash(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def patch_blocks(plan, saved):
    """Find required replacements/insertions without inferring deletions/moves."""
    actual = extract(saved)
    if actual['unmanaged_body_elements']:
        raise ValueError('Unmanaged existing content requires explicit migration; refusing to regenerate it')
    existing = [b['id'] for b in actual['blocks']]
    canonical = [b['id'] for b in plan['blocks']]
    if any(key not in canonical for key in existing):
        raise ValueError('Existing blocks are absent from the requested canonical scope; deletion or backward-stage changes require review')
    if existing != [key for key in canonical if key in existing]:
        raise ValueError('Existing block order differs from the canonical order; automatic movement is forbidden')
    result = check(plan, saved, scope='targeted')
    global_errors = [e for e in result['errors'] if 'block' not in e]
    if global_errors:
        raise ValueError('Existing global formatting cannot be repaired by a block patch: ' +
                         json.dumps(global_errors, ensure_ascii=False))
    changed = {e['block'] for e in result['errors']}
    live = list(existing)
    updates = []
    for index, original in enumerate(plan['blocks']):
        key = original['id']
        if key in existing and key not in changed:
            continue
        block = deepcopy(original)
        if key not in live:
            following = next((name for name in canonical[index + 1:] if name in live), None)
            if following is not None:
                block['insert_before'] = following
                live.insert(live.index(following), key)
            else:
                preceding = next((name for name in reversed(canonical[:index]) if name in live), None)
                if preceding is None:
                    raise ValueError('Cannot patch a new block without an existing canonical anchor')
                block['insert_after'] = preceding
                live.insert(live.index(preceding) + 1, key)
        updates.append(block)
    if live != canonical:
        raise ValueError('Planned insertions do not reproduce the canonical block order')
    return updates, [key for key in existing if key not in {b['id'] for b in updates}]


def build(data, output, plan_output, report_output, scope='full', mode='create',
          expected_sha256=None, input_path=None):
    if mode not in {'create', 'patch'}:
        raise ValueError('mode must be create or patch')
    output, plan_output, report_output = (Path(x).resolve() for x in (output, plan_output, report_output))
    if len({output, plan_output, report_output}) != 3:
        raise ValueError('DOCX, plan, and report paths must be different')
    if output.suffix.lower() != '.docx' or any(x.suffix.lower() != '.json' for x in (plan_output, report_output)):
        raise ValueError('Output extensions must be DOCX, JSON plan, and JSON report')
    input_file_sha256 = None
    if input_path is not None:
        input_path = Path(input_path).resolve()
        if input_path in {output, plan_output, report_output}:
            raise ValueError('Outputs must not overwrite the input manuscript')
        raw = input_path.read_bytes()
        if json.loads(raw.decode('utf-8-sig')) != data:
            raise ValueError('Manuscript file changed after it was read')
        input_file_sha256 = hashlib.sha256(raw).hexdigest()
    if any(x.exists() for x in (plan_output, report_output)):
        raise ValueError('Plan/report files already exist; choose new review-output paths')
    if output == RoleBank().reference.resolve():
        raise ValueError('Cannot overwrite the retained MASTER')
    if mode == 'create' and output.exists():
        raise ValueError('Create refuses an existing DOCX; use patch with its expected SHA-256')
    if mode == 'patch' and (not expected_sha256 or not output.is_file() or file_hash(output) != expected_sha256):
        raise ValueError('Current DOCX version changed or expected SHA-256 is missing')
    plan = compile_plan(data, scope)
    if mode == 'patch':
        updates, preserved = patch_blocks(plan, output)
    else:
        updates, preserved = plan['blocks'], []
    for path in (output, plan_output, report_output):
        path.parent.mkdir(parents=True, exist_ok=True)
    staged = output.parent / ('gyogwaseo-build-' + uuid.uuid4().hex + '.docx')
    reserved = []
    committed = False
    try:
        if mode == 'create':
            write(plan, staged)
        elif updates:
            with staged.open('xb') as stream:
                stream.write(output.read_bytes())
            write({'blocks': updates}, staged, mode='patch', expected_sha256=expected_sha256)
        candidate = staged if staged.exists() else output
        candidate_check = check(plan, candidate, scope='full')
        if candidate_check['status'] != 'SAVED_CONTENT_MATCH':
            raise ValueError('Candidate failed saved text/format checks; original DOCX was preserved: ' +
                             json.dumps(candidate_check['errors'], ensure_ascii=False))
        if input_path is not None and file_hash(input_path) != input_file_sha256:
            raise ValueError('Manuscript changed before committing the DOCX')
        if mode == 'patch' and file_hash(output) != expected_sha256:
            raise ValueError('Concurrent DOCX change detected before committing')
        # Reserve sidecar names exclusively before touching the final DOCX.
        # They are task-created files and are removed if committing fails.
        with ExitStack() as stack:
            streams = []
            for path in (plan_output, report_output):
                streams.append(stack.enter_context(path.open('x', encoding='utf-8')))
                reserved.append(path)
            if mode == 'create':
                # Same-directory hard linking is exclusive: unlike replace(),
                # it can never overwrite a file that appeared after preflight.
                os.link(staged, output)
                committed = True
            elif updates:
                os.replace(staged, output)
                committed = True
            final_check = check(plan, output, scope='full')
            if final_check['status'] != 'SAVED_CONTENT_MATCH':
                raise ValueError('Final physical file no longer matches the checked candidate')
            if final_check['saved_sha256'] != candidate_check['saved_sha256']:
                raise ValueError('Final physical file changed after candidate validation')
            result = {
                'status': 'BUILT_NOT_FINAL', 'scope': scope, 'mode': mode,
                'output': str(output), 'plan_output': str(plan_output), 'report_output': str(report_output),
                'input_path': str(input_path) if input_path is not None else None,
                'input_file_sha256': input_file_sha256, 'manuscript_sha256': canonical_hash(data),
                'plan_sha256': final_check['plan_sha256'], 'contract_sha256': final_check['contract_sha256'],
                'reference_sha256': final_check['reference_sha256'], 'saved_sha256': final_check['saved_sha256'],
                'changed_blocks': [b['id'] for b in updates], 'preserved_blocks': preserved,
                'saved_docx_validation': final_check,
                'independent_content_review': 'NOT_PERFORMED', 'semantic_review': 'NOT_PERFORMED',
                'word_visual_review': 'NOT_PERFORMED', 'release_validation': 'NOT_PERFORMED',
                'next_step': 'Complete independent content and Word visual reviews, then run verify_release.py',
            }
            streams[0].write(json.dumps(plan, ensure_ascii=False, indent=2))
            streams[1].write(json.dumps(result, ensure_ascii=False, indent=2))
        if json.loads(plan_output.read_text(encoding='utf-8')) != plan:
            raise ValueError('Saved plan could not be re-read unchanged')
        saved_report = json.loads(report_output.read_text(encoding='utf-8'))
        if saved_report['saved_sha256'] != file_hash(output):
            raise ValueError('DOCX changed during report verification')
        return result
    except Exception:
        if not committed:
            for path in reserved:
                path.unlink(missing_ok=True)
        raise
    finally:
        if staged.exists():
            staged.unlink()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', type=Path)
    parser.add_argument('output', type=Path)
    parser.add_argument('plan', type=Path)
    parser.add_argument('report', type=Path)
    parser.add_argument('--scope', choices=['learning', 'full'], default='full')
    parser.add_argument('--mode', choices=['create', 'patch'], default='create')
    parser.add_argument('--expected-sha256')
    args = parser.parse_args()
    data = json.loads(args.input.read_text(encoding='utf-8-sig'))
    result = build(data, args.output, args.plan, args.report, args.scope, args.mode,
                   args.expected_sha256, args.input)
    print(json.dumps({k: v for k, v in result.items() if k != 'saved_docx_validation'}, ensure_ascii=False))


if __name__ == '__main__':
    main()
