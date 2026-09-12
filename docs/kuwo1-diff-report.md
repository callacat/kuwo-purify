# KUWO-1 mod vs 官方基线 dex 全量 diff 报告

> 样本: kuwo-12.2.2.0-tiantian-mod.apk（15 dex，CN=xinshidai0 重签）
> 基线: kuwo-12.2.2.0-official.apk（集合口径：双侧同为 APK 全量 classes*.dex，红线对齐，防 hg2 式漂移误报）
> 方法=类名对齐+调试指令剥离（继承番茄 16a / 红果 HG-1 修正口径）。分类判定权在老马，本报告只出素材。

## 1. 总览

- mod 类总数: 118381 ｜ 官方基线类总数: 118374
- **真新增类: 7**（全文见 kuwo1-diff-baksmali/added/）
- **真删除类: 0**（全文见 kuwo1-diff-baksmali/removed/）
- **修改类: 1869**（差异方法全文见 kuwo1-diff-baksmali/changed/，[MOD-ADDED]/[MOD-CHANGED vs BASE-ORIGINAL]/[BASE-REMOVED-IN-MOD] 三段标注）
- 修改类中差异方法: 新增 1691 / 删除 683 / 修改 4244

- 跨 dex 重复类名（mod）: 0 ｜（base）: 0（应为 0，非 0 需红旗解释）

## 2. 真新增类清单（按包前缀分组）

### `tian0/` — 4 类
- `tian0/tan.smali`
- `tian0/ۣ۟ۡۤۢ.smali`
- `tian0/۟ۢ۠۟ۨ.smali`
- `tian0/۟ۥۣ۠ۤ.smali`

### `cn/kuwo/` — 2 类
- `cn/kuwo/base/bean/vipnew/ۣۣۣۣ۟.smali`
- `cn/kuwo/peculiar/specialinfo/۟ۤۤۨ۟.smali`

### `tian0/hidden/` — 1 类
- `tian0/hidden/Hidden0.smali`

## 3. 修改类清单（按差异方法总数降序）

| 类 | +新增 | -删除 | ~修改 | 合计 |
|---|---|---|---|---|

## 4. 真删除类清单

（无——mod 未删除任何基线类）

## 5. 归档结构

```
kuwo1-diff-baksmali/
├── added/    真新增类 baksmali 全文
├── changed/  修改类差异方法全文（三段标注）
└── removed/  删除类基线全文
```
