#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""DM-1 W1：东明版 vs 官方基线 方法级全量 diff（baksmali 双侧、类名对齐同集合）

口径红线（派单 §1-W1 + 老线 hg2 漂移教训）：
  ①双侧同集合 = 两侧都取 APK 内全部 classes*.dex 的反编译全集（东明 18dex / 官方 15dex），
    按类路径对齐；红旗计数只用双侧同名类同名方法的交集口径，绝不拿「一侧全量−一侧交集」充当。
  ②归一化剥重编译噪声：:cond/:goto/:try_start/:try_end/:catch_all/:catch/:sswitch 等标签→:LBL；
    const-string(/jumbo) 归一；invoke-*(/range) 归一；move/iget/iput/sget/sput/move-result/cmp* 宽度后缀归一；
    .registers/.param/.annotation(含块)/.line/.catch(All)/.prologue/.local/.source/.implicit/裸0x载荷/整行与行内#注释 滤除；
    v 寄存器按首现次序重编号（V0,V1,…，引号外），p 寄存器保留（由签名决定、跨侧重编号稳定）。
  ③高信噪「体首 return 截断」专表：双侧同名方法、mod 体首实指令=return-* 且 base 体首非 return
    且 mod 方法非 native/abstract。
输入：work/smali-mod/<dex>/<pkg>/X.smali 与 work/smali-base/<dex>/<pkg>/X.smali
输出（work/dm-out/）：
  dm1-method-changes.tsv   class_key \t method_sig \t kind \t base_lines \t mod_lines \t base_first \t mod_first
                           kind ∈ changed | added_method | removed_method
  dm1-return-truncated.tsv class_key \t method_sig \t base_first \t mod_first \t mod_hdr
  dm1-new-classes.tsv      class_key \t dexes
  dm1-removed-classes.tsv  class_key \t dexes
  dm1-stats.md             口径与总数账
  dm1-dex-method-diff.md   主报告（含截断专表）
"""
import os
import re
import sys

WORK = sys.argv[1] if len(sys.argv) > 1 else 'work'
MOD = os.path.join(WORK, 'smali-mod')
BASE = os.path.join(WORK, 'smali-base')
OUT = os.path.join(WORK, 'dm-out')
os.makedirs(OUT, exist_ok=True)

METHOD_RE = re.compile(r'^\.method\s+(.+)$')
PROTO_RE = re.compile(r'([^\s(]+)\(([^)]*)\)(\S+)$')
# 指令级噪声滤除（annotation 块另在解析器里整块跳）
SKIP_DIR_RE = re.compile(
    r'^\.(registers|param|line|catch|catchall|prologue|local|restart local|end local|source|'
    r'packed-switch|sparse-switch|end packed-switch|end sparse-switch|implicit)\b')
PAYLOAD_HEX_RE = re.compile(r'^0x[0-9a-fA-F]{1,8}$')
RETURN_RE = re.compile(r'^return(?:-[\w./]+)?\b')
FAM_RE = re.compile(
    r'^(move|move-result|move-result-object|move-result-wide|iget|iput|sget|sput|cmp|cmpg|cmpl|const-string)'
    r'(?:[-/][a-z0-9]+)+$')
INVOKE_RE = re.compile(r'^invoke-([a-z]+)(?:/range)?$')


def quote_split(s):
    """切分为 (文本, 是否在引号内) 段序列，\" 转义不误判。"""
    segs, buf, inq, i = [], [], False, 0
    while i < len(s):
        c = s[i]
        if c == '"':
            back, j = 0, i - 1
            while j >= 0 and s[j] == '\\':
                back, j = back + 1, j - 1
            if back % 2 == 0:
                segs.append((''.join(buf), inq))
                buf = []
                inq = not inq
            else:
                buf.append(c)
        else:
            buf.append(c)
        i += 1
    segs.append((''.join(buf), inq))
    return segs


def outside(s, fn):
    return ''.join(t if q else fn(t) for t, q in quote_split(s))


def strip_comment(s):
    return outside(s, lambda t: t.split('#', 1)[0]).rstrip()


def sig_of_hdr(hdr):
    m = PROTO_RE.search(hdr.strip())
    return '%s(%s)%s' % m.groups() if m else hdr.strip()


def is_special(hdr):
    h = ' ' + hdr.strip() + ' '
    return ' native ' in h or ' abstract ' in h


def norm_body(lines):
    """归一化方法体：滤噪 + 标签占位 + 助记符归族 + v 寄存器首现序重编号。"""
    regs, out, in_ann = {}, [], False
    for ln in lines:
        s = ln.strip()
        if in_ann:
            if s == '.end annotation':
                in_ann = False
            continue
        if not s or s == '.end method':
            continue
        if s.startswith('.annotation'):
            in_ann = True
            continue
        if SKIP_DIR_RE.match(s) or PAYLOAD_HEX_RE.match(s):
            continue
        s = strip_comment(s)
        if not s:
            continue
        if s.startswith(':'):
            out.append(':LBL')
            continue
        toks = s.split(' ', 1)
        op, rest = toks[0], (toks[1] if len(toks) > 1 else '')
        m = FAM_RE.match(op)
        if m:
            op = m.group(1)
        else:
            mi = INVOKE_RE.match(op)
            if mi:
                op = 'invoke-' + mi.group(1)

        def remap(t):
            def r(mm):
                num = mm.group(1)
                if num not in regs:
                    regs[num] = 'V%d' % len(regs)
                return regs[num]
            return re.sub(r'\bv(\d+)\b', r, t)
        rest = outside(rest, remap) if rest else ''
        out.append((op + ' ' + rest).rstrip())
    return out


