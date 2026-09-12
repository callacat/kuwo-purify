# 官方基线登记：kuwo-12.2.2.0-official.apk

> 本文件第一行 64 位 hex = CI 校验用官方基线 sha256（CI 拉 Release asset 后 `sha256sum -c` 强校验）。
> 未登记前占位符会让 CI fail-fast，属预期。

OFFICIAL-SHA256-PENDING

## 元数据（基线到手后回填）
- 下载源：PENDING
- 实测 HTTP：PENDING
- 大小：应用宝标称 225093203 B（待实测核对）
- versionName：12.2.2.0（应用宝详情页 version_name=12.2.2.0 + 豌豆荚 vcode=12220/vname=12.2.2.0 双源确认存在该版本）
- 官方证书 DN：PENDING
- 官方证书 SHA-256：PENDING
- 验签工具与输出：PENDING

## 候选源调研（真实抓取记录，子代理 a32e635a 回收）
- 应用宝 sj.qq.com/appdetail/cn.kuwo.player → HTTP 200，页面含 version_name=12.2.2.0、apk_size=225093203、developer=北京酷我科技有限公司、update_time=1788427441（2026-09-03）
- 豌豆荚 /apps/28047 → 详情页 data-app-vcode=12220 data-app-vname=12.2.2.0（app-id 28047）
- APKPure：仅到 11.3.x，已排除
- 直链实测与下载：进行中（见 task-context-KUWO1.md）
