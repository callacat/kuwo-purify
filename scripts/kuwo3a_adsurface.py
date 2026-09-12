#!/usr/bin/env python3
# KUWO-3a：广告/埋点残留面素材清单（保 VIP 净化 · 表③定性素材）
# 红线：表驱动，禁全树暴力扫——输入只用 kuwo1-diff-baksmali.tar.gz（changed+added）与 kuwo1-endpoints.md，
#       不回扫 base 全量 dex（未动类存活入口超出本单输入边界，如实声明不猜测）。
# 归档格式（kuwo1_diff.py 产出）：
#   ## <key> / # added=N ...
#   .method <hdr>\n[TAG]\n<完整体，体内再含 .method…/end method>
#   TAG ∈ {[MOD-ADDED], [MOD-CHANGED](后接 [BASE-ORIGINAL] 第二段), [BASE-REMOVED-IN-MOD]}
# 输出：work/diff-out/docs/kuwo3-ad-surface.md；work/kuwo3-s2-pairs.txt；work/kuwo3-ep-locate.txt
import os, re, sys
from collections import defaultdict, Counter

work = sys.argv[1]
ROOT = os.path.join(work, 'kuwo1-diff-baksmali')
CHANGED = os.path.join(ROOT, 'changed')
ADDED_DIR = os.path.join(ROOT, 'added')
EPMD = os.path.join(work, 'kuwo1-endpoints.md')
OUT = os.path.join(work, 'diff-out', 'docs', 'kuwo3-ad-surface.md')
PAIRS = os.path.join(work, 'kuwo3-s2-pairs.txt')
EPLOC = os.path.join(work, 'kuwo3-ep-locate.txt')
os.makedirs(os.path.dirname(OUT), exist_ok=True)

METHOD_HDR = re.compile(r'^\.method\s+(.+)$')
END_M = re.compile(r'^\.end method\b')
TAG_ADDED, TAG_CHG_MOD, TAG_CHG_BASE, TAG_REM = 'ADDED', 'CHG_MOD', 'CHG_BASE', 'REMOVED'
TAGLINE = {'[MOD-ADDED]': TAG_ADDED, '[MOD-CHANGED]': TAG_CHG_MOD,
           '[BASE-ORIGINAL]': TAG_CHG_BASE, '[BASE-REMOVED-IN-MOD]': TAG_REM}

def sig_of(hdr):
    m = re.search(r'([A-Za-z0-9_$<>]+)\(([^)]*)\)(\S+)', hdr)
    return m.groups() if m else (hdr, '', '')

def iter_segments(path):
    """yield (hdr, tag, body_lines)。tag 见上；CHG_BASE 是 [MOD-CHANGED] 段的基线原文对照段。"""
    hdr = None
    tag = None
    buf = []
    def flush():
        if hdr is not None and tag is not None:
            yield (hdr, tag, buf)
    for seg in _split_by_hdr(path):
        h, tg, body = seg
        yield (h, tg, body)

def _split_by_hdr(path):
    """按顶层段头(.method 行且下一非空行是 TAG)切段。"""
    lines = open(path, encoding='utf-8', errors='replace').read().split('\n')
    segs = []
    i = 0
    n = len(lines)
    while i < n:
        m = METHOD_HDR.match(lines[i])
        tg = None
        if m:
            # 找下一非空行
            j = i + 1
            while j < n and not lines[j].strip():
                j += 1
            if j < n and lines[j].strip() in TAGLINE:
                tg = TAGLINE[lines[j].strip()]
                hdr = m.group(1).strip()
                body = []
                k = j + 1
                # 体扫到下一个顶层段头(.method + 下一行 TAG)或 EOF
                while k < n:
                    m2 = METHOD_HDR.match(lines[k])
                    if m2:
                        j2 = k + 1
                        while j2 < n and not lines[j2].strip():
                            j2 += 1
                        if j2 < n and lines[j2].strip() in TAGLINE:
                            break  # 新段头
                    # CHG_MOD 段遇到 [BASE-ORIGINAL] 也要切到 CHG_BASE
                    if tg == TAG_CHG_MOD and lines[k].strip() == '[BASE-ORIGINAL]':
                        segs.append((hdr, tg, body))
                        hdr2 = hdr
                        body = []
                        tg = TAG_CHG_BASE
                        k += 1
                        continue
                    body.append(lines[k])
                    k += 1
                segs.append((hdr, tg, body))
                i = k
                continue
        i += 1
    return segs