def parse_methods(path):
    """返回 OrderedDict: method_sig -> {hdr, special, first, norm, dupn}。同名重复签名以 #DUPn 区分。"""
    meths = {}
    hdr = None
    buf = []
    with open(path, encoding='utf-8', errors='replace') as f:
        for line in f:
            m = METHOD_RE.match(line.strip())
            if m and hdr is None:
                hdr = m.group(1).strip()
                buf = []
                continue
            if hdr is not None:
                if line.strip() == '.end method':
                    body = norm_body(buf)
                    base_sig = sig_of_hdr(hdr)
                    sig = base_sig
                    n = 1
                    while sig in meths:
                        n += 1
                        sig = '%s#DUP%d' % (base_sig, n)
                    # 体首「实」指令：标签占位 :LBL 不是指令，跳过取首条真实指令
                    first = next((l for l in body if not l.startswith(':')),
                                 ':LBL' if body else '(empty)')
                    meths[sig] = {
                        'hdr': hdr,
                        'special': is_special(hdr),
                        'first': first,
                        'norm': body,
                    }
                    hdr = None
                else:
                    buf.append(line)
    return meths


def index_smali(root):
    """class_key(rel path w/o dex 前缀与 .smali 后缀) -> [abs_path, [dex来源...]]。"""
    idx = {}
    for droot, _, fs in os.walk(root):
        for f in fs:
            if not f.endswith('.smali'):
                continue
            p = os.path.join(droot, f)
            rel = os.path.relpath(p, root)
            parts = rel.split(os.sep)
            dexn = parts[0] if len(parts) > 1 else 'classes'
            key = '/'.join(parts[1:])[:-6] if len(parts) > 1 else rel[:-6]
            e = idx.get(key)
            if e is None:
                idx[key] = [p, [dexn]]
            else:
                e[1].append(dexn)
    return idx


def read_bytes(p):
    with open(p, 'rb') as f:
        return f.read()


