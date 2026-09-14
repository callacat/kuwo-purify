#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""DM-1 W2：东明版去广告点位 × 天天版交叉 + ad 桶掐净度

回答的问题（派单 DM-1 §W2）：东明的去广告刀做在哪几刀、与天天版是否同一把刀、
广告 SDK 面掐净没有——不是「有没有做」。只呈现状事实，禁止 A/B/C/D 分类与好坏定性。

口径红线：
  ①归一化/体首实指令与 W1 同源——直接 import dm1_method_diff 的
    norm_body/METHOD_RE/RETURN_RE/is_special/sig_of_hdr/parse_methods/index_smali，
    绝不另写第二套（两侧口径一致是交叉成立的前提）。
  ②分桶正则 = DM-1 派单原文桶正则小写化（mobilead|ad.|ads|splash|BirthScreen|
    banner|interstitial|freemium|specialdialog|uilib.m 等，含天天版实见 tmeads）；
    优先序 ad > hippy > update > other。com/dm/ 作者自带类命中 update 正则时
    按「作者更新通道」单列，不计入「官方更新刀」。
  ③天天版截断 = kuwo1-diff-baksmali 归档 changed/ 分段：[MOD-CHANGED] 段与其配对的
    [BASE-ORIGINAL] 段分别 dm1.norm_body 归一化取体首实指令（跳过 :LBL），
    mod 首=return-* 且 base 首非 return 且非 native/abstract → 截断点 (class_key, sig)。
    added_nop 桩 = [MOD-ADDED] 段（及 added/ 整文件类）体首=return-* 且非 native/abstract
    且归一化行数 ≤2。
  ④残活扫描表驱动：只解析 ad 桶路径命中的类（mod 归档），不暴力扫全树（D7 红线）。
  ⑤交叉三分：(class_key, method_sig) 为键——东明截断 ∩ 天天截断 = 组内共享刀；
    仅东明 = 东明独有刀；仅天天 = 天天有东明无。

输入（WORK=work 目录绝对路径；传入其父目录时自动下钻 work/）：
  WORK/in1/dm1-return-truncated.tsv   class_key method_sig base_first mod_first mod_hdr
  WORK/in1/dm1-method-changes.tsv     class_key method_sig kind base_lines mod_lines base_first mod_first
  WORK/in1/dm1-new-classes.tsv        class_key dexes
  WORK/in1/dm1-smali-mod.tar.gz       （或已解出 WORK/smali-mod/，顶层 smali-mod/<dex>/<pkg>/X.smali）
  WORK/intt/kuwo1-diff-baksmali.tar.gz（或已解出 WORK/intt/kuwo1-diff-baksmali/，{changed,added,removed}/…）
输出（WORK/dm-out/）：
  dm2-trunc-buckets.tsv  class_key sig bucket base_first mod_first
  dm2-cross.tsv          class_key sig dm_trunc tt_trunc verdict(shared|dm_only|tt_only)
  dm2-ad-residual.tsv    class_key status(killed|touched|untouched) 入口方法(;分隔≤20)
  dm2-ad-surface.md      主报告（关键数字摘要 + 四张表全文 + 现状结论句）
