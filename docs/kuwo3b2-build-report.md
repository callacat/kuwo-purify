# KUWO round 4 构建报告（run 34739826622）

- 产物：Release kuwo3-round4 / kuwo-12.2.2.0-purified-r4.apk
- sha256：3e0ded91779478ce030e5cd93e98feae0305e0f01bc338314f21c9a5bd391e86
- 大小：242125949 B
- patch 全集 5 处：P1=1（c.h()V return-void）/ P2=2（b3/a init nop）/ P3=2（sd/d FireEye nop）/ B2=1（q1.b.a init 2×nop）/ B1=1（uilib.m F 按值过滤）——3b2+R2b 点位全集，其余未碰
- 签名：本线 keystore CN=KUWO-Purify（cert sha256 见 verify-kuwo3b2.txt），v1+v2+v3
- 验证：apksigner verify 过 + 五桩 dex 反解 + dex 数 15
- 版本一致性：round 单源=Release tag kuwo3-round4 自动递增（3→4）
