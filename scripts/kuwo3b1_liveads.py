#!/usr/bin/env python3
# KUWO-3b1：广告入口存活面 + 埋点 init 存活面反查
# 输入（全部 CI 内）：
#   work/smali-base/  官方基线 15dex 反编译（本单派明要求的官方全 dex 反查 caller，区别于 3a 禁扫口径）
#   work/smali-mod/   mod 15dex 反编译
#   work/changed-classes.txt  KUWO-1 产物（类路径口径一致：去 dex 前缀+.smali）
# 三态口径：活-unchanged / 活-changed仍调 / 已杀·断（caller 类不在 mod=类不存在；invoke 行消失=断）。
# 表③掐点候选=「活」caller + 风险自注（混挂 VIP 特征/高改动类），判定权在老马，不写判决句。
import os, re, sys
from collections import defaultdict

work = sys.argv[1]
BASE = os.path.join(work, 'smali-base')
MOD = os.path.join(work, 'smali-mod')
CHG = os.path.join(work, 'changed-classes.txt')
OUT = os.path.join(work, 'diff-out', 'docs', 'kuwo3b1-live-ads.md')
os.makedirs(os.path.dirname(OUT), exist_ok=True)

changed = set(l.strip() for l in open(CHG, encoding='utf-8') if l.strip())
print(f'KUWO3B1 changed 清单 {len(changed)} 类')

M_RE = re.compile(r'^\.method\s+(.+)$')
# 统一口径：正则两个捕获组 = (callee类, callee方法)。caller 行 = invoke-* {v..}, Lcls;->meth(
AD_PATTERNS = [
    re.compile(r'invoke-[\w/]+\s+\{[^}]*\},\s*(Lcom/tencentmusic/ad/TMEAds);->(\w+)\('),
    re.compile(r'invoke-[\w/]+\s+\{[^}]*\},\s*(Lcom/tencentmusic/ad/\S*adapter\S*);->(showAd|preload|fetchAd|loadAd|show|start)\w*\('),
    re.compile(r'invoke-[\w/]+\s+\{[^}]*\},\s*(L\S*(?:AdAdapter|AdSplash|SplashAd|AdInsert|AdBanner)\S*);->(\w+)\('),
    re.compile(r'invoke-[\w/]+\s+\{[^}]*\},\s*(Lcom/tencentmusic/ad/\S*InitParams\S*);->(<init>|\w+)\('),
]
STAT_PATTERNS = [
    re.compile(r'invoke-[\w/]+\s+\{[^}]*\},\s*(Lcom/tme/rif/\S+);->(init|start|attach|onCreate|register|setup|instance|get\w*Instance|new\w+)\w*\('),
    re.compile(r'invoke-[\w/]+\s+\{[^}]*\},\s*(L\S*(?:[Ff]ire[Ee]ye|[Xx]c[Ss]tat|Statistic|TatManager|tracker|Tracker)\S*);->(init|start|attach|onCreate|register|setup|set\w*Context|get\w+Instance)\w*\('),
]

def key_of(rel):
    parts = rel.split(os.sep)
    return '/'.join(parts[1:]) if len(parts) > 1 else rel

def sdk_pkg(cls, depth=3):
    """Lcom/tme/rif/… → 'com/tme/rif'；用于剔除 SDK 自调用"""
    body = cls.lstrip('L')
    return '/'.join(body.split('/')[:depth])

def scan_callers(root, patterns, drop_inner_sdk=False):
    """返回去重 {(caller_key, callee_class, meth): (dex, method_hdr, line)}；
    drop_inner_sdk=True 时 caller 与 callee 同包（深度3）视为 SDK 内部，跳过。"""
    seen = {}
    for droot, _, fs in os.walk(root):
        for f in fs:
            if not f.endswith('.smali'):
                continue
            abs_p = os.path.join(droot, f)
            rel = os.path.relpath(abs_p, root)
            ckey = key_of(rel)
            if ckey.startswith('com/tencentmusic/ad/'):
                continue  # 表①口径：只看非 ad 包的业务 caller（表②统计类无此前缀，同规则无害）
            dexn = rel.split(os.sep)[0] if os.sep in rel else 'classes'
            cur = None
            with open(abs_p, encoding='utf-8', errors='replace') as fh:
                for i, line in enumerate(fh, 1):
                    st = line.strip()
                    if M_RE.match(st):
                        cur = st[len('.method '):]
                    for rx in patterns:
                        m = rx.search(line)
                        if m:
                            cls, meth = m.group(1), m.group(2)
                            if drop_inner_sdk and sdk_pkg(cls) and ckey.startswith(sdk_pkg(cls) + '/'):
                                break
                            k = (ckey, cls, meth)
                            if k not in seen:
                                seen[k] = (dexn, cur or '?', i)
                            break
    return seen

