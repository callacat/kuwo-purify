04d89f31046d544be00a0c413bc5ea3ddd4040d3157bd2e96ca7a9194df0c882

# 官方基线登记：kuwo-12.2.2.0-official.apk

> 本文件第一行 64 位 hex = CI 校验用官方基线 sha256（CI 拉 Release asset 后 `sha256sum -c` 强校验）。
> GitHub 服务端 digest 与本地实测逐位一致（Release 387647133，state=uploaded）。

## 元数据（已核实）
- 下载源：豌豆荚 `https://www.wandoujia.com/apps/28047/download/dot` → 302 → `ucdl.25pp.com/fs08/2026-09-03/.../2_1e0dc6b5....apk?vcode=12220&pkg=cn.kuwo.player&md5=820f8e468d9130f5ac5cc6d14230da10`（短时效签名直链）
- SHA-256：04d89f31046d544be00a0c413bc5ea3ddd4040d3157bd2e96ca7a9194df0c882
- MD5：820f8e468d9130f5ac5cc6d14230da10（与 302 Location 内嵌 md5 参数逐位一致）
- 大小：234,633,069 B
- versionName：12.2.2.0（AXML 解码：versionCode=12220 / package=cn.kuwo.player，逐位一致）
- dex 数：15（与 mod 同构，交叉佐证为同一版本底包）
- 官方证书 DN：`CN=Kuwo, OU=Kuwo, O=Kuwo, L=Beijing, ST=Beijing, C=CN`
- 官方证书 SHA-256：`7c2be94824519118d4477f314532d844084440fbacc8a1941cffdb0f6fd62c2a`（apksigner 与 openssl 两工具交叉一致）
- 验签：apksigner v1+v2+v3 全部 Verified（v3.1/v4/SourceStamp false 属正常）
- 官方性判定：**CN=Kuwo ≠ mod 的 CN=xinshidai0**，证书逐字节不同 → 确认官方签名包，可作净化审读基线

## 备注
- 应用宝标称 apk_size=225093203 与实际 234633069 差 9.5MB（疑渠道快照/分包差异），不影响本包自验链完整性。
- 候选源调研结论：APKPure/APKCombo 仅到 11.3.x（排除）；应用宝 PC 端匿名直链已死（版本元数据可信）；华为 AppGallery 需客户端；酷我官网无手机版直链。**豌豆荚为唯一可复现匿名直链源**。
