#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""DM-1 W5：东明版 assets/dcxll 消费方定位 + 与官方基线条目对拍（rid recvvcvacUOp2j）

职责（派单 W5，纯 stdlib，重活全在 runner——D7 红线）：
  ①解 work/in1/dm1-smali-mod.tar.gz 到 work/（tar 顶层 smali-mod/，W1 产物）。
  ②Java 层消费方：全部 .smali 找子串 dcxll（大小写不敏感）；分列 assets/dcxll 与 dcxll(超集) 计数；
    每命中记（相对路径/行号/内容截200/回溯最近 .method 得所在方法）；命中类聚合为消费方集合。
  ③消费方类方法面：全部 .method 声明一行一个（含 access/静态/native）；const-string 命中落 ±5 行上下文文件。
  ④native 层：抽 lib/ 下 3 净新增 so（libkijhhh/libabcdefgaaa/libdiacore）+ 顺手抽 libhippy.so 对照，
    strings -a 与 strings -e l 过滤 dcxll（无命中=正常，不 FATAL）。
  ⑤dcxll 本体核验：apk 内 assets/dcxll 再解 zip → 预期 4 件（AndroidManifest.xml + META-INF/ANDROIDK.{RSA,SF}
    + MANIFEST.MF），逐条与官方 apk 同路径条目 sha256 对拍；不符预期不 FATAL，如实记差异。
  ⑥报告 dm5-dcxll-consumer.md：关键数字/命中明细/方法面/对拍表/用途现状（只写事实链，禁 A/B/C/D 定性）。
收口行（workflow grep 判据，勿在他处复用该标记）：
  [dm5] java_hits=%d consumers=%d so_hits=%d entries=%d
