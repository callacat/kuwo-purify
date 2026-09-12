# kuwo-purify

酷我音乐 cn.kuwo.player 12.2.2.0「天天(新时代/CN=xinshidai0)」mod 净化审计线（rid recvv1L7iC5va5）。
目标 = 后门审计 → 净化后自听，不分发。方案与阶段拆分见任务目录 `方案-KUWO净化v1.md`（仓内镜像 docs/）。

## 当前状态（KUWO-1 · 码农 CI 线）
- 输入样本：Release `samples` / `kuwo-12.2.2.0-tiantian-mod.apk`（sha256 f2f20005…8732b，禁再上传）
- 官方基线：Release `samples` / `kuwo-12.2.2.0-official.apk`（获取与证书登记见 docs/baseline-official.md）
- 执行：`.github/workflows/kuwo-crack-audit.yml`（workflow_dispatch）
- 产物：docs/kuwo1-diff-report.md 等三份报告入 git；baksmali 全文归档 + 三清单 txt 走 Release `kuwo1-artifacts`

## 纪律
- 重活全在 GitHub Actions runner；CT110/本机零重活（D7）
- 版权物不落 git（.gitignore 兜底）
- 审计素材只出表格不做定性（判定权在老马）；未审计包禁止装任何设备