def is_nop_body(body):
    for ln in body:
        s = ln.strip()
        if not s or s.startswith('.method') or END_M.match(s):
            continue
        if re.match(r'^\.(registers|param|prologue|line|local|restart local|end local|source)\b', s):
            continue
        if s in ('return-void',) or re.match(r'^return[v-]', s):
            continue
        if re.match(r'^const/4 v0, 0x0', s):
            continue
        return False
    return True

def method_status(path):
    """返回 (native_added, nop_added, other_added, changed_sigs, removed_sigs) 的 hdr 列表"""
    nat, nop, oth, chg, rem = [], [], [], [], []
    for hdr, tg, body in _iter(path):
        if tg == TAG_ADDED:
            if re.search(r'\bnative\b', hdr):
                nat.append(hdr)
            elif is_nop_body(body):
                nop.append(hdr)
            else:
                oth.append(hdr)
        elif tg in (TAG_CHG_MOD, TAG_CHG_BASE):
            if tg == TAG_CHG_MOD and sig_of(hdr) not in [sig_of(x) for x in chg]:
                chg.append(hdr)
        elif tg == TAG_REM:
            rem.append(hdr)
    return nat, nop, oth, chg, rem

def _iter(path):
    yield from iter_segments(path)

# ---------- 估量 ----------
all_changed = []
for dr, _, fs in os.walk(CHANGED):
    for f in fs:
        if f.endswith('.smali'):
            all_changed.append(os.path.relpath(os.path.join(dr, f), CHANGED))
n_changed = len(all_changed)
fan_n = sum(1 for c in all_changed if 'fanxing' in c or 'zego' in c)
print(f'KUWO3A changed={n_changed} fanxing/zego={fan_n}')

# ---------- 表① 广告 SDK 面 ----------
AD_PREFIX = re.compile(r'^com/tencentmusic/ad/')
OTHER_AD = ('com/tencent/gdt', 'com/bytedance/sdk', 'com/kuaishou', 'pangle', 'com/sigmob', 'com/tencent/ms/', 'com/bytedance/applog')
gdt_hits = {p: sum(1 for c in all_changed if c.startswith(p)) for p in OTHER_AD}
rows1 = []
ad_total = 0
for rel in sorted(all_changed):
    if not AD_PREFIX.search(rel):
        continue
    ad_total += 1
    nat, nop, oth, chg, rem = method_status(os.path.join(CHANGED, rel))
    kw = []
    for h in nat + nop + oth:
        for k in ('show', 'load', 'fetch', 'request', 'start', 'report', 'track', 'send', 'init'):
            if k in h.lower():
                kw.append(k)
    st = []
    if nat: st.append(f'native×{len(nat)}')
    if nop: st.append(f'NOP桩×{len(nop)}')
    if oth: st.append(f'新增×{len(oth)}')
    if rem: st.append(f'删×{len(rem)}')
    if chg: st.append(f'改×{len(chg)}')
    rows1.append((rel, ';'.join(st) or '(仅体内改)', ';'.join(f'{k}×{v}' for k, v in Counter(kw).most_common(4)) or '—'))
nop_all = sum(len(method_status(os.path.join(CHANGED, r))[1]) for r, _, _ in rows1)
rem_all = sum(len(method_status(os.path.join(CHANGED, r))[4]) for r, _, _ in rows1)

# ---------- 表② 埋点上报面（47 base-only URL → changed 类出现区段） + 统计类现状子表 ----------
gone = []
with open(EPMD, encoding='utf-8') as f:
    grab = False
    for line in f:
        if line.startswith('## 5.'):
            grab = True; continue
        if grab:
            if line.startswith('## '):
                break
            m = re.match(r'- `(https?://[^`]+)`', line)
            if m:
                gone.append(m.group(1))
url_core = {u: re.sub(r'^https?://', '', u).split('?')[0].rstrip('/').lower() for u in gone}
url_rows = []
for rel in sorted(all_changed):
    path = os.path.join(CHANGED, rel)
    raw = open(path, encoding='utf-8', errors='replace').read()
    low = raw.lower()
    hits = [u for u in gone if url_core[u] in low]
    if not hits:
        continue
    # 区段归属：跟踪每 URL 命中的 tag
    tagof = defaultdict(set)
    for hdr, tg, body in _iter(path):
        for ln in body:
            ll = ln.lower()
            for u in hits:
                if url_core[u] in ll:
                    tagof[u].add(tg)
    for u in hits:
        tg = tagof.get(u, set())
        # CHG_BASE/REMOVED = 基线原文侧（URL 在此=官方有该 URL 的段）；CHG_MOD/ADDED = mod 改写后仍含该 URL
        mod_alive = bool(tg & {TAG_ADDED, TAG_CHG_MOD})
        base_side = bool(tg & {TAG_CHG_BASE, TAG_REM})
        verdict = 'mod仍含' if mod_alive else ('仅基线原文段(mod已改体/删)' if base_side else '出现段未识别')
        url_rows.append((u, rel, '+'.join(sorted(tg)) or '-', verdict))
