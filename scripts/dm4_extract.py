#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""DM-1 W4：东明版酷我 12.2.2.0 作者自有类（DM-0 实锤 90 类）八组提取 + 网络命中面自动专节。

输入（由 workflow dm-author-code-decompile 产出）：
  work/jdx/out{9,16,17,18}/sources/    jadx 单 dex 反编译产物（--no-imports：全限定包名）
输出（work/dm-out/）：
  java/<组名>/**                        作者类 Java 全文（打包 dm4-author-java.tar.gz 走 Release）
  dm4-groups.json                       每组统计（files/lines/net_hits/highlight 摘要）
  dm4-author-code.md                    报告（总表 + 每组清单/方法表/命中表/重点点名）
口径纪律：
  * 只陈述「该方法在此类、该正则在此行命中」级事实，不判 A/B/C/D、不做安全定性；
  * 缺组 = FATAL 立即 exit 1（作者类必须都在，防反编译静默失败留白）；
  * 收口只打一行 [dm4] groups=8 ...，workflow 门以该 marker 判定（FATAL 消息不带 marker）。
"""
import json
import os
import re
import shutil
import sys

WORK = sys.argv[1] if len(sys.argv) > 1 else 'work'
JDX = os.path.join(WORK, 'jdx')
OUT = os.path.join(WORK, 'dm-out')
JAVA_OUT = os.path.join(OUT, 'java')

# (组名, out 序号=classesN.dex, sources 相对路径前缀) —— DM-0 实锤分布
GROUPS = [
    ('G1_com_dm_dia', 18, 'com/dm/dia'),
    ('G2_com_vip_yf', 17, 'com/vip/yf'),
    ('G3_com_kw_cj', 17, 'com/kw/cj'),
    ('G4_njggg', 17, 'njggg'),
    ('G5_abcdefgaaa', 18, 'abcdefgaaa'),
    ('G6_kwpass', 17, 'kwpass'),
    ('G7_rj_lddne', 9, 'rj/lddne'),
    ('G8_nt_phkc', 16, 'nt/phkc'),
]

# 网络/反射/设备指纹/加解密面正则口径（派单 W4 给定，命中=仅此口径）
NET_RE = re.compile(
    r'https?://|okhttp|HttpURL|URLConnection|openConnection|java\.net|Socket|'
    r'DatagramChannel|InputStreamReader|getAssets|AssetManager|WebView|loadUrl|'
    r'System\.load|loadLibrary|Runtime\.getRuntime|ProcessBuilder|\bexec\(|'
    r'getSharedPreferences|SQLite|ContentResolver|ContentProvider|Uri\.|download|Download|'
    r'registerReceiver|PackageManager|telephony|getDeviceId|ANDROID_ID|Build\.MODEL|'
    r'base64|Base64|Cipher|SecretKey|MessageDigest|MD5|SHA')
MOD_RE = re.compile(r'^\s*(public|private|protected|static|final|synchronized|native|abstract|default)\b')
NATIVE_RE = re.compile(r'\bnative\b')
LOADLIB_RE = re.compile(r'loadLibrary\s*\(\s*"([^"]+)"|System\.load\s*\(\s*"([^"]+)"')
STR_RE = re.compile(r'"([^"\\\n]{3,120})"')
PROV_RE = re.compile(r'\b(?:public|protected)\b[^;{]*\b(?:query|insert|update|delete|call|getType)\s*\(')
G1V_TOKENS = ('attachBaseContext', 'onCreate')
G1O_TOKENS = ('sPendingDownloadUrl', 'MAX_REQUESTS_PER_HOUR', 'KEY_REQUEST_WINDOW_START', 'UpdateCheckCallback')

# md 展示上限（超出显式标注截断，计数以 json 全量为准）
CAP_METHODS = 250
CAP_HITS = 400
CAP_HL = 120
CAP_STRINGS = 60


def clip(s, n):
    s = s.strip()
    return s if len(s) <= n else s[: n - 1] + '…'


def esc(s):
    """md 表格单元转义。"""
    return s.replace('|', '\\|').replace('\n', ' ')


def list_group_files(name, n, prefix):
    """返回 (src_root, [绝对路径])；不复制，供缺组先行判定。"""
    src_root = os.path.join(JDX, 'out%d' % n, 'sources')
    grp_root = os.path.join(src_root, *prefix.split('/'))
    files = []
    if os.path.isdir(grp_root):
        for dirpath, _dirs, fnames in os.walk(grp_root):
            for fn in fnames:
                if fn.endswith('.java'):
                    files.append(os.path.join(dirpath, fn))
    return src_root, sorted(files)


def scan_file(fp, rel):
    try:
        with open(fp, 'r', encoding='utf-8', errors='replace') as f:
            lines = f.read().splitlines()
    except OSError as e:
        print('WARN: 读取失败 %s: %s' % (rel, e))
        lines = []
    rec = {'rel': rel.replace(os.sep, '/'), 'lines': len(lines),
           'hits': [], 'methods': [], 'natives': [], 'loadlibs': [],
           'strs': [], 'provs': []}
    for i, ln in enumerate(lines, 1):
        if NET_RE.search(ln):
            rec['hits'].append([i, clip(ln, 160)])
        st = ln.strip()
        if not st or st.startswith('*') or st.startswith('//'):
            continue
        if MOD_RE.search(ln) and ('(' in ln or st.endswith(';')):
            rec['methods'].append([i, clip(ln, 120)])
        if NATIVE_RE.search(ln) and '(' in ln:
            rec['natives'].append([i, clip(ln, 120)])
        m = LOADLIB_RE.search(ln)
        if m:
            rec['loadlibs'].append([i, clip(ln, 140), m.group(1) or m.group(2) or ''])
        if PROV_RE.search(ln):
            rec['provs'].append([i, clip(ln, 140)])
        if len(rec['strs']) < 400:
            for s in STR_RE.findall(ln):
                if len(s) >= 4:
                    rec['strs'].append(clip(s, 120))
                    if len(rec['strs']) >= 400:
                        break
    return rec


def build_highlights(gname, files):
    """组内重点点名（专节内高亮，若存在）。返回 {label: [ {file, entries:[[lineno,text],...] } ]}"""
    hl = {}
    def _pick(files, pred):
        return [f for f in files if pred(f)]

    if gname == 'G1_com_dm_dia':
        v = _pick(files, lambda f: os.path.basename(f['rel']) == 'v.java')
        hl['v.java attachBaseContext/onCreate'] = [
            {'file': f['rel'], 'entries': [[i, t] for i, t in f['methods']
                                           if any(tok in t for tok in G1V_TOKENS)]}
            for f in v]
        o = _pick(files, lambda f: os.path.basename(f['rel']) == 'o.java')
        hl['o.java UpdateCheckCallback 关键字段/方法'] = [
            {'file': f['rel'], 'entries': [[i, t] for i, t in f['methods']
                                           if any(tok in t for tok in G1O_TOKENS)]}
            for f in o]
    elif gname == 'G2_com_vip_yf':
        js = _pick(files, lambda f: os.path.basename(f['rel']).startswith('Json'))
        hl['JsonUtils/JsonModifiers 类清单+modifier 字符串常量'] = [
            {'file': f['rel'], 'entries':
                [['- 方法', '; '.join(t for _i, t in f['methods'][:CAP_HL]) or '(无)'],
                 ['- 字符串常量', '; '.join(sorted(set(f['strs']))[:CAP_STRINGS]) or '(无)']]}
            for f in js]
    elif gname == 'G7_rj_lddne':
        pv = _pick(files, lambda f: bool(f['provs']))
        hl['provider query/insert/update/delete/call/getType'] = [
            {'file': f['rel'], 'entries': f['provs']} for f in pv]
    elif gname in ('G4_njggg', 'G5_abcdefgaaa', 'G6_kwpass'):
        ll = _pick(files, lambda f: bool(f['loadlibs']))
        nt = _pick(files, lambda f: bool(f['natives']))
        hl['loadLibrary 调用'] = [{'file': f['rel'], 'entries': f['loadlibs']} for f in ll]
        hl['native 方法声明'] = [{'file': f['rel'], 'entries': f['natives']} for f in nt]
    else:
        # 其余组通用：native 声明 + loadLibrary（存在才列）
        nt = _pick(files, lambda f: bool(f['natives'] or f['loadlibs']))
        hl['native 声明/loadLibrary（通用点名）'] = [
            {'file': f['rel'], 'entries': f['loadlibs'] + f['natives']} for f in nt]
    return {k: v for k, v in hl.items() if v is not None}


def main():
    os.makedirs(OUT, exist_ok=True)
    if os.path.isdir(JAVA_OUT):
        shutil.rmtree(JAVA_OUT)

    # 第一遍：定位八组文件，缺组 = FATAL（防反编译静默失败留白）
    plan = []
    missing = []
    for gname, n, prefix in GROUPS:
        src_root, files = list_group_files(gname, n, prefix)
        if not files:
            missing.append('%s (out%d/sources/%s)' % (gname, n, prefix))
        plan.append((gname, n, prefix, src_root, files))
    if missing:
        print('DM4-FATAL 缺组（jadx 产物中无该组 java，作者类必须都在）: %s' % '; '.join(missing))
        sys.exit(1)

    groups = []
    for gname, n, prefix, src_root, files in plan:
        recs = []
        for fp in files:
            rel = os.path.relpath(fp, src_root)
            dst = os.path.join(JAVA_OUT, gname, rel)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copyfile(fp, dst)
            recs.append(scan_file(fp, rel))
        hl = build_highlights(gname, recs)
        groups.append({
            'name': gname, 'out': n, 'dex': 'classes%d.dex' % n, 'prefix': prefix,
            'files': recs,
            'n_files': len(recs),
            'n_lines': sum(r['lines'] for r in recs),
            'n_hits': sum(len(r['hits']) for r in recs),
            'n_methods': sum(len(r['methods']) for r in recs),
            'highlight': hl,
        })

    # dm4-groups.json（每组 files/lines/net_hits/highlight 摘要——摘要=计数+首 30 条样例行）
    js = {'generated_by': 'scripts/dm4_extract.py (DM-1 W4)',
          'net_regex': '派单 W4 给定口径（URL/okhttp/java.net/Socket/loadLibrary/WebView/'
                       'SharedPreferences/ContentProvider/telephony/Base64/Cipher/MD5/SHA 等）',
          'groups': [], 'totals': {}}
    for g in groups:
        hs = {}
        for label, items in g['highlight'].items():
            hs[label] = {'files': len(items),
                         'sample': [{'file': it['file'], 'entries': it['entries'][:30]} for it in items[:10]]}
        js['groups'].append({'name': g['name'], 'dex': g['dex'], 'prefix': g['prefix'],
                             'files': g['n_files'], 'lines': g['n_lines'],
                             'net_hits': g['n_hits'], 'method_decls': g['n_methods'],
                             'highlight': hs})
    T_FILES = sum(g['n_files'] for g in groups)
    T_LINES = sum(g['n_lines'] for g in groups)
    T_HITS = sum(g['n_hits'] for g in groups)
    js['totals'] = {'groups': len(groups), 'files': T_FILES, 'lines': T_LINES, 'net_hits': T_HITS}
    with open(os.path.join(OUT, 'dm4-groups.json'), 'w', encoding='utf-8') as f:
        json.dump(js, f, ensure_ascii=False, indent=1)

    # 报告 md
    md = []
    md.append('# DM-1 W4：东明版作者自有类反编译八组汇总（jadx，CI 自动产物）')
    md.append('')
    md.append('- 样本：dongming-kuwo-12.2.2.0.apk（sha256 50251119906266d50b872af8de4372c95b40548e175630b85af918e985d43588）')
    md.append('- 反编译：jadx --no-res --no-debug-info --no-imports --show-bad-code，单 dex 直喂 classes9/16/17/18.dex')
    md.append('- 口径：仅陈述「该方法在此类、该正则在此行命中」级事实；**不判 A/B/C/D、不做安全定性**。')
    md.append('- 网络面命中口径 = 派单给定正则（URL/okhttp/java.net/Socket/loadLibrary/WebView/getAssets/'
              'SharedPreferences/SQLite/ContentProvider·Resolver/telephony/getDeviceId/ANDROID_ID/Build.MODEL/'
              'Base64/Cipher/SecretKey/MessageDigest/MD5/SHA 等），命中=仅此正则，非仅此正则即无风险。')
    md.append('')
    md.append('## 总表')
    md.append('')
    md.append('| 组 | 源 dex | 路径前缀 | 文件数 | 行数 | 方法/字段声明 | 网络面命中 |')
    md.append('|---|---|---|---:|---:|---:|---:|')
    for g in groups:
        md.append('| %s | %s | %s | %d | %d | %d | %d |' % (
            g['name'], g['dex'], g['prefix'], g['n_files'], g['n_lines'], g['n_methods'], g['n_hits']))
    md.append('| **合计** | | | **%d** | **%d** | | **%d** |' % (T_FILES, T_LINES, T_HITS))
    md.append('')
    for g in groups:
        md.append('## %s（%s，前缀 %s）' % (g['name'], g['dex'], g['prefix']))
        md.append('')
        md.append('### 文件清单')
        md.append('')
        md.append('| 文件 | 行数 | 声明数 | 命中数 |')
        md.append('|---|---:|---:|---:|')
        for r in g['files']:
            md.append('| %s | %d | %d | %d |' % (esc(r['rel']), r['lines'], len(r['methods']), len(r['hits'])))
        md.append('')
        md.append('### 方法/字段声明粗提取（public|private|protected|static|final|native 等，前 %d 字符）' % 120)
        md.append('')
        shown = 0
        for r in g['files']:
            for i, t in r['methods']:
                if shown >= CAP_METHODS:
                    md.append('- …（截断：全组共 %d 条声明，完整清单见 tar.gz 全文）' % g['n_methods'])
                    shown = -1
                    break
                md.append('- `%s:%d` %s' % (esc(r['rel']), i, esc(t)))
                shown += 1
            if shown == -1:
                break
        if shown >= 0:
            md.append('- （共 %d 条）' % g['n_methods'])
        md.append('')
        md.append('### 网络面命中专节（文件:行号 + 行内容前 160 字符）')
        md.append('')
        if g['n_hits'] == 0:
            md.append('该组未发现网络/反射/设备指纹面命中（仅限正则口径）。')
        else:
            md.append('| 位置 | 内容 |')
            md.append('|---|---|')
            hshown = 0
            for r in g['files']:
                for i, t in r['hits']:
                    if hshown >= CAP_HITS:
                        md.append('| …截断 | 全组共 %d 条命中，未展示 %d 条，完整以 dm4-groups.json 计数与 tar.gz 全文为准 |' % (
                            g['n_hits'], g['n_hits'] - CAP_HITS))
                        hshown = -1
                        break
                    md.append('| %s:%d | %s |' % (esc(r['rel']), i, esc(t)))
                    hshown += 1
                if hshown == -1:
                    break
        md.append('')
        md.append('### 重点点名')
        md.append('')
        any_hl = False
        for label, items in g['highlight'].items():
            entries_total = sum(len(it['entries']) for it in items)
            if not items or entries_total == 0:
                continue
            any_hl = True
            md.append('**%s**' % label)
            md.append('')
            for it in items:
                md.append('- `%s`' % esc(it['file']))
                for e in it['entries'][:CAP_HL]:
                    md.append('  - %s: %s' % (esc(str(e[0])), esc(str(e[1]))))
                if len(it['entries']) > CAP_HL:
                    md.append('  - …（截断，共 %d 条）' % len(it['entries']))
            md.append('')
        if not any_hl:
            md.append('该组无预置重点点名命中（或该组无点名项，仅限正则口径）。')
            md.append('')
        md.append('> Java 全文见 Release `dm1-artifacts` / `dm4-author-java.tar.gz` → `java/%s/`。' % g['name'])
        md.append('')
    md.append('## 说明')
    md.append('')
    md.append('- 本报告由 CI 自动生成（workflow dm-author-code-decompile），命中与清单均为正则口径的事实罗列，')
    md.append('  组级判读在后续人工/深查环节完成，本报告不做定性。')
    with open(os.path.join(OUT, 'dm4-author-code.md'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(md) + '\n')

    print('[dm4] groups=8 files=%d lines=%d nethits=%d' % (T_FILES, T_LINES, T_HITS))


if __name__ == '__main__':
    main()
