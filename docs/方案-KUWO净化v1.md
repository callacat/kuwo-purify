# KUWO 净化方案（v1，2026-09-13 老马）

任务 rid: recvv1L7iC5va5 | 样本: callacat/kuwo-purify Release `samples` / asset `kuwo-12.2.2.0-tiantian-mod.apk`
SHA-256: f2f20005e7234025383a517053703a922173fd05dbc7d6a48d09c62fe9b8732b（242,089,148 B）
作者归属判定：见 KUWO-0-作者归属核验.md —— **非番茄/红果壳作者**（证书 CN=xinshidai0 ≠ CN=L），路线=直接改包重签（无 Tinker 壳）。

## 阶段拆分

### KUWO-1：基线 + 全量 diff + 后门审计素材（码农，CI 执行）
1. **获取官方基线** cn.kuwo.player 12.2.2.0（版本必须逐位一致）：候选源 APKPure(仅到 11.3.x，不够则继续找 APKCombo/豌豆荚/应用宝/酷我官网 CDN)、华为 AppGallery dcn 直链。拿到后 sha256 登记 + `apksigner verify --print-certs` 记录官方证书。找不到 12.2.2.0 就用最近官方版本做 diff 基线并在报告标注版本差风险。
2. 双包 dex 逐一对比（mod 15 dex vs 官方 dex），产出 diff-report：新增类清单 / 修改方法清单 / 删除方法清单 + 差异方法 baksmali 全文 tar.gz（发 Release，勿入 git 树）。
3. 端点审计：mod 全 dex URL 常量 vs 官方 URL 常量集合差，重点候选 `api.ktvdaren.com` 的引用类/用途链。
4. 网络出口/动态加载/敏感 API 三项素材输出（老马定性，码农不做分类判定）。
5. native so 清单 hash 对比（官方 so 未动=攻击面收敛 Java 层；动了的列名单独标红）。
6. 报告 docs/kuwo1-diff-report.md + CI 构建产物发 Release。

### KUWO-2：老马分类判定（编排方，非 CI）
基于 diff-report 表驱动分类 A/B/C/D，出净化蓝图点位表。

### KUWO-3：净化重打包（码农，CI）
按蓝图 apktool d -r → smali patch → b → zipalign -P 16 → apksigner v1v2v3。
**注意**：作者 keystore 私钥不可得 → 净化版用本线自签 keystore（沿用仓库既有 CN=L 或新生成，报告写明）→ 装机需先卸载天天版（INSTALL_FAILED_UPDATE_INCOMPATIBLE 预期内）。

### KUWO-4：真机四判据实测（老马）
金丝雀基线（官方包）→ 装净化版 → 冷启动无 FATAL / VIP 态在 / 去广告生效 / 播放功能实测 → force-stop 收尾。

## 红线（写进每轮派单）
- 重活全在 CI（D7），CT110 与码农本机不跑 baksmali 全树扫/重打包
- 样本已在 Release，禁止任何上传动作
- 版权物不入库（.gitignore 兜底）
- 审计闭环前禁止把未审计天天版底包装任何测试机
