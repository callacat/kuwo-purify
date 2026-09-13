# KUWO-3b2 round 1 构建报告（run 34730840890）

- 产物：Release kuwo3-round1 / kuwo-12.2.2.0-purified-r1.apk
- sha256：9acc52daeb9a390e15d6bc002fd7f801c29d6cc896b9513a521f3ef0ac92869b
- 大小：242125949 B
- patch 点：P1=1（c.h()V return-void）/ P2=2（b3/a ConfigManager+ServiceManager init nop）/ P3=2（sd/d FireEye init+start nop）——与点位表全集一致，其余候选未碰
- 签名：本线新生成 keystore CN=KUWO-Purify（cert sha256 见 verify-kuwo3b2.txt），v1+v2+v3
- 验证：apksigner verify 过 + 三桩 dex 反解生效（c.smali h()V 首指令 return-void、b3/a 与 sd/d invoke→nop）+ dex 数 15
- 版本一致性：round 单源=Release tag kuwo3-round1 自动递增（无→1），产物名/报告/tag 三处同源
