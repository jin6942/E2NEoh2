"""Compact, read-only R preparation. Reuse canonical checks; never certify R.

PDF extraction is diagnostic, not a proof of visual equivalence. Unexpected
fonts are inventoried, not forbidden; extracted characters may differ from
visible glyphs. Every diagnostic needs an actual review disposition.
"""
import argparse
from copy import deepcopy
from ctypes import byref, c_int, create_string_buffer
import hashlib
import json
from pathlib import Path
import re
from zipfile import ZipFile, BadZipFile

from lxml import etree
from book_plan import compile_plan
from check_book import check as check_book
from check_saved_docx import check as check_saved, expected_element
from export_handoff import render


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def compact(text):
    # For PDF diagnostics only. The canonical DOCX/FINAL checks remain exact.
    # Word may omit the invisible joiners of the approved key marker in PDF text.
    # Do not erase arbitrary format controls or change any visible characters.
    text = re.sub(r'\s+', '', text.replace('\u00a0', ' '))
    return text.replace('★\ufeff핵\ufeff심', '★핵심')


def footer_patterns(docx):
    """Recognize footer text from actual Word footer XML, including PAGE fields.

    Match near the physical page foot only. No blanket coordinate crop, generic
    digit deletion, or removal of words such as 'answer' anywhere in the body.
    Unsupported field structures simply remain as PDF differences.
    """
    ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    patterns=[]
    with ZipFile(docx) as archive:
        for name in archive.namelist():
            if not re.fullmatch(r'word/footer\d+\.xml',name):
                continue
            root=etree.fromstring(archive.read(name))
            for para in root.findall('.//w:p',ns):
                pieces=[];field=False;page=False;result=False
                for node in para.iter():
                    tag=etree.QName(node).localname
                    if tag=='fldChar':
                        state=node.get('{'+ns['w']+'}fldCharType')
                        if state=='begin':field=True;page=False;result=False
                        elif state=='separate':result=True
                        elif state=='end':field=False;page=False;result=False
                    elif tag=='instrText' and field:
                        page=bool(re.fullmatch(r'\s*PAGE\s*(?:\\\*\s*MERGEFORMAT\s*)?',node.text or '',re.I))
                        if page:pieces.append(r'\d+')
                    elif tag=='t' and not (field and result and page):
                        pieces.append(re.escape(compact(node.text or '')))
                pattern=''.join(pieces)
                # Never exclude a bare page digit; a sufficiently specific
                # literal footer must accompany a PAGE field.
                if len(re.sub(r'\\d\+', '',pattern))>=3:
                    patterns.append(pattern)
    return patterns


def remove_known_footers(chars, patterns, height):
    """chars are (unicode, box), with PDF bottom-origin coordinates."""
    indices=[i for i,(ch,box) in enumerate(chars) if ch and not ch.isspace()]
    visible=''.join(chars[i][0] for i in indices)
    removed=set()
    for pattern in patterns:
        for match in re.finditer(pattern,visible):
            span=indices[match.start():match.end()]
            if span and all(chars[i][1] is not None and chars[i][1][3]<height*.08 for i in span):
                removed.update(span)
    return ''.join(ch for i,(ch,box) in enumerate(chars) if i not in removed)


def marker_following_prefixes(docx):
    # Standalone answer symbols at the end of a Word paragraph have no word
    # to bind. Only inspect combinations that actually occur in one paragraph.
    ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    result={ch:set() for ch in '★①②③④⑤'}
    with ZipFile(docx) as archive:
        root=etree.fromstring(archive.read('word/document.xml'))
        for para in root.findall('.//w:p',ns):
            text=''.join(para.xpath('.//w:t/text()',namespaces=ns))
            text=text.replace('★\ufeff핵\ufeff심','★핵심')
            for match in re.finditer(r'([★①②③④⑤])\s*(\S+)',text):
                result[match[1]].add(compact(match[2])[:16])
    return result