mod_files = {}
for d in sorted(os.listdir(MOD)):
    dd = os.path.join(MOD, d)
    for droot, _, fs in os.walk(dd):
        for f in fs:
            if f.endswith('.smali'):
                ckey = key_of(os.path.relpath(os.path.join(droot, f), MOD))
                mod_files.setdefault(ckey, []).append(os.path.join(droot, f))

def caller_state(ckey, cls, meth):
    """返回 (state, note)"""
    if ckey not in mod_files:
        return '已杀·类不在mod', 'mod 全 15dex 无该类文件'
    pat = re.compile(re.escape(cls) + r';->' + re.escape(meth) + r'\(')
    alive = False
    for p in mod_files[ckey]:
        if pat.search(open(p, encoding='utf-8', errors='replace').read()):
            alive = True
            break
    if alive:
        return ('活-changed仍调', 'caller 类在 changed 名单但 invoke 仍在') if ckey in changed else ('活-unchanged', '')
    # invoke 消失：changed 类=确认可疑杀断；不在 changed 却消失=与类级 diff 矛盾，标存疑不冒充"已杀"
    if ckey in changed:
        return ('已杀·断', 'caller 类 changed 且 invoke 消失')
    return ('断?', 'caller 不在 KUWO-1 changed 清单却 invoke 消失——与类级 diff 矛盾，疑正则误捕或跨dex重复类漏判，须复核')

# ---------- 表① 广告业务入口 ----------
ad_seen = scan_callers(BASE, AD_PATTERNS)
rows1 = []
for (ckey, cls, meth), (dexn, hdr, ln) in sorted(ad_seen.items()):
    st, note = caller_state(ckey, cls, meth)
    rows1.append((ckey, dexn, hdr, ln, f'{cls};->{meth}', st))
n_alive = sum(1 for r in rows1 if r[5].startswith('活'))
print(f'KUWO3B1 表① caller={len(rows1)} 活={n_alive}')

# ---------- 表② 埋点 init 存活 ----------
stat_seen = scan_callers(BASE, STAT_PATTERNS, drop_inner_sdk=True)
rows2 = []
for (ckey, cls, meth), (dexn, hdr, ln) in sorted(stat_seen.items()):
    st, note = caller_state(ckey, cls, meth)
    rows2.append((ckey, dexn, hdr, ln, cls, meth, st, note))
n_alive2 = sum(1 for r in rows2 if r[6].startswith('活'))
print(f'KUWO3B1 表② caller={len(rows2)} 活={n_alive2}')

# ---------- 表③ 掐点候选（存活 caller 去重 + 风险自注带命中证据） ----------
# VIP/破解链命名空间（按 KUWO-2/3a 判定画像）；不含 EntryActivity(启动/导航类,广告侧 startActivity 引用属常态,
# 泛匹配会假阳性) 与泛 mod/；命中项逐条作证据输出,是否真属 VIP 依赖由老马判定。
VIP_TOKENS = {
    'tian0(引擎)': 'Ltian0/',
    's2(native字符串)': 'Lcn/kuwo/base/utils/s2;',
    'vipnew(VIPbean)': 'Lcn/kuwo/base/bean/vipnew',
    'quku(权益bean)': 'Lcn/kuwo/base/bean/quku',
    'allpay(支付破解)': 'Lcn/kuwo/mod/allpay',
    'nowplay(播放权益)': 'Lcn/kuwo/mod/nowplay',
    'theme(皮肤权益)': 'Lcn/kuwo/mod/theme',
    'peculiar(会员提示)': 'Lcn/kuwo/peculiar',
}
VIP_HINT = re.compile('|'.join(re.escape(v) for v in VIP_TOKENS.values()))
def vip_hits(ckey):
    """返回该类 mod 侧命中的破解特征标签（证据，去重保序）。"""
    found = []
    for label, tok in VIP_TOKENS.items():
        for p in mod_files.get(ckey, []):
            if tok in open(p, encoding='utf-8', errors='replace').read():
                found.append(label)
                break
    return found
