# KUWO-R2a 动态抓栈结论（老马 2026-09-13 12:15-12:28，ACE5 真机 192.168.1.157）

## 执行环境更正
- **实际设备 = ACE5（PKG110，arm64-v8a，Android root uid=0）192.168.1.157:6666**，非 PJD110。
  - PJD110 模拟器（100.64.0.3:5555，houdini x86_64）设备可用但其 frida-server=17.16.2 与 CT110 客户端 17.18.0 版本不匹配（`connection closed`），未强升（houdini attach 另有风险）。
- 两机均已装 kuwo3-round1 净化版（base.apk sha256=9acc52daeb9a390e15d6bc002fd7f801c29d6cc896b9513a521f3ef0ac92869b，size 242125949，与 Release kuwo3-round1 资产一致，versionName=12.2.2.0）。
- frida-server 17.18.0 android-arm64 官方构建 push 至 ACE5 /data/local/tmp（sha256=fa64b920…），`adb forward tcp:27042` + frida python remote 驱动。
- **脚本坑与修复（已实证）**：
  1. 仓内 scripts/kuwo_r2a_bubble_hook.js 是 frida-compile 半成品（frida 17+ 不再注入 Java 全局，直跑报 `ReferenceError: 'Java' is not defined`）→ 本地 hookbuild/ 补 `shim-java.ts`（`import Java from 'frida-java-bridge'; globalThis.Java = Java`）重编译 compiled.js（446KB）后正常。码农下轮请把 entry 的 shim 一起入仓或改直连 frida 兼容写法。
  2. 触发方式 = spawn 冷启动即命中（见下），无需登录/前后台 5 轮——**「免登录复现不了」结论作废**：文案设置发生在 EntryActivity.onCreate 同步链。
  3. 偶发 `spawn already in progress`/frida-server 掉线：pkill frida-server 重拉 + force-stop App 即可恢复。

## 命中栈（R2b patch 点位，原始日志 r2/kw_r2a_raw_1228.log 986 行，关键栈 r2/kw_r2a_key_stacks.txt）

### 点位①【弹窗本体】文案直接 setText（[TXT] 命中，冷启动 +7s）
```
"QQ频道:新时代，天天免费"
  at cn.kuwo.base.uilib.m.F(SourceFile:10)
  at cn.kuwo.base.uilib.m.E(Unknown Source:1)
  at androidx.core.app.ComponentActivity.onCreate
  ...
  at cn.kuwo.player.activities.EntryActivity.onCreate(Unknown Source:1073)
```
→ **注入桥 A = `cn.kuwo.base.uilib.m` 的 E→F 调用面**（登录页 Activity onCreate 时直接给 TextView 塞推广文案，覆盖微信登录按钮区域）。掐法候选：m.F/m.E 方法体前置空返回（宁残骸不断链），**禁动 EntryActivity 本体**（VIP 红线）——uilib.m 是通用工具类需码农静态确认调用面是否仅此文案一处，若共用需按值过滤。

### 点位②【bubble config 解析链】（[EQ] 命中 36 次，冷启动 +10s 起持续）
```
JSONObject.optString("buttonVIPText"/"buttonUrl"/"buttonUrl2")
  at cn.kuwo.peculiar.specialdialogconfig.a.O2(SourceFile:3/5)
  at cn.kuwo.peculiar.specialdialogconfig.a.K1(SourceFile:10)
  at cn.kuwo.peculiar.specialdialogconfig.a.init(SourceFile:2)
  at q1.b.a(SourceFile:1)
  at q1.b.G0(SourceFile:5)
  at cn.kuwo.base.utils.s2.s7(Native Method)
  at cn.kuwo.ui.online.library.recommend.LibraryRecommendViewModel.v
  ...（kotlinx 协程 preload）
```
→ **注入桥 B = `cn.kuwo.peculiar.specialdialogconfig.a`（O2/K1/init）+ `q1.b.G0/a`**——bubble config JSON 字段填充点，由 s2.s7（解密产出）喂入。掐法候选：`q1.b.G0` 或 `specialdialogconfig.a.init/K1` 单向桥 stub（返回空 config），**s2.s7/s2 主链、tian0/libtian 不动**（解密本体，VIP 功能面）。

### 未命中面（供参考，勿追）
- `s2.E` overload 注册成功但窗口内零命中（本轮文案走 s7 路径，非 E）；`s2.U3` 零命中；Dialog.show/PopupWindow 零命中（文案非弹窗控件，是 View 级 setText 直显——与东哥截图「浮层覆盖登录按钮」吻合，属 decor 级注入）。
- String.equals needle「频道/新时代/天天免费/mqqLandingPage」未命中（这些串作 JSONObject value 不经 equals 比较），下轮如需 value 明文可加 `JSONObject.optString` 返回值 hook。

## 后门排查（东哥②问）补充实证
- bubble config 解析发生在**本地 APK 内**（specialdialogconfig 类），字段 key=buttonUrl/buttonVIPText/buttonUrl2 与官方 freemium bubble 体系一致；文案内容运行时产出、无落盘（与 3b1 静态结论互印：官方原版不弹=mod 劫持 config 内容）。
- 本轮未抓到响应体明文 URL（U3/E 未命中）；静态链已实锤请求=官方 `v1/user/freemium/automatic/bubble`（kuwo.cn 域）→ **维持结论：下发通道官方、内容劫持在 mod 侧解密链，无第三方 C2**。若码农要钉死 value 面，可在 R2b 验证轮加 optString 返回 hook。

## R2b 交给码农的判定
- 双桥：① uilib.m.F/E（登录页直显文案）② specialdialogconfig.a/q1.b.G0（bubble config 字段填充）。
- 优先掐②（config 空则渲染面无数据）；①若为硬编码兜底文案（静态确认 uilib.m 内该串来源）则一并掐。
- CI 构建 Release kuwo3-round2 → 老马装机复测（冷启动+切后台回登录页双场景）。