def marker_breaks(chars, following_prefixes=None):
    issues=[]
    for i,(ch,box) in enumerate(chars):
        if ch not in '★①②③④⑤' or not box:
            continue
        if following_prefixes is not None:
            tail=compact(''.join(c for c,b in chars[i:i+100]))[1:]
            if not any(tail.startswith(prefix) for prefix in following_prefixes.get(ch,set())):
                continue
        joined_key=''.join(c for c,b in chars[i:i+5])=='★\ufeff핵\ufeff심'
        following=next(((c,b,j) for j,(c,b) in enumerate(chars[i+1:],i+1)
                        if c and not c.isspace() and b and not (joined_key and j==i+1)),None)
        if following and abs((box[1]+box[3])-(following[1][1]+following[1][3]))/2>max(3,box[3]-box[1]):
            issues.append({'marker':ch,'character_index':i,'next_character':following[0],
                           'next_character_index':following[2],'marker_box':list(box),'next_box':list(following[1])})
    return issues


def inspect_pdf(pdf, docx):
    import pypdfium2 as pdfium
    import pypdfium2.raw as raw
    patterns=footer_patterns(docx);prefixes=marker_following_prefixes(docx);pages=[];texts=[];fonts=set()
    document=pdfium.PdfDocument(str(pdf))
    try:
        for number in range(len(document)):
            page=document[number];tp=page.get_textpage()
            try:
                chars=[];page_fonts=set()
                for i in range(tp.count_chars()):
                    value=raw.FPDFText_GetUnicode(tp,i)
                    ch=chr(value) if value else '\ufffd'
                    try:box=tp.get_charbox(i)
                    except Exception:box=None
                    chars.append((ch,box))
                    flags=c_int();size=raw.FPDFText_GetFontInfo(tp,i,None,0,byref(flags))
                    if size:
                        buffer=create_string_buffer(size)
                        raw.FPDFText_GetFontInfo(tp,i,buffer,size,byref(flags))
                        page_fonts.add(buffer.value.decode('utf-8',errors='replace'))
                fonts.update(page_fonts)
                texts.append(remove_known_footers(chars,patterns,page.get_size()[1]))
                pages.append({'page':number+1,'characters':len(chars),'fonts':sorted(page_fonts),
                              'marker_break_candidates':marker_breaks(chars,prefixes)})
            finally:tp.close();page.close()
    finally:document.close()
    return {'pages':pages,'fonts':sorted(fonts),'text':''.join(texts),
            'footer_policy':'Only actual DOCX footer patterns near page foot excluded; no body crop'}


def plan_text(plan):
    values=[]
    for block in plan['blocks']:
        for item in block['elements']:
            value=expected_element(item)
            # Preserve saved DOCX table row/cell/paragraph reading order.
            def flatten(v):
                if isinstance(v,str):return v
                return ''.join(flatten(x) for x in v)
            values.append(value['text'] if value['kind']=='paragraph' else flatten(value['rows']))
    return ''.join(values)


