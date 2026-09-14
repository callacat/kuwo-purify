# DM-1 W5 assets/dcxll 消费方定位 + 条目对拍报告

> 口径：Java 层 = W1 东明全量 smali（18 dex）逐行大小写不敏感子串；
> native 层 = 3 净新增 so + libhippy.so(对照) 的 strings -a/-e l 过滤 dcxll；
> 对拍 = dcxll 内条目 vs 官方 apk 同路径条目 sha256。不符预期不 FATAL，如实记录。

## 关键数字

| 指标 | 值 |
|---|---|
| Java 层命中（dcxll 超集） | 1 处 |
| 其中 assets/dcxll | 0 处 |
| 消费方类 | 1 个 |
| native strings 命中 | 0 处（含对照 hippy，分列见下表） |
| dcxll 内 4 件对拍一致 | 1/4 YES |
| assets/dcxll 本体 | 1429799 B（登记值 1429799，一致）sha256 2d52a4ffd3f542c656da1c74f86eabf07cc1340b4231a8f6fdcecc323e7389c8 |

## Java 层命中明细（全量见 dm5-consumer-hits.tsv）

| 类 | 所在方法 | 行 | kind | 内容(≤200) |
|---|---|---|---|---|
| `rj/lddne/valniaxvw/ehaqrlygmlwebgteqg` | `.method protected attachBaseContext(Landroid/content/Context;)V` | 901 | dcxll | `const-string v9, "dcxll"` |

## 消费方类方法面（供判断谁调起 dcxll 读取）

### `rj/lddne/valniaxvw/ehaqrlygmlwebgteqg`
- 文件 `smali-mod/classes9/rj/lddne/valniaxvw/ehaqrlygmlwebgteqg.smali`
```smali
.method static constructor <clinit>()V
.method public constructor <init>()V
.method protected attachBaseContext(Landroid/content/Context;)V
.method public invoke(Ljava/lang/Object;Ljava/lang/reflect/Method;[Ljava/lang/Object;)Ljava/lang/Object;
```

## dcxll 条目对拍表（entry/size/sha256/match_official；全量见 dm5-dcxll-entries.tsv）

| entry | size | sha256 | match_official | 东明主包内也存在? |
|---|---|---|---|---|
| `AndroidManifest.xml` | 246648 | 3c40aedee653d1e709f237ba5d842aa77d518b39a886887795033f3de0382fe4 | YES | 是 |
| `META-INF/ANDROIDK.RSA` | 900 | 49ef54ba731a52e733d05f9b182ef8f2cc37e3cb9f97e72bbe78eb532c4e362c | NO(diff) | 否 |
| `META-INF/ANDROIDK.SF` | 1526051 | f8ecb28a8a7fa25df0bcc862096e85562940e97c5a1bf665ef8343c9590c3e62 | NO(diff) | 否 |
| `META-INF/MANIFEST.MF` | 1525924 | aa14cde872cbc80e0302586a4bace808abd4982981314d3af2d00953a8483d6e | NO(diff) | 否 |

预期 4 件在东明主包的缺失核验（背景：三签名件+AndroidManifest 应从主包挪入 dcxll）：
- `AndroidManifest.xml`：东明主包 存在(异常,记差异)；dcxll 内 在；与官方对拍 YES
- `META-INF/ANDROIDK.RSA`：东明主包 不存在(符合预期)；dcxll 内 在；与官方对拍 NO(diff)
- `META-INF/ANDROIDK.SF`：东明主包 不存在(符合预期)；dcxll 内 在；与官方对拍 NO(diff)
- `META-INF/MANIFEST.MF`：东明主包 不存在(符合预期)；dcxll 内 在；与官方对拍 NO(diff)

## native strings dcxll 命中（so 命中明细落 dm5-so-hits.txt）

| so | 扫描器 | dcxll 命中行数 |
|---|---|---|
| `lib/arm64-v8a/libkijhhh.so` | strings -a / -e l | 0 |
| `lib/arm64-v8a/libabcdefgaaa.so` | strings -a / -e l | 0 |
| `lib/arm64-v8a/libdiacore.so` | strings -a / -e l | 0 |
| `lib/arm64-v8a/libhippy.so` | strings -a / -e l | 0 |

（strings 两法 0 命中 —— 无命中属正常，非错误）

## 用途现状（只写事实链，禁 A/B/C/D 定性）

- 类 `rj/lddne/valniaxvw/ehaqrlygmlwebgteqg` 方法 `.method protected attachBaseContext(Landroid/content/Context;)V` 第 901 行含 `const-string v9, "dcxll"`（const-string 命中，±5 行上下文见 dm5-context-rj_lddne_valniaxvw_ehaqrlygmlwebgteqg.txt）；体内 invoke 引用：`invoke-static {v7, v3}, Landroid/util/Base64;->decode(Ljava/lang/String;I)[B`; `invoke-direct {v5, v7}, Ljava/io/ByteArrayInputStream;-><init>([B)V`; `invoke-direct {v0, v5}, Ljava/io/DataInputStream;-><init>(Ljava/io/InputStream;)V`; `invoke-virtual {v0}, Ljava/io/DataInputStream;->read()I`; `invoke-virtual {v0}, Ljava/io/DataInputStream;->readInt()I`; `invoke-virtual {v0, v9}, Ljava/io/DataInputStream;->readFully([B)V`; `invoke-direct {v8, v9}, Landroid/content/pm/Signature;-><init>([B)V`; `invoke-direct {v0, v5}, Ljava/lang/String;-><init>([B)V`; `invoke-static {v0}, Ljava/lang/Class;->forName(Ljava/lang/String;)Ljava/lang/Class;`; `invoke-direct {v5, v7}, Ljava/lang/String;-><init>([B)V`; `invoke-virtual {v0, v5, v7}, Ljava/lang/Class;->getDeclaredMethod(Ljava/lang/String;[Ljava/lang/Class;)Ljava/lang/reflect/Method;`; `invoke-virtual {v5, v7, v8}, Ljava/lang/reflect/Method;->invoke(Ljava/lang/Object;[Ljava/lang/Object;)Ljava/lang/Object;`
- 上下文文件：dm5-context-rj_lddne_valniaxvw_ehaqrlygmlwebgteqg.txt

