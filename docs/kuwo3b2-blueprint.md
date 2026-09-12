# KUWO-3b2 净化蓝图（点位表 v1，老马 2026-09-13）

> 唯一事实源。码农按点位机械执行+反解回读自证，勿改判定、勿扩面。
> 输入素材：docs/kuwo3b1-live-ads.md（run 34724957449，三态修复后版本）+ KUWO-2 判定书。

## 设计：掐总闸放掉链，宁少勿多（round1 最小面）

表① 175 条业务入口全活，但**逐条掐=撒网**（4244 方法面 NPE 风险）。正确解=掐 init 总闸，让所有下游 caller 经 isInitialized=false 自动死链（u.smali Wa() 等入口自带 isInitialized 守卫，实表已证）。GDT/AMS（com/qq/e）与 fanxing 直播 banner 面 **round1 不动**——真机实测若仍有肉眼广告，round2 加刀（每轮带新证据）。

## 点位表（全部在 smali 原始路径下，apktool d -r）

| # | dex | 文件 | 方法 | 现状 | 改法 | 依据 |
|---|---|---|---|---|---|---|
| P1 | classes8 | `cn/kuwo/mod/mobilead/tmead/c.smali` | `public static h()V` | 活，含 TMEAds init/registerProxy/InitParams 全链 | **方法体整体置 `return-void`**（保留 .method/.end method 与 modifiers；.registers 保留或置 3 不动） | 表③：TMEAds SDK 唯一 init 入口 caller，独立业务类无破解链引用；void 返回干净掐 |
| P2 | classes | `b3/a.smali` | `public b()V` | 活，370/375 行 rif 双 init | **只删 2 行**：`Lcom/tme/rif/config/ConfigManager;->init` 与 `Lcom/tme/rif/service/ServiceManager;->init` 的 invoke 行（各连同其前的 const-string 参数字符串行，若该行仅服务此次调用）；其余指令全保留。**动手前读完整个 b() 方法体**，若两 invoke 的返回值寄存器被后续引用（理论上 V 返回无值）或 const 行被复用，则改为整体不碰+报告说明 | 表②：rif=TME 直播/互动 SDK init 入口 |
| P3 | classes9 | `sd/d.smali` | `public b(Landroid/content/Context;Ljava/lang/String;)V` | 活，635/642 FireEye init/start（544 CrashReport/590 ANRReport init 已是 `断?`） | **只删 2 行**：`FireEye;->init`、`FireEye;->start` invoke 及其独占参数字符串行；其余保留。同 P2 规则：先读整个方法体防悬空 | 表②：fireeye=TME 监控上报 SDK；掐除崩溃/行为上报面 |
| K1-K2 | — | 作者已杀开屏 2 刀（SplashAdapter.showAd$default + OperExpertSplashAdapter.showAd return-void） | **保持原样勿动** | — | 已生效 |

## 红线（MUST NOT）
1. **禁动**：`cn/kuwo/base/utils/s2*`、`tian0/*`、`cn/kuwo/peculiar/*`、`vipnew`、`lib/arm64-v8a/libtian.so`（A/D 破解链，KUWO-2 定案）
2. 禁动 com/tencentmusic/ad 包内部（SDK 内部不撒网，掐的是外部入口）
3. 禁动 EntryActivity$d / mobilead/n / fo1/* / AdBannerView / com/qq/e/*（round1 范围外）
4. 表② 3 条 `断?` 项（sd/d 内 CrashReport/ANRReport）不新增掐点——存疑误捕不补刀

## 签名与构建
- 自签 keystore 新生成（**作者 CN=xinshidai0 私钥不可得**）：CN=KUWOclean；**CI secrets 零缺失门先过**——workflow 每个 secrets.X 引用逐项在仓 Settings 实配后再 dispatch（先 `git grep -o 'secrets\.[A-Z_]*' .github/workflows/kuwo3b*.yml` 列全清单）
- 链：apktool d -r → 3 点位 patch → b → zipalign -P 16 → apksigner v1+v2+v3 → verify
- 反解回读自证：构建后 apktool d 产物，逐点位 dump 方法体确认落位（P1=return-void 打头；P2/P3=对应 invoke 行 0 命中），证据写 docs/kuwo3b2-report.md
- 产物发 Release tag=kuwo3b-round1（asset 名 kuwo-12.2.2.0-clean-r1.apk + sha256.txt），**workflow 名含 kuwo**（loop 过滤依赖）

## 验收（老马真机四判据，构建绿后我执行）
①装机（先卸载天天版，签名不同预期内）②冷启动无 FATAL+稳定窗 ③VIP 态/播放/歌单不回归（对比 06:20 天天版基线截图 k4/）④**广告面消失判定**：首页 feed 无广告卡+无开屏+外联对照（`ss -tnp` 腾讯系 443 条数应显著低于天天版基线）⑤测完 force-stop。
VIP/播放若回归=失败回炉，按新栈归因，不算 P1 无效（区分"引擎未 init 被依赖"与"点位错误"）。
