#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""DM-1 W3：东明版净新增 arm64-v8a so 深查 + 官方对拍 + 老线样本 sha256 交叉

输入（workflow 已备好）：
  work/dongming.apk  work/official.apk  work/cross/*.apk
职责：
  1 双侧抽 lib/**/*.so → work/so-dm/ 与 work/so-official/（文件名 <abi>__<base> 防同名）；
    dm so 数 = 官方数 + 3 断言（不满足仅 WARN 不 FATAL，口径交人复核）。
  2 sha256 对拍表 dm3-sha-cross.tsv（abi\ttdm_name\ttdm_sha256\ttin_official_same_sha\tofficial_name）：
    Y=继承；N 且官方无同名=净新增；N 且官方同名不同 hash=同名异体（红旗单列计数）。
  3 净新增 so 深度档案（work/dm-out/）：<n>-imports / -net-imports / -strings-ascii /
    -strings-utf16 / -hits / -b64-decoded / -elfmeta / -exports（<n> 为 so 基名去 .so）。
  4 老线交叉：dm3-xcheck.tsv；命中登记 dm3-xcheck-hit.tsv 并打印 [dm3] CROSS_HIT，
    未命中打印 [dm3] CROSS_MISS（两者必居其一，供日志检索）。供应链关联=登记事实，不下结论。
  5 报告 dm3-native-so-audit.md + 结构化数据 dm3-so-report-data.json。
口径红线：以上为静态导入符号与字符串层证据；未发现外联证据 ≠ 证明无网络能力；
  本脚本不做 A/B/C/D 定性。
退出约定：正常收口必打 [dm3] 摘要行（workflow 以 grep [dm3] 判活）；
  致命错误打 [dm3-fatal]（不含 [dm3] 标记→判活失败，交人看日志）。