def check_files(manuscript, plan, docx, pdf, learning_final, assessment_final):
    paths={k:Path(v) for k,v in locals().copy().items()}
    blobs={k:p.read_bytes() for k,p in paths.items()}
    bindings={k+'_sha256':sha(raw) for k,raw in blobs.items()}
    from verify_release import package_inventory
    bindings['package_sha256']=package_inventory(Path(__file__).resolve().parent.parent)['sha256']
    data=json.loads(blobs['manuscript'].decode('utf-8-sig'))
    given=json.loads(blobs['plan'].decode('utf-8-sig'))
    errors=[];warnings=[]
    def warn(code,detail):warnings.append({'id':f'R-{len(warnings)+1:04d}','code':code,'detail':detail})
    try:
        structure=check_book(data)
        if structure.get('status')!='STRUCTURE_PASS':
            errors.append({'code':'STRUCTURE','detail':structure.get('errors',[])})
        fresh=compile_plan(data);old=deepcopy(given)
        for value in (fresh,old):value.pop('input_sha256',None)
        if old!=fresh:errors.append({'code':'PLAN_MISMATCH','detail':'Current canonical plan differs'})
        handoffs=render(data)
        for name in ('learning','assessment'):
            if blobs[name+'_final'].decode('utf-8-sig')!=handoffs[name]:
                errors.append({'code':'FINAL_MISMATCH','detail':name})
        saved=check_saved(given,paths['docx'],'full',assets=Path(__file__).resolve().parent.parent/'assets')
        if saved.get('status')!='SAVED_CONTENT_MATCH' or saved.get('format_errors'):
            errors.append({'code':'SAVED_DOCX','detail':saved.get('errors',[]),'format_errors':saved.get('format_errors',[])})
    except (ValueError,KeyError,TypeError,AttributeError,BadZipFile) as exc:
        errors.append({'code':'CANONICAL_CHECK','detail':str(exc)})
    pdf_report={}
    try:
        pdf_report=inspect_pdf(paths['pdf'],paths['docx'])
        observed=pdf_report.pop('text')
        expected=plan_text(given)
        a,b=compact(expected),compact(observed)
        pdf_report['normalized_text_equal']=a==b
        pdf_report['normalization']='Whitespace including NBSP and invisible joiners in the exact approved ★핵심 marker only; no spelling, glyph or punctuation substitutions'
        pdf_report['expected_characters']=len(a);pdf_report['observed_characters']=len(b)
        if not a or a!=b:
            at=next((i for i,(x,y) in enumerate(zip(a,b)) if x!=y),min(len(a),len(b)))
            warn('PDF_TEXT_DIFFERENCE',{'first_difference':at,'expected':a[max(0,at-35):at+65],
                 'observed':b[max(0,at-35):at+65],'action':'Inspect actual pages; extraction order/glyphs are not visual proof'})
        for row in pdf_report['pages']:
            if row['marker_break_candidates']:warn('PDF_MARKER_BREAK',row)
    except Exception as exc:
        warn('PDF_EXTRACTION_UNVERIFIED',str(exc))
    for block in given.get('blocks',[]):
        for item in block.get('elements',[]):
            text=plan_text({'blocks':[{'elements':[item]}]})
            if re.search(r'\b(?:TODO|TBD|lorem)\b|추후|예시',text,re.I):
                warn('PLACEHOLDER_CANDIDATE',{'block':block.get('id'),'role':item.get('role'),'text':text[:180]})
            if (re.fullmatch(r'(?:mock|workbook)_question_(?:prompt(?:_spaced)?|passage|choice)',item.get('role',''))
                    or item.get('role') in {'given_box','mock_summary_spaced'}) and re.search(r'정답|해설|오답 정리',text):
                warn('STUDENT_ANSWER_TEXT_CANDIDATE',{'block':block.get('id'),'role':item.get('role'),'text':text[:180]})
    return {'schema_version':1,'type':'release_text_preflight','status':'NOT_CERTIFIED',
            'bindings':bindings,'machine_status':'FAIL' if errors else 'PASS','errors':errors,'warnings':warnings,
            'pdf':pdf_report,'independent_review':'NOT_PERFORMED','visual_review':'NOT_PERFORMED',
            'limits':['No automatic source/answer/font edits; R and J/K must resolve diagnostics on actual files.',
                      'Text equivalence does not prove pagination, clipping, translation or answer validity.']}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    for name in ('manuscript','plan','docx','pdf','learning_final','assessment_final','output'):
        parser.add_argument(name,type=Path)
    args=vars(parser.parse_args());output=args.pop('output')
    if output.resolve() in {p.resolve() for p in args.values()} or output.exists():
        raise ValueError('Use a new report path, never an input or existing file')
    result=check_files(**args)
    raw=(json.dumps(result,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
    with output.open('xb') as stream:stream.write(raw)
    if output.read_bytes()!=raw:raise ValueError('Report reread differs')
    print(json.dumps({'status':result['status'],'machine_status':result['machine_status'],
                      'warnings':len(result['warnings'])},ensure_ascii=False))
    return 1 if result['errors'] else 0


if __name__=='__main__':raise SystemExit(main())
