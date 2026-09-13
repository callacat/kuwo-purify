# KUWO round 6 构建报告（run 34745599225）

- 产物：Release kuwo3-round6 / kuwo-12.2.2.0-purified-r6.apk
- sha256：725fe78091325eecb085aef71a15864b0ca17b845cd2cb288eadc2bec2311b37
- 大小：242125949 B
- patch 全集 4 处（round6：P1/B2 均撤销=真机实测副作用）：P2=2（b3/a init nop）/ P3=2（sd/d FireEye nop）/ B1=1（uilib.m F 按值过滤）/ C1=1（specialdialogconfig.a.init 体首 return-void 兜底）——其余未碰
- 签名：本线 keystore CN=KUWO-Purify（cert sha256 见 verify-kuwo3b2.txt），v1+v2+v3
- 验证：apksigner verify 过 + 四桩 dex 反解（P1/B2 已撤销）+ dex 数 15
- 版本一致性：round 单源=Release tag kuwo3-round6 自动递增（5→6）
