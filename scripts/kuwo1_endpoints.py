#!/usr/bin/env python3
# KUWO-1：端点素材——mod 全 dex URL/域名常量集 − 官方基线 URL 常量集 = 差集清单
# 红线：双侧同集合基准（mod 全部 smali vs base 全部 smali），排除 hg2 式基线定义漂移。
# 重点嫌疑 api.ktvdaren.com 输出引用类 + 每处引用的上下文（前后各 8 行）。
# 输入：work/smali-mod/ work/smali-base/
# 输出：work/diff-out/docs/kuwo1-endpoints.md + work/ep-diff-urls.txt
import os, re, sys
from collections import defaultdict

work = sys.argv[1]
MOD = os.path.join(work, 'smali-mod')
BASE = os.path.join(work, 'smali-base')
OUT = os.path.join(work, 'diff-out', 'docs', 'kuwo1-endpoints.md')
os.makedirs(os.path.dirname(OUT), exist_ok=True)

STR_RE = re.compile(r'^\s*const-string(?:/16|/jumbo)?\s+v\d+,\s*"((?:[^"\\]|\\.)*)"\s*$')
URL_RE = re.compile(r'https?://[a-zA-Z0-9_\-./:%~#?&=]+')
DOM_RE = re.compile(r'\b[a-zA-Z0-9][a-zA-Z0-9\-]{0,60}(?:\.[a-zA-Z0-9][a-zA-Z0-9\-]{0,60})+\.[a-zA-Z]{2,}\b')
# 官方/常见基础设施域（kuwo/酷狗/腾讯系 CDN 与常规库域名），差集报告中单列信息区不参与"新增可疑"排序
OFFICIAL_DOM = re.compile(r'(?:kuwo\.cn|kugou\.com|kgimg\.com|tdwxk\.com|kuwo\.vip|qq\.com|qlogo\.cn|gtimg\.com|gtimg\.cn|idqqimg\.com|weixin\.qq\.com|gtags\.net)$', re.I)
NOISE_DOM = re.compile(r'\.(?:xml|w3\.org|apache\.org|purl\.org|json-schema\.org|slf4j\.org|javase|java\.oracle|android\.com|gnu\.org|mozilla\.org|example|localhost|githubusercontent|schema)$', re.I)

def norm_url(u):
    return u.rstrip('./:').lower()

def scan(path):
    """返回 (urls set, doms set)，doms 仅从非 URL 字符串提取（对齐 hg1 口径）。"""
    urls, doms = set(), set()
    with open(path, encoding='utf-8', errors='replace') as f:
        for line in f:
            m = STR_RE.match(line.rstrip('\n'))
            if not m:
                continue
            s = m.group(1)
            found = set(norm_url(u) for u in URL_RE.findall(s))
            found = {u for u in found if not NOISE_DOM.search(u.split('://')[-1].split('/')[0] if '://' in u else u)}
            urls |= found
            if not found:
                for d in DOM_RE.findall(s):
                    d = d.lower().strip('.')
                    if NOISE_DOM.search(d) or d[0].isdigit():
                        continue
                    doms.add(d)
    return urls, doms

def walk_collect(root):
    url_by_class, dom_by_class = defaultdict(set), defaultdict(set)
    for droot, _, fs in os.walk(root):
        for f in fs:
            if not f.endswith('.smali'):
                continue
            abs_p = os.path.join(droot, f)
            rel = os.path.relpath(abs_p, root).split(os.sep)
            key = '/'.join(rel[1:]) if len(rel) > 1 else rel[0]
            u, d = scan(abs_p)
            if u: url_by_class[key] |= u
            if d: dom_by_class[key] |= d
    return url_by_class, dom_by_class

mod_urls, mod_doms = walk_collect(MOD)
base_urls, base_dom_set = walk_collect(BASE)

new_urls = {u for u in set(mod_urls) - set(base_urls)}
new_doms = {d for d in set(mod_doms) - set(base_dom_set)}
gone_urls = sorted(set(base_urls) - set(mod_urls))

# 差集 URL 的引用类（url_by_class 是 class->urls，反转为 url->classes）
url2cls = defaultdict(set)
for k, us in mod_urls.items():
    for u in us:
        if u in new_urls:
            url2cls[u].add(k)
