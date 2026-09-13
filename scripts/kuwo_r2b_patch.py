#!/usr/bin/env python3
# KUWO-R2b：根除「QQ频道：新时代，天天免费」——双桥 patch（老马 R2a 动态实锤点位，正式版）
# 桥②（config 面，优先）：q1.b.a(Lq1/a;)V 的 invoke-interface Lq1/a;->init()V → 等宽 2×nop
#   （invoke-interface = 2 code units；config 永不初始化+注册列表空 = 解密产出永不喂入。
#    宁残骸不断链：specialdialogconfig.a 类本体与 G0 单例结构不动，只断 init 调用。）
# 桥①（渲染面，按值过滤）：cn/kuwo/base/uilib/m.smali F(Ljava/lang/String;Z)V 体首插值过滤——
#   p0 含 "QQ频道" 则直接 return-void（String.contains 跳转实现；uilib.m 是 36 方法通用 toast 工具，
#   整类掐坏官方功能，按值过滤只拦推广文案；EntryActivity/s2 主链/tian0/libtian 禁动）。
# 等宽规则（3b2 经验）：invoke-kind 2 code units=2×nop；/range 3=3×nop；baksmali 文本行拆。
# 输出：改前后证据 + 计数门 fail-fast（B2=1，B1=1）
import os, re, sys

SRC = sys.argv[1]
EVID = sys.argv[2] if len(sys.argv) > 2 else 'patch-r2b-evidence.txt'
ev = open(EVID, 'w', encoding='utf-8')

def find_file(rel):
    for d in sorted(os.listdir(SRC)):
        if not d.startswith('smali'):
            continue
        p = os.path.join(SRC, d, rel)
        if os.path.exists(p):
            return p
    return None

def record(tag, path, before_lines, idx, after_lines, label):
    ev.write(f'=== {tag} {label} {os.path.relpath(path, SRC)} ===\n[BEFORE]\n' +
             ''.join(before_lines[max(0, idx-2):min(len(before_lines), idx+3)]) +
             '\n[AFTER]\n' + ''.join(after_lines[max(0, idx-2):min(len(after_lines), idx+3)]) + '\n\n')

# ---------- 桥②：q1.b.a(Lq1/a;)V init invoke → 2×nop ----------
p2 = find_file('q1/b.smali')
if not p2:
    print('R2B-PATCH FATAL B2: q1/b.smali 未找到'); sys.exit(1)
lines = open(p2, encoding='utf-8').read().split('\n')
out, in_m, hit2 = [], False, 0
for idx, ln in enumerate(lines):
    if re.match(r'^\.method\s+', ln):
        in_m = bool(re.match(r'^\.method private static a\(Lq1/a;\)V\s*$', ln))
        out.append(ln); continue
    if ln.strip() == '.end method':
        in_m = False; out.append(ln); continue
    if in_m and re.search(r'invoke-interface\s+\{p0\},\s*Lq1/a;->init\(\)V', ln):
        indent = re.match(r'\s*', ln).group(0)
        out.append(indent + 'nop')
        out.append(indent + 'nop')
        out.append(indent + '# R2B-B2 invoke-interface(2 units)→2×nop 等宽替换')
        out.append(indent + '# R2B-B2 原行: ' + ln.strip())
        record('B2', p2, lines, idx, out, label='a(Lq1/a;)V init')
        hit2 += 1
        continue
    out.append(ln)
if hit2 != 1:
    print(f'R2B-PATCH FATAL B2: init invoke 命中 {hit2} != 1'); sys.exit(1)
open(p2, 'w', encoding='utf-8').write('\n'.join(out))
print('B2 done: q1.b.a(Lq1/a;)V init → 2×nop')

# ---------- 桥①：uilib.m F(String,Z) 体首值过滤 ----------
p1 = find_file('cn/kuwo/base/uilib/m.smali')
if not p1:
    print('R2B-PATCH FATAL B1: uilib/m.smali 未找到'); sys.exit(1)
lines = open(p1, encoding='utf-8').read().split('\n')
out, in_m, hit1 = [], False, 0
for idx, ln in enumerate(lines):
    if re.match(r'^\.method\s+', ln):
        in_m = bool(re.match(r'^\.method public static F\(Ljava/lang/String;Z\)V\s*$', ln))
        out.append(ln); continue
    if ln.strip() == '.end method':
        in_m = False; out.append(ln); continue
    if in_m and (re.match(r'^\s*\.registers\s+\d+', ln) or re.match(r'^\s*\.locals\s+\d+', ln)):
        indent = re.match(r'\s*', ln).group(0)
        out.append(ln)
        # F(String,Z)：.registers 8 → v0..v7，参数 p0=v6/p1=v7（static 无 this）。
        # 值过滤必须用本地寄存器 v0（体首未赋值安全；v6 覆写会毁 p0 文案本体导致 contains 恒 false）：
        #   const-string v0, "QQ频道" ; invoke-virtual {p0, v0}, String;->contains(...)Z
        #   move-result v0 ; if-eqz v0, :cond_r2b_normal ; return-void ; :cond_r2b_normal
        out.append(indent + 'const-string v0, "QQ频道"')
        out.append(indent + 'invoke-virtual {p0, v0}, Ljava/lang/String;->contains(Ljava/lang/CharSequence;)Z')
        out.append(indent + 'move-result v0')
        out.append(indent + 'if-eqz v0, :cond_r2b_normal')
        out.append(indent + 'return-void')
        out.append(indent + ':cond_r2b_normal')
        out.append(indent + '# R2B-B1 按值过滤: 文案含「QQ频道」直接 return（官方其它 toast 文案不受影响；v0=本地寄存器体首未赋值安全）')
        record('B1', p1, lines, idx, out, label='F(String,Z) 体首值过滤')
        hit1 += 1
        continue
    out.append(ln)
if hit1 != 1:
    print(f'R2B-PATCH FATAL B1: F(String,Z) 锚定 {hit1} != 1（.registers/.locals 段未找到）'); sys.exit(1)
open(p1, 'w', encoding='utf-8').write('\n'.join(out))
print('B1 done: uilib.m F(String,Z) 体首值过滤跳转')

ev.close()
print('R2B-PATCH DONE B1=1 B2=1')