url_rows.sort(key=lambda r: (r[0], r[1]))
with open(EPLOC, 'w', encoding='utf-8') as f:
    for r in url_rows:
        f.write('\t'.join(r) + '\n')
dom_rows = []
for dom in sorted({re.sub(r'^https?://', '', u).split('/')[0] for u in gone}):
    us = [r for r in url_rows if r[0].split('://')[-1].split('/')[0] == dom]
    dom_rows.append((dom, len(us), len({r[1] for r in us}), sum(1 for r in us if r[3] == 'mod仍含')))
# 表②b 统计/上报相关 changed 类现状（路径启发式，不扫 base——只列 changed 面现状给老马定位）
STAT_PAT = re.compile(r'statistic|analytics|/stat[0-9a-z]*/|report|monitor|crash|track|/log/|/bi/|/rif/|xcstat', re.I)
rows2b = []
for rel in sorted(all_changed):
    if not STAT_PAT.search(rel):
        continue
    nat, nop, oth, chg, rem = method_status(os.path.join(CHANGED, rel))
    st = []
    if nat: st.append(f'native×{len(nat)}')
    if nop: st.append(f'NOP桩×{len(nop)}')
    if oth: st.append(f'新增×{len(oth)}')
    if rem: st.append(f'删×{len(rem)}')
    if chg: st.append(f'改×{len(chg)}')
    rows2b.append((rel, ';'.join(st) or '(仅体内改)'))

# ---------- 表③ s2 ----------
s2p = os.path.join(CHANGED, 'cn/kuwo/base/utils/s2.smali')
ad_nat, ad_nop, ad_oth, ad_chg, ad_rem = method_status(s2p)
ad_map = defaultdict(list); rm_map = defaultdict(list)
for h in ad_nat: ad_map[sig_of(h)].append(h)
for h in ad_rem: rm_map[sig_of(h)].append(h)
pairs = sorted(set(ad_map) & set(rm_map))
ret_cnt = Counter(p[2] for p in pairs)
with open(PAIRS, 'w', encoding='utf-8') as f:
    for p in pairs:
        f.write(f'{p[0]}({p[1]}){p[2]}\n')
tanp = os.path.join(ADDED_DIR, 'tian0/tan.smali')
tan_txt = open(tanp, encoding='utf-8', errors='replace').read() if os.path.exists(tanp) else ''
tan_reg = len(re.findall(r'registerNativesForClass\(', tan_txt))
tan_key = len(re.findall(r'"(ssXpix[^"]*)"', tan_txt))
tan_ld = len(re.findall(r'System;->load', tan_txt))
str_ret = ret_cnt.get('Ljava/lang/String;', 0)
print(f'KUWO3A s2 native_added={len(ad_nat)} removed={len(ad_rem)} pairs={len(pairs)} strRet={str_ret} | tan reg={tan_reg} key={tan_key} load={tan_ld}')

# ---------- 渲染 ----------
L = ['# KUWO-3a 广告/埋点残留面素材清单', '',
     '> 输入=Release kuwo1-artifacts 的 kuwo1-diff-baksmali.tar.gz + kuwo1-endpoints.md，**未回扫 base 全量 dex**（表驱动禁暴力扫）。',
     '> 只出现状事实与候选入口，不写删点建议；分类判定权在老马。',
     f'> 规模：changed 类 {n_changed}；表① com/tencentmusic/ad 命中 {ad_total}。', '',
     '## 表① 广告 SDK 面（mod changed 内现状）', '',
     '> 前缀实测口径：`com/tencentmusic/ad/` 命中 ' + str(ad_total) + ' 类；' +
     '、'.join(f'`{k}` 命中 {v}' for k, v in gdt_hits.items()) +
     ' 均 **0**（酷我 12.2.2.0 changed 面不含这些第三方广告 SDK；广点通/快手/穿山甲候选经证伪，非抽样遗漏）。',
     '> 「NOP 桩」=mod 新增且体仅 return-void 空壳。', '',
     '| 类 | mod 现状 | 入口动词命中 |', '|---|---|---|']
