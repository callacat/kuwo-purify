# KUWO-3a 广告/埋点残留面素材清单

> 输入=Release kuwo1-artifacts 的 kuwo1-diff-baksmali.tar.gz + kuwo1-endpoints.md，**未回扫 base 全量 dex**（表驱动禁暴力扫）。
> 只出现状事实与候选入口，不写删点建议；分类判定权在老马。
> 规模：changed 类 1869；表① com/tencentmusic/ad 命中 202。

## 表① 广告 SDK 面（mod changed 内现状）

> 前缀实测口径：`com/tencentmusic/ad/` 命中 202 类；`com/tencent/gdt` 命中 0、`com/bytedance/sdk` 命中 0、`com/kuaishou` 命中 0、`pangle` 命中 0、`com/sigmob` 命中 0、`com/tencent/ms/` 命中 0、`com/bytedance/applog` 命中 0 均 **0**（酷我 12.2.2.0 changed 面不含这些第三方广告 SDK；广点通/快手/穿山甲候选经证伪，非抽样遗漏）。
> 「NOP 桩」=mod 新增且体仅 return-void 空壳。

| 类 | mod 现状 | 入口动词命中 |
|---|---|---|
| `com/tencentmusic/ad/TMEAds.smali` | 改×5 | — |
| `com/tencentmusic/ad/a0/b.smali` | 改×1 | — |
| `com/tencentmusic/ad/a0/d.smali` | 改×1 | — |
| `com/tencentmusic/ad/a1/c.smali` | 改×1 | — |
| `com/tencentmusic/ad/a1/g.smali` | 改×1 | — |
| `com/tencentmusic/ad/a1/h.smali` | 改×3 | — |
| `com/tencentmusic/ad/a3/a.smali` | 改×1 | — |
| `com/tencentmusic/ad/adapter/ams/AMSSplashAdapter.smali` | 改×4 | — |
| `com/tencentmusic/ad/adapter/ams/nativead/AMSNativeAdAdapter$a.smali` | 改×1 | — |
| `com/tencentmusic/ad/adapter/common/RewardVideoAdapter.smali` | 改×2 | — |
| `com/tencentmusic/ad/adapter/common/SplashAdapter.smali` | 改×1 | — |
| `com/tencentmusic/ad/adapter/mad/hybridad/MADHybridCacheAdAdapter$b.smali` | 改×1 | — |
| `com/tencentmusic/ad/adapter/mad/hybridad/MADHybridCacheAdAdapter$c.smali` | 改×2 | — |
| `com/tencentmusic/ad/adapter/mad/nativead/MADNativeAdAdapter.smali` | 改×4 | — |
| `com/tencentmusic/ad/adapter/mad/reward/MADRewardVideoAdAdapter$b.smali` | 改×4 | — |
| `com/tencentmusic/ad/adapter/mad/reward/MADRewardVideoAdAdapter$c.smali` | 改×8 | — |
| `com/tencentmusic/ad/adapter/mad/reward/MADRewardVideoAdAdapter.smali` | 改×11 | — |
| `com/tencentmusic/ad/adapter/mad/splash/MADBaseSplashAdapter$c.smali` | 改×4 | — |
| `com/tencentmusic/ad/adapter/mad/splash/MADBaseSplashAdapter.smali` | 改×4 | — |
| `com/tencentmusic/ad/adapter/mad/splash/MADSplashPreloadAdapter$a.smali` | 改×2 | — |
| `com/tencentmusic/ad/adapter/mad/splash/MADSplashPreloadAdapter.smali` | 改×1 | — |
| `com/tencentmusic/ad/adapter/madams/splash/OperBaseSplashAdapter$Companion.smali` | 改×1 | — |
| `com/tencentmusic/ad/adapter/madams/splash/OperBaseSplashAdapter.smali` | 改×4 | — |
| `com/tencentmusic/ad/adapter/madams/splash/OperExpertSplashAdapter$a.smali` | 改×1 | — |
| `com/tencentmusic/ad/adapter/madams/splash/OperExpertSplashAdapter.smali` | 改×11 | — |
| `com/tencentmusic/ad/adapter/madams/splash/OperationPreloadAdapter.smali` | 改×1 | — |
| `com/tencentmusic/ad/b1/a.smali` | 改×1 | — |
| `com/tencentmusic/ad/b2/b.smali` | 改×1 | — |
| `com/tencentmusic/ad/b3/b.smali` | 改×1 | — |
| `com/tencentmusic/ad/b5/a.smali` | 改×1 | — |
| `com/tencentmusic/ad/base/config/Conf.smali` | 改×2 | — |
| `com/tencentmusic/ad/base/net/Request$a.smali` | 改×4 | — |
| `com/tencentmusic/ad/base/widget/TMEAdRoundFrameLayout$a.smali` | 改×1 | — |
| `com/tencentmusic/ad/base/widget/TMEAdRoundImageView$b$a.smali` | 改×1 | — |
| `com/tencentmusic/ad/c/a.smali` | 改×1 | — |
| `com/tencentmusic/ad/c3/d.smali` | 改×1 | — |
| `com/tencentmusic/ad/core/InitParams$Builder.smali` | 改×12 | — |
| `com/tencentmusic/ad/core/LoadAdParams$Builder.smali` | 改×7 | — |
| `com/tencentmusic/ad/core/a.smali` | 改×1 | — |
| `com/tencentmusic/ad/core/constant/SourceType.smali` | 改×1 | — |
| `com/tencentmusic/ad/core/model/PosConfigBean.smali` | 改×1 | — |
| `com/tencentmusic/ad/core/player/VideoView.smali` | 改×4 | — |
| `com/tencentmusic/ad/core/player/e.smali` | 改×1 | — |
| `com/tencentmusic/ad/core/player/nativeanim/a$c.smali` | 改×1 | — |
| `com/tencentmusic/ad/core/player/nativeanim/a.smali` | 改×2 | — |
| `com/tencentmusic/ad/d0/d.smali` | 改×1 | — |
| `com/tencentmusic/ad/d2/j.smali` | 改×1 | — |
| `com/tencentmusic/ad/d2/n.smali` | 改×6 | — |
| `com/tencentmusic/ad/e/a.smali` | 改×2 | — |
| `com/tencentmusic/ad/e0/b.smali` | 改×1 | — |
| `com/tencentmusic/ad/f5/f.smali` | 改×1 | — |
| `com/tencentmusic/ad/g1/l.smali` | 改×3 | — |
| `com/tencentmusic/ad/g1/m.smali` | 改×1 | — |
| `com/tencentmusic/ad/g2/a.smali` | 改×2 | — |
| `com/tencentmusic/ad/h0/a.smali` | 改×3 | — |
| `com/tencentmusic/ad/h2/f.smali` | 改×1 | — |
| `com/tencentmusic/ad/h2/j.smali` | 改×1 | — |
| `com/tencentmusic/ad/h3/f.smali` | 改×1 | — |
| `com/tencentmusic/ad/h4/a.smali` | 改×1 | — |
| `com/tencentmusic/ad/h5/a.smali` | 改×1 | — |
| `com/tencentmusic/ad/h5/b.smali` | 改×1 | — |
| `com/tencentmusic/ad/h5/c$a.smali` | 改×2 | — |
| `com/tencentmusic/ad/h5/c$b.smali` | 改×1 | — |
| `com/tencentmusic/ad/h5/c$c.smali` | 改×1 | — |
| `com/tencentmusic/ad/h5/c$d.smali` | 改×1 | — |
| `com/tencentmusic/ad/h5/c.smali` | 改×1 | — |
| `com/tencentmusic/ad/h5/j.smali` | 改×1 | — |
| `com/tencentmusic/ad/h5/m.smali` | 改×1 | — |
| `com/tencentmusic/ad/i/b.smali` | 改×1 | — |
| `com/tencentmusic/ad/i/h.smali` | 改×1 | — |
| `com/tencentmusic/ad/i/j.smali` | 改×1 | — |
| `com/tencentmusic/ad/i1/a$a.smali` | 改×2 | — |
| `com/tencentmusic/ad/i2/a.smali` | 改×9 | — |
| `com/tencentmusic/ad/i2/d.smali` | 改×2 | — |
| `com/tencentmusic/ad/integration/TMEAdTool.smali` | 改×4 | — |
| `com/tencentmusic/ad/integration/TMEMediaOption$Builder.smali` | 改×4 | — |
| `com/tencentmusic/ad/integration/apptask/TMEAppActiveTaskAD.smali` | 改×1 | — |
| `com/tencentmusic/ad/integration/apptask/TMEAppDownloadTaskAD.smali` | 改×1 | — |
| `com/tencentmusic/ad/integration/hippyad/HippyAdManagerModule.smali` | 改×1 | — |
| `com/tencentmusic/ad/integration/maskad/TMEMaskAd.smali` | 改×1 | — |
| `com/tencentmusic/ad/integration/nativead/TMENativeAdAsset$DefaultImpls.smali` | 改×1 | — |
| `com/tencentmusic/ad/integration/nativead/TMENativeAdTemplate$Builder.smali` | 改×3 | — |
| `com/tencentmusic/ad/integration/nativead/TMENativeAdTemplate.smali` | 改×1 | — |
| `com/tencentmusic/ad/integration/operationsplash/operationSplash/TMEOperationSplashAD.smali` | 改×3 | — |
| `com/tencentmusic/ad/integration/params/RewardVideoAdParams$Builder.smali` | 改×9 | — |
| `com/tencentmusic/ad/integration/rewardvideo/RewardADListener$DefaultImpls.smali` | 改×1 | — |
| `com/tencentmusic/ad/integration/rewardvideo/TMERewardVideoAD.smali` | 改×5 | — |
| `com/tencentmusic/ad/integration/web/TMEJsAD.smali` | 改×3 | — |
| `com/tencentmusic/ad/integration/web/TMEWebAD.smali` | 改×16 | — |
| `com/tencentmusic/ad/j2/a.smali` | 改×1 | — |
| `com/tencentmusic/ad/j5/b.smali` | 改×2 | — |
| `com/tencentmusic/ad/j5/i.smali` | 改×1 | — |
| `com/tencentmusic/ad/k/a.smali` | 改×1 | — |
| `com/tencentmusic/ad/k1/a$a.smali` | 改×1 | — |
| `com/tencentmusic/ad/k2/a.smali` | 改×1 | — |
| `com/tencentmusic/ad/k4/a.smali` | 改×2 | — |
| `com/tencentmusic/ad/k4/b.smali` | 改×2 | — |
| `com/tencentmusic/ad/k4/d.smali` | 改×1 | — |
| `com/tencentmusic/ad/k4/j.smali` | 改×4 | — |
| `com/tencentmusic/ad/k5/l.smali` | 改×1 | — |
| `com/tencentmusic/ad/l2/c$c.smali` | 改×1 | — |
| `com/tencentmusic/ad/l2/c.smali` | 改×1 | — |
| `com/tencentmusic/ad/l2/f.smali` | 改×1 | — |
| `com/tencentmusic/ad/m2/b$b.smali` | 改×1 | — |
| `com/tencentmusic/ad/m2/b.smali` | 改×5 | — |
| `com/tencentmusic/ad/m4/a.smali` | 改×1 | — |
| `com/tencentmusic/ad/m5/a.smali` | 改×1 | — |
| `com/tencentmusic/ad/n/k.smali` | 改×2 | — |
| `com/tencentmusic/ad/n0/i.smali` | 改×1 | — |
| `com/tencentmusic/ad/n0/j.smali` | 改×1 | — |
| `com/tencentmusic/ad/n1/a.smali` | 改×1 | — |
| `com/tencentmusic/ad/n2/a.smali` | 改×1 | — |
| `com/tencentmusic/ad/n2/c.smali` | 改×1 | — |
| `com/tencentmusic/ad/n3/b.smali` | 改×2 | — |
| `com/tencentmusic/ad/n4/b0.smali` | 改×1 | — |
| `com/tencentmusic/ad/n4/d.smali` | 改×1 | — |
| `com/tencentmusic/ad/n4/h.smali` | 改×1 | — |
| `com/tencentmusic/ad/n4/q.smali` | 改×1 | — |
| `com/tencentmusic/ad/n4/t.smali` | 改×3 | — |
| `com/tencentmusic/ad/n5/a.smali` | 改×1 | — |
| `com/tencentmusic/ad/n5/j.smali` | 改×1 | — |
| `com/tencentmusic/ad/n5/k.smali` | 改×2 | — |
| `com/tencentmusic/ad/n5/m.smali` | 改×6 | — |
| `com/tencentmusic/ad/o/e$a.smali` | 改×1 | — |
| `com/tencentmusic/ad/o/f.smali` | 改×1 | — |
| `com/tencentmusic/ad/o4/a.smali` | 改×1 | — |
| `com/tencentmusic/ad/p1/a.smali` | 改×1 | — |
| `com/tencentmusic/ad/p2/b.smali` | 改×1 | — |
| `com/tencentmusic/ad/p5/c.smali` | 改×1 | — |
| `com/tencentmusic/ad/q0/a$a.smali` | 改×1 | — |
| `com/tencentmusic/ad/q0/i.smali` | 改×1 | — |
| `com/tencentmusic/ad/q0/k.smali` | 改×1 | — |
| `com/tencentmusic/ad/q0/n.smali` | 改×2 | — |
| `com/tencentmusic/ad/q0/o.smali` | 改×1 | — |
| `com/tencentmusic/ad/q4/e.smali` | 改×1 | — |
| `com/tencentmusic/ad/r3/b.smali` | 改×1 | — |
| `com/tencentmusic/ad/r4/b.smali` | 改×1 | — |
| `com/tencentmusic/ad/r4/c.smali` | 改×1 | — |
| `com/tencentmusic/ad/r4/d.smali` | 改×2 | — |
| `com/tencentmusic/ad/r4/e.smali` | 改×1 | — |
| `com/tencentmusic/ad/r4/f$a.smali` | 改×1 | — |
| `com/tencentmusic/ad/r4/f.smali` | 改×7 | — |
| `com/tencentmusic/ad/r4/i.smali` | 改×1 | — |
| `com/tencentmusic/ad/r4/j.smali` | 改×1 | — |
| `com/tencentmusic/ad/r4/k.smali` | 改×1 | — |
| `com/tencentmusic/ad/r4/m.smali` | 改×1 | — |
| `com/tencentmusic/ad/r4/q.smali` | 改×1 | — |
| `com/tencentmusic/ad/r4/s$a.smali` | 改×1 | — |
| `com/tencentmusic/ad/r4/s.smali` | 改×12 | — |
| `com/tencentmusic/ad/r4/v.smali` | 改×1 | — |
| `com/tencentmusic/ad/r4/w.smali` | 改×1 | — |
| `com/tencentmusic/ad/r4/y.smali` | 改×1 | — |
| `com/tencentmusic/ad/s1/d$b.smali` | 改×1 | — |
| `com/tencentmusic/ad/s1/d.smali` | 改×4 | — |
| `com/tencentmusic/ad/s2/a.smali` | 改×2 | — |
| `com/tencentmusic/ad/s2/b.smali` | 改×1 | — |
| `com/tencentmusic/ad/s2/d.smali` | 改×4 | — |
| `com/tencentmusic/ad/t/c$a.smali` | 改×1 | — |
| `com/tencentmusic/ad/t/c.smali` | 改×4 | — |
| `com/tencentmusic/ad/t2/a.smali` | 改×1 | — |
| `com/tencentmusic/ad/t4/b.smali` | 改×7 | — |
| `com/tencentmusic/ad/tmead/core/activity/TmeAdCommonWebViewActivityProxy$d.smali` | 改×1 | — |
| `com/tencentmusic/ad/tmead/core/model/MADAdExt.smali` | 改×2 | — |
| `com/tencentmusic/ad/tmead/core/track/mad/MADReportObj.smali` | 改×3 | — |
| `com/tencentmusic/ad/tmead/core/widget/scratch/ScratchTextureView$b.smali` | 改×1 | — |
| `com/tencentmusic/ad/tmead/nativead/activity/TMEAdVideoTopActivityProxy$c.smali` | 改×1 | — |
| `com/tencentmusic/ad/tmead/nativead/activity/TMEAdVideoTopActivityProxy$e.smali` | 改×1 | — |
| `com/tencentmusic/ad/tmead/nativead/activity/TMEAdVideoTopActivityProxy.smali` | 改×1 | — |
| `com/tencentmusic/ad/tmead/nativead/template/danmu/TMEDanMuView$b.smali` | 改×1 | — |
| `com/tencentmusic/ad/tmead/nativead/template/danmu/TMEDanMuView$c$a.smali` | 改×1 | — |
| `com/tencentmusic/ad/tmead/nativead/template/flipgallerybanner/impl/a.smali` | 改×2 | — |
| `com/tencentmusic/ad/tmead/nativead/template/gallerybanner/GalleryBannerWidget$b.smali` | 改×1 | — |
| `com/tencentmusic/ad/tmead/nativead/template/gallerybanner/GalleryBannerWidget.smali` | 改×2 | — |
| `com/tencentmusic/ad/tmead/nativead/template/gallerybanner/impl/GalleryBannerCustomViewDefaultImpl.smali` | 改×1 | — |
| `com/tencentmusic/ad/tmead/nativead/template/slidercard/SliderCardWidget.smali` | 改×1 | — |
| `com/tencentmusic/ad/tmead/nativead/widget/BaseMediaView.smali` | 改×1 | — |
| `com/tencentmusic/ad/tmead/nativead/widget/ExpressMediaControllerView$b.smali` | 改×1 | — |
| `com/tencentmusic/ad/tmead/nativead/widget/ExpressMediaControllerView$f.smali` | 改×1 | — |
| `com/tencentmusic/ad/tmead/nativead/widget/ExpressMediaControllerView.smali` | 改×3 | — |
| `com/tencentmusic/ad/tmead/nativead/widget/FeedLayoutMediaView.smali` | 改×1 | — |
| `com/tencentmusic/ad/tmead/nativead/widget/MediaView.smali` | 改×1 | — |
| `com/tencentmusic/ad/tmead/reward/proxy/TMEPlayableRewardActivityProxy.smali` | 改×1 | — |
| `com/tencentmusic/ad/tmead/reward/proxy/TMERewardActivityProxy.smali` | 改×1 | — |
| `com/tencentmusic/ad/tmead/reward/proxy/TMEVLRewardActivityProxy.smali` | 改×3 | — |
| `com/tencentmusic/ad/u4/d.smali` | 改×1 | — |
| `com/tencentmusic/ad/v1/h.smali` | 改×2 | — |
| `com/tencentmusic/ad/w/b.smali` | 改×1 | — |
| `com/tencentmusic/ad/w0/k.smali` | 改×4 | — |
| `com/tencentmusic/ad/w2/a.smali` | 改×2 | — |
| `com/tencentmusic/ad/w3/b.smali` | 改×3 | — |
| `com/tencentmusic/ad/w3/g.smali` | 改×3 | — |
| `com/tencentmusic/ad/w3/i$a.smali` | 改×2 | — |
| `com/tencentmusic/ad/w4/a.smali` | 改×1 | — |
| `com/tencentmusic/ad/x1/e$a.smali` | 改×1 | — |
| `com/tencentmusic/ad/y/b.smali` | 改×1 | — |
| `com/tencentmusic/ad/y0/a.smali` | 改×1 | — |
| `com/tencentmusic/ad/y4/e.smali` | 改×1 | — |
| `com/tencentmusic/ad/y4/m.smali` | 改×1 | — |
| `com/tencentmusic/ad/z0/b.smali` | 改×1 | — |
| `com/tencentmusic/ad/z2/a.smali` | 改×2 | — |
| `com/tencentmusic/ad/z2/b.smali` | 改×2 | — |
| `com/tencentmusic/ad/z2/c.smali` | 改×6 | — |

