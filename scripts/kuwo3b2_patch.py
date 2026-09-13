#!/usr/bin/env python3
# KUWO-3b2：净化 patch（老马点位表 §2 执行单，patch 点全集=3 处，宁残骸不断链）
# 锚定：mod 侧方法签名（官方行号仅索引，dex 重编译后行号会漂移）。
#   P1 cn/kuwo/mod/mobilead/tmead/c.smali → .method public static h()V 体首插 return-void（掐 TMEAds init 枢纽）
#   P2 b3/a.smali → .method public b()V 内 ConfigManager/ServiceManager 两个 init invoke 行 → 等宽 nop 序列
#   P3 sd/d.smali → .method public b(Landroid/content/Context;Ljava/lang/String;)V 内 FireEye init/start 两 invoke → 等宽 nop
# 等宽规则：invoke-kind {vA, vB, ..}, meth@C = 2 code units；invoke-kind/range {vCCCC..vNNNN}, meth@C = 3 code units。
#   .code 16 位单元口径：nop 0000 每 1 unit → invoke 2 units = 2×nop；/range 3 units = 3×nop。baksmali 文本按行拆分。
# 输出：每个 patch 打印改前/后 5 行 smali 证据 + 命中计数；计数不达预期=exit 1（fail-fast，防静默漏 patch）。
import os, re, sys

SRC = sys.argv[1]  # apktool 解包根（含 smali*/）
EVID = sys.argv[2] if len(sys.argv) > 2 else 'patch-evidence.txt'
EXPECT = {'P1': 1, 'P2': 2, 'P3': 2}
hits = {k: 0 for k in EXPECT}
ev = open(EVID, 'w', encoding='utf-8')

def find_file(rel):
    """跨 smali* 目录找类文件（dex 目录不定）"""
    for d in sorted(os.listdir(SRC)):
        if not d.startswith('smali'):
            continue
        p = os.path.join(SRC, d, rel)
        if os.path.exists(p):
            return p
    return None

def invoke_units(line):
    return 3 if re.match(r'\s*invoke-[\w-]+/range', line) else 2

def record(tag, path, lines, idx, after_lines=None, label=''):
    ctx = ''.join(lines[max(0, idx-2):min(len(lines), idx+3)])
    ev.write(f'=== {tag} {label} {os.path.relpath(path, SRC)} ===\n[BEFORE]\n{ctx}\n')
    if after_lines is not None:
        ev.write('[AFTER]\n' + ''.join(after_lines[max(0, idx-2):min(len(after_lines), idx+3)]))
    ev.write('\n')

# ---------- P1：c.smali h()V 体首 return-void ----------
p1 = find_file('cn/kuwo/mod/mobilead/tmead/c.smali')
if not p1:
    print('KUWO3B2-PATCH FATAL P1: c.smali 未找到'); sys.exit(1)
lines = open(p1, encoding='utf-8').read().split('\n')
# round5：P1 撤销（老马 r4 实测副作用：h()V return-void 殃及同包 BirthScreenHelper 初始化 → u$l.run NPE 崩死 → App 起不来）。
# B2 已掐 config 唯一喂入口（q1.b.a init nop），bubble 链已断；P1 是保险冗余，撤销后 h()V 保持原样。
# 撤销方式=不插入 return-void，仅验证 h()V 存在且无历史桩残留（防 round4 工作树污染），fail-fast。
in_h, found, stub = False, False, False
for ln in lines:
    if re.match(r'^\.method\s+public static h\(\)V\s*$', ln):
        found = True
        in_h = True
        continue
    if ln.strip() == '.end method':
        in_h = False
    if in_h and 'KUWO3B2-P1 return-void inserted' in ln:
        stub = True
if not found:
    print('KUWO3B2-PATCH FATAL P1(撤销模式): c.smali h()V 未找到(签名漂移?)'); sys.exit(1)
if stub:
    print('KUWO3B2-PATCH FATAL P1(撤销模式): h()V 内有 round4 历史桩残留——工作树非干净解包,重跑 apktool d'); sys.exit(1)
hits['P1'] = 1
print('P1 done(撤销模式): h()V 保持原样，无 return-void 桩（round5，r4 副作用修复）')

# ---------- P2/P3：invoke → 等宽 nop ----------
def patch_invokes(path, method_sig, callee_regexes, tag):
    if not path:
        print(f'KUWO3B2-PATCH FATAL {tag}: 文件未找到'); sys.exit(1)
    lines = open(path, encoding='utf-8').read().split('\n')
    out, in_m, n_hit = [], False, 0
    for idx, ln in enumerate(lines):
        if re.match(r'^\.method\s+', ln):
            in_m = bool(re.match(r'^\.method\s+' + re.escape(method_sig) + r'\s*$', ln))
            out.append(ln); continue
        if ln.strip() == '.end method':
            in_m = False; out.append(ln); continue
        if in_m:
            hit = None
            for rx in callee_regexes:
                if re.search(rx, ln):
                    hit = rx; break
            if hit and re.match(r'\s*invoke-[\w-]+(?:/range)?\s', ln):
                n_units = invoke_units(ln)
                indent = re.match(r'\s*', ln).group(0)
                for _ in range(n_units):
                    out.append(indent + 'nop')
                out.append(indent + f'# KUWO3B2-{tag} invoke→{n_units}×nop (等宽替换: {hit[:48]}...)')
                record(tag, path, lines, idx, label=method_sig[:40] + ' L' + str(idx+1) + ': ' + ln.strip()[:80])
                n_hit += 1
                continue
        out.append(ln)
    if n_hit != EXPECT[tag]:
        print(f'KUWO3B2-PATCH FATAL {tag}: 命中 {n_hit} != 预期 {EXPECT[tag]}（签名/正则漂移，宁失败不静默）')
        sys.exit(1)
    open(path, 'w', encoding='utf-8').write('\n'.join(out))
    print(f'{tag} done: {n_hit} invoke → 等宽 nop')
    return n_hit

p2 = find_file('b3/a.smali')
hits['P2'] = patch_invokes(
    p2, 'public b()V',
    [r'Lcom/tme/rif/config/ConfigManager;->init', r'Lcom/tme/rif/service/ServiceManager;->init'],
    'P2')

p3 = find_file('sd/d.smali')
hits['P3'] = patch_invokes(
    p3, 'public b(Landroid/content/Context;Ljava/lang/String;)V',
    [r'Lcom/tme/fireeye/lib/base/FireEye;->init', r'Lcom/tme/fireeye/lib/base/FireEye;->start'],
    'P3')

ev.close()
print(f'KUWO3B2-PATCH DONE P1={hits["P1"]} P2={hits["P2"]} P3={hits["P3"]}')
if any(hits[k] != EXPECT[k] for k in EXPECT):
    sys.exit(1)
