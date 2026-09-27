import sys, json
sys.argv=['x']
import make_manuscript as mm
data = mm.main('learning')
import check_learning_content as c
for s in data['sentences']:
    try:
        c.glossary(s, {w['id'] for u in data['units'] for w in u['today_words']}, require_reading_checks=True)
    except Exception as e:
        print(s['id'], type(e).__name__, e)
try:
    r=c.check(data, scope='learning'); print(r['status'])
except Exception as e:
    import traceback; traceback.print_exc(limit=-3)
