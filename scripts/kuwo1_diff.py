#!/usr/bin/env python3
# KUWO-1：mod 15dex vs 官方基线全量 diff（baksmali 后按类名对齐）
# 口径继承番茄 16a / 红果 HG-1 两轮修正方法论：
#   ①调试指令剥离（.line/.prologue/.local/.source，保留 .catch）
#   ②类名对齐排除 dex 挪位噪声（直接改包重签必然重排 dex）
#   ③红线（hg2 端点大漂移误报教训）：两侧集合基准必须一致——
#     双侧都取 APK 内全部 classes*.dex 的反编译全集，不做任何单侧过滤。
# 输入：work/smali-mod/ 与 work/smali-base/（每 dex 一个子目录）
# 输出：work/diff-out/docs/kuwo1-diff-report.md + kuwo1-diff-baksmali/(added|changed|removed)/
#      work/added-classes.txt work/removed-classes.txt work/changed-classes.txt
import os, re, sys, shutil

work = sys.argv[1]
MOD = os.path.join(work, 'smali-mod')
BASE = os.path.join(work, 'smali-base')
OUTD = os.path.join(work, 'diff-out', 'docs')
BAK = os.path.join(OUTD, 'kuwo1-diff-baksmali')
os.makedirs(BAK, exist_ok=True)
for s in ('added', 'changed', 'removed'):
    os.makedirs(os.path.join(BAK, s), exist_ok=True)

METHOD_RE = re.compile(r'^\.method\s+(.+)$')
DEBUG_RE = re.compile(r'^\s*\.(line|prologue|local|end local|restart local|source)\b')

def collect_by_classname(root):
    """类名(去 dex 前缀) -> [绝对路径, 来源dex列表]。同名跨 dex 冲突会记录。"""
    idx = {}
    for droot, _, fs in os.walk(root):
        for f in fs:
            if not f.endswith('.smali'):
                continue
            abs_p = os.path.join(droot, f)
            rel = os.path.relpath(abs_p, root)
            parts = rel.split(os.sep)
            dexn = parts[0] if len(parts) > 1 else 'classes'
            key = os.path.join(*parts[1:]) if len(parts) > 1 else rel
            if key in idx:
                idx[key][1].append(dexn)
            else:
                idx[key] = [abs_p, [dexn]]
    return idx

def norm_method_body(text):
    out = []
    for line in text.split('\n'):
        s = line.strip()
        if DEBUG_RE.match(line) or not s:
            continue
        out.append(s)
    return '\n'.join(out)

def parse_methods(path):
    methods, order = {}, []
    cur_name, cur_buf = None, None
    with open(path, encoding='utf-8', errors='replace') as f:
        for line in f:
            m = METHOD_RE.match(line.strip())
            if m:
                cur_name = m.group(1).strip()
                cur_buf = [line]
            elif cur_name is not None:
                cur_buf.append(line)
                if line.strip() == '.end method':
                    body = norm_method_body(''.join(cur_buf))
                    if cur_name in methods:
                        cur_name += ' #DUP'
                    methods[cur_name] = body
                    order.append(cur_name)
                    cur_name, cur_buf = None, None
    return methods, order

mod = collect_by_classname(MOD)
base = collect_by_classname(BASE)

mod_conflict = {k: v[1] for k, v in mod.items() if len(v[1]) > 1}
base_conflict = {k: v[1] for k, v in base.items() if len(v[1]) > 1}

mod_keys = set(mod)
base_keys = set(base)
added = sorted(mod_keys - base_keys)
removed = sorted(base_keys - mod_keys)

method_stats = []          # (类名, a, r, c)
total_a = total_r = total_c = 0
changed_cls = []
for key in sorted(mod_keys & base_keys):
    bm, _ = parse_methods(base[key][0])
    mm, order = parse_methods(mod[key][0])
    a = [n for n in mm if n not in bm]
    r = [n for n in bm if n not in mm]
    c = [n for n in mm if n in bm and mm[n] != bm[n]]
    if a or r or c:
        changed_cls.append(key)
        total_a += len(a); total_r += len(r); total_c += len(c)
        dst = os.path.join(BAK, 'changed', key)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        with open(dst, 'w', encoding='utf-8') as out:
            out.write(f'## {key}\n# added={len(a)} removed={len(r)} changed={len(c)}\n\n')
            for n in a:
                out.write(f'.method {n}\n[MOD-ADDED]\n{mm[n]}\n\n')
            for n in c:
                out.write(f'.method {n}\n[MOD-CHANGED]\n{mm[n]}\n[BASE-ORIGINAL]\n{bm[n]}\n\n')
            for n in r:
                out.write(f'.method {n}\n[BASE-REMOVED-IN-MOD]\n{bm[n]}\n\n')

