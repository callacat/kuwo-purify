# DM-1 W3 净新增 native so 深查报告

> 东明版 12.2.2.0.apk vs 官方 12.2.2.0.apk；Java 层明文 0 非厂商域名，C2 嫌疑集中于此。
> 本文件为 CI（dm-native-so-audit.yml）自动回写，重活全在 runner（D7）。

## 关键数字摘要

| 指标 | 数 |
|---|---|
| dm so 总数 | 145 |
| 官方 so 总数 | 142 |
| 净新增 so（预期 3） | 3 |
| 同名异体（官方同名不同 hash，红旗） | 0 |
| 老线交叉 so 行 | 385 |
| 老线交叉命中 | 0 |

| 净新增 so | abi | 大小(B) | sha256 前16 | 网络族导入 | URL命中 | IP命中 | b64解码 |
|---|---|---|---|---|---|---|---|
| `libabcdefgaaa.so` | arm64-v8a | 1070584 | `f4a86934b3b3645a` | 0 | 2 | 0 | 0 |
| `libdiacore.so` | arm64-v8a | 20128 | `be38358c3961816d` | 0 | 2 | 0 | 0 |
| `libkijhhh.so` | arm64-v8a | 980912 | `2c75bfa825f40c74` | 5 | 2 | 1 | 0 |

## libabcdefgaaa.so（arm64-v8a）

### ELF 元信息
- NEEDED: `liblog.so`, `libc.so`, `libm.so`, `libdl.so`
- RPATH/RUNPATH: (无) / (无)
- BuildID: `ef1211fe45aecd9017df41fa6251ecfc33cab01d`
- .comment: `clang version 21.1.8 (https://github.com/komimoe/Arkari.git 4dadca110eb923bb1794a1bc7d0f19c8de36c6bf) | Android (13989888, +pgo, +bolt, +lto, +mlgo, based on r563880c) clang version 21.0.0 (https://android.googlesource.com/toolchain/llvm-project 5e96669f06077099aa41290cdb4c5e6fa0f59349)`
- 全文见 `libabcdefgaaa-elfmeta.txt`（含 size -A 节大小 / file）

### 导出面
- GLOBAL FUNC 导出：1 个；JNI_OnLoad：present；Java_* 显式导出：0 个
- registerNatives 属运行时动态注册，导出表不可见，静态侧只能看 JNI_OnLoad 存在性

### 网络族导入（0 命中）

### strings 命中明细（每模式计数 + 前 30 条样本）
- `url` https?:// → 2 命中
    - [ascii] `clang version 21.1.8 (https://github.com/komimoe/Arkari.git 4dadca110eb923bb1794a1bc7d0f19c8de36c6bf)`
    - [ascii] `Android (13989888, +pgo, +bolt, +lto, +mlgo, based on r563880c) clang version 21.0.0 (https://android.googlesource.com/toolchain/llvm-project 5e96669f06077099aa41290cdb4c5e6fa0f59349)`
- `ipv4` \b([0-9]{1,3}\.){3}[0-9]{1,3}\b → 0 命中
- `vendor_domain` \b(taobao|baidu|qq|weixin|wechat|163|126|kuwo|kugou|tencent|umeng|bugly|alipay|aliyun|volc|bytedance|github|gitlab|gitee)\. → 1 命中
    - [ascii] `clang version 21.1.8 (https://github.com/komimoe/Arkari.git 4dadca110eb923bb1794a1bc7d0f19c8de36c6bf)`
- `tld_path` \.(com|cn|net|top|xyz|icu|click|tk|me|io|app)/\b → 2 命中
    - [ascii] `clang version 21.1.8 (https://github.com/komimoe/Arkari.git 4dadca110eb923bb1794a1bc7d0f19c8de36c6bf)`
    - [ascii] `Android (13989888, +pgo, +bolt, +lto, +mlgo, based on r563880c) clang version 21.0.0 (https://android.googlesource.com/toolchain/llvm-project 5e96669f06077099aa41290cdb4c5e6fa0f59349)`
- `telegram` t\.me/ → 0 命中
- `onion` \.onion → 0 命中
- `base64_kw` base64 → 0 命中
- `pem` -----BEGIN → 0 命中
- `so_ref` \.so\b → 5 命中
    - [ascii] `libc.so`
    - [ascii] `libdl.so`
    - [ascii] `liblog.so`
    - [ascii] `libm.so`
    - [ascii] `libabcdefgaaa.so`
