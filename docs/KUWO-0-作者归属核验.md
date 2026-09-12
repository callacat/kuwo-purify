# KUWO-0 作者归属核验 + 基线摸底（2026-09-13，老马）

## 样本
- 来源：东哥 09-13 01:12 传协作群，文件 `酷我音乐_12.2.2.0高级版 天天_@𝑷𝑱𝑨𝑷𝑲.apk`
- 大小：242,089,148 B；SHA-256 `f2f20005e7234025383a517053703a922173fd05dbc7d6a48d09c62fe9b8732b`
- GitHub 存证：callacat/kuwo-purify Release `samples`，asset `kuwo-12.2.2.0-tiantian-mod.apk`（服务端 digest 对拍一致）

## 作者归属判定：**不是同一作者（与番茄/红果壳作者无关联）**

### 铁证：外层签名证书
| 包 | 证书 DN | SHA-256 |
|---|---|---|
| 酷我 mod（天天） | `CN=xinshidai0` | `4f0a1e41747885479ef23bc505af3894259d73daac24fa2c8b0274c3c5f7360a` |
| 番茄壳 / 红果壳 | `CN=L,OU=L,O=L,...` | `eae34eaf890161920c66a2e8e5fa4c2757b8249e279dd4143ca50e39d008c328` |

证书逐字节不同 = 不同 keystore = 不同作者（私钥不跨人共享，无第二种解释）。
v1 签名条目名 `META-INF/新时代.SF/.RSA`（"xinshidai"= 新时代拼音），作者标识与文件名"天天"同一人设（天天→新时代系列 mod 作者）。

### 结构指纹：手法完全不同
| 观测 | 酷我 mod | 番茄/红果壳 |
|---|---|---|
| Tinker 壳 + 内嵌官方原包 | ❌ 无（无 assets/base.apk、无 liborgapk.so、无 tinker 字符串） | ✅ 壳包结构 |
| 签名层 | v1 完整重签（新时代.SF 条目名） | v2/v3-only，v1 剥除 |
| dex 数 | 15（classes.dex~classes15.dex） | 壳 23 dex + 内层原包 |
| zip 指纹 | 主体 flag=2048(UTF8)，无 comment | 混合 flag（含未加密 20/20/0 段） |
| Overlapped entries | 0（zipfile 全量可读，无加工损伤） | 有（zip bomb 拒读） |

结论：**直接改包重签路线**（apktool 级修改 + 自己的 keystore 全量重签），不是壳中壳。

## 对"能否复用之前操作"的回答
- ❌ 不能复用「该作者壳画像基线」（番茄 round16a / HG-1 重合率 diff 法）——作者不同、无壳层、没有可对比的既有作者代码画像。
- ✅ 可复用「净化方法论」（apk-repatch-pipeline 破解版底包改造路线的通用部分）：
  1. 全量 diff 先于任何 patch——但基线换成**官方酷我音乐 12.2.2.0**（本包内嵌无原包，需另行获取官方同版本）
  2. 差异方法分类权在老马（A 保/B 去广告保留/C 后门去除/D 会员增值保留）
  3. 表驱动+指纹抽样审读，禁全树暴力扫
  4. CI 构建（gha-build-farm 或本线新建 workflow），CT110 零重活
  5. 保守 patch：掐入口不撒网；产物同作者 keystore 重签（保覆盖安装）——注意：作者 keystore 私钥我们**没有**，净化版只能自签，装前需卸载天天版（记录在安装测试风险面）
- ⚠️ 与壳线最大差异：本包**签名非官方**，若酷我服务端按证书维度风控（音乐 App 常见=本地解锁+服务端弱风控），装官方能听的可能这里受限——金丝雀对照法先测。

## 非官方域名初扫（外层 dex URL 常量，Java 层）
354 域名中，剔除官方(kugou/kgimg/kuwo/腾讯系/字节系)后 ≥2 次命中仅少量长尾：github.com(注释/库残留)、dev.voicecloud.cn、da.mmarket.com、duiba、qbox.me、**api.ktvdaren.com**（2 次，来路不明，C 类嫌疑第一位候选）。无卡密/设备码/UI 关键词（设备码|卡密 命中 0）——**表面比番茄壳干净**，native so 层未深审，端点全量核查归 KUWO-1。