- 表① 202 类合计：NOP 桩新增方法 0 个、mod 删除方法 0 个，其余为改体/新增实现。

> fanxing/zego 直播区：changed 实测 873 类（派单估 ~300，实际更大），本单三表不含其定性，规模差异如实登记供老马排期。

## 表② 埋点上报面（47 base-only URL 的 mod 现状归属）

> 方法：KUWO-1「基线 URL 在 mod 消失」47 个 → 在 changed 类归档中定位其出现的差异区段。
> 判读口径：URL 落在 [BASE-REMOVED-IN-MOD]/[BASE-ORIGINAL] 段=mod 已删/改写该方法体；落在 [MOD-ADDED]/[MOD-CHANGED]=改写后仍含上报体（存活）。

| 域名 | 命中URL数 | 涉及changed类 | mod仍含 |
|---|---|---|---|
| `abt-kuwo.tencentmusic.com` | 1 | 1 | 0 |
| `artistfeeds.tencentmusic.com` | 1 | 1 | 0 |
| `artistpicserver.kuwo.cn` | 2 | 1 | 0 |
| `baby.kuwo.cn` | 1 | 1 | 0 |
| `beian.miit.gov.cn` | 1 | 1 | 0 |
| `dataplan.kuwo.cn` | 1 | 1 | 0 |
| `down.shouji.kuwo.cn` | 1 | 1 | 0 |
| `h5app.kuwo.cn` | 4 | 1 | 0 |
| `imagexc.kuwo.cn` | 1 | 1 | 0 |
| `jx.kuwo.cn` | 1 | 1 | 0 |
| `kwmatch.kuwo.cn` | 1 | 1 | 0 |
| `m.kuwo.cn` | 2 | 1 | 0 |
| `mlyric.kuwo.cn` | 1 | 1 | 0 |
| `mobi.kuwo.cn` | 1 | 1 | 0 |
| `mobi.tencentmusic.com` | 1 | 1 | 0 |
| `mobile.kuwo.cn` | 2 | 1 | 0 |
| `mobilebasedata.kuwo.cn` | 1 | 1 | 0 |
| `mobileinterfaces.kuwo.cn` | 2 | 1 | 0 |
| `musicpay.kuwo.cn` | 1 | 1 | 0 |
| `ncomment.kuwo.cn` | 1 | 1 | 0 |
| `nmobi.kuwo.cn` | 1 | 1 | 0 |
| `nmsearch.kuwo.cn` | 1 | 1 | 0 |
| `nmsublist.kuwo.cn` | 1 | 1 | 0 |
| `privacy.qq.com` | 1 | 1 | 0 |
| `proxy.kuwo.cn` | 1 | 1 | 0 |
| `rich.kuwo.cn` | 1 | 1 | 0 |
| `search.kuwo.cn` | 1 | 1 | 0 |
| `treehole.tencentmusic.com` | 2 | 1 | 0 |
| `vip1.kuwo.cn` | 3 | 1 | 0 |
| `wapi.kuwo.cn` | 2 | 1 | 0 |
| `wapi.tencentmusic.com` | 1 | 1 | 0 |
| `www.kuwo.cn` | 1 | 1 | 0 |
| `xcstat.kuwo.cn` | 1 | 1 | 0 |
| `y.qq.com` | 1 | 1 | 0 |
| `y.tencentmusic.com` | 2 | 1 | 0 |

