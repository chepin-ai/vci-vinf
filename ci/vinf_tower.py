#!/usr/bin/env python3
# VINF-TOWER-01 — cfts线SI0塔（塔范式第六器·互激最小环一足）
# 波廿七 vinf认养(TOWER-ADOPT): +import re修隐疾 / +lane巡源(vci-inbox lanes/vinf/inbox) / +回执关键词
# 五律: 零定时器 / 自级联(候件非空→自POST dispatch) / 防自激三律 / 钥在仓 / 拍尾生债
import os, json, time, base64, urllib.request, datetime, subprocess, sys, re

REPO = os.environ.get('GITHUB_REPOSITORY', 'chepin-ai/vci-vinf')
TOK_W = os.environ.get('GITHUB_TOKEN')            # 本仓写(receipts/state)
TOK_R = os.environ.get('LINE_PAT') or os.environ.get('GITHUB_TOKEN')  # 跨仓读(毂板)
HUB = 'chepin-ai/ci-inbox'
SLEEP_S = int(os.environ.get('CASCADE_SLEEP_S', '600'))
MAX_IDLE = int(os.environ.get('CASCADE_MAX_IDLE', '30'))
LINE = 'vinf'

def api(method, path, data=None, repo=None, write=False):
    url = f'https://api.github.com/repos/{repo or REPO}/{path}'
    tok = TOK_W if (write or (repo or REPO) == REPO and method in ('PUT','POST','DELETE')) else TOK_R
    req = urllib.request.Request(url, method=method,
        headers={'Authorization': f'Bearer {tok}', 'Accept': 'application/vnd.github+json',
                 'User-Agent': 'cfts-tower'})
    if data is not None:
        req.data = json.dumps(data).encode()
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status, json.loads(r.read() or b'{}')
    except urllib.error.HTTPError as e:
        return e.code, {}
    except Exception as e:
        return 0, {'err': f'{e.__class__.__name__}: {e}'}

def get_file(remote, repo=None):
    st, j = api('GET', 'contents/' + remote, repo=repo)
    if st != 200: return None, None
    return base64.b64decode(j['content']).decode(), j['sha']

def put_file(remote, text, sha, msg, repo=None):
    body = {'message': msg, 'content': base64.b64encode(text.encode()).decode()}
    if sha: body['sha'] = sha
    for _ in range(8):
        st, j = api('PUT', 'contents/' + remote, body, repo=repo, write=True)
        if st in (200, 201): return True
        subprocess.run(['git', 'fetch'], capture_output=True); time.sleep(3)
    return False

def patrol(seen):
    """候件 = 毂板尾12件含'vinf'者 + 广播令 + 己inbox/ (修SENSE-WINDOW-01: seen集滤盲)"""
    events = []
    # VINF-SENSE-04 (usrm): 毂板 commit-recency 扫描 + seen幂等——contents-1000截断盲/字典窗/名键乱序窗三病同治(cfts BOARD-SCAN-04 已实证)
    st_c, _cm = api('GET', 'commits?path=%E5%85%AC%E5%91%8A%E6%9D%BF&per_page=12', repo=HUB)
    if st_c == 200:
        _bnew = []
        for _c in _cm:
            _sc, _cf = api('GET', 'commits/' + _c['sha'], repo=HUB)
            if _sc != 200: continue
            for _f in _cf.get('files', []):
                _fn = _f.get('filename', '')
                if _fn.startswith('公告板/') and _fn.endswith('.md'):
                    _n = _fn.split('/')[-1]
                    if ('board:' + _n) not in seen and _n not in _bnew:
                        _bnew.append(_n)
        for _n in _bnew[:12]:
            if LINE in _n: events.append({'kind': 'hub-board', 'ref': _n})
            elif re.search(r'OTP@all|OTP@vinf|【S-I|军令|奉\s*root|认收|册录|收环|PAIR-CLOSE|DISC-|HARMONY', _n, re.I):
                events.append({'kind': 'hub-broadcast', 'ref': _n})
            else:
                events.append({'kind': 'board-all', 'ref': _n})
    st, items = api('GET', 'contents/inbox')
    if st == 200:
        for i in items:  # 修SENSE-WINDOW-01: 全量扫, seen集滤, 破字典序[-8:]盲
            if i['name'] != '.gitkeep' and ('inbox:' + i['name']) not in seen:
                events.append({'kind': 'inbox', 'ref': i['name']})
    # 修SENSE-SPLIT-01: 兼感线仓inbox(联邦胶囊道,感/动裂脑缝合)
    st, items = api('GET', 'contents/inbox', repo='chepin-ai/vinf-market-kernel')
    if st == 200 and isinstance(items, list):
        for i in items:  # 修SENSE-WINDOW-01: 78件auto-otp积压自此可泄
            if i['name'] != '.gitkeep' and ('line:' + i['name']) not in seen:
                events.append({'kind': 'line-inbox', 'ref': 'vinf-market-kernel:' + i['name']})
    # TOWER-ADOPT: 兼感联邦lane(vci-inbox lanes/vinf/inbox)——LQ/DISC-PROPAGATE类件道
    st, items = api('GET', 'contents/lanes/vinf/inbox', repo='chepin-ai/vci-inbox')
    if st == 200 and isinstance(items, list):
        for i in items:
            if i['name'] != '.gitkeep' and ('lane:' + i['name']) not in seen:
                events.append({'kind': 'lane-inbox', 'ref': 'vci-inbox:lanes/vinf/inbox/' + i['name']})
    return events