- `path_proc` /data/|/sdcard/|/proc/|/sys/class/net|/system/bin/sh → 0 命中
- `exec_kw` execv|system\(|popen|dlopen|dlsym → 0 命中

- base64 候选解码命中：0（见 `libabcdefgaaa-b64-decoded.txt`，可打印>0.8 且含 http|.|:|/）

## libdiacore.so（arm64-v8a）

### ELF 元信息
- NEEDED: `libjnigraphics.so`, `libm.so`, `libdl.so`, `libc.so`
- RPATH/RUNPATH: (无) / (无)
- BuildID: `2e94303575063a7980a7732b66cfcdbef06d6665`
- .comment: `Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) clang version 19.0.1 (https://android.googlesource.com/toolchain/llvm-project 97a699bf4812a18fb657c2779f5296a4ab2694d2)`
- 全文见 `libdiacore-elfmeta.txt`（含 size -A 节大小 / file）

### 导出面
- GLOBAL FUNC 导出：10 个；JNI_OnLoad：present；Java_* 显式导出：0 个
- registerNatives 属运行时动态注册，导出表不可见，静态侧只能看 JNI_OnLoad 存在性

### 网络族导入（0 命中）

### strings 命中明细（每模式计数 + 前 30 条样本）
- `url` https?:// → 2 命中
    - [ascii] `Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) clang version 19.0.1 (https://android.googlesource.com/toolchain/llvm-project 97a699bf4812a18fb657c2779f5296a4ab2694d2)`
    - [ascii] `Android (13624864, based on r530567e) clang version 19.0.1 (https://android.googlesource.com/toolchain/llvm-project 97a699bf4812a18fb657c2779f5296a4ab2694d2)`
- `ipv4` \b([0-9]{1,3}\.){3}[0-9]{1,3}\b → 0 命中
- `vendor_domain` \b(taobao|baidu|qq|weixin|wechat|163|126|kuwo|kugou|tencent|umeng|bugly|alipay|aliyun|volc|bytedance|github|gitlab|gitee)\. → 0 命中
- `tld_path` \.(com|cn|net|top|xyz|icu|click|tk|me|io|app)/\b → 2 命中
    - [ascii] `Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) clang version 19.0.1 (https://android.googlesource.com/toolchain/llvm-project 97a699bf4812a18fb657c2779f5296a4ab2694d2)`
    - [ascii] `Android (13624864, based on r530567e) clang version 19.0.1 (https://android.googlesource.com/toolchain/llvm-project 97a699bf4812a18fb657c2779f5296a4ab2694d2)`
- `telegram` t\.me/ → 0 命中
- `onion` \.onion → 0 命中
- `base64_kw` base64 → 0 命中
- `pem` -----BEGIN → 0 命中
- `so_ref` \.so\b → 5 命中
    - [ascii] `libc.so`
    - [ascii] `libjnigraphics.so`
    - [ascii] `libm.so`
    - [ascii] `libdl.so`
    - [ascii] `libdiacore.so`
- `path_proc` /data/|/sdcard/|/proc/|/sys/class/net|/system/bin/sh → 0 命中
- `exec_kw` execv|system\(|popen|dlopen|dlsym → 0 命中

- base64 候选解码命中：0（见 `libdiacore-b64-decoded.txt`，可打印>0.8 且含 http|.|:|/）

## libkijhhh.so（arm64-v8a）

### ELF 元信息
- NEEDED: `liblog.so`, `libz.so`, `libstdc++.so`, `libm.so`, `libc.so`, `libdl.so`
- RPATH/RUNPATH: (无) / (无)
- BuildID: `N/A`
- .comment: `GCC: (GNU) 4.9 20140827 (prerelease) | clang version 3.6`
- 全文见 `libkijhhh-elfmeta.txt`（含 size -A 节大小 / file）

### 导出面
- GLOBAL FUNC 导出：192 个；JNI_OnLoad：present；Java_* 显式导出：0 个
- registerNatives 属运行时动态注册，导出表不可见，静态侧只能看 JNI_OnLoad 存在性

### 网络族导入（5 命中）
- `connect`
- `gethostbyname`
- `recv`
- `send`
- `socket`
- 导入侧 exec 族：`dlopen`, `dlsym`

### strings 命中明细（每模式计数 + 前 30 条样本）
- `url` https?:// → 2 命中
    - [ascii] `http://10.18.32.87:8080/myApp/HelloWorld`
    - [ascii] `http://`
- `ipv4` \b([0-9]{1,3}\.){3}[0-9]{1,3}\b → 1 命中
    - [ascii] `http://10.18.32.87:8080/myApp/HelloWorld`
- `vendor_domain` \b(taobao|baidu|qq|weixin|wechat|163|126|kuwo|kugou|tencent|umeng|bugly|alipay|aliyun|volc|bytedance|github|gitlab|gitee)\. → 0 命中
- `tld_path` \.(com|cn|net|top|xyz|icu|click|tk|me|io|app)/\b → 0 命中
- `telegram` t\.me/ → 0 命中
- `onion` \.onion → 0 命中
- `base64_kw` base64 → 0 命中
- `pem` -----BEGIN → 0 命中
- `so_ref` \.so\b → 13 命中
    - [ascii] `liblog.so`
    - [ascii] `libz.so`
    - [ascii] `libstdc++.so`
    - [ascii] `libm.so`
    - [ascii] `libc.so`
    - [ascii] `libdl.so`
    - [ascii] `lib89d474a4-df75-4f52-9328-32d1180a94f8.so`
    - [ascii] `liblog.so`
    - [ascii] `libc.so`
    - [ascii] `libm.so`
    - [ascii] `libdl.so`
    - [ascii] `lib89d474a4-df75-4f52-9328-32d1180a94f8.so`
    - [ascii] `xxx.so`
- `path_proc` /data/|/sdcard/|/proc/|/sys/class/net|/system/bin/sh → 5 命中
    - [ascii] `/proc/meminfo`
    - [ascii] `/sys/class/net/wlan0/address`
    - [ascii] `/sys/class/net/eth0/address`
    - [ascii] `/proc/version`
    - [ascii] `/proc/self/maps`
- `exec_kw` execv|system\(|popen|dlopen|dlsym → 2 命中
    - [ascii] `dlsym`
    - [ascii] `dlopen`

- base64 候选解码命中：0（见 `libkijhhh-b64-decoded.txt`，可打印>0.8 且含 http|.|:|/）

## 老线交叉对拍

0 命中：净新增 so 的 sha256 与天天版/红果/番茄老线样本（385 行 so）均不同。
注：同族改壳常改重编导致 hash 漂移，0 命中 ≠ 非同作者，只登记不断。

## 诚实口径（必读）

以上为静态导入符号与字符串层证据；未发现外联证据 ≠ 证明无网络能力，静态分析不能证绝对无（混淆/运行时拼接可规避本层检测）。
本报告不做 A/B/C/D 定性；净新增口径、同名异体红旗与老线命中均交人工复核。
