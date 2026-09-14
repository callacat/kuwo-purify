# DM-1 W1 方法级 diff 统计口径（双侧同集合）

| 指标 | 数 | 说明 |
|---|---|---|
| 东明版 smali 文件数（全集） | 118464 | 18 dex 全部 |
| 官方版 smali 文件数（全集） | 118374 | 15 dex 全部 |
| 双侧同名对齐类 | 118374 | 可比集合（红旗只在此口径数） |
| 字节一致（未触碰） | 52832 | 快路径，免解析 |
| 内容差异类（深解析） | 65542 | 进方法级 diff |
| 新增类（仅东明有） | 90 | 与 DM-0「真新增90类」口径应一致或为其超集（同名跨dex算一类） |
| 删除类（仅官方有） | 0 | DM-0 结论应为 0，命中即异常 |
| mod 侧同名类跨 dex 重复 | 0 | 应为0 |
| base 侧同名类跨 dex 重复 | 0 | 应为0 |
| 语义变化方法（归一化后仍异） | 259 | 体级噪声剥离后 |
| 仅 mod 方法 | 1 | 差异类内的新增方法 |
| 仅 base 方法 | 0 | 差异类内被删方法 |
| ★体首 return 截断红旗 | 8 | 高信噪作者真实点位 |

## 新增类按包前缀聚合（top）
- `com/dm/dia` × 44
- `com/vip/yf` × 25
- `com/kw/cj` × 14
- `abcdefgaaa/Loader` × 1
- `abcdefgaaa/hidden/Hidden0` × 1
- `kwpass/KpkUtilX` × 1
- `njggg/Loader` × 1
- `njggg/hidden/Hidden0` × 1
- `nt/phkc/rrqfjf` × 1
- `rj/lddne/valniaxvw` × 1