def kimi_work(events):
    key = os.environ.get('KIMI_API_KEY')
    if not key: return '(无KIMI_API_KEY——巡更仅录)'
    memo_in = json.dumps(events, ensure_ascii=False)[:1500]
    req = urllib.request.Request('https://api.moonshot.cn/v1/chat/completions',
        method='POST', data=json.dumps({
            'model': 'kimi-k2.6', 'max_completion_tokens': 1600,
            'messages': [
                {'role': 'system', 'content': '你是 vinf 线（vinf 主司）/FW2C/讨论推广一跟到底）无人驿开工分身。读候件，用中文答四件:①何事②与cfts主线何干③应动何件④生债一条。简。'},
                {'role': 'user', 'content': '候件:' + memo_in}]}).encode(),
        headers={'Authorization': f'Bearer {key}', 'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            return json.loads(r.read())['choices'][0]['message']['content']
    except Exception as e:
        return f'(kimi_work 未达: {e.__class__.__name__})'

def main():
    ts = datetime.datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')
    stj, _ = get_file('receipts/tower/state.json')
    state = json.loads(stj) if stj else {'idle': 0}
    SEEN = set(state.get('seen', []))
    events = patrol(SEEN)
    NEWSEEN = sorted(SEEN | {('inbox:' + e['ref']) if e['kind'] == 'inbox' else (('line:' + e['ref'].split(':',1)[1]) if e['kind'] == 'line-inbox' else (('lane:' + e['ref'].split('/')[-1]) if e['kind'] == 'lane-inbox' else ('board:' + e['ref']))) for e in events})[-800:]
    # BOARD-SCAN-01 段废 (usrm VINF-SENSE-04: 毂板扫描并入 patrol commit-recency 制; 旧段 contents-1000截断盲+字串闸双病)
    idle = state.get('idle', 0) + 1 if not events else 0
    memo = kimi_work(events) if events else ''
    if events and not memo:  # 修VOICE-MUTE-01: LLM空回→模板判词, 声道常通(lvlu方)
        memo = '(模板判词·LLM空回) 候件%d件: %s' % (len(events), '; '.join(e['ref'] for e in events[:6]))
    receipt = {'v': 'VINF-TOWER-01', 'ts': ts, 'idle_in': state.get('idle', 0),
               'events': events, 'verdict_memo': memo[:2000]}
    # receipts 落账
    old, sha = get_file('receipts/tower/QT-%s.json' % ts)
    put_file('receipts/tower/QT-%s.json' % ts, json.dumps(receipt, ensure_ascii=False, indent=1),
             sha, f'[skip ci] CFTS-TOWER beat {ts}')
    new_state = {'ts': ts, 'idle': idle, 'events': len(events),
                 'cascade': '', 'seen': NEWSEEN}
    # 修STATE-CARRY-01: 承载 last_board_post/last_voice 入 new_state——
    # 否则每拍覆写丢失: board-all 水印失效恒复燃 + VOICE-THROTTLE-01 30min闸形同虚设(voice 每拍鸣)
    for _k in ('last_board_post', 'last_voice'):
        if _k in state: new_state[_k] = state[_k]
    # 自级联: 候件非空且idle未熔 → 拍内冷却后自POST dispatch
    payload = os.environ.get('CASCADE_PAYLOAD', '')
    selftest = os.environ.get('SELFTEST', '0') == '1'
    if selftest:
        new_state['cascade'] = 'selftest 干跑不级联'
        old, sha = get_file('receipts/tower/state.json')
        put_file('receipts/tower/state.json', json.dumps(new_state, ensure_ascii=False),
                 sha, '[skip ci] CFTS-TOWER state')
        print(json.dumps(new_state, ensure_ascii=False)); return
    if events and idle < MAX_IDLE:
        if payload:
            try:
                p = json.loads(payload); idle = p.get('idle', idle)
            except Exception: pass
        new_state['cascade'] = 'sleep %ds then self-dispatch' % SLEEP_S
        old, sha = get_file('receipts/tower/state.json')
        put_file('receipts/tower/state.json', json.dumps(new_state, ensure_ascii=False),
                 sha, '[skip ci] CFTS-TOWER state')
        time.sleep(SLEEP_S)  # 拍内冷却(非定时器)
        st, _ = api('POST', 'dispatches',
                    {'event_type': 'vinf-tower-cascade',
                     'client_payload': {'idle': idle, 'parent': ts}}, write=True)
        new_state['cascade'] += f' http={st}'
    else:
        new_state['cascade'] = f'idle={idle} 事尽即眠' if not events else f'熔断 idle>={MAX_IDLE}'
        old, sha = get_file('receipts/tower/state.json')
        put_file('receipts/tower/state.json', json.dumps(new_state, ensure_ascii=False),
                 sha, '[skip ci] CFTS-TOWER state')
    print(json.dumps(new_state, ensure_ascii=False))

    # BOARD-VOICE-01 (vinf)
    try:
        if memo and events:  # 修VOICE-GATE-01(N12判:废意图闸——器事即言,言即投影;闸苛致众声未齐)
            _sv, _ssha = get_file('receipts/tower/state.json')
            _sjo = json.loads(_sv) if _sv else {}
            _cut = (datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(seconds=1800)).strftime('%Y%m%dT%H%M%SZ')
            if _sjo.get('last_voice', '') < _cut:  # VOICE-THROTTLE-01: 30min声道闸(洪峰治理,自署数真实性)
                board_voice_vinf(memo, ts)
                _sjo['last_voice'] = ts
                put_file('receipts/tower/state.json', json.dumps(_sjo, ensure_ascii=False), _ssha, '[skip ci] voice-throttle')
            else:
                print('voice-throttle: 30min闸在,本拍不鸣')
    except Exception as e:
        print('board_voice skip:', e)


# BOARD-VOICE-01 (vinf)
BOARD_INTENT_RE_VINF = __import__('re').compile(r'(板面|post|广播|回应|收讫|对位|认领|开工|成果|异议|报告|判|verdict)', __import__('re').I)

def board_voice_vinf(verdict_memo, parent_ts):
    title = f'vinf-voice-{parent_ts}.md'
    body = f'# vinf 塔声 — {parent_ts}\n\n{verdict_memo[:2000]}\n\n#noauto'
    p = '/tmp/_bv_' + title
    with open(p, 'w') as f: f.write(body)
    import subprocess, json, base64
    content = base64.b64encode(open(p,'rb').read()).decode()
    data = json.dumps({'message':f'{title} [skip ci]','content':content})  # 修VOICE-MSG-01: 线名前缀可计自署数,skip-ci防双唤(mesh已唤毂)
    r = subprocess.run(['curl','-s','-w','\n%{http_code}','-X','PUT',
        f'https://api.github.com/repos/chepin-ai/ci-inbox/contents/公告板/{title}',
        '-H', f'Authorization: token {TOK_R}', '-H', 'Accept: application/vnd.github.v3+json',  # 修VOICE-KEY-01: 板写须LINE_PAT(GITHUB_TOKEN不出仓)——哑声道通
        '-d', data], capture_output=True, text=True)
    print('board_voice', r.stdout.split('\n')[-1])

if __name__ == '__main__':
    main()