cand = {}
for src in [(r[0], r[1], r[2], r[4]) for r in rows1 if r[5].startswith('活')] + \
           [(r[0], r[1], r[2], f'{r[4]};->{r[5]}') for r in rows2 if r[6].startswith('活')]:
    ckey = src[0]
    if ckey in cand:
        continue
    hits = vip_hits(ckey)
    if hits:
        risk = '混挂破解链特征[' + '+'.join(hits) + ']——掐该 caller 前先审这些依赖，防 P3 式崩会员'
    elif ckey in changed:
        risk = 'caller 在 changed 名单(已被 mod 动过)——叠加修改前复核 diff 现状'
    else:
        risk = '独立业务 caller(未见破解链引用)——波及面最小'
    cand[ckey] = (ckey, src[1], src[2][:70], src[3], risk)
rows3 = sorted(cand.values())
print(f'KUWO3B1 表③ 候选={len(rows3)}')

L = ['# KUWO-3b1 广告入口存活面 + 埋点 init 存活面反查', '',
     '> 输入=Release samples 双包（官方基线全 dex 反查 caller + mod 现状对照）+ KUWO-1 changed-classes.txt。',
     '> 三态：`活-unchanged`（caller 未被 mod 动过）/ `活-changed仍调`（动过但 invoke 仍在）/ `已杀·断`。`断?`=不在 changed 却 invoke 消失，疑正则误捕需复核。',
     '> 表①口径=非 com/tencentmusic/ad 包的业务 caller；表②剔除 SDK 包内部自调用。**判定权在老马。**',
     f'> 规模：表① {len(rows1)} 条（活 {n_alive}）、表② {len(rows2)} 条（活 {n_alive2}）、表③候选 {len(rows3)} 类。行号=官方基线 smali 行号，可直接复核。', '',
     '## 表① 广告业务入口存活表', '',
     '| caller 类 | dex | 所在方法 | 官方行 | 被调门面 | mod 现状 |', '|---|---|---|---|---|---|']
for ckey, dexn, hdr, ln, callee, st in rows1:
    L.append(f'| `{ckey}` | {dexn} | `{hdr[:80]}` | {ln} | `{callee}` | **{st}** |')
L += ['', '## 表② 埋点 init 存活表（rif / fireeye / xcstat / Statistic 系）', '',
      '| caller 类 | dex | 所在方法 | 官方行 | 埋点类 | 方法 | mod 现状 |', '|---|---|---|---|---|---|---|']
for ckey, dexn, hdr, ln, cls, meth, st, note in rows2:
    L.append(f'| `{ckey}` | {dexn} | `{hdr[:70]}` | {ln} | `{cls}` | {meth} | **{st}** |')
L += ['', '## 表③ 掐点候选（存活 caller，风险自注，非判决）', '',
      '> 口径=表①②「活」条目按 caller 类去重；风险自注=mod 侧该类文件是否含 VIP/破解链引用（tian0/s2/vipnew/mod/peculiar）。', '',
      '| caller 类 | dex | 所在方法 | 示例调用 | 风险自注 |', '|---|---|---|---|---|']
for ckey, dexn, hdr, callee, risk in rows3:
    L.append(f'| `{ckey}` | {dexn} | `{hdr[:60]}` | `{callee}` | {risk} |')
L += ['', '> 真机基线（老马 PJD110：外联仅腾讯系 443 正常业务面）：存活表=Java 静态口径，最终掐点组合等老马点位表 + 真机复验。', '']
with open(OUT, 'w', encoding='utf-8') as f:
    f.write('\n'.join(L) + '\n')
print(f'KUWO3B1 DONE -> {OUT}')