"""
import hashlib
import io
import os
import subprocess
import sys
import tarfile
import zipfile

WORK = sys.argv[1] if len(sys.argv) > 1 else 'work'
SMALI = os.path.join(WORK, 'smali-mod')
TARBALL = os.path.join(WORK, 'in1', 'dm1-smali-mod.tar.gz')
APK_DM_CANDS = [os.path.join(WORK, n) for n in
                ('dongming-kuwo-12.2.2.0.apk', 'dongming.apk')]
APK_OFF_CANDS = [os.path.join(WORK, n) for n in
                 ('kuwo-12.2.2.0-official.apk', 'official.apk')]
OUT = os.path.join(WORK, 'dm-out')
SODIR = os.path.join(WORK, 'dm-so')
os.makedirs(OUT, exist_ok=True)

# 3 净新增 so（arm64-v8a）+ libhippy.so 对照（存在才扫）
NEW_SO = ('libkijhhh.so', 'libabcdefgaaa.so', 'libdiacore.so')
CTL_SO = ('libhippy.so',)
EXPECTED = ('AndroidManifest.xml', 'META-INF/ANDROIDK.RSA',
            'META-INF/ANDROIDK.SF', 'META-INF/MANIFEST.MF')
EXPECTED_BLOB_SIZE = 1429799  # 背景登记值，仅对照记录，不符不 FATAL


def fatal(msg):
    # 注意：致命路径绝不出现 "[dm5]" 标记（那是成功收口 grep 判据）
    raise SystemExit('FATAL dm5: ' + msg)


def sha(b):
    return hashlib.sha256(b).hexdigest()


def pick_existing(cands, what):
    for c in cands:
        if os.path.isfile(c):
            return c
    fatal('%s 缺失（候选 %s）' % (what, ', '.join(cands)))


# ① tar 解包
def extract_tar():
    if not os.path.isfile(TARBALL):
        fatal('缺 W1 产物 %s —— 先跑 dm-dex-method-diff（W1）' % TARBALL)
    with tarfile.open(TARBALL, 'r:gz') as tf:
        try:
            tf.extractall(WORK, filter='data')
        except TypeError:  # 老 py 无 filter 参数（runner 3.12 走 data 过滤）
            tf.extractall(WORK)
    if not os.path.isdir(SMALI):
        fatal('tar 解包后未见 %s（W1 tar 顶层结构异常）' % SMALI)


def class_key(rel):
    """smali-mod/<dex>/a/b/C.smali -> a/b/C；无 dex 层则退化为文件名去后缀。"""
    parts = rel.split('/')
    seg = parts[2:] if len(parts) > 3 else parts[-1:]
    return '/'.join(seg)[:-6]


def is_method_hdr(s):
    return s == '.method' or s.startswith('.method ')


# ② Java 层扫描
def scan_java():
    hits = []
    for droot, _, fs in os.walk(SMALI):
        for fn in sorted(fs):
            if not fn.endswith('.smali'):
                continue
            p = os.path.join(droot, fn)
            rel = os.path.relpath(p, WORK).replace(os.sep, '/')
            with open(p, encoding='utf-8', errors='replace') as f:
                lines = f.read().splitlines()
            cur = '(类级/前无.method)'
            for i, line in enumerate(lines):
                s = line.strip()
                if is_method_hdr(s):
                    cur = s
                low = line.lower()
                if 'dcxll' not in low:
                    continue
                hits.append({
                    'rel': rel, 'cls': class_key(rel), 'path': p, 'idx': i,
                    'line': i + 1, 'content': s[:200], 'method': cur,
                    'kind': 'assets/dcxll' if 'assets/dcxll' in low else 'dcxll',
                    'is_const': s.startswith('const-string'),
                })
    return hits


# ③ 方法面 + 上下文 + 方法体内 invoke
def method_surface(path):
    ms = []
    with open(path, encoding='utf-8', errors='replace') as f:
        for line in f:
            s = line.strip()
            if is_method_hdr(s):
                ms.append(s)
    return ms


def invokes_in_method(path, idx):
    """回溯最近 .method、前探 .end method，收集体内去重后的 invoke-* 行。"""
    with open(path, encoding='utf-8', errors='replace') as f:
        lines = f.read().splitlines()
    a = idx
    while a > 0 and not is_method_hdr(lines[a].strip()):
        a -= 1
    b = idx
    n = len(lines)
    while b < n and lines[b].strip() != '.end method':
        b += 1
    out, seen = [], set()
    for l in lines[a:b]:
        s = l.strip()
        if s.startswith('invoke-') and s not in seen:
            seen.add(s)
            out.append(s[:160])
    return out


def context_lines(path, idx, span=5):
    with open(path, encoding='utf-8', errors='replace') as f:
        lines = f.read().splitlines()
    return lines[max(0, idx - span):idx + span + 1]


def write_context_files(hits):
    """const-string 命中 → dm5-context-<class转下划线>.txt（同类多命中合并分节）。"""
    by_cls = {}
    for h in hits:
        if h['is_const']:
            by_cls.setdefault(h['cls'], []).append(h)
    written = []
    for cls, hs in sorted(by_cls.items()):
        fn = os.path.join(OUT, 'dm5-context-%s.txt' % cls.replace('/', '_'))
        with open(fn, 'w', encoding='utf-8') as f:
            f.write('# DM-1 W5 const-string 命中上下文（±5 行） class=%s\n' % cls)
            for h in hs:
                f.write('\n## %s  L%d\n```smali\n' % (h['rel'], h['line']))
                for s in context_lines(h['path'], h['idx']):
                    f.write(s + '\n')
                f.write('```\n')
        written.append(fn)
    return written


# ④ native 层
def native_scan(zf):
    want = set(NEW_SO) | set(CTL_SO)
    extracted = {}
    for n in zf.namelist():
        if not n.startswith('lib/') or not n.endswith('.so'):
            continue
        base = n.rsplit('/', 1)[-1]
        if base in want:
            os.makedirs(SODIR, exist_ok=True)
            dest = os.path.join(SODIR, n.replace('/', '_'))
            with open(dest, 'wb') as f:
                f.write(zf.read(n))
            extracted.setdefault(base, []).append((n, dest))
    hit_lines, errs, scanned = [], [], []
    for base in NEW_SO + CTL_SO:
        for n, dest in extracted.get(base, []):
            for label, args in (('strings -a', ['strings', '-a', dest]),
                                ('strings -e l', ['strings', '-e', 'l', dest])):
                try:
                    r = subprocess.run(args, capture_output=True,
                                       text=True, errors='replace', timeout=900)
                    if r.returncode != 0:
                        errs.append('%s %s rc=%d %s' %
                                    (n, label, r.returncode, (r.stderr or '').strip()[:200]))
                    c0 = len(hit_lines)
                    for line in r.stdout.splitlines():
                        if 'dcxll' in line.lower():
                            hit_lines.append('%s\t%s\t%s' % (n, label, line.strip()[:300]))
                    scanned.append((base, n, label, len(hit_lines) - c0))
                except FileNotFoundError:
                    errs.append('strings 不可用（runner 缺 binutils？）')
                except subprocess.TimeoutExpired:
                    errs.append('%s %s timeout(900s)' % (n, label))
    return extracted, hit_lines, errs, scanned


# ⑤ dcxll 本体核验
def check_dcxll(zf_dm, zf_off):
    off_names = set(zf_off.namelist()) if zf_off else set()
    dm_names = set(zf_dm.namelist())
    blob = zf_dm.read('assets/dcxll') if 'assets/dcxll' in dm_names else None
    inner, inner_names, badzip = None, set(), False
    if blob is not None:
        try:
            inner = zipfile.ZipFile(io.BytesIO(blob))
            inner_names = set(inner.namelist())
        except zipfile.BadZipFile:
            badzip = True
    rows = []
    order = list(EXPECTED) + sorted(inner_names - set(EXPECTED))
    for e in order:
        if inner is not None and e in inner_names:
            b = inner.read(e)
            sz, sh = len(b), sha(b)
            if zf_off is None:
                m = 'SKIP(no-official)'
            elif e in off_names:
                m = 'YES' if sha(zf_off.read(e)) == sh else 'NO(diff)'
            else:
                m = 'OFFICIAL-MISSING'
        else:
            sz, sh, m = '-', 'DCXLL-MISSING', '-'
        rows.append((e, sz, sh, m, e in dm_names))
    info = {'blob': blob, 'badzip': badzip}
    return rows, info


def w_tsv(name, header, rows):
    with open(os.path.join(OUT, name), 'w', encoding='utf-8') as f:
        f.write('\t'.join(header) + '\n')
        for r in rows:
            f.write('\t'.join(str(x) for x in r) + '\n')


def main():
    extract_tar()
    apk_dm = pick_existing(APK_DM_CANDS, '东明样本 apk')
    apk_off_p = None
    for c in APK_OFF_CANDS:
        if os.path.isfile(c):
            apk_off_p = c
            break

    hits = scan_java()
    assets_hits = [h for h in hits if h['kind'] == 'assets/dcxll']
    consumers = sorted({h['cls'] for h in hits})
    consumer_files = {}
    for h in hits:
        consumer_files.setdefault(h['cls'], set()).add(h['rel'] + '|' + h['path'])

    zf_off = zipfile.ZipFile(apk_off_p) if apk_off_p else None
    with zipfile.ZipFile(apk_dm) as zf:
        extracted, so_hit_lines, so_errs, scanned = native_scan(zf)
        rows, info = check_dcxll(zf, zf_off)
    if zf_off:
        zf_off.close()

    ctx_files = write_context_files(hits)

    w_tsv('dm5-consumer-hits.tsv',
          ('rel_file', 'class', 'method', 'line', 'kind', 'content'),
          [(h['rel'], h['cls'], h['method'], h['line'], h['kind'], h['content']) for h in hits])
    w_tsv('dm5-dcxll-entries.tsv',
          ('entry', 'size', 'sha256', 'match_official'),
          [(e, sz, sh, m) for e, sz, sh, m, _in_dm in rows])
    if so_hit_lines:
        with open(os.path.join(OUT, 'dm5-so-hits.txt'), 'w', encoding='utf-8') as f:
            f.write('\n'.join(so_hit_lines) + '\n')

    yes_cnt = sum(1 for r in rows if r[0] in EXPECTED and r[3] == 'YES')
    exp_rows = {r[0]: r for r in rows if r[0] in EXPECTED}

    # ⑥ 报告
    rep = []
    rep.append('# DM-1 W5 assets/dcxll 消费方定位 + 条目对拍报告\n')
    rep.append('> 口径：Java 层 = W1 东明全量 smali（18 dex）逐行大小写不敏感子串；')
    rep.append('> native 层 = 3 净新增 so + libhippy.so(对照) 的 strings -a/-e l 过滤 dcxll；')
    rep.append('> 对拍 = dcxll 内条目 vs 官方 apk 同路径条目 sha256。不符预期不 FATAL，如实记录。\n')
    rep.append('## 关键数字\n')
    rep.append('| 指标 | 值 |')
    rep.append('|---|---|')
    rep.append('| Java 层命中（dcxll 超集） | %d 处 |' % len(hits))
    rep.append('| 其中 assets/dcxll | %d 处 |' % len(assets_hits))
    rep.append('| 消费方类 | %d 个 |' % len(consumers))
    rep.append('| native strings 命中 | %d 处（含对照 hippy，分列见下表） |' % len(so_hit_lines))
    rep.append('| dcxll 内 4 件对拍一致 | %d/4 YES |' % yes_cnt)
    blob = info['blob']
    if blob is not None:
        rep.append('| assets/dcxll 本体 | %d B（登记值 %d，%s）sha256 %s |'
                   % (len(blob), EXPECTED_BLOB_SIZE,
                      '一致' if len(blob) == EXPECTED_BLOB_SIZE else '不一致，如实记差异',
                      sha(blob)))
    else:
        rep.append('| assets/dcxll 本体 | 东明 apk 内不存在该条目 |')
    if info['badzip']:
        rep.append('| ⚠ assets/dcxll 非合法 zip | BadZipFile，无法列条目 |')
    rep.append('')

    rep.append('## Java 层命中明细（全量见 dm5-consumer-hits.tsv）\n')
    if not hits:
        rep.append('（0 命中）')
    else:
        rep.append('| 类 | 所在方法 | 行 | kind | 内容(≤200) |')
        rep.append('|---|---|---|---|---|')
        for h in hits[:500]:
            rep.append('| `%s` | `%s` | %d | %s | `%s` |'
                       % (h['cls'], h['method'], h['line'], h['kind'], h['content']))
        if len(hits) > 500:
            rep.append('\n（共 %d 行，报告仅列前 500，全量见 Release 附件 dm5-consumer-hits.tsv）' % len(hits))
    rep.append('')

    rep.append('## 消费方类方法面（供判断谁调起 dcxll 读取）\n')
    if not consumers:
        rep.append('（无消费方类）')
    for cls in consumers:
        rep.append('### `%s`' % cls)
        for ref in sorted(consumer_files[cls]):
            rel, _, path = ref.partition('|')
            rep.append('- 文件 `%s`' % rel)
            ms = method_surface(path)
            rep.append('```smali')
            for m in ms[:150]:
                rep.append(m)
            if len(ms) > 150:
                rep.append('# ...共 %d 个方法，余下略（回源 smali 文件看全量）' % len(ms))
            rep.append('```')
    rep.append('')

    rep.append('## dcxll 条目对拍表（entry/size/sha256/match_official；全量见 dm5-dcxll-entries.tsv）\n')
    rep.append('| entry | size | sha256 | match_official | 东明主包内也存在? |')
    rep.append('|---|---|---|---|---|')
    for e, sz, sh, m, in_dm in rows:
        rep.append('| `%s` | %s | %s | %s | %s |' % (e, sz, sh, m, '是' if in_dm else '否'))
    rep.append('')
    rep.append('预期 4 件在东明主包的缺失核验（背景：三签名件+AndroidManifest 应从主包挪入 dcxll）：')
    for e in EXPECTED:
        r = exp_rows.get(e)
        rep.append('- `%s`：东明主包 %s；dcxll 内 %s；与官方对拍 %s'
                   % (e,
                      ('存在(异常,记差异)' if (r and r[4]) else '不存在(符合预期)'),
                      ('在' if (r and r[2] != 'DCXLL-MISSING') else '缺失(记差异)'),
                      (r[3] if r else '-')))
    rep.append('')

    rep.append('## native strings dcxll 命中（so 命中明细落 dm5-so-hits.txt）\n')
    rep.append('| so | 扫描器 | dcxll 命中行数 |')
    rep.append('|---|---|---|')
    for base in NEW_SO + CTL_SO:
        entries = extracted.get(base, [])
        if not entries:
            tag = '未抽取到（apk 无该 so）' if base in CTL_SO else '★预期净新增却缺失'
            rep.append('| %s | — | %s |' % (base, tag))
        else:
            for n, _d in entries:
                cnt = sum(c for _b, nn, _l, c in scanned if nn == n)
                rep.append('| `%s` | strings -a / -e l | %d |' % (n, cnt))
    if so_hit_lines:
        rep.append('\n命中行（so \\t 扫描器 \\t 内容，前 100）：')
        rep.append('```')
        for l in so_hit_lines[:100]:
            rep.append(l)
        rep.append('```')
    else:
        rep.append('\n（strings 两法 0 命中 —— 无命中属正常，非错误）')
    if so_errs:
        rep.append('\n扫描异常记录：')
        for e in so_errs:
            rep.append('- %s' % e)
    rep.append('')

    rep.append('## 用途现状（只写事实链，禁 A/B/C/D 定性）\n')
    if hits:
        seen_pair = set()
        for h in hits:
            key = (h['cls'], h['method'])
            if key in seen_pair:
                continue
            seen_pair.add(key)
            inv = invokes_in_method(h['path'], h['idx'])
            note = '' if not h['is_const'] else '（const-string 命中，±5 行上下文见 dm5-context-%s.txt）' % h['cls'].replace('/', '_')
            if inv:
                rep.append('- 类 `%s` 方法 `%s` 第 %d 行含 `%s`%s；体内 invoke 引用：%s'
                           % (h['cls'], h['method'], h['line'], h['content'], note,
                              '; '.join('`%s`' % s for s in inv[:12])))
            else:
                rep.append('- 类 `%s` 方法 `%s` 第 %d 行含 `%s`%s；体内无可见 invoke-* 调用 → 消费方已定位，语义解读见 W4 对应类 Java 全文'
                           % (h['cls'], h['method'], h['line'], h['content'], note))
    if ctx_files:
        rep.append('- 上下文文件：%s' % ', '.join(os.path.basename(x) for x in ctx_files))
    if not hits and not so_hit_lines:
        rep.append('- 无 Java 消费者且 3 so strings 层无 dcxll → 可能性仅剩 native 运行时解密/拼接字符串，列为本项最大不确定点')
    elif not hits and so_hit_lines:
        rep.append('- Java 层 0 引用但 so strings 有命中 → 消费在 native 层，明细见上表；语义解读见 W3 三 so 深查')
    rep.append('')
    with open(os.path.join(OUT, 'dm5-dcxll-consumer.md'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(rep) + '\n')

    print('[dm5] java_hits=%d consumers=%d so_hits=%d entries=%d'
          % (len(hits), len(consumers), len(so_hit_lines), len(rows)))


if __name__ == '__main__':
    main()