- **结构发现（重要，防误读）**：47/47 个消失 URL 命中 `cn/kuwo/base/utils/s2.smali` 的删除/原文段——即这些 URL 是 s2 字符串池 getter 的明文，被 native 化搬运（表③ 672 对）后从 Java 侧消失。
- mod 仍含上报体的类命中 0 处。
> ⚠️ **「URL 消失」≠「上报链被删」**：调用这些 getter 的统计/上报类若未进 changed 名单，native 化后运行时字符串仍可能指向同一端点（native 侧不可见于 Java 差集）。判定权在老马，此处仅提示误读风险。
> 全行明细（URL×类×区段×判读）→ kuwo3-ep-locate.txt。

### 表②b 统计/上报相关 changed 类现状（路径启发式，仅 changed 面）

> 口径：changed 1869 类中路径含 statistic/analytics/stat*/report/monitor/crash/track/log/bi/rif/xcstat 者；「未动区」存活入口不在 changed 集内，禁全扫不列。

| 类 | mod 现状 |
|---|---|
| `com/kugou/fanxing/allinone/watch/liveroominone/bi/SearchStatisticManager.smali` | 改×3 |
| `com/kugou/fanxing/allinone/watch/liveroominone/helper/EnterLiveRoomFailApmReporter.smali` | 改×2 |
| `com/kugou/fanxing/allinone/watch/liveroominone/helper/FABottomSheetDialogReportHelper.smali` | 改×1 |
| `com/kugou/fanxing/allinone/watch/liveroominone/helper/StayRoomReportHelper.smali` | 改×2 |
| `com/tencent/wns/jce/QMF_SERVICE/WNS_PUSH_SDK/WnsPushReportReq.smali` | 改×1 |
| `com/tencent/youtu/sdkkitframework/liveness/FaceTrackerState.smali` | 改×1 |
| `com/tencentmusic/ad/tmead/core/track/mad/MADReportObj.smali` | 改×3 |
| `com/tme/fireeye/crash/comm/utils/DeviceUtils.smali` | 改×1 |
| `com/tme/fireeye/crash/comm/utils/Utils.smali` | 改×2 |
| `com/tme/fireeye/crash/protocol/fireeye/RqdStrategy.smali` | 改×1 |
| `com/tme/fireeye/memory/bitmap/BitmapDetectorManager$exceedBitmapReporter$1.smali` | 改×1 |
| `com/tme/fireeye/memory/bitmap/BitmapDetectorManager$invisibleBitmapReporter$1.smali` | 改×1 |
| `com/tme/fireeye/memory/viewdetect/ViewVisibleDetectManager$reporter$1.smali` | 改×1 |
| `com/tme/lib_webcontain_hippy/core/report/HippyReporter$Companion$hippyLoadResultReport$1.smali` | 改×1 |
| `com/tme/lib_webcontain_hippy/core/report/HippyReporter$Companion.smali` | 改×2 |
| `com/tme/rif/client/api/LiveClient.smali` | 改×1 |
| `com/tme/rif/client/api/LiveClientInternal.smali` | 改×1 |
| `com/tme/rif/common/utils/Uri2PathUtil.smali` | 改×1 |
| `com/tme/rif/config/AppBuildConfig.smali` | 改×1 |
| `com/tme/rif/config/ConfigManager.smali` | 改×1 |
| `com/tme/rif/service/statistics/ReportParam.smali` | 改×1 |
| `com/tme/rif/service/webbridge/LiveWebBridge$enableJsBridge$callback$1.smali` | 改×3 |
| `com/tme/rif/service/webpage/model/WebChromeClientCallback$DefaultImpls.smali` | 改×7 |
| `com/tme/rif/service/webpage/model/WebViewClientCallback$DefaultImpls.smali` | 改×7 |
| `com/tme/rif/service/webpage/model/a.smali` | 改×7 |
| `com/tme/rif/service/webpage/model/b.smali` | 改×7 |

- 表②b 合计 26 类。

## 表③ s2.smali(+672/-672) 定性素材

- mod 新增 **native 声明方法 672 个** ↔ 基线删除非 native 方法 672 个，**签名（名+参+返回）100% 配对 672 对**——纯 Java 实现体→native 声明位移，零净增/净缺。
- 配对返回类型：String 664 / void 5 / StringBuilder 3 / 其他 0
- 配对签名 672 行 → kuwo3-s2-pairs.txt（Release kuwo3a-artifacts）
- 挂载画像对照：tian0/tan `registerNativesForClass`×1、密钥串 `ssXpix…`×1、`System.load`×0 → s2 native 实现由 tan 注册桥挂接 libtian.so（Soforge 壳，KUWO-1 定案）。
- **事实结论段（供老马引用）**：672 对全 String 进出 + tan 的 Long.decode 密钥链 → s2=官方工具类字符串加解密方法整体 native 化搬运（VIP 字符串加密面），非功能删除。净化视角属 D 类会员机制依赖，**不属 B 广告面**。

