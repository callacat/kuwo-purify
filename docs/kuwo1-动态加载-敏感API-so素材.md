# KUWO-1 素材表（动态加载 / 敏感API / native so）

> 仅列素材，定性判定权在老马。业务区=cn.kuwo 及 mod 新增类；噪音区=androidx/腾讯系等 SDK 既有代码。
> 净新增口径：mod 命中行（去 dex 前缀+行号）集合减 base 同口径集合。

## A. 动态加载/执行命中表

| 能力 | mod 总命中 | 净新增(不在base) | 业务区净新增样例(≤10) |
|---|---|---|---|
| DexClassLoader | 101 | 1 | (净新增全在噪音区) |
| PathClassLoader | 67 | 0 | — |
| InMemoryDexClassLoader | 0 | 0 | — |
| DelegateLastClassLoader | 4 | 0 | — |
| URLClassLoader | 3 | 0 | — |
| BaseDexCookie/VMRuntime.loadDex | 33 | 0 | — |
| Runtime.exec | 45 | 0 | — |
| ProcessBuilder | 36 | 0 | — |
| System.load(0) | 39 | 0 | — |
| Reflect.newInstance | 2056 | 0 | — |

### A-噪音区（SDK 既有，信息项）

- DexClassLoader: 1 处噪音区命中，如 `classes4/com/tencent/smtt/export/external/DexClassLoaderProvider` L23

## B. 敏感API命中表（只看 cn.kuwo 业务命名空间 + 新增类）

| 能力 | mod 总命中 | 净新增 | 业务区净新增样例(≤10) |
|---|---|---|---|
| getDeviceId/IMEI | 133 | 0 | — |
| getSubscriberId | 8 | 0 | — |
| AndroidID | 18 | 0 | — |
| getInstalledPackages | 3 | 0 | — |
| PackageInfo.signing | 363 | 0 | — |
| GET_SIGNATURES | 0 | 0 | — |
| Accessibility | 435 | 0 | — |
| Camera | 736 | 0 | — |
| Contacts | 4 | 0 | — |
| SMS | 0 | 0 | — |
| Location | 34 | 0 | — |
| Clipboard | 57 | 0 | — |
| Root/Su探测 | 7 | 0 | — |

## C. 逐 so hash 对比

- so 总数: mod 143 ｜ base 142
- **mod 独有（红名单）: 1**
- base 独有: 0
- **两侧同名但 hash 不同（红名单）: 0**

### mod 独有 so

- `lib_arm64-v8a_libtian.so` sha256=84982a71e8ea7e96012c7682cbc0031df0d097d2264f3eb4c3deb03e9712b9b5

### 同名不同 hash so

（无差异——mod 未修改任何同名 so；注意 ABI 目录名若两侧不一致则本表为空属预期，以独有清单为准）