收口：print '[dm2] trunc=… shared=… …' 一行供 workflow 断言。
"""
import os
import re
import sys
import tarfile
from collections import Counter

# —— 先解析 WORK（dm1 模块级会按 sys.argv[1] 建 OUT，须先把参数修正为真实 work 目录）——
WORK = sys.argv[1] if len(sys.argv) > 1 else 'work'
if not os.path.isdir(os.path.join(WORK, 'in1')) and \
        os.path.isdir(os.path.join(WORK, 'work', 'in1')):
    WORK = os.path.join(WORK, 'work')
if len(sys.argv) > 1:
    sys.argv[1] = WORK
else:
    sys.argv.append(WORK)

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dm1_method_diff as dm1  # 同源复用（见 docstring 红线①）

IN1 = os.path.join(WORK, 'in1')
INTT = os.path.join(WORK, 'intt')
OUT = os.path.join(WORK, 'dm-out')
os.makedirs(OUT, exist_ok=True)

# —— ② 分桶正则（派单原文小写化；优先序 ad > hippy > update > other）——
AD_RE = re.compile(r'mobilead|/ad\.|/ad/|(^|/)ad[._/]|ads|splash|birthscreen|'
                   r'banner|interstitial|freemium|specialdialog|uilib/m\.|tmeads')
HIPPY_RE = re.compile(r'hippy')
UPDATE_RE = re.compile(r'update|upgrade|checkversion|versioncheck|rfix|hotfix')
AUTHOR_RE = re.compile(r'^com/dm/')  # 作者自带包：update 命中时单列为「作者更新通道」


def bucket_of(class_key):
    k = class_key.lower()
    if AD_RE.search(k):
        return 'ad'
    if HIPPY_RE.search(k):
        return 'hippy'
    if UPDATE_RE.search(k):
        return 'update'
    return 'other'


# 入口判定（残活重点表）：方法名 ^(init|start|show|load|onCreate|bindData|render)
# 或含 Ad 且非 getter/setter。
ENTRY_HEAD_RE = re.compile(r'^(init|start|show|load|onCreate|bindData|render)')
GETSET_RE = re.compile(r'^(get|set)[A-Z]')


def is_entry_sig(sig):
    name = sig.partition('(')[0]
    if ENTRY_HEAD_RE.match(name):
        return True
    return 'Ad' in name and not GETSET_RE.match(name)


def read_tsv(path, ncols):
    if not os.path.isfile(path):
        sys.exit('FATAL: 缺输入 %s（先跑 W1 dm-dex-method-diff）' % path)
    rows = []
    with open(path, encoding='utf-8') as f:
        f.readline()  # 表头丢弃
        for line in f:
            line = line.rstrip('\n')
            if not line:
                continue
            r = line.split('\t')
            r += [''] * (ncols - len(r))
            rows.append(r[:ncols])
    return rows


def extract_if_absent(tar_path, cand_dir, tmp_root, topname):
    """优先用 workflow 已解出的目录；否则脚本自解 tar（顶层名不符 topname 时取公共顶层）。"""
    if os.path.isdir(cand_dir):
        return cand_dir
    if not os.path.isfile(tar_path):
        sys.exit('FATAL: 归档与解出目录皆无：%s / %s' % (cand_dir, tar_path))
    os.makedirs(tmp_root, exist_ok=True)
    with tarfile.open(tar_path, 'r:gz') as tf:
        names = tf.getnames()
        top = os.path.commonpath(names) if names else topname
        try:
            tf.extractall(tmp_root, filter='data')
        except TypeError:  # 老 py 无 filter 参数
            tf.extractall(tmp_root)
    p = os.path.join(tmp_root, topname)
    if not os.path.isdir(p):
        p = os.path.join(tmp_root, top)
    if not os.path.isdir(p):
        sys.exit('FATAL: 归档顶层结构不符预期：%s（期望 %s/）' % (tar_path, topname))
    return p


def rel_key(path, root):
    """相对路径（posix 风格、去 .smali 后缀）= class_key，与 dm1.index_smali 同口径。"""
    rel = os.path.relpath(path, root)
    parts = rel.split(os.sep)
    stem = parts[-1]
    if stem.endswith('.smali'):
        parts[-1] = stem[:-6]
    return '/'.join(parts)


# —— ③ 天天版分段归档解析（格式承 kuwo1_diff.py，切段逻辑承 kuwo3a_adsurface.py）——
TAGLINE = {'[MOD-ADDED]': 'ADDED', '[MOD-CHANGED]': 'CHG_MOD',
           '[BASE-ORIGINAL]': 'CHG_BASE', '[BASE-REMOVED-IN-MOD]': 'REMOVED'}


def split_segments(path):
    """yield (hdr, tag, body_lines)。顶层段头 = .method 行且下一非空行为 TAG 行；
    CHG_MOD 段体在 [BASE-ORIGINAL] 处切成 CHG_BASE 段（同 hdr）。"""
    with open(path, encoding='utf-8', errors='replace') as f:
        lines = f.read().split('\n')
    segs = []
    i, n = 0, len(lines)
    while i < n:
        m = dm1.METHOD_RE.match(lines[i].strip())
        if m:
            j = i + 1
            while j < n and not lines[j].strip():
                j += 1
            if j < n and lines[j].strip() in TAGLINE:
                tag = TAGLINE[lines[j].strip()]
                hdr = m.group(1).strip()
                body = []
                k = j + 1
                while k < n:
                    m2 = dm1.METHOD_RE.match(lines[k].strip())
                    if m2:
                        j2 = k + 1
                        while j2 < n and not lines[j2].strip():
                            j2 += 1
                        if j2 < n and lines[j2].strip() in TAGLINE:
                            break  # 新段头
                    if tag == 'CHG_MOD' and lines[k].strip() == '[BASE-ORIGINAL]':
                        segs.append((hdr, tag, body))
                        tag = 'CHG_BASE'
                        body = []
                        k += 1
                        continue
                    body.append(lines[k])
                    k += 1
                segs.append((hdr, tag, body))
                i = k
                continue
        i += 1
    return segs


def body_first(body_lines):
    """归档段体 →（norm 行列表, 体首实指令）。体内自含的 .method 头行先滤掉
    （kuwo1_diff 写档时 body 复带了 .method 行），其余噪声交 dm1.norm_body；
    体首实指令口径与 dm1.parse_methods 完全一致（跳 :LBL）。"""
    cleaned = [ln for ln in body_lines if not ln.strip().startswith('.method')]
    norm = dm1.norm_body(cleaned)
    first = next((l for l in norm if not l.startswith(':')),
                 ':LBL' if norm else '(empty)')
    return norm, first


def walk_smali(root):
    if not os.path.isdir(root):
        return
    for d, _, fs in os.walk(root):
        for f in fs:
            if f.endswith('.smali'):
                yield os.path.join(d, f)


def main():
    # —— 1. W1 产物 ——
    trunc_rows = read_tsv(os.path.join(IN1, 'dm1-return-truncated.tsv'), 5)
    changes_rows = read_tsv(os.path.join(IN1, 'dm1-method-changes.tsv'), 7)
    new_rows = read_tsv(os.path.join(IN1, 'dm1-new-classes.tsv'), 2)

    dm_trunc = []  # (key, sig, base_first, mod_first)
    dm_trunc_set = {}
    for k, sig, bf, mf, _hdr in trunc_rows:
        dm_trunc.append((k, sig, bf, mf))
        dm_trunc_set[(k, sig)] = (bf, mf)
    changes_set = {}
    for k, sig, kind, _bl, _ml, _bf, _mf in changes_rows:
        changes_set.setdefault(k, []).append((sig, kind))
    new_keys = set(k for k, _d in new_rows)

    # —— 2. 解包（workflow 已解则直接用，缺目录脚本兜底自解）——
    mod_root = extract_if_absent(os.path.join(IN1, 'dm1-smali-mod.tar.gz'),
                                 os.path.join(WORK, 'smali-mod'),
                                 os.path.join(WORK, 'dm2-tmp-mod'), 'smali-mod')
    tt_root = extract_if_absent(os.path.join(INTT, 'kuwo1-diff-baksmali.tar.gz'),
                                os.path.join(INTT, 'kuwo1-diff-baksmali'),
                                os.path.join(WORK, 'dm2-tmp-tt'), 'kuwo1-diff-baksmali')
    tt_changed = os.path.join(tt_root, 'changed')
    tt_added = os.path.join(tt_root, 'added')

    # —— 3. 天天版截断集与 added_nop 桩 ——
    tt_trunc = {}          # (key, sig) -> (base_first, mod_first)
    tt_stub = []           # (key, sig) 空桩
    n_chg_pair_anom = 0    # CHG_MOD 缺 [BASE-ORIGINAL] 配对（格式异常计数，如实登记）
    for p in walk_smali(tt_changed):
        key = rel_key(p, tt_changed)
        by = {}
        for hdr, tag, body in split_segments(p):
            by.setdefault(hdr, {}).setdefault(tag, []).extend(body)
        for hdr, tags in by.items():
            sig = dm1.sig_of_hdr(hdr)
            special = dm1.is_special(hdr)
            if 'CHG_MOD' in tags:
                if 'CHG_BASE' not in tags:
                    n_chg_pair_anom += 1
                else:
                    _mn, mfirst = body_first(tags['CHG_MOD'])
                    _bn, bfirst = body_first(tags['CHG_BASE'])
                    if (not special) and dm1.RETURN_RE.match(mfirst) \
                            and not dm1.RETURN_RE.match(bfirst):
                        tt_trunc[(key, sig)] = (bfirst, mfirst)
            if 'ADDED' in tags:
                mn, mfirst = body_first(tags['ADDED'])
                if (not special) and dm1.RETURN_RE.match(mfirst) and len(mn) <= 2:
                    tt_stub.append((key, sig))
    for p in walk_smali(tt_added):
        key = rel_key(p, tt_added)
        for sig, mth in dm1.parse_methods(p).items():
            if (not mth['special']) and dm1.RETURN_RE.match(mth['first']) \
                    and len(mth['norm']) <= 2:
                tt_stub.append((key, sig))

    # —— 4. 交叉三分 ——
    cross_rows = []
    n_shared = n_dm_only = n_tt_only = 0
    for k, sig in sorted(set(dm_trunc_set) | set(tt_trunc)):
        d, t = (k, sig) in dm_trunc_set, (k, sig) in tt_trunc
        v = 'shared' if d and t else ('dm_only' if d else 'tt_only')
        n_shared += v == 'shared'
        n_dm_only += v == 'dm_only'
        n_tt_only += v == 'tt_only'
        cross_rows.append((k, sig, '1' if d else '0', '1' if t else '0', v))

    # —— 5. 东明截断分桶 ——
    bucket_rows = []
    bucket_cnt = Counter()
    ad_trunc_keys = set()
    for k, sig, bf, mf in dm_trunc:
        b = bucket_of(k)
        bucket_cnt[b] += 1
        bucket_rows.append((k, sig, b, bf, mf))
        if b == 'ad':
            ad_trunc_keys.add(k)
    # update 桶单列：作者通道 vs 官方刀
    upd_official = [(k, sig) for k, sig, b, _1, _2 in bucket_rows
                    if b == 'update' and not AUTHOR_RE.match(k)]
    upd_author = [(k, sig) for k, sig, b, _1, _2 in bucket_rows
                  if b == 'update' and AUTHOR_RE.match(k)]
    hippy_trunc = [(k, sig, dm_trunc_set[(k, sig)]) for k, sig, b, _1, _2 in bucket_rows
                   if b == 'hippy']
    # —— 5b. hippy 桶 path 级命中列表（method-changes 侧）——
    hippy_changes = [(k, sig, kind) for k, sigs in changes_set.items()
                     if 'hippy' in k.lower() for sig, kind in sigs]

    # —— 6. ad 桶残活（表驱动：只解析 mod 归档里 ad 命中路径的类）——
    mod_idx = dm1.index_smali(mod_root)
    ad_keys = sorted(k for k in mod_idx if AD_RE.search(k.lower()))
    residual_rows = []
    n_killed = n_touched = n_untouched = 0
    focus_rows = []  # 未动且有入口 = 重点残活
    touched_or_trunc_cls = set(changes_set) | {k for k, _s in dm_trunc_set}
    for k in ad_keys:
        mth = dm1.parse_methods(mod_idx[k][0])
        killed = [sig for sig, m in mth.items()
                  if (not m['special']) and dm1.RETURN_RE.match(m['first'])]
        entries = sorted(sig for sig in mth if is_entry_sig(sig))
        if killed:
            st = 'killed'
            n_killed += 1
        elif k in changes_set:
            st = 'touched'
            n_touched += 1
        else:
            st = 'untouched'
            n_untouched += 1
            if entries:
                focus_rows.append((k, entries))
        residual_rows.append((k, st, ';'.join(entries[:20]) or '—'))
    n_resid_alive = n_touched + n_untouched
    n_resid_alive_with_entry = sum(1 for _k, st, e in residual_rows
                                   if st != 'killed' and e != '—')

    # —— 7. hippy 桶掐净度 + update 桶对照 + 作者通道事实 ——
    hippy_mod_keys = sorted(k for k in mod_idx if 'hippy' in k.lower())
    n_hippy_total = len(hippy_mod_keys)
    hippy_hit = [k for k in hippy_mod_keys if k in touched_or_trunc_cls]
    n_hippy_hit = len(hippy_hit)
    upd_shared = sum(1 for k, s in upd_official if (k, s) in tt_trunc)
    upd_tt_only = sorted((k, s) for k, s in tt_trunc
                         if (k, s) not in dm_trunc_set and bucket_of(k) == 'update'
                         and not AUTHOR_RE.match(k))
    dia_o_present = 'com/dm/dia/o' in new_keys
    n_dm_new = sum(1 for k in new_keys if k.startswith('com/dm/'))

    # —— 8. 落盘 TSV ——
    def w_tsv(name, header, rows):
        with open(os.path.join(OUT, name), 'w', encoding='utf-8') as f:
            f.write('\t'.join(header) + '\n')
            for r in rows:
                f.write('\t'.join(str(x) for x in r) + '\n')

    w_tsv('dm2-trunc-buckets.tsv',
          ('class_key', 'sig', 'bucket', 'base_first', 'mod_first'), bucket_rows)
    w_tsv('dm2-cross.tsv',
          ('class_key', 'sig', 'dm_trunc', 'tt_trunc', 'verdict'), cross_rows)
    w_tsv('dm2-ad-residual.tsv',
          ('class_key', 'status', 'entry_sigs'), residual_rows)

    # —— 9. 主报告 ——
    L = []
    L.append('# DM-1 W2 东明版去广告点位 × 天天版交叉报告\n')
    L.append('> 口径：截断判定/归一化/体首实指令与 W1 完全同源（import dm1_method_diff）；')
    L.append('> 分桶=DM-1 派单原文正则小写化（优先序 ad>hippy>update>other，com/dm/ 作者类 update 命中单列）；')
    L.append('> 天天版侧=kuwo1-diff-baksmali 归档 [MOD-CHANGED]×[BASE-ORIGINAL] 配对，同一归一化。')
    L.append('> 本报告只呈现状事实（刀位/交叉/残活），无 A/B/C/D 分类与好坏定性，判定权在主控。\n')
    L.append('## 关键数字摘要\n')
    L.append('| 指标 | 数 |')
    L.append('|---|---|')
    L.append('| 东明体首 return 截断（总数） | %d |' % len(dm_trunc))
    L.append('| ├ ad 桶刀 | %d |' % bucket_cnt['ad'])
    L.append('| ├ hippy 桶刀 | %d |' % bucket_cnt['hippy'])
    L.append('| ├ update 桶刀（官方，排除 com/dm/ 作者类） | %d |' % len(upd_official))
    L.append('| ├ update 桶刀（com/dm/ 作者类，单列） | %d |' % len(upd_author))
    L.append('| └ other 桶刀 | %d |' % bucket_cnt['other'])
    L.append('| 交叉：组内共享刀 | %d |' % n_shared)
    L.append('| 交叉：东明独有刀 | %d |' % n_dm_only)
    L.append('| 交叉：天天有东明无刀 | %d |' % n_tt_only)
    L.append('| 天天版截断集总数（归档口径） | %d |' % len(tt_trunc))
    L.append('| 天天版 return-* 空桩（MOD-ADDED/added，norm≤2 行） | %d |' % len(tt_stub))
    if n_chg_pair_anom:
        L.append('| ⚠ 归档 CHG_MOD 缺 BASE 配对段（格式异常，未计截断） | %d |' % n_chg_pair_anom)
    L.append('| ad 桶类（东明全量归档路径命中） | %d |' % len(ad_keys))
    L.append('| ├ 已掐（含体首 return-* 方法，非 native/abstract） | %d |' % n_killed)
    L.append('| ├ 动过未掐净（进 dm1-method-changes） | %d |' % n_touched)
    L.append('| └ 未动 | %d（其中 %d 类有入口方法=重点残活） |' % (n_untouched, len(focus_rows)))
    L.append('| hippy 掐净度 | 归档命中 %d 类，被掐/动 %d 类 |' % (n_hippy_total, n_hippy_hit))
    L.append('| 作者更新通道事实 | 新增类含 `com/dm/dia/o`：%s；com/dm/* 新增 %d 类 |'
             % ('是' if dia_o_present else '否', n_dm_new))
    L.append('')

    L.append('## 表1 东明截断分桶（dm2-trunc-buckets.tsv 全文）\n')
    L.append('| 类 | 方法 | 桶 | base体首 | mod体首 |')
    L.append('|---|---|---|---|---|')
    for k, sig, b, bf, mf in bucket_rows:
        L.append('| `%s` | `%s` | %s | `%s` | `%s` |' % (k, sig, b, bf, mf))

    L.append('\n## 表2 与天天版三分交叉（dm2-cross.tsv 全文，verdict=shared|dm_only|tt_only）\n')
    L.append('| 类 | 方法 | 东明掐 | 天天掐 | verdict |')
    L.append('|---|---|---|---|---|')
    for k, sig, d, t, v in cross_rows:
        L.append('| `%s` | `%s` | %s | %s | %s |' % (k, sig, d, t, v))

    L.append('\n## 表3 ad 桶残活（dm2-ad-residual.tsv 全文；killed=掐净 touched=动过未掐净 untouched=未动）\n')
    L.append('| 类 | status | 入口方法（≤20） |')
    L.append('|---|---|---|')
    for k, st, e in residual_rows:
        L.append('| `%s` | %s | `%s` |' % (k, st, e))
    L.append('\n### 表3b 重点残活（未动 且 有公开 init/showAd/show/start 类入口方法）\n')
    if focus_rows:
        for k, entries in focus_rows:
            L.append('- `%s` → %s' % (k, '; '.join('`%s`' % e for e in entries[:20])))
    else:
        L.append('（无——未动的 ad 桶类均无入口方法命中）')

    L.append('\n## 表4 hippy / update 桶明细与事实链\n')
    L.append('### 4.1 hippy 桶\n')
    L.append('- 东明 hippy 截断刀 %d 处：' % len(hippy_trunc))
    for k, sig, (bf, mf) in hippy_trunc:
        L.append('  - `%s` `%s`（base `%s` → mod `%s`）' % (k, sig, bf, mf))
    if not hippy_trunc:
        L.append('  - （无）')
    L.append('- 东明 method-changes 中 hippy 命中 %d 处（动过面；仅列前 100）：'
             % len(hippy_changes))
    for k, sig, kind in hippy_changes[:100]:
        L.append('  - `%s` `%s` [%s]' % (k, sig, kind))
    L.append('- 归档 path 级含 hippy 类共 %d 个，其中被东明掐/动 %d 个。' % (n_hippy_total, n_hippy_hit))
    L.append('')
    L.append('### 4.2 update 桶\n')
    L.append('- 官方 update 截断（东明）%d 刀，其中与天天共享 %d，东明独有 %d，天天有东明无 %d：'
             % (len(upd_official), upd_shared, len(upd_official) - upd_shared, len(upd_tt_only)))
    for k, s in upd_tt_only:
        L.append('  - tt_only `%s` `%s`' % (k, s))
    L.append('- 作者通道单列（com/dm/ 命中 update 正则，不计官方刀）%d 处：' % len(upd_author))
    for k, s in upd_author:
        L.append('  - `%s` `%s`' % (k, s))
    L.append('- 事实链（只记不判）：「官方更新被掐点位」（上列官方 update 刀）与「作者更新保留」'
             '（新增类含 `com/dm/dia/o`=%s，com/dm/* 新增 %d 类）并存。'
             % ('是' if dia_o_present else '否', n_dm_new))
    L.append('')
    L.append('## 结论（现状描述）\n')
    L.append('> 东明去广告刀集中在 %d 类共 %d 刀（ad 桶截断，其中 %d 刀与天天版同 (类,方法) 点位）；'
             '广告 SDK 面残活 %d 类（ad 桶动过未掐净 %d + 未动 %d），其中入口在跑的 %d 类。'
             % (len(ad_trunc_keys), bucket_cnt['ad'],
                sum(1 for k, s, b, _1, _2 in bucket_rows if b == 'ad' and (k, s) in tt_trunc),
                n_resid_alive, n_touched, n_untouched, n_resid_alive_with_entry))
    with open(os.path.join(OUT, 'dm2-ad-surface.md'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(L) + '\n')

    print('[dm2] trunc=%d shared=%d dm_only=%d tt_only=%d ad_killed=%d ad_touched=%d '
          'ad_untouched=%d hippy=%d update=%d'
          % (len(dm_trunc), n_shared, n_dm_only, n_tt_only,
             n_killed, n_touched, n_untouched, len(hippy_trunc), len(upd_official)))


if __name__ == '__main__':
    main()