"""
import base64
import binascii
import hashlib
import json
import os
import re
import subprocess
import sys
import zipfile

WORK = sys.argv[1] if len(sys.argv) > 1 else 'work'
DM_APK = os.path.join(WORK, 'dongming.apk')
OFF_APK = os.path.join(WORK, 'official.apk')
CROSS_DIR = os.path.join(WORK, 'cross')
SO_DM = os.path.join(WORK, 'so-dm')
SO_OFF = os.path.join(WORK, 'so-official')
OUT = os.path.join(WORK, 'dm-out')

EXPECTED_NEW = 3          # 派单背景：libkijhhh.so / libabcdefgaaa.so / libdiacore.so
NET_RE = re.compile(
    r'socket|connect|getaddrinfo|gethostby|sendto|recvfrom|\brecv\b|\bsend\b'
    r'|SSL_|TLS_|curl|inet_|\bbind\b|\blisten\b|\bselect\b|\bpoll\b|epoll'
    r'|gethostname|connectx')
EXEC_RE = re.compile(r'execv|system\(|popen|dlopen|dlsym')
B64_RE = re.compile(r'^[A-Za-z0-9+/]{40,}={0,2}$')
B64_DEC_MEANING_RE = re.compile(r'http|\.|:|/')
# (键, 编译后正则, 展示名)
HIT_PATTERNS = [
    ('url', re.compile(r'https?://'), 'https?://'),
    ('ipv4', re.compile(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'), r'\b([0-9]{1,3}\.){3}[0-9]{1,3}\b'),
    ('vendor_domain', re.compile(
        r'\b(?:taobao|baidu|qq|weixin|wechat|163|126|kuwo|kugou|tencent|umeng|bugly'
        r'|alipay|aliyun|volc|bytedance|github|gitlab|gitee)\.'),
     r'\b(taobao|baidu|qq|weixin|wechat|163|126|kuwo|kugou|tencent|umeng|bugly|alipay|aliyun|volc|bytedance|github|gitlab|gitee)\.'),
    ('tld_path', re.compile(r'\.(?:com|cn|net|top|xyz|icu|click|tk|me|io|app)/\b'),
     r'\.(com|cn|net|top|xyz|icu|click|tk|me|io|app)/\b'),
    ('telegram', re.compile(r't\.me/'), 't\\.me/'),
    ('onion', re.compile(r'\.onion'), '\\.onion'),
    ('base64_kw', re.compile(r'base64'), 'base64'),
    ('pem', re.compile(r'-----BEGIN'), '-----BEGIN'),
    ('so_ref', re.compile(r'\.so\b'), '\\.so\\b'),
    ('path_proc', re.compile(r'/data/|/sdcard/|/proc/|/sys/class/net|/system/bin/sh'),
     '/data/|/sdcard/|/proc/|/sys/class/net|/system/bin/sh'),
    ('exec_kw', EXEC_RE, 'execv|system\\(|popen|dlopen|dlsym'),
]
# readelf -sW --dyn-syms 数据行：Num: Value Size Type Bind Vis Ndx Name(可含空格)
RE_SYM = re.compile(r'^\s*(\d+):\s+([0-9a-fA-F]+)\s+(\d+)\s+(\w+)\s+(\w+)\s+(\w+)\s+(\S+)\s*(.*)$')
FILE_SAMPLE_CAP = 200     # hits 文件内每模式样本行上限
REPORT_SAMPLE_CAP = 30    # 报告内每模式样本行上限


def run(cmd):
    """subprocess 容错封装：永不抛，返回 (rc, stdout, stderr)。"""
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, errors='replace', timeout=900)
        return p.returncode, p.stdout or '', p.stderr or ''
    except Exception as e:  # noqa: BLE001
        return -1, '', '%s: %r' % (cmd[0], e)


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def write_text(path, text):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)


def extract_sos(apk, outdir):
    """抽 lib/**/*.so → outdir/<abi>__<relpath>；返回 {(abi, basename): 落盘绝对路径}。"""
    os.makedirs(outdir, exist_ok=True)
    idx = {}
    with zipfile.ZipFile(apk) as z:
        for n in z.namelist():
            if not n.startswith('lib/') or not n.endswith('.so'):
                continue
            parts = n[len('lib/'):].split('/')
            if len(parts) < 2:
                continue
            abi = parts[0]
            base = parts[-1]
            saved = abi + '__' + n[len('lib/'):].replace('/', '__')
            dst = os.path.join(outdir, saved)
            with open(dst, 'wb') as f:
                f.write(z.read(n))
            idx[(abi, base)] = dst
    return idx


def parse_dynsyms(path):
    """readelf -sW --dyn-syms → (全量文本, UND 名列表, GLOBAL FUNC 导出名列表)。"""
    rc, out, err = run(['readelf', '-sW', '--dyn-syms', path])
    if rc != 0 and not out:
        return '$ readelf -sW --dyn-syms（失败 rc=%s）\n%s' % (rc, err), [], []
    und, exp = [], []
    for line in out.splitlines():
        m = RE_SYM.match(line)
        if not m:
            continue
        _num, _val, _sz, typ, bind, _vis, ndx, name = m.groups()
        name = name.strip()
        if not name:
            continue
        if ndx == 'UND':
            und.append(name)
        elif typ == 'FUNC' and bind == 'GLOBAL':
            exp.append(name)
    return out, und, exp


def elf_meta(path):
    """NEEDED/RPATH/RUNPATH + BuildID + .comment + size -A + file。"""
    rc_d, d_out, d_err = run(['readelf', '-dW', path])
    rc_n, n_out, _ = run(['readelf', '-n', path])
    rc_c, c_out, _ = run(['readelf', '-p', '.comment', path])
    rc_s, s_out, _ = run(['size', '-A', path])
    rc_f, f_out, _ = run(['file', path])
    needed = re.findall(r'\(NEEDED\)\s+Shared library:\s+\[([^\]]+)\]', d_out)
    rpath = re.findall(r'\(RPATH\)\s+Library rpath:\s+\[([^\]]+)\]', d_out)
    runpath = re.findall(r'\(RUNPATH\)\s+Library runpath:\s+\[([^\]]+)\]', d_out)
    mb = re.search(r'Build ID:\s*([0-9a-fA-F]+)', n_out)
    buildid = mb.group(1) if mb else 'N/A'
    comments = []
    if rc_c == 0:
        for line in c_out.splitlines():
            mc = re.match(r'\s*\[\s*\d+\]\s+(.*)$', line)
            if mc and mc.group(1).strip():
                comments.append(mc.group(1).strip())
    comment = ' | '.join(comments) if comments else 'N/A'
    meta_text = (
        '$ readelf -dW\n%s\n$ readelf -n\n%s\n$ readelf -p .comment\n%s\n'
        '$ size -A\n%s\n$ file\n%s\n' % (d_out or d_err, n_out, c_out or '(N/A)', s_out, f_out))
    return {
        'needed': needed, 'rpath': rpath, 'runpath': runpath,
        'buildid': buildid, 'comment': comment, 'meta_text': meta_text,
    }


def b64_candidates(ascii_lines):
    """^[A-Za-z0-9+/]{40,}={0,2}$ 行 → b64decode(validate) 且可打印>0.8 且含 http|.|:|/ 者入选。"""
    hits = []
    for ln in ascii_lines:
        s = ln.strip()
        if not s or not B64_RE.match(s):
            continue
        try:
            dec = base64.b64decode(s, validate=True)
        except (binascii.Error, ValueError):
            continue
        if not dec:
            continue
        printable = sum(1 for b in dec if 32 <= b < 127 or b in (9, 10, 13))
        if printable / len(dec) <= 0.8:
            continue
        dtxt = ''.join(chr(b) if 32 <= b < 127 else '.' for b in dec)
        if not B64_DEC_MEANING_RE.search(dtxt):
            continue
        hits.append((s, dtxt))
    return hits


def profile_one_so(name, so_path, data):
    """单个净新增 so 全档案 → work/dm-out/。name 为基名(含 .so)。"""
    stem = name[:-3] if name.endswith('.so') else name
    entry = {'file': name}
    dyn_text, und, exp = parse_dynsyms(so_path)
    entry['export_count'] = len(exp)
    entry['jniload_present'] = 'JNI_OnLoad' in exp
    entry['j_underscore_exports'] = [e for e in exp if e.startswith('Java_')]

    # imports.txt：全量 dyn-syms + UND 清单
    imp_lines = ['$ readelf -sW --dyn-syms（全量）', dyn_text,
                 '', '== UND(U) 导入符号清单（%d 个）==' % len(und)] + und
    write_text(os.path.join(OUT, stem + '-imports.txt'), '\n'.join(imp_lines) + '\n')

    # exports.txt：GLOBAL FUNC 导出面
    exp_lines = ['== GLOBAL FUNC 导出（%d 个）==' % len(exp), *exp,
                 '', 'JNI_OnLoad: %s' % ('present' if entry['jniload_present'] else 'ABSENT'),
                 'Java_* 显式注册导出: %d 个' % len(entry['j_underscore_exports']),
                 '（registerNatives 动态注册无导出痕迹，JNI_OnLoad 内运行时绑定）']
    write_text(os.path.join(OUT, stem + '-exports.txt'), '\n'.join(exp_lines) + '\n')

    # net-imports：对 UND 名跑网络族正则
    net_hits = sorted({n for n in und if NET_RE.search(n)})
    entry['net_import_count'] = len(net_hits)
    body = ['== UND 导入符号 × 网络族正则（%d 命中）==' % len(net_hits)]
    body += net_hits if net_hits else ['(无命中)']
    write_text(os.path.join(OUT, stem + '-net-imports.txt'), '\n'.join(body) + '\n')
    entry['net_imports'] = net_hits

    # exec 族在导入符号侧再查一次
    entry['exec_import_hits'] = sorted({n for n in und if EXEC_RE.search(n)})

    # strings 两份全量落盘
    rc_a, a_out, a_err = run(['strings', '-a', so_path])
    write_text(os.path.join(OUT, stem + '-strings-ascii.txt'),
               a_out if rc_a == 0 else '(strings -a 失败 rc=%s)\n%s' % (rc_a, a_err))
    rc_u, u_out, u_err = run(['strings', '-e', 'l', so_path])
    write_text(os.path.join(OUT, stem + '-strings-utf16.txt'),
               u_out if rc_u == 0 else '(strings -e l 失败 rc=%s)\n%s' % (rc_u, u_err))
    ascii_lines = a_out.splitlines()
    utf16_lines = u_out.splitlines() if rc_u == 0 else []

    # hits：每模式独立计数（ascii + utf16 合并），落盘 + 计数进报告
    pat_counts, pat_samples = {}, {}
    hit_lines = ['== strings 模式命中（ascii %d 行 + utf16 %d 行）==' % (len(ascii_lines), len(utf16_lines))]
    for key, rx, shown in HIT_PATTERNS:
        matched = [('ascii', ln) for ln in ascii_lines if rx.search(ln)] \
                + [('utf16', ln) for ln in utf16_lines if rx.search(ln)]
        pat_counts[key] = len(matched)
        pat_samples[key] = matched[:REPORT_SAMPLE_CAP]
        hit_lines += ['', '---- [%s] %s → %d 命中 ----' % (key, shown, len(matched))]
        hit_lines += ['[%s] %s' % (src, ln) for src, ln in matched[:FILE_SAMPLE_CAP]]
    write_text(os.path.join(OUT, stem + '-hits.txt'), '\n'.join(hit_lines) + '\n')
    entry['pattern_counts'] = pat_counts
    entry['pattern_samples'] = {k: v for k, v in pat_samples.items()}
    entry['url_hits'] = pat_counts.get('url', 0)
    entry['ip_hits'] = pat_counts.get('ipv4', 0)

    # base64 候选
    cands = b64_candidates(ascii_lines)
    entry['b64_decode_hits'] = len(cands)
    if cands:
        bl = ['== base64 候选（解码可打印>0.8 且含 http|.|:|/，%d 条）==' % len(cands)]
        for raw, dec in cands:
            bl.append('RAW : %s' % raw[:80])
            bl.append('DEC : %s' % dec[:160])
            bl.append('')
        write_text(os.path.join(OUT, stem + '-b64-decoded.txt'), '\n'.join(bl) + '\n')

    # elfmeta
    meta = elf_meta(so_path)
    entry['needed'] = meta['needed']
    entry['buildid'] = meta['buildid']
    entry['comment'] = meta['comment']
    entry['rpath'] = meta['rpath']
    entry['runpath'] = meta['runpath']
    write_text(os.path.join(OUT, stem + '-elfmeta.txt'), meta['meta_text'])
    data['so'].append(entry)


def cross_check(new_sos, data):
    """老线样本 so sha256 全量对拍净新增集；new_sos: {sha256: (abi, name)}。"""
    rows, hits = [], []
    if os.path.isdir(CROSS_DIR):
        for sample in sorted(os.listdir(CROSS_DIR)):
            if not sample.endswith('.apk'):
                continue
            sp = os.path.join(CROSS_DIR, sample)
            try:
                z = zipfile.ZipFile(sp)
            except Exception as e:  # noqa: BLE001
                print('[dm3-warn] cross open failed %s: %r' % (sample, e))
                continue
            with z:
                for n in z.namelist():
                    if not n.startswith('lib/') or not n.endswith('.so'):
                        continue
                    sha = hashlib.sha256(z.read(n)).hexdigest()
                    rows.append((sample, n, sha))
                    if sha in new_sos:
                        abi, name = new_sos[sha]
                        hits.append((name, n, sha, sample))
    with open(os.path.join(OUT, 'dm3-xcheck.tsv'), 'w', encoding='utf-8') as f:
        f.write('sample_file\tso_path\tsha256\n')
        for r in rows:
            f.write('\t'.join(r) + '\n')
    with open(os.path.join(OUT, 'dm3-xcheck-hit.tsv'), 'w', encoding='utf-8') as f:
        f.write('dm_so\tso_path\tsha256\t样本来源\n')
        for h in hits:
            f.write('\t'.join(h) + '\n')
    data['xcheck_rows'] = len(rows)
    data['xcheck_hits'] = [{'dm_so': h[0], 'so_path': h[1], 'sha256': h[2], 'from': h[3]} for h in hits]
    if hits:
        for h in hits:
            print('[dm3] CROSS_HIT %s == %s (%s)' % (h[0], h[1], h[3]))
    else:
        print('[dm3] CROSS_MISS（老线样本 so 与净新增 so sha256 交集为空，样本行 %d）' % len(rows))
    return len(hits)


def build_report(data):
    rep = []
    rep.append('# DM-1 W3 净新增 native so 深查报告\n')
    rep.append('> 东明版 12.2.2.0.apk vs 官方 12.2.2.0.apk；Java 层明文 0 非厂商域名，C2 嫌疑集中于此。')
    rep.append('> 本文件为 CI（dm-native-so-audit.yml）自动回写，重活全在 runner（D7）。\n')

    rep.append('## 关键数字摘要\n')
    rep.append('| 指标 | 数 |')
    rep.append('|---|---|')
    rep.append('| dm so 总数 | %d |' % data['dm_count'])
    rep.append('| 官方 so 总数 | %d |' % data['off_count'])
    rep.append('| 净新增 so（预期 %d） | %d |' % (EXPECTED_NEW, data['n_new']))
    rep.append('| 同名异体（官方同名不同 hash，红旗） | %d |' % data['n_variant'])
    rep.append('| 老线交叉 so 行 | %d |' % data['xcheck_rows'])
    rep.append('| 老线交叉命中 | %d |' % data['xhit_count'])
    rep.append('')
    rep.append('| 净新增 so | abi | 大小(B) | sha256 前16 | 网络族导入 | URL命中 | IP命中 | b64解码 |')
    rep.append('|---|---|---|---|---|---|---|---|')
    for e in data['so']:
        rep.append('| `%s` | %s | %s | `%s` | %d | %d | %d | %d |' % (
            e['file'], e.get('abi', '-'), e.get('size', '-'), e.get('sha256', '-')[:16],
            e.get('net_import_count', -1), e.get('url_hits', -1), e.get('ip_hits', -1),
            e.get('b64_decode_hits', -1)))
    rep.append('')
    if data['n_variant']:
        rep.append('**同名异体红旗清单**（官方同路径存在但 hash 不同）：')
        for a, b in data['variants']:
            rep.append('- `%s/%s`' % (a, b))
        rep.append('')

    for e in data['so']:
        rep.append('## %s（%s）\n' % (e['file'], e.get('abi', '-')))
        if e.get('error'):
            rep.append('深档失败：%s（其余条目见 dm3-so-report-data.json）\n' % e['error'])
            continue
        rep.append('### ELF 元信息')
        rep.append('- NEEDED: %s' % (', '.join('`%s`' % x for x in e['needed']) or '(无)'))
        rep.append('- RPATH/RUNPATH: %s / %s' % (
            ', '.join(e['rpath']) or '(无)', ', '.join(e['runpath']) or '(无)'))
        rep.append('- BuildID: `%s`' % e['buildid'])
        rep.append('- .comment: `%s`' % e['comment'])
        rep.append('- 全文见 `%s-elfmeta.txt`（含 size -A 节大小 / file）\n'
                   % e['file'][:-3])
        rep.append('### 导出面')
        rep.append('- GLOBAL FUNC 导出：%d 个；JNI_OnLoad：%s；Java_* 显式导出：%d 个' % (
            e['export_count'], 'present' if e['jniload_present'] else 'ABSENT',
            len(e['j_underscore_exports'])))
        for x in e['j_underscore_exports'][:50]:
            rep.append('  - `%s`' % x)
        if len(e['j_underscore_exports']) > 50:
            rep.append('  - …（全量见 -exports.txt）')
        rep.append('- registerNatives 属运行时动态注册，导出表不可见，静态侧只能看 JNI_OnLoad 存在性\n')
        rep.append('### 网络族导入（%d 命中）' % e['net_import_count'])
        for x in e['net_imports'][:100]:
            rep.append('- `%s`' % x)
        if e['net_import_count'] > 100:
            rep.append('- …（全量见 -net-imports.txt）')
        if e['exec_import_hits']:
            rep.append('- 导入侧 exec 族：' + ', '.join('`%s`' % x for x in e['exec_import_hits']))
        rep.append('')
        rep.append('### strings 命中明细（每模式计数 + 前 %d 条样本）' % REPORT_SAMPLE_CAP)
        for key, _rx, shown in HIT_PATTERNS:
            rep.append('- `%s` %s → %d 命中' % (key, shown, e['pattern_counts'].get(key, 0)))
            samples = e['pattern_samples'].get(key, [])
            if samples:
                for src, ln in samples:
                    rep.append('    - [%s] `%s`' % (src, ln.replace('`', '').strip()[:200]))
        rep.append('')
        rep.append('- base64 候选解码命中：%d（见 `%s-b64-decoded.txt`，可打印>0.8 且含 http|.|:|/）\n'
                   % (e['b64_decode_hits'], e['file'][:-3]))

    rep.append('## 老线交叉对拍\n')
    if data['xcheck_hits']:
        rep.append('| dm_so | 命中样本内 so 路径 | sha256 | 样本来源 |')
        rep.append('|---|---|---|---|')
        for h in data['xcheck_hits']:
            rep.append('| `%s` | `%s` | `%s` | `%s` |' % (h['dm_so'], h['so_path'], h['sha256'][:16] + '…', h['from']))
        rep.append('\n哈希命中 = 供应链关联**登记事实**，不下结论（同源编译或同一分发者，待后续人工核）。')
    else:
        rep.append('0 命中：净新增 so 的 sha256 与天天版/红果/番茄老线样本（%d 行 so）均不同。' % data['xcheck_rows'])
        rep.append('注：同族改壳常改重编导致 hash 漂移，0 命中 ≠ 非同作者，只登记不断。')
    rep.append('')

    rep.append('## 诚实口径（必读）\n')
    rep.append('以上为静态导入符号与字符串层证据；未发现外联证据 ≠ 证明无网络能力，'
               '静态分析不能证绝对无（混淆/运行时拼接可规避本层检测）。')
    rep.append('本报告不做 A/B/C/D 定性；净新增口径、同名异体红旗与老线命中均交人工复核。')
    write_text(os.path.join(OUT, 'dm3-native-so-audit.md'), '\n'.join(rep) + '\n')


def main():
    for p in (DM_APK, OFF_APK):
        if not os.path.isfile(p):
            print('[dm3-fatal] missing input: %s' % p)
            return 2
    os.makedirs(OUT, exist_ok=True)
    data = {'so': [], 'variants': [], 'xcheck_hits': [], 'xcheck_rows': 0}

    # 1 双侧解 so
    dm = extract_sos(DM_APK, SO_DM)
    off = extract_sos(OFF_APK, SO_OFF)
    data['dm_count'], data['off_count'] = len(dm), len(off)
    print('[dm3] so counts: dm=%d official=%d (expect dm=official+%d)'
          % (len(dm), len(off), EXPECTED_NEW))
    if len(dm) != len(off) + EXPECTED_NEW:
        print('[dm3] WARN 净增 so 数 != %d，口径交人复核（dm=%d off=%d）'
              % (EXPECTED_NEW, len(dm), len(off)))

    # 2 sha256 对拍
    new_sos, variants = [], []
    with open(os.path.join(OUT, 'dm3-sha-cross.tsv'), 'w', encoding='utf-8') as f:
        f.write('abi\tdm_name\tdm_sha256\tin_official_same_sha\tofficial_name\n')
        for (abi, base), p in sorted(dm.items()):
            sha = sha256_file(p)
            op = off.get((abi, base))
            if op is None:
                f.write('%s\t%s\t%s\tN\t\n' % (abi, base, sha))
                new_sos.append((abi, base, p, sha))
            else:
                osha = sha256_file(op)
                same = 'Y' if osha == sha else 'N'
                f.write('%s\t%s\t%s\t%s\t%s\n' % (abi, base, sha, same, os.path.basename(op)))
                if same == 'N':
                    variants.append((abi, base))
    data['n_new'] = len(new_sos)
    data['n_variant'] = len(variants)
    data['variants'] = variants
    print('[dm3] net-new=%d variant-red=%d' % (len(new_sos), len(variants)))
    if len(new_sos) != EXPECTED_NEW:
        print('[dm3] WARN 净新增 so 数=%d ≠ 预期 %d（逐档仍全部处理）' % (len(new_sos), EXPECTED_NEW))

    # 3 净新增逐 so 深档（单点失败不拖垮全局）
    for abi, base, p, sha in new_sos:
        before = len(data['so'])
        try:
            profile_one_so(base, p, data)
            e = data['so'][-1]
            e['abi'], e['size'], e['sha256'] = abi, os.path.getsize(p), sha
        except Exception as ex:  # noqa: BLE001
            if len(data['so']) == before:
                data['so'].append({'file': base, 'abi': abi, 'size': os.path.getsize(p),
                                   'sha256': sha, 'error': repr(ex)})
            print('[dm3] WARN profile %s failed: %r' % (base, ex))

    # 4 老线交叉
    new_map = {sha: (abi, base) for abi, base, _p, sha in new_sos}
    data['xhit_count'] = cross_check(new_map, data)

    # 5 报告 + JSON
    build_report(data)
    slim = json.loads(json.dumps(data, ensure_ascii=False))
    for e in slim['so']:
        e.pop('pattern_samples', None)  # JSON 留计数与清单，样本行在 md/txt
    write_text(os.path.join(OUT, 'dm3-so-report-data.json'),
               json.dumps(slim, ensure_ascii=False, indent=1) + '\n')

    tot_net = sum(e.get('net_import_count', 0) for e in data['so'])
    tot_url = sum(e.get('url_hits', 0) for e in data['so'])
    tot_ip = sum(e.get('ip_hits', 0) for e in data['so'])
    tot_b64 = sum(e.get('b64_decode_hits', 0) for e in data['so'])
    print('[dm3] new=%d net_imports=%d url=%d ip=%d b64=%d xhit=%d'
          % (data['n_new'], tot_net, tot_url, tot_ip, tot_b64, data['xhit_count']))
    return 0


if __name__ == '__main__':
    sys.exit(main())
