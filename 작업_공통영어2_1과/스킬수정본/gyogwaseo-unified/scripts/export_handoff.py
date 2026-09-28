"""Export complete QC handoff TXT from the same common manuscript as the DOCX.

Produces two content-only files by default. Optional teacher QC diagnostics must
not enter FINAL. It does not certify FINAL status or import an edited TXT by
guessing slashes/markers. Existing files need their current hashes.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import uuid

from check_book import check
from check_learning_content import check as check_learning
from book_plan import gloss_text, passage_runs, CIRCLES, syntax_practices
from source_contract import (display_lesson, lesson_identity, unit_subheadings, normalize_course,
                             display_book_name, display_publisher_author, display_source_label)
from structure_hints import display_lines


def sha(value):
    return hashlib.sha256(value).hexdigest()


def header(data, scope):
    m=data['metadata']
    lines=[f'[교재명] {display_book_name(m)}',f'[과목] {normalize_course(m["course"])}',
           f'[출판사·저자] {display_publisher_author(m)}',
           '[UNIT] '+lesson_identity(m,data.get('cover'))['internal_id'],
           '[학생용 과 표시] '+display_lesson(m,data.get('cover'))]
    if m.get('edition'):
        lines.append('[교육과정·판본] '+m['edition'])
    for source in data['sources']:
        prov=source['provenance']
        lines.append('[권위 원문] '+prov['filename']+' · '+prov['location'])
    return lines+['[자료 범위] '+scope,'']


def numbered_meanings(rows):
    lines=['| 번호 | 뜻 | 번호 | 뜻 | 번호 | 뜻 |','| --- | --- | --- | --- | --- | --- |']
    for i in range(0,len(rows),3):
        cells=[]
        for j in range(i,i+3):
            cells.extend([str(j+1),rows[j]['meaning_ko'].replace('|','\\|')] if j<len(rows) else ['',''])
        lines.append('| '+' | '.join(cells)+' |')
    return lines


def render(data,scope='both',*,qc_diagnostics=False):
    """Render content; optional author length diagnostics are for question QC only."""
    if scope not in {'learning','assessment','both'}:
        raise ValueError('Unknown export scope')
    if qc_diagnostics and scope=='learning':
        raise ValueError('QC diagnostics require an assessment handoff, never a learning FINAL')
    result=check(data) if scope!='learning' else {'status':'STRUCTURE_PASS','learning':check_learning(data,scope='learning')}
    if scope=='learning':
        result['status']=result['learning']['status']
    if result['status']!='STRUCTURE_PASS':
        raise ValueError('Manuscript structure must pass before exporting a complete handoff')
    sentences={(s['source_id'],s['id']):s for s in data['sentences']}
    sources={s['id']:s for s in data['sources']}
    numbers={(src['id'],s['id']):i for src in sources.values() for i,s in enumerate(src['sentences'],1)}
    questions={q['id']:q for q in data.get('assessment',{}).get('questions',[])}
    explanations={e['id']:e for e in data.get('assessment',{}).get('explanations',[])}
    source_requests={q['id']:q for q in data.get('question_sources',[])}
    learning=header(data,'혼공해석지 + 지문분석지')
    assessment=header(data,'워크북 + 미니 모의고사 + 정답해설')
    def source_range(src,ids):
        return f'{display_source_label(sources[src])} · 원문 문장 {numbers[(src,ids[0])]}~{numbers[(src,ids[-1])]}'
    def qlines(qid):
        q=questions[qid];e=explanations[qid];view=result['question_views'][qid]
        lines=[f'[{qid}]','SET:',data.get('set_labels',{}).get(q['set_id'],q['set_id']),
               'SOURCE:',view['source_id'],'SOURCE_RANGE:',source_range(view['source_id'],view['source_sentence_ids']),
               'TYPE:',q['type'],'QUESTION:',q['question']]
        if qc_diagnostics:
            lines+=['LENGTH_REVIEW:',json.dumps(source_requests[qid]['length_review'],ensure_ascii=False),
                    'LENGTH_COMPARISON:',json.dumps(view['length_comparison'],ensure_ascii=False)]
        if q.get('passage_group_id'):
            lines+=['PASSAGE_GROUP:',q['passage_group_id']]
        elif q['type'] in {'삽입','순서'}:
            lines+=['GIVEN:',view['given']]
        if q.get('passage_group_id'):
            pass
        elif q['type']=='순서':
            lines+=['BLOCKS:']+[f'({k}) '+re.sub(r'[\r\n]+[ \t]*',' ',view['blocks'][k]) for k in 'ABC']
        else:
            lines+=['PASSAGE:',''.join(r['text'] for r in passage_runs(view)).replace('\u00a0',' ')]
        if q.get('target'):
            lines+=['TARGET:',q['target']]
        if q.get('prompt_underlines'):
            lines+=['PROMPT_UNDERLINES:',json.dumps(q['prompt_underlines'],ensure_ascii=False)]
        if q['type']=='요약':
            lines+=['[요약문]',q['summary']]
        if q['choice_mode']!='in_passage':
            lines+=['CHOICES:']+[CIRCLES[c['number']-1]+' '+c['text'] for c in sorted(q['choices'],key=lambda x:x['number'])]
        lines+=['ANSWER:',str(e['answer']),'EVIDENCE:',e['evidence'],'EXPLANATION:',e['explanation'],
                'WRONG_ANALYSIS:']+[CIRCLES[c['number']-1]+' '+c['text'] for c in sorted(e['wrong_reasons'],key=lambda x:x['number'])]
        if q['choice_mode']=='text':
            lines+=['CHOICES_KR:']+[CIRCLES[c['number']-1]+' '+c['text'] for c in sorted(e['choices_ko'],key=lambda x:x['number'])]
        return lines+[f'[/{qid}]','']

    for unit_number,u in enumerate(data['units'],1):
        uid=u['id'];src=u['source_id'];ids=u['sentence_ids'];a=u['analysis']
        learning += [f'===== [지문] {uid} =====','[SOURCE] '+src,'[학습 단위] '+uid,
                     '[원문 범위] '+source_range(src,ids)]
        for heading in unit_subheadings(data,u):
            learning += ['[원문 소제목] '+heading['text'],
                         '[소제목 출처] '+heading['id']+' · '+heading['location']+
                         ' · 앞 문장 '+heading['before_sentence_id']+' · SHA256 '+heading['artifact_sha256']]
        # Legacy hooks are omitted here too, so a later handoff cannot restore them.
        for sid in ids:
            s=sentences[(src,sid)];n=numbers[(src,sid)]
            english=' / '.join(s['text'][c['start']:c['end']] for c in s['chunks'])
            learning += [f'----- [문장 {n}] -----','[핵심 문장] '+('예' if s['key'] else '아니오'),
                         '[원문]',s['text'],'[혼공 끊어읽기]',english]
            sv_line=result['learning']['sv_lines'][f'{src}/{sid}']
            if sv_line:
                learning.append('[S/V] '+sv_line)
            learning += ['[각주]',' / '.join(('★ ' if g['star'] else '')+gloss_text(g) for g in s['glosses'])]
            for h in s.get('hints',[]):
                lines=display_lines(h)
                learning += ['[구조 힌트] '+lines[0], *lines[1:]]
            learning+=['[분석 끊어읽기 영어]',english,'[분석 끊어읽기 한국어]',
                       ' / '.join(c['ko'] for c in s['chunks']),'[자연 해석]',s['natural_ko'],f'----- [/문장 {n}] -----','']
        learning += [f'----- [분석 단위] {uid} -----','[SOURCE_RANGE] '+source_range(src,ids),
                     '['+a['heading_kind']+'] '+a['title_or_topic_en']+' ('+a['title_or_topic_ko']+')',
                     '[글의 의도/요지]',a['intent_ko'],'[글의 흐름]']
        learning += ['('+row.get('label','흐름')+') '+source_range(src,row['sentence_ids'])+
                     ' — '+row['text_ko'] for row in a['flow']]
        learning.append('[각 문장 쉬운 풀이]')
        for row in a['easy_explanations']:
            learning += [f'[{numbers[(src,row["sentence_id"])]}번 문장] '+sentences[(src,row['sentence_id'])]['text'],
                         ' '.join(row['explanatory_sentences'])]
        learning.append('[구문으로 해석하기]')
        for row in a['grammar_points']:
            original=sentences[(src,row['sentence_id'])]['text']
            learning.append(row['title']+f' [{numbers[(src,row["sentence_id"])]}번 문장]: '+original[slice(*row['span'])]+' — '+row['explanation'])
        learning.append('[유의어·반의어]')
        for rel in a['relations']:
            learning.append(' / '.join(name+': '+rel[key]['text']+' ('+rel[key]['meaning_ko']+')'
                                      for name,key in [('표제어','head'),('유의어','synonym'),('반의어','antonym')]))
        learning+=['----- [/분석 단위] -----','===== [/지문] =====','']
        if scope=='learning':
            continue
        wb=u['workbook']
        terms={t['id']:t for row in a['relations'] for t in row.values()}
        relations=[terms[x] for x in wb['relation_order']]
        assessment += [f'[WB{unit_number:02d}]','SOURCE:',src,'LEARNING_UNIT:',uid,'SOURCE_RANGE:',source_range(src,ids),
                       '[1. 오늘의 낱말]','우리말 뜻을 쓰세요.']
        assessment += [f'{i}. '+row['text'] for i,row in enumerate(u['today_words'],1)]
        if relations:
            assessment += ['[2. 유의어·반의어 뜻 쓰기]','우리말 뜻을 쓰세요.']
            assessment += [f'{i}. '+row['text'] for i,row in enumerate(relations,1)]
        assessment += ['[3. 실전문제]']+qlines(wb['question_id'])
        syntax_enabled = data['metadata'].get('syntax_training_version') == 1
        if syntax_enabled:
            assessment += ['[4. 구문 결합해서 해석하기]']
            for i,(point,expression,supports) in enumerate(syntax_practices(u,sentences),1):
                formula = point['practice']['formula_support']
                assessment += [f'{i}. '+expression+' → ______________________________',
                               '도움말: '+' / '.join([formula['en']+' — '+formula['ko']]+[g['headword']+' — '+g['meaning_ko'] for g in supports])]
            assessment.append('')
        key_number = 5 if syntax_enabled else 4
        assessment += [f'[{key_number}. 핵심 문장 {len(wb["key_sentence_ids"])}개 다시 해석하기]']
        assessment += [f'{i}. '+sentences[(src,sid)]['text'] for i,sid in enumerate(wb['key_sentence_ids'],1)]
        assessment += [f'[/WB{unit_number:02d}]','[워크북 정답]','[1. 오늘의 낱말]']+numbered_meanings(u['today_words'])
        if relations:
            assessment += ['[2. 유의어·반의어 뜻 쓰기]']+numbered_meanings(relations)
        if syntax_enabled:
            assessment += ['[4. 구문 결합해서 해석하기]']
            assessment += [f'{i}. '+point['practice']['answer_ko'] for i,(point,_,_) in enumerate(syntax_practices(u,sentences),1)]
        assessment += [f'[{key_number}. 핵심 문장 해석]']
        assessment += [f'{i}. '+sentences[(src,sid)]['natural_ko'] for i,sid in enumerate(wb['key_sentence_ids'],1)]
        assessment.append('')
    printed_groups=set()
    for plan in data.get('assessment',{}).get('plan',[]) if scope!='learning' else []:
        if plan['set_id']!='workbook':
            gid=questions[plan['id']].get('passage_group_id')
            if gid and gid not in printed_groups:
                view=result['passage_group_views'][gid]
                assessment += [f'[PASSAGE_GROUP {gid}]','QUESTION_IDS:',', '.join(view['question_ids']),
                    'SOURCE:',view['source_id'],'SOURCE_RANGE:',source_range(view['source_id'],view['source_sentence_ids']),
                    'PASSAGE:',''.join(r['text'] for r in passage_runs(view)).replace('\u00a0',' '),
                    'ANNOTATIONS_BASIS:',
                    'Transformed passage before generated labels; zero-based Unicode codepoints [start,end). '
                    'These are not offsets in the displayed PASSAGE; text identifies each marked span.',
                    'ANNOTATIONS:',json.dumps([
                        dict(mark,text=view['passage'][slice(*mark['span'])]) if 'span' in mark else dict(mark)
                        for mark in view['annotations']],ensure_ascii=False),f'[/PASSAGE_GROUP {gid}]','']
                printed_groups.add(gid)
            assessment+=qlines(plan['id'])
    return {'learning':'\n'.join(learning).rstrip()+'\n','assessment':'\n'.join(assessment).rstrip()+'\n'}


def save(path,body,expected):
    raw=body.encode('utf-8')
    if path.exists() and (not expected or sha(path.read_bytes())!=expected):
        raise ValueError('Existing handoff requires its current SHA-256')
    if not path.exists() and expected:
        raise ValueError('Expected existing handoff is absent')
    if not path.exists():
        with path.open('xb') as f:f.write(raw)
    else:
        temp=path.with_name('.'+path.name+'.'+uuid.uuid4().hex+'.tmp')
        with temp.open('xb') as f:f.write(raw)
        if sha(path.read_bytes())!=expected:
            raise ValueError('Handoff changed during update; staged temporary file retained')
        os.replace(temp,path)
    if path.read_bytes()!=raw:
        raise ValueError('Saved handoff differs from rendered content')


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input',type=Path)
    parser.add_argument('--learning',type=Path);parser.add_argument('--assessment',type=Path)
    parser.add_argument('--qc-diagnostics',action='store_true',
                        help='Teacher assessment QC only: include author length-review diagnostics; never use for FINAL')
    parser.add_argument('--expected-learning-sha256');parser.add_argument('--expected-assessment-sha256')
    parser.add_argument('--review-packet',type=Path,help='Separate review JSON; never a FINAL')
    parser.add_argument('--review-role',choices=['learning','questions-blind','questions-compare'])
    parser.add_argument('--unit-id',action='append');parser.add_argument('--question-id',action='append')
    parser.add_argument('--baseline',type=Path);parser.add_argument('--changed-only',action='store_true')
    a=parser.parse_args()
    if a.review_packet:
        if not a.review_role or any([a.learning,a.assessment,a.expected_learning_sha256,a.expected_assessment_sha256,a.qc_diagnostics]):
            parser.error('Review export requires --review-role and cannot write full handoffs in the same call')
        if a.review_packet.resolve() in {a.input.resolve(),a.baseline.resolve() if a.baseline else a.input.resolve()}:
            parser.error('Review packet must not overwrite an input')
        from review_packets import make_packet,save_packet
        raw=a.input.read_bytes();data=json.loads(raw.decode('utf-8-sig'))
        baseline_raw=a.baseline.read_bytes() if a.baseline else None
        baseline=json.loads(baseline_raw.decode('utf-8-sig')) if baseline_raw is not None else None
        packet=make_packet(data,a.review_role,unit_ids=a.unit_id,question_ids=a.question_id,
                           baseline=baseline,changed_only=a.changed_only)
        packet['input_digest']['file_sha256']=sha(raw)
        packet['input_digest']['file_sha256_status']='EXACT_INPUT_BYTES'
        if baseline_raw is not None and a.review_role != 'questions-blind' and 'baseline_digest' in packet:
            packet['baseline_digest']['file_sha256']=sha(baseline_raw)
            packet['baseline_digest']['file_sha256_status']='EXACT_INPUT_BYTES'
        save_packet(a.review_packet,packet)
        print(json.dumps({'status':'REVIEW_PACKET_NOT_FINAL','path':str(a.review_packet),
                          'sha256':sha(a.review_packet.read_bytes())},ensure_ascii=False))
        return
    if a.review_role or a.unit_id or a.question_id or a.baseline or a.changed_only:
        parser.error('Partial review options require --review-packet; full FINAL export never becomes partial')
    if a.qc_diagnostics and (a.assessment is None or 'FINAL' in a.assessment.stem.upper()):
        parser.error('--qc-diagnostics requires an assessment QC output and must never be used for FINAL')
    outputs=[x for x in [a.learning,a.assessment] if x is not None]
    if not outputs or len({a.input.resolve(),*(x.resolve() for x in outputs)})!=len(outputs)+1:
        raise ValueError('Input and both output paths must be different')
    for path,expected in [(a.learning,a.expected_learning_sha256),(a.assessment,a.expected_assessment_sha256)]:
        if path is not None and path.exists() and (not expected or sha(path.read_bytes())!=expected):
            raise ValueError('Both outputs must be preflighted before either is written')
    scope='both' if a.learning and a.assessment else ('learning' if a.learning else 'assessment')
    data=json.loads(a.input.read_text(encoding='utf-8-sig'));result=render(data,scope,qc_diagnostics=a.qc_diagnostics)
    if a.learning:save(a.learning,result['learning'],a.expected_learning_sha256)
    if a.assessment:save(a.assessment,result['assessment'],a.expected_assessment_sha256)
    print(json.dumps({'status':'QC_CONTENT_EXPORTED_AND_REREAD','input_sha256':sha(a.input.read_bytes()),
                      'learning_sha256':sha(a.learning.read_bytes()) if a.learning else None,
                      'assessment_sha256':sha(a.assessment.read_bytes()) if a.assessment else None,
                      'independent_review':'NOT_PERFORMED'},ensure_ascii=False))


if __name__=='__main__':main()
