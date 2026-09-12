#!/usr/bin/env python3
# KUWO-1 素材③④⑤：动态加载命中表 / 敏感API命中表（cn.kuwo 业务命名空间）/ so hash 对比
# 红线：只出素材表格，不做定性；androidx/腾讯系 SDK 命中列噪音区不计入业务区。
# 输入：work/smali-mod/ work/smali-base/ 与 work/so-mod/ work/so-base/（so 为 APK 原文件）
# 输出：work/diff-out/docs/kuwo1-materials.md
import os, re, sys, hashlib
from collections import defaultdict

work = sys.argv[1]
MOD = os.path.join(work, 'smali-mod')
BASE = os.path.join(work, 'smali-base')
SO_MOD = os.path.join(work, 'so-mod')
SO_BASE = os.path.join(work, 'so-base')
OUT = os.path.join(work, 'diff-out', 'docs', 'kuwo1-materials.md')
os.makedirs(os.path.dirname(OUT), exist_ok=True)

DYN_PATTERNS = [
    ('DexClassLoader', re.compile(r'Ldalvik/system/DexClassLoader;')),
    ('PathClassLoader', re.compile(r'Ldalvik/system/PathClassLoader;')),
    ('InMemoryDexClassLoader', re.compile(r'Ldalvik/system/InMemoryDexClassLoader;')),
    ('DelegateLastClassLoader', re.compile(r'Ldalvik/system/DelegateLastClassLoader;')),
    ('URLClassLoader', re.compile(r'Ljava/net/URLClassLoader;')),
    ('BaseDexCookie/VMRuntime.loadDex', re.compile(r'Ldalvik/system/VMRuntime;->loadDex|Ldalvik/system/BaseDexClassLoader;')),
    ('Runtime.exec', re.compile(r'Ljava/lang/Runtime;->exec')),
    ('ProcessBuilder', re.compile(r'Ljava/lang/ProcessBuilder;')),
    ('System.load(0)', re.compile(r'Ljava/lang/System;->load(?:0)?\(')),
    ('Reflect.newInstance', re.compile(r'Ljava/lang/reflect/Method;->invoke|Ljava/lang/Class;->forName|Ljava/lang/reflect/Constructor;->newInstance')),
]
SENS_PATTERNS = [
    ('getDeviceId/IMEI', re.compile(r'Landroid/telephony/TelephonyManager;->getDeviceId|getImei|getDeviceId')),
    ('getSubscriberId', re.compile(r'Landroid/telephony/TelephonyManager;->getSubscriberId|getSubscriberId')),
    ('AndroidID', re.compile(r'ANDROID_ID')),
    ('getInstalledPackages', re.compile(r'Landroid/content/pm/PackageManager;->getInstalledPackages|getInstalledApplications')),
    ('PackageInfo.signing', re.compile(r'Landroid/content/pm/PackageInfo;->signatures|Landroid/content/pm/PackageInfo;->signingInfo|REQUEST_UNINSTALL|getPackageInfo')),
    ('GET_SIGNATURES', re.compile(r'0x40\b.*getPackageInfo|GET_SIGNATURES')),
    ('Accessibility', re.compile(r'Landroid/accessibilityservice|Landroid/view/accessibility/AccessibilityEvent;')),
    ('Camera', re.compile(r'Landroid/hardware/Camera;|Landroid/media/MediaRecorder;')),
    ('Contacts', re.compile(r'Landroid/provider/ContactsContract')),
    ('SMS', re.compile(r'Landroid/telephony/SmsManager;|Landroid/provider/Telephony$Sms')),
    ('Location', re.compile(r'Landroid/location/LocationManager;')),
    ('Clipboard', re.compile(r'Landroid/content/ClipboardManager;|Landroid/text/ClipboardManager;')),
    ('Root/Su探测', re.compile(r'"su"|/system/xbin/su|magisk|supersu', re.I)),
]
NOISE_PKG = re.compile(r'^(?:androidx/|kotlin/|kotlinx/|com/tencent/|com/bumptech/|tv/danmaku/|com/google/|org/apache/|com/alibaba/|okhttp3/|retrofit2/|com/squareup/|io/reactivex|com/bytedance/|com/pangle/|com/qq/|com/alipay/|com/umeng/|org/chromium/|android/)', re.I)

def walk_smali(root):
    for droot, _, fs in os.walk(root):
        for f in fs:
            if f.endswith('.smali'):
                abs_p = os.path.join(droot, f)
                rel = os.path.relpath(abs_p, root).split(os.sep)
                stem = '/'.join(rel[1:-1] + [rel[-1][:-6]]) if len(rel) > 1 else rel[0][:-6]
                yield (stem, abs_p, rel[0] if len(rel) > 1 else 'classes')

def scan_patterns(root, patterns):
    """返回 {api名: [(class, line_no, line_text)]}，class 带来源 dex 前缀防歧义。"""
    hits = defaultdict(list)
    for cls, abs_p, dexdir in walk_smali(root):
        with open(abs_p, encoding='utf-8', errors='replace') as fh:
            for i, line in enumerate(fh, 1):
                for name, rx in patterns:
                    if rx.search(line):
                        hits[name].append((f'{dexdir}/{cls}', i, line.strip()))
    return hits

