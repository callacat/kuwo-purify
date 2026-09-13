# KUWO round 5 构建报告（run 34741354727）

- 产物：Release kuwo3-round5 / kuwo-12.2.2.0-purified-r5.apk
- sha256：bf425d4e23684308811b0fafaad8863639e151a05a53e62e38f066da3614a49d
- 大小：242125949 B
- patch 全集 4 处（round5，P1 已撤销=老马 r4 实测副作用）：P2=2（b3/a init nop）/ P3=2（sd/d FireEye nop）/ B2=1（q1.b.a init 2×nop）/ B1=1（uilib.m F 按值过滤）——其余未碰
- 签名：本线 keystore CN=KUWO-Purify（cert sha256 见 verify-kuwo3b2.txt），v1+v2+v3
- 验证：apksigner verify 过 + 四桩 dex 反解（P1 已撤销）+ dex 数 15
- 版本一致性：round 单源=Release tag kuwo3-round5 自动递增（4→5）