dom2cls = defaultdict(set)
for k, ds in mod_doms.items():
    for d in ds:
        if d in new_doms:
            dom2cls[d].add(k)

# 官方域内新增 URL（升级信息项） vs 非官方域新增（重点区）
sus_urls = sorted(u for u in new_urls if not OFFICIAL_DOM.search(u.split('://')[-1].split('/')[0]))
off_urls = sorted(set(new_urls) - set(sus_urls))
sus_doms = sorted(d for d in new_doms if not OFFICIAL_DOM.search(d))
off_doms = sorted(set(new_doms) - set(sus_doms))

FOCUS = 'ktvdaren'
focus_ctx = []
for droot, _, fs in os.walk(MOD):
    for f in fs:
        if not f.endswith('.smali'):
            continue
        abs_p = os.path.join(droot, f)
        rel = os.path.relpath(abs_p, MOD)
        with open(abs_p, encoding='utf-8', errors='replace') as fh:
            lines = fh.readlines()
        for i, line in enumerate(lines):
            if FOCUS in line:
                ctx = ''.join(lines[max(0, i-8):min(len(lines), i+9)])
                focus_ctx.append((rel, i+1, line.strip(), ctx))

report = ['# KUWO-1 端点素材（mod 全 dex URL 常量集 − 官方基线 URL 常量集）', '',
          '> 集合口径红线：双侧同为全量 classes*.dex 反编译后 const-string 提取，同 regex 同过滤。',
          '> 本表只是素材清单，定性判定权在老马。', '',
          '## 1. 差集总览', '',
          f'- mod URL 常量: {sum(len(v) for v in mod_urls.values())} 处 / 去重 {len(mod_urls)} 个',
          f'- base URL 常量: {sum(len(v) for v in base_urls.values())} 处 / 去重 {len(base_urls)} 个',
          f'- **新增 URL（mod 有 base 无）: {len(new_urls)} 个**（非官方域 {len(sus_urls)} + 官方域 {len(off_urls)}）',
          f'- 基线 URL 在 mod 消失: {len(gone_urls)} 个',
          f'- **新增裸域名（非 URL 字符串）: {len(new_doms)} 个**（非官方 {len(sus_doms)}）', '',
          '## 2. 新增 URL —— 非官方域嫌疑区（重点素材）', '',
          '| URL | 引用类 |', '|---|---|']
for u in sus_urls:
    cls = ', '.join(f'`{c}`' for c in sorted(url2cls[u])) or '(未定位)'
    report.append(f'| `{u}` | {cls} |')
report += ['', '## 3. 新增 URL —— 官方域（信息项）', '']
for u in off_urls:
    report.append(f'- `{u}`')
report += ['', '## 4. 新增裸域名 —— 非官方域（重点素材）', '']
for d in sus_doms:
    cls = ', '.join(f'`{c}`' for c in sorted(dom2cls[d])) or '(未定位)'
    report.append(f'- `{d}` — 引用: {cls}')
report += ['', '## 5. 基线 URL 在 mod 中消失清单（信息项）', '']
for u in gone_urls:
    report.append(f'- `{u}`')
report += ['', f'## 6. 头号嫌疑 api.ktvdaren.com 引用上下文（老马初扫 2 次命中）', '']
if not focus_ctx:
    report.append('（本轮 smali 扫描未命中，注意：可能来自字符串解码/native 层，需另线索）')
for rel, ln, hit, ctx in focus_ctx:
    report += [f'### `{rel}` L{ln}', '```smali', ctx.rstrip(), '```', '']
with open(OUT, 'w', encoding='utf-8') as f:
    f.write('\n'.join(report) + '\n')

with open(os.path.join(work, 'ep-diff-urls.txt'), 'w', encoding='utf-8') as f:
    f.write('\n'.join(sorted(new_urls)) + '\n')

print(f'KUWO1-EP new_urls={len(new_urls)}(sus={len(sus_urls)}) gone={len(gone_urls)} new_doms={len(new_doms)}(sus={len(sus_doms)}) focus_hits={len(focus_ctx)}')