mod_dyn = scan_patterns(MOD, DYN_PATTERNS)
base_dyn = scan_patterns(BASE, DYN_PATTERNS)
mod_sens = scan_patterns(MOD, SENS_PATTERNS)
base_sens = scan_patterns(BASE, SENS_PATTERNS)

def split_noise(lst):
    biz, noise = [], []
    for c, i, l in lst:
        # c 形如 classes3/cn/kuwo/player/... —— 去掉 dex 前缀后按包根判噪音
        tail = c.split('/', 1)[1] if '/' in c else c
        if NOISE_PKG.search(tail):
            noise.append((c, i, l))
        else:
            biz.append((c, i, l))
    return biz, noise

def diff_lines(mod_hits, base_hits, topn=40):
    """mod 命中行集合 - base 命中行集合 = 净新增（同类同行文本相同视为既有）。"""
    base_set = {(c.split('/', 1)[-1], l) for c, i, l in base_hits}
    new = [(c, i, l) for c, i, l in mod_hits if (c.split('/', 1)[-1], l) not in base_set]
    return new

report = ['# KUWO-1 素材表（动态加载 / 敏感API / native so）', '',
          '> 仅列素材，定性判定权在老马。业务区=cn.kuwo 及 mod 新增类；噪音区=androidx/腾讯系等 SDK 既有代码。',
          '> 净新增口径：mod 命中行（去 dex 前缀+行号）集合减 base 同口径集合。', '',
          '## A. 动态加载/执行命中表', '',
          '| 能力 | mod 总命中 | 净新增(不在base) | 业务区净新增样例(≤10) |', '|---|---|---|---|']
for name, _ in DYN_PATTERNS:
    modh, baseh = mod_dyn.get(name, []), base_dyn.get(name, [])
    new = diff_lines(modh, baseh)
    biz, noise = split_noise(new)
    samples = '; '.join(f'`{c}` L{i}' for c, i, l in biz[:10]) or ('(净新增全在噪音区)' if new else '—')
    report.append(f'| {name} | {len(modh)} | {len(new)} | {samples} |')
report += ['', '### A-噪音区（SDK 既有，信息项）', '']
for name, _ in DYN_PATTERNS:
    modh, baseh = mod_dyn.get(name, []), base_dyn.get(name, [])
    _, noise = split_noise(diff_lines(modh, baseh))
    if noise:
        report.append(f'- {name}: {len(noise)} 处噪音区命中，如 `{noise[0][0]}` L{noise[0][1]}')
report += ['', '## B. 敏感API命中表（只看 cn.kuwo 业务命名空间 + 新增类）', '',
           '| 能力 | mod 总命中 | 净新增 | 业务区净新增样例(≤10) |', '|---|---|---|---|']
for name, _ in SENS_PATTERNS:
    modh, baseh = mod_sens.get(name, []), base_sens.get(name, [])
    new = diff_lines(modh, baseh)
    biz, noise = split_noise(new)
    samples = '; '.join(f'`{c}` L{i}' for c, i, l in biz[:10]) or ('(净新增全在噪音区)' if new else '—')
    report.append(f'| {name} | {len(modh)} | {len(new)} | {samples} |')
report += ['', '## C. 逐 so hash 对比', '']
def so_map(root):
    m = {}
    for abifile in sorted(os.listdir(root)) if os.path.isdir(root) else []:
        p = os.path.join(root, abifile)
        if os.path.isfile(p):
            m[abifile] = hashlib.sha256(open(p, 'rb').read()).hexdigest()
    return m
sm, sb = (so_map(SO_MOD), so_map(SO_BASE)) if (os.path.isdir(SO_MOD) and os.path.isdir(SO_BASE)) else ({}, {})
only_mod = sorted(set(sm) - set(sb)); only_base = sorted(set(sb) - set(sm))
changed = sorted(k for k in set(sm) & set(sb) if sm[k] != sb[k])
report += [f'- so 总数: mod {len(sm)} ｜ base {len(sb)}', f'- **mod 独有（红名单）: {len(only_mod)}**', f'- base 独有: {len(only_base)}', f'- **两侧同名但 hash 不同（红名单）: {len(changed)}**', '',
           '### mod 独有 so', '']
for k in only_mod:
    report.append(f'- `{k}` sha256={sm[k]}')
report += ['', '### 同名不同 hash so', '']
if changed:
    report.append('| so | mod sha256 | base sha256 |')
    report.append('|---|---|---|')
    for k in changed:
        report.append(f'| `{k}` | `{sm[k][:16]}…` | `{sb[k][:16]}…` |')
else:
    report.append('（无差异——mod 未修改任何同名 so；注意 ABI 目录名若两侧不一致则本表为空属预期，以独有清单为准）')
with open(OUT, 'w', encoding='utf-8') as f:
    f.write('\n'.join(report) + '\n')

print(f'KUWO1-MAT dyn_mod={sum(len(v) for v in mod_dyn.values())} dyn_new={sum(len(diff_lines(mod_dyn.get(n,[]),base_dyn.get(n,[]))) for n,_ in DYN_PATTERNS)} sens_new={sum(len(diff_lines(mod_sens.get(n,[]),base_sens.get(n,[]))) for n,_ in SENS_PATTERNS)} so_onlymod={len(only_mod)} so_changed={len(changed)}')