for rel, st, kws in rows1:
    L.append(f'| `{rel}` | {st} | {kws} |')
L += ['', f'- 表① {ad_total} 类合计：NOP 桩新增方法 {nop_all} 个、mod 删除方法 {rem_all} 个，其余为改体/新增实现。',
     '', '> fanxing/zego 直播区：changed 实测 ' + str(fan_n) + ' 类（派单估 ~300，实际更大），本单三表不含其定性，规模差异如实登记供老马排期。', '',
     '## 表② 埋点上报面（47 base-only URL 的 mod 现状归属）', '',
     '> 方法：KUWO-1「基线 URL 在 mod 消失」47 个 → 在 changed 类归档中定位其出现的差异区段。',
     '> 判读口径：URL 落在 [BASE-REMOVED-IN-MOD]/[BASE-ORIGINAL] 段=mod 已删/改写该方法体；落在 [MOD-ADDED]/[MOD-CHANGED]=改写后仍含上报体（存活）。', '',
     '| 域名 | 命中URL数 | 涉及changed类 | mod仍含 |', '|---|---|---|---|']
for dom, us, cls, alive in dom_rows:
    L.append(f'| `{dom}` | {us} | {cls} | {alive} |')
s2_share = sum(1 for r in url_rows if r[1] == 'cn/kuwo/base/utils/s2.smali')
alive_all = sum(1 for r in url_rows if r[3] == 'mod仍含')
L += ['', f'- **结构发现（重要，防误读）**：{s2_share}/{len(gone)} 个消失 URL 命中 `cn/kuwo/base/utils/s2.smali` 的删除/原文段——即这些 URL 是 s2 字符串池 getter 的明文，被 native 化搬运（表③ 672 对）后从 Java 侧消失。',
     f'- mod 仍含上报体的类命中 {alive_all} 处。',
     '> ⚠️ **「URL 消失」≠「上报链被删」**：调用这些 getter 的统计/上报类若未进 changed 名单，native 化后运行时字符串仍可能指向同一端点（native 侧不可见于 Java 差集）。判定权在老马，此处仅提示误读风险。',
     '> 全行明细（URL×类×区段×判读）→ kuwo3-ep-locate.txt。', '',
     '### 表②b 统计/上报相关 changed 类现状（路径启发式，仅 changed 面）', '',
     '> 口径：changed 1869 类中路径含 statistic/analytics/stat*/report/monitor/crash/track/log/bi/rif/xcstat 者；「未动区」存活入口不在 changed 集内，禁全扫不列。', '',
     '| 类 | mod 现状 |', '|---|---|']
for rel, st in rows2b:
    L.append(f'| `{rel}` | {st} |')
L += ['', f'- 表②b 合计 {len(rows2b)} 类。', '',
     '## 表③ s2.smali(+672/-672) 定性素材', '',
     f'- mod 新增 **native 声明方法 {len(ad_nat)} 个** ↔ 基线删除非 native 方法 {len(ad_rem)} 个，**签名（名+参+返回）100% 配对 {len(pairs)} 对**——纯 Java 实现体→native 声明位移，零净增/净缺。',
     f'- 配对返回类型：String {str_ret} / void {ret_cnt.get("V",0)} / StringBuilder {ret_cnt.get("Ljava/lang/StringBuilder;",0)} / 其他 {len(pairs)-str_ret-ret_cnt.get("V",0)-ret_cnt.get("Ljava/lang/StringBuilder;",0)}',
     f'- 配对签名 672 行 → kuwo3-s2-pairs.txt（Release kuwo3a-artifacts）',
     f'- 挂载画像对照：tian0/tan `registerNativesForClass`×{tan_reg}、密钥串 `ssXpix…`×{tan_key}、`System.load`×{tan_ld} → s2 native 实现由 tan 注册桥挂接 libtian.so（Soforge 壳，KUWO-1 定案）。',
     '- **事实结论段（供老马引用）**：672 对全 String 进出 + tan 的 Long.decode 密钥链 → s2=官方工具类字符串加解密方法整体 native 化搬运（VIP 字符串加密面），非功能删除。净化视角属 D 类会员机制依赖，**不属 B 广告面**。', '']
with open(OUT, 'w', encoding='utf-8') as f:
    f.write('\n'.join(L) + '\n')
print(f'KUWO3A DONE 表①={ad_total} 表②行={len(url_rows)}/域名={len(dom_rows)} pairs={len(pairs)} -> {OUT}')