for key in added:
    dst = os.path.join(BAK, 'added', key)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.copyfile(mod[key][0], dst)
for key in removed:
    dst = os.path.join(BAK, 'removed', key)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.copyfile(base[key][0], dst)

for name, keys in (('added-classes.txt', added), ('changed-classes.txt', changed_cls), ('removed-classes.txt', removed)):
    with open(os.path.join(work, name), 'w', encoding='utf-8') as f:
        f.write('\n'.join(keys) + '\n')

report = ['# KUWO-1 mod vs 官方基线 dex 全量 diff 报告', '',
          '> 样本: kuwo-12.2.2.0-tiantian-mod.apk（15 dex，CN=xinshidai0 重签）',
          '> 基线: kuwo-12.2.2.0-official.apk（集合口径：双侧同为 APK 全量 classes*.dex，红线对齐，防 hg2 式漂移误报）',
          '> 方法=类名对齐+调试指令剥离（继承番茄 16a / 红果 HG-1 修正口径）。分类判定权在老马，本报告只出素材。', '',
          '## 1. 总览', '',
          f'- mod 类总数: {len(mod_keys)} ｜ 官方基线类总数: {len(base_keys)}',
          f'- **真新增类: {len(added)}**（全文见 kuwo1-diff-baksmali/added/）',
          f'- **真删除类: {len(removed)}**（全文见 kuwo1-diff-baksmali/removed/）',
          f'- **修改类: {len(changed_cls)}**（差异方法全文见 kuwo1-diff-baksmali/changed/，[MOD-ADDED]/[MOD-CHANGED vs BASE-ORIGINAL]/[BASE-REMOVED-IN-MOD] 三段标注）',
          f'- 修改类中差异方法: 新增 {total_a} / 删除 {total_r} / 修改 {total_c}', '',
          f'- 跨 dex 重复类名（mod）: {len(mod_conflict)} ｜（base）: {len(base_conflict)}（应为 0，非 0 需红旗解释）', '',
          '## 2. 真新增类清单（按包前缀分组）', '']
groups = {}
for key in added:
    stem = key[:-6] if key.endswith('.smali') else key
    pkg = '/'.join(stem.split('/')[:-1])
    top = '/'.join(pkg.split('/')[:2]) if pkg else '(root)'
    groups.setdefault(top, []).append(key)
for top in sorted(groups, key=lambda x: -len(groups[x])):
    report.append(f'### `{top}/` — {len(groups[top])} 类')
    for k in groups[top]:
        report.append(f'- `{k}`')
    report.append('')
report += ['## 3. 修改类清单（按差异方法总数降序）', '',
           '| 类 | +新增 | -删除 | ~修改 | 合计 |', '|---|---|---|---|---|']
for key, a, r, c in sorted(method_stats, key=lambda x: -(x[1]+x[2]+x[3])):
    report.append(f'| `{key}` | {a} | {r} | {c} | {a+r+c} |')
report += ['', '## 4. 真删除类清单', '']
if removed:
    for key in removed:
        report.append(f'- `{key}`')
else:
    report.append('（无——mod 未删除任何基线类）')
report += ['', '## 5. 归档结构', '',
           '```', 'kuwo1-diff-baksmali/', '├── added/    真新增类 baksmali 全文', '├── changed/  修改类差异方法全文（三段标注）', '└── removed/  删除类基线全文', '```', '']
with open(os.path.join(OUTD, 'kuwo1-diff-report.md'), 'w', encoding='utf-8') as f:
    f.write('\n'.join(report))

print(f'KUWO1-DIFF added={len(added)} removed={len(removed)} changed={len(changed_cls)} (+{total_a}/-{total_r}/~{total_c})')
print(f'KUWO1-DIFF mod_cls={len(mod_keys)} base_cls={len(base_keys)} conflict_mod={len(mod_conflict)} conflict_base={len(base_conflict)}')
print(f'baksmali 归档文件数: {sum(len(fs) for _,_,fs in os.walk(BAK))}')