def main():
    mod = index_smali(MOD)
    base = index_smali(BASE)
    mod_keys, base_keys = set(mod), set(base)
    new_cls = sorted(mod_keys - base_keys)
    gone_cls = sorted(base_keys - mod_keys)
    common = sorted(mod_keys & base_keys)
    mod_conflict = {k: v[1] for k, v in mod.items() if len(v[1]) > 1}
    base_conflict = {k: v[1] for k, v in base.items() if len(v[1]) > 1}

    identical = 0
    changed_files = []
    for k in common:
        mp, bp = mod[k][0], base[k][0]
        b1, b2 = read_bytes(mp), read_bytes(bp)
        if b1 == b2:
            identical += 1
        else:
            changed_files.append(k)

    changes_rows = []
    trunc_rows = []
    n_changed_m = n_added_m = n_removed_m = 0
    for k in changed_files:
        mb = parse_methods(mod[k][0])
        bb = parse_methods(base[k][0])
        for sig in sorted(set(mb) | set(bb)):
            b, mth = bb.get(sig), mb.get(sig)
            if b and mth:
                if b['norm'] != mth['norm']:
                    n_changed_m += 1
                    changes_rows.append((k, sig, 'changed', len(b['norm']), len(mth['norm']),
                                         b['first'], mth['first']))
                # 截断红旗：双侧同签名、mod 非 native/abstract、mod 体首 return-*、base 体首非 return
                if (not mth['special']) and RETURN_RE.match(mth['first']) \
                        and not RETURN_RE.match(b['first']):
                    trunc_rows.append((k, sig, b['first'], mth['first'], mth['hdr']))
            elif mth:
                n_added_m += 1
                changes_rows.append((k, sig, 'added_method', '-', len(mth['norm']), '-', mth['first']))
            else:
                n_removed_m += 1
                changes_rows.append((k, sig, 'removed_method', len(b['norm']), '-', b['first'], '-'))

    def w_tsv(name, header, rows):
        with open(os.path.join(OUT, name), 'w', encoding='utf-8') as f:
            f.write('\t'.join(header) + '\n')
            for r in rows:
                f.write('\t'.join(str(x) for x in r) + '\n')

    w_tsv('dm1-method-changes.tsv',
          ('class_key', 'method_sig', 'kind', 'base_lines', 'mod_lines', 'base_first', 'mod_first'),
          changes_rows)
    w_tsv('dm1-return-truncated.tsv',
          ('class_key', 'method_sig', 'base_first', 'mod_first', 'mod_hdr'), trunc_rows)
    w_tsv('dm1-new-classes.tsv', ('class_key', 'dexes'),
          [(k, ','.join(mod[k][1])) for k in new_cls])
    w_tsv('dm1-removed-classes.tsv', ('class_key', 'dexes'),
          [(k, ','.join(base[k][1])) for k in gone_cls])

    # 包前缀聚合（新增方法面，W2/W4 交叉用）
    from collections import Counter
    newpkg = Counter()
    for k in new_cls:
        parts = k.split('/')
        newpkg['/'.join(parts[:3]) if len(parts) >= 3 else k] += 1

    stats = []
    stats.append('# DM-1 W1 方法级 diff 统计口径（双侧同集合）\n')
    stats.append('| 指标 | 数 | 说明 |')
    stats.append('|---|---|---|')
    stats.append('| 东明版 smali 文件数（全集） | %d | 18 dex 全部 |' % len(mod_keys))
    stats.append('| 官方版 smali 文件数（全集） | %d | 15 dex 全部 |' % len(base_keys))
    stats.append('| 双侧同名对齐类 | %d | 可比集合（红旗只在此口径数） |' % len(common))
    stats.append('| 字节一致（未触碰） | %d | 快路径，免解析 |' % identical)
    stats.append('| 内容差异类（深解析） | %d | 进方法级 diff |' % len(changed_files))
    stats.append('| 新增类（仅东明有） | %d | 与 DM-0「真新增90类」口径应一致或为其超集（同名跨dex算一类） |' % len(new_cls))
    stats.append('| 删除类（仅官方有） | %d | DM-0 结论应为 0，命中即异常 |' % len(gone_cls))
    stats.append('| mod 侧同名类跨 dex 重复 | %d | %s' % (len(mod_conflict), ('样例:' + ';'.join(list(mod_conflict)[:5])) if mod_conflict else '应为0') + ' |')
    stats.append('| base 侧同名类跨 dex 重复 | %d | 应为0 |' % len(base_conflict))
    stats.append('| 语义变化方法（归一化后仍异） | %d | 体级噪声剥离后 |' % n_changed_m)
    stats.append('| 仅 mod 方法 | %d | 差异类内的新增方法 |' % n_added_m)
    stats.append('| 仅 base 方法 | %d | 差异类内被删方法 |' % n_removed_m)
    stats.append('| ★体首 return 截断红旗 | %d | 高信噪作者真实点位 |' % len(trunc_rows))
    stats.append('')
    stats.append('## 新增类按包前缀聚合（top）')
    for pfx, c in newpkg.most_common(30):
        stats.append('- `%s` × %d' % (pfx, c))
    with open(os.path.join(OUT, 'dm1-stats.md'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(stats) + '\n')

    rep = []
    rep.append('# DM-1 W1 东明版 vs 官方 方法级 diff 报告\n')
    rep.append('> 口径：全量双侧同集合（类名对齐，baksmali 双侧全集）；归一化剥重编译噪声后仍异才计「语义变化」；')
    rep.append('> 红旗「体首 return 截断」= 双侧同签名、mod 首实指令 return-* 且 base 首非 return、且 mod 非 native/abstract。')
    rep.append('> 分类判定（A/B/C/D）不在本线职责，本表只给现状事实。\n')
    rep.extend(stats[1:])  # 复用统计块（去掉重复标题）
    rep.append('\n## ★ 体首 return 截断专表（全量，含 base/mod 体首指令）\n')
    rep.append('| 类 | 方法签名 | base体首 | mod体首 |')
    rep.append('|---|---|---|---|')
    for k, sig, bf, mf, hdr in trunc_rows[:2000]:
        rep.append('| `%s` | `%s` | `%s` | `%s` |' % (k, sig, bf, mf))
    if len(trunc_rows) > 2000:
        rep.append('\n（截断表共 %d 行，报告仅列前 2000，全量见 Release 附件 dm1-return-truncated.tsv）' % len(trunc_rows))
    rep.append('\n## 语义变化方法清单（类×方法，全量见 dm1-method-changes.tsv）\n')
    rep.append('| 类 | 方法 | 类型 | base行数 | mod行数 |')
    rep.append('|---|---|---|---|---|')
    for row in changes_rows[:3000]:
        rep.append('| `%s` | `%s` | %s | %s | %s |' % (row[0], row[1], row[2], row[3], row[4]))
    if len(changes_rows) > 3000:
        rep.append('\n（变化清单共 %d 行，报告仅列前 3000，全量见 Release 附件 dm1-method-changes.tsv）' % len(changes_rows))
    rep.append('\n## 内容差异类清单（深解析集）\n')
    for k in changed_files[:1500]:
        rep.append('- `%s`' % k)
    with open(os.path.join(OUT, 'dm1-dex-method-diff.md'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(rep) + '\n')

    print('[dm1] classes mod=%d base=%d common=%d identical=%d changed_files=%d '
          'new_cls=%d gone_cls=%d | methods changed=%d added=%d removed=%d truncated=%d'
          % (len(mod_keys), len(base_keys), len(common), identical, len(changed_files),
             len(new_cls), len(gone_cls), n_changed_m, n_added_m, n_removed_m, len(trunc_rows)))


if __name__ == '__main__':
    main()
