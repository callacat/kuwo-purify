# KUWO-3b1 广告入口存活面 + 埋点 init 存活面反查

> 输入=Release samples 双包（官方基线全 dex 反查 caller + mod 现状对照）+ KUWO-1 changed-classes.txt。
> 三态：`活-unchanged`（caller 未被 mod 动过）/ `活-changed仍调`（动过但 invoke 仍在）/ `已杀·断`。`断?`=不在 changed 却 invoke 消失，疑正则误捕需复核。
> 表①口径=非 com/tencentmusic/ad 包的业务 caller；表②剔除 SDK 包内部自调用。**判定权在老马。**
> 规模：表① 175 条（活 175）、表② 7 条（活 4）、表③候选 91 类。行号=官方基线 smali 行号，可直接复核。

## 表① 广告业务入口存活表

| caller 类 | dex | 所在方法 | 官方行 | 被调门面 | mod 现状 |
|---|---|---|---|---|---|
| `cn/kuwo/mod/mobilead/n.smali` | classes8 | `public F(Landroid/view/ViewGroup;Landroid/view/View;Lcn/kuwo/mod/mobilead/r;Z)V` | 683 | `Lcom/tencentmusic/ad/TMEAds;->updateLastShowSplashTimeForClient` | **活-unchanged** |
| `cn/kuwo/mod/mobilead/tmead/TMESplashOneshotExt.smali` | classes8 | `public static final x(Lcom/tencentmusic/ad/integration/operationsplash/operation` | 819 | `Lcom/tencentmusic/ad/integration/operationsplash/operationSplash/TMEOperSplashAdAsset;->getSplashSource` | **活-unchanged** |
| `cn/kuwo/mod/mobilead/tmead/c.smali` | classes8 | `public static h()V` | 435 | `Lcom/tencentmusic/ad/TMEAds;->init` | **活-unchanged** |
| `cn/kuwo/mod/mobilead/tmead/c.smali` | classes8 | `public static j()Z` | 493 | `Lcom/tencentmusic/ad/TMEAds;->isInitialized` | **活-unchanged** |
| `cn/kuwo/mod/mobilead/tmead/c.smali` | classes8 | `public static h()V` | 442 | `Lcom/tencentmusic/ad/TMEAds;->registerAdImageLoadProxy` | **活-unchanged** |
| `cn/kuwo/mod/mobilead/tmead/c.smali` | classes8 | `public static h()V` | 449 | `Lcom/tencentmusic/ad/TMEAds;->registerSchemeHandlerProxy` | **活-unchanged** |
| `cn/kuwo/mod/mobilead/tmead/c.smali` | classes8 | `public static o(Ljava/lang/String;)V` | 606 | `Lcom/tencentmusic/ad/TMEAds;->updateQimei` | **活-unchanged** |
| `cn/kuwo/mod/mobilead/tmead/c.smali` | classes8 | `public static q(Ljava/lang/String;)V` | 677 | `Lcom/tencentmusic/ad/TMEAds;->updateUserInfo` | **活-unchanged** |
| `cn/kuwo/mod/mobilead/tmead/c.smali` | classes8 | `public static h()V` | 307 | `Lcom/tencentmusic/ad/core/InitParams$Builder;-><init>` | **活-unchanged** |
| `cn/kuwo/mod/mobilead/tmead/c.smali` | classes8 | `public static h()V` | 334 | `Lcom/tencentmusic/ad/core/InitParams$Builder;->amsMediaSource` | **活-unchanged** |
| `cn/kuwo/mod/mobilead/tmead/c.smali` | classes8 | `public static h()V` | 429 | `Lcom/tencentmusic/ad/core/InitParams$Builder;->build` | **活-unchanged** |
| `cn/kuwo/mod/mobilead/tmead/c.smali` | classes8 | `public static h()V` | 320 | `Lcom/tencentmusic/ad/core/InitParams$Builder;->debugMode` | **活-unchanged** |
| `cn/kuwo/mod/mobilead/tmead/c.smali` | classes8 | `public static h()V` | 341 | `Lcom/tencentmusic/ad/core/InitParams$Builder;->enableLog` | **活-unchanged** |
| `cn/kuwo/mod/mobilead/tmead/c.smali` | classes8 | `private static d(Lcom/tencentmusic/ad/core/InitParams$Builder;Ljava/lang/String;` | 105 | `Lcom/tencentmusic/ad/core/InitParams$Builder;->loginAppId` | **活-unchanged** |
| `cn/kuwo/mod/mobilead/tmead/c.smali` | classes8 | `private static d(Lcom/tencentmusic/ad/core/InitParams$Builder;Ljava/lang/String;` | 115 | `Lcom/tencentmusic/ad/core/InitParams$Builder;->loginOpenid` | **活-unchanged** |
| `cn/kuwo/mod/mobilead/tmead/c.smali` | classes8 | `private static d(Lcom/tencentmusic/ad/core/InitParams$Builder;Ljava/lang/String;` | 100 | `Lcom/tencentmusic/ad/core/InitParams$Builder;->loginType` | **活-unchanged** |
| `cn/kuwo/mod/mobilead/tmead/c.smali` | classes8 | `public static h()V` | 386 | `Lcom/tencentmusic/ad/core/InitParams$Builder;->setAndroidId` | **活-unchanged** |
| `cn/kuwo/mod/mobilead/tmead/c.smali` | classes8 | `public static h()V` | 400 | `Lcom/tencentmusic/ad/core/InitParams$Builder;->setILinkAppId` | **活-unchanged** |
| `cn/kuwo/mod/mobilead/tmead/c.smali` | classes8 | `public static h()V` | 327 | `Lcom/tencentmusic/ad/core/InitParams$Builder;->setLogProxy` | **活-unchanged** |
| `cn/kuwo/mod/mobilead/tmead/c.smali` | classes8 | `public static h()V` | 415 | `Lcom/tencentmusic/ad/core/InitParams$Builder;->setOpenUdid` | **活-unchanged** |
| `cn/kuwo/mod/mobilead/tmead/c.smali` | classes8 | `public static h()V` | 362 | `Lcom/tencentmusic/ad/core/InitParams$Builder;->setQimei` | **活-unchanged** |
| `cn/kuwo/mod/mobilead/tmead/c.smali` | classes8 | `public static h()V` | 377 | `Lcom/tencentmusic/ad/core/InitParams$Builder;->setQimeiVersion` | **活-unchanged** |
| `cn/kuwo/mod/mobilead/tmead/c.smali` | classes8 | `public static h()V` | 395 | `Lcom/tencentmusic/ad/core/InitParams$Builder;->setWxAppId` | **活-unchanged** |
| `cn/kuwo/mod/mobilead/tmead/c.smali` | classes8 | `public static h()V` | 348 | `Lcom/tencentmusic/ad/core/InitParams$Builder;->sourceType` | **活-unchanged** |
| `cn/kuwo/mod/mobilead/tmead/c.smali` | classes8 | `public static h()V` | 353 | `Lcom/tencentmusic/ad/core/InitParams$Builder;->userId` | **活-unchanged** |
| `cn/kuwo/mod/mobilead/tmead/u$a.smali` | classes8 | `public onADDismissed()V` | 168 | `Lcom/tencentmusic/ad/integration/operationsplash/operationSplash/TMEOperSplashAdAsset;->getSplashType` | **活-unchanged** |
| `cn/kuwo/mod/mobilead/tmead/u.smali` | classes8 | `public Wa(Landroid/app/Activity;Ljava/lang/String;ILqc/b$b;)Z` | 2077 | `Lcom/tencentmusic/ad/TMEAds;->isInitialized` | **活-unchanged** |
| `cn/kuwo/mod/mobilead/tmead/u.smali` | classes8 | `private Y0()Ljava/lang/String;` | 1217 | `Lcom/tencentmusic/ad/integration/operationsplash/operationSplash/TMEOperSplashAdAsset;->getTagText` | **活-unchanged** |
| `cn/kuwo/mod/mobilead/z.smali` | classes8 | `public constructor <init>()V` | 95 | `Lcn/kuwo/base/bean/shieldadinfo/SplashAdShakeShieldInfo;->getThreshold` | **活-unchanged** |
| `cn/kuwo/mod/mobilead/z.smali` | classes8 | `public constructor <init>()V` | 104 | `Lcn/kuwo/base/bean/shieldadinfo/SplashAdShakeShieldInfo;->getWeights` | **活-unchanged** |
| `cn/kuwo/player/activities/EntryActivity$d.smali` | classes9 | `public a(IZ)V` | 72 | `Lcom/tencentmusic/ad/TMEAds;->updateLastShowSplashTimeForClient` | **活-unchanged** |
| `cn/kuwo/ui/search/i.smali` | classes10 | `public static a(Ljava/lang/String;)Z` | 1578 | `Lcom/tencentmusic/ad/TMEAds;->forceUpdatePosConfig` | **活-unchanged** |
| `cn/kuwo/ui/settings/FeedBackSetInfoFragment.smali` | classes10 | `public onClick(Landroid/view/View;)V` | 1272 | `Lcom/tencentmusic/ad/TMEAds;->forceUpdatePosConfig` | **活-unchanged** |
| `cn/kuwo/ui/settings/SettingSubFragment$g.smali` | classes10 | `public a(Lgl/z;ZI)V` | 619 | `Lcom/tencentmusic/ad/TMEAds;->setInteractiveAdPrivacyConfig` | **活-unchanged** |
| `cn/kuwo/ui/settings/SettingSubViewModel$getTMEAdsInteractiveAbilityEnabled$2.smali` | classes10 | `public final invokeSuspend(Ljava/lang/Object;)Ljava/lang/Object;` | 194 | `Lcom/tencentmusic/ad/TMEAds;->getInteractiveAdPrivacyConfig` | **活-unchanged** |
| `com/kugou/fanxing/modul/ad/view/AdBannerView$a.smali` | classes15 | `public final onClick(Landroid/view/View;)V` | 77 | `Lcom/kugou/fanxing/modul/ad/view/AdBannerView;->setAdVisibible` | **活-unchanged** |
| `com/kugou/fanxing/modul/ad/view/AdBannerView$c.smali` | classes15 | `public onADStatusChanged()V` | 106 | `Lcom/kugou/fanxing/modul/ad/view/AdBannerView;->a` | **活-unchanged** |
| `com/kugou/fanxing/modul/ad/view/AdBannerView$c.smali` | classes15 | `public onADClicked()V` | 71 | `Lcom/kugou/fanxing/modul/ad/view/AdBannerView;->b` | **活-unchanged** |
| `com/kugou/fanxing/modul/ad/view/AdBannerView$c.smali` | classes15 | `public onADClicked()V` | 77 | `Lcom/kugou/fanxing/modul/ad/view/AdBannerView$b;->a` | **活-unchanged** |
| `com/kugou/fanxing/modul/ad/view/AdBannerView.smali` | classes15 | `public final setAdVisibible(Z)V` | 544 | `Lcom/kugou/fanxing/modul/ad/view/AdBannerView;->c` | **活-unchanged** |
| `com/kugou/fanxing/modul/ad/view/AdBannerView.smali` | classes15 | `public constructor <init>(Landroid/content/Context;Landroid/util/AttributeSet;I)` | 149 | `Lcom/kugou/fanxing/modul/ad/view/AdBannerView;->getLayoutId` | **活-unchanged** |
| `com/kugou/fanxing/modul/shortplay/delegate/e$c.smali` | classes2 | `public final run()V` | 69 | `Lcom/kugou/fanxing/modul/ad/view/AdBannerView;->setAdVisibible` | **活-unchanged** |
| `com/kugou/fanxing/modul/shortplay/delegate/e.smali` | classes2 | `public onDestroy()V` | 1231 | `Lcom/kugou/fanxing/modul/ad/view/AdBannerView;->c` | **活-unchanged** |
| `com/kugou/fanxing/modul/shortplay/delegate/e.smali` | classes2 | `private final Ib(Lcom/qq/e/tg/nativ/NativeUnifiedADData;)V` | 494 | `Lcom/kugou/fanxing/modul/ad/view/AdBannerView;->d` | **活-unchanged** |
| `com/kugou/fanxing/modul/shortplay/delegate/e.smali` | classes2 | `private final Fb()V` | 334 | `Lcom/kugou/fanxing/modul/ad/view/AdBannerView;->e` | **活-unchanged** |
| `com/kugou/fanxing/modul/shortplay/delegate/e.smali` | classes2 | `private final Hb()V` | 460 | `Lcom/kugou/fanxing/modul/ad/view/AdBannerView;->f` | **活-unchanged** |
| `com/kugou/fanxing/modul/shortplay/delegate/e.smali` | classes2 | `private final Ib(Lcom/qq/e/tg/nativ/NativeUnifiedADData;)V` | 504 | `Lcom/kugou/fanxing/modul/ad/view/AdBannerView;->setAdVisibible` | **活-unchanged** |
| `com/kugou/fanxing/modul/shortplay/delegate/e.smali` | classes2 | `private final Ib(Lcom/qq/e/tg/nativ/NativeUnifiedADData;)V` | 516 | `Lcom/kugou/fanxing/modul/ad/view/AdBannerView;->setOnAdClickListener` | **活-unchanged** |
| `com/qq/e/comm/managers/plugin/a.smali` | classes3 | `public final a()V` | 74 | `Lcom/tencent/ams/fusion/dynamic/SplashAdDynamicEngineManager;->getInstance` | **活-unchanged** |
| `com/qq/e/comm/managers/plugin/a.smali` | classes3 | `public final a()V` | 84 | `Lcom/tencent/ams/fusion/dynamic/SplashAdDynamicEngineManager;->preWarmMosaicEngine` | **活-unchanged** |
| `com/qq/e/comm/plugin/tangramsplash/a/a.smali` | classes3 | `public static a(Ljava/lang/String;)V` | 127 | `Lcom/tencent/ams/fusion/dynamic/SplashAdDynamicConfig;->setAdInfo` | **活-unchanged** |
| `com/qq/e/comm/plugin/tangramsplash/a/a.smali` | classes3 | `public static a(Ljava/lang/String;)V` | 114 | `Lcom/tencent/ams/fusion/dynamic/SplashAdDynamicConfig;->setAppName` | **活-unchanged** |
| `com/qq/e/comm/plugin/tangramsplash/a/a.smali` | classes3 | `public static a(Ljava/lang/String;)V` | 87 | `Lcom/tencent/ams/fusion/dynamic/SplashAdDynamicConfig;->setIpAddress` | **活-unchanged** |
| `com/qq/e/comm/plugin/tangramsplash/a/a.smali` | classes3 | `public static a(Ljava/lang/String;)V` | 101 | `Lcom/tencent/ams/fusion/dynamic/SplashAdDynamicConfig;->setIsDebugJs` | **活-unchanged** |
| `com/qq/e/comm/plugin/tangramsplash/a/a.smali` | classes3 | `public static a(Ljava/lang/String;)V` | 109 | `Lcom/tencent/ams/fusion/dynamic/SplashAdDynamicConfig;->setIsDebugMode` | **活-unchanged** |
| `com/qq/e/comm/plugin/tangramsplash/a/a.smali` | classes3 | `public static a(Ljava/lang/String;)V` | 104 | `Lcom/tencent/ams/fusion/dynamic/SplashAdDynamicConfig;->setIsDebugTemplate` | **活-unchanged** |
| `com/qq/e/comm/plugin/tangramsplash/a/a.smali` | classes3 | `public static a(Ljava/lang/String;)V` | 124 | `Lcom/tencent/ams/fusion/dynamic/SplashAdDynamicConfig;->setLocalFilePath` | **活-unchanged** |
| `com/qq/e/comm/plugin/tangramsplash/a/a.smali` | classes3 | `public static a(Ljava/lang/String;)V` | 119 | `Lcom/tencent/ams/fusion/dynamic/SplashAdDynamicConfig;->setTid` | **活-unchanged** |
| `com/qq/e/comm/plugin/tangramsplash/a/b$1.smali` | classes3 | `public run()V` | 153 | `Lcom/tencent/ams/fusion/dynamic/SplashAdDynamicEngineManager;->getInstance` | **活-unchanged** |
| `com/qq/e/comm/plugin/tangramsplash/a/b$1.smali` | classes3 | `public run()V` | 194 | `Lcom/tencent/ams/fusion/dynamic/SplashAdDynamicEngineManager;->preWarmMosaicEngine` | **活-unchanged** |
| `com/qq/e/comm/plugin/tangramsplash/a/b$3.smali` | classes3 | `public run()V` | 67 | `Lcom/tencent/ams/fusion/dynamic/SplashAdDynamicView;->recycleMosaicEngine` | **活-unchanged** |
| `com/qq/e/comm/plugin/tangramsplash/a/b.smali` | classes3 | `private ab()V` | 959 | `Lcom/tencent/ams/fusion/dynamic/SplashAdDynamicView;->getEngine` | **活-unchanged** |
| `com/qq/e/comm/plugin/tangramsplash/a/b.smali` | classes3 | `protected a(Ljava/io/File;I)V` | 2548 | `Lcom/tencent/ams/fusion/dynamic/SplashAdDynamicView;->showSplashAd` | **活-unchanged** |
| `com/qq/e/comm/plugin/tangramsplash/d/d.smali` | classes3 | `private h(Ljava/lang/String;Z)V` | 3551 | `Lcom/tencent/ams/fusion/dynamic/SplashAdDynamicEngineManager;->getInstance` | **活-unchanged** |
| `com/qq/e/comm/plugin/tangramsplash/d/d.smali` | classes3 | `private h(Ljava/lang/String;Z)V` | 3575 | `Lcom/tencent/ams/fusion/dynamic/SplashAdDynamicEngineManager;->preWarmMosaicEngine` | **活-unchanged** |
| `com/qq/e/tg/splash/TGSplashAD$ADListenerAdapter.smali` | classes3 | `public onADEvent(Lcom/qq/e/comm/adevent/ADEvent;)V` | 300 | `Lcom/qq/e/tg/splash/TGSplashAdListener;->onADClicked` | **活-unchanged** |
| `com/qq/e/tg/splash/TGSplashAD$ADListenerAdapter.smali` | classes3 | `public onADEvent(Lcom/qq/e/comm/adevent/ADEvent;)V` | 383 | `Lcom/qq/e/tg/splash/TGSplashAdListener;->onADDismissed` | **活-unchanged** |
| `com/qq/e/tg/splash/TGSplashAD$ADListenerAdapter.smali` | classes3 | `public onADEvent(Lcom/qq/e/comm/adevent/ADEvent;)V` | 253 | `Lcom/qq/e/tg/splash/TGSplashAdListener;->onADExposure` | **活-unchanged** |
| `com/qq/e/tg/splash/TGSplashAD$ADListenerAdapter.smali` | classes3 | `public onADEvent(Lcom/qq/e/comm/adevent/ADEvent;)V` | 242 | `Lcom/qq/e/tg/splash/TGSplashAdListener;->onADFetch` | **活-unchanged** |
| `com/qq/e/tg/splash/TGSplashAD$ADListenerAdapter.smali` | classes3 | `public onADEvent(Lcom/qq/e/comm/adevent/ADEvent;)V` | 311 | `Lcom/qq/e/tg/splash/TGSplashAdListener;->onADPresent` | **活-unchanged** |
| `com/qq/e/tg/splash/TGSplashAD$ADListenerAdapter.smali` | classes3 | `public onADEvent(Lcom/qq/e/comm/adevent/ADEvent;)V` | 231 | `Lcom/qq/e/tg/splash/TGSplashAdListener;->onADSkip` | **活-unchanged** |
| `com/qq/e/tg/splash/TGSplashAD$ADListenerAdapter.smali` | classes3 | `public onADEvent(Lcom/qq/e/comm/adevent/ADEvent;)V` | 282 | `Lcom/qq/e/tg/splash/TGSplashAdListener;->onADTick` | **活-unchanged** |
| `com/qq/e/tg/splash/TGSplashAD$ADListenerAdapter.smali` | classes3 | `public onADEvent(Lcom/qq/e/comm/adevent/ADEvent;)V` | 365 | `Lcom/qq/e/tg/splash/TGSplashAdListener;->onNoAD` | **活-unchanged** |
| `com/qq/e/tg/splash/TGSplashAD$ADListenerAdapter.smali` | classes3 | `public onADEvent(Lcom/qq/e/comm/adevent/ADEvent;)V` | 213 | `Lcom/qq/e/tg/splash/TGSplashAdListenerV2;->onADFetchWithResult` | **活-unchanged** |
| `com/qq/e/tg/splash/TGSplashAD$ADListenerAdapter.smali` | classes3 | `public onADEvent(Lcom/qq/e/comm/adevent/ADEvent;)V` | 176 | `Lcom/qq/e/tg/splash/TGSplashAdListenerV3;->onLimitAdViewClicked` | **活-unchanged** |
| `com/qq/e/tg/splash/TGSplashAD$ADListenerAdapter.smali` | classes3 | `public onADEvent(Lcom/qq/e/comm/adevent/ADEvent;)V` | 98 | `Lcom/qq/e/tg/splash/TGSplashAdListenerV4;->onAlphaVideoTransformStart` | **活-unchanged** |
| `com/qq/e/tg/splash/TGSplashAD$ADListenerAdapter.smali` | classes3 | `public onADEvent(Lcom/qq/e/comm/adevent/ADEvent;)V` | 146 | `Lcom/qq/e/tg/splash/TGSplashAdListenerV4;->onRealtimeAdReceived` | **活-unchanged** |
| `com/qq/e/tg/splash/TGSplashAD.smali` | classes3 | `private static a(Lcom/qq/e/tg/splash/TGSplashAdListener;I)V` | 823 | `Lcom/qq/e/tg/splash/TGSplashAdListener;->onNoAD` | **活-unchanged** |
| `com/tencent/ams/fusion/dynamic/SplashAdDynamicEngineManager$1.smali` | classes3 | `public onEngineInitializeError(I)V` | 46 | `Lcom/tencent/ams/fusion/dynamic/SplashAdDynamicEngineManager$InitCallback;->onInitFailed` | **活-unchanged** |
| `com/tencent/ams/fusion/dynamic/SplashAdDynamicEngineManager$1.smali` | classes3 | `public onEngineInitialized()V` | 69 | `Lcom/tencent/ams/fusion/dynamic/SplashAdDynamicEngineManager$InitCallback;->onInitSuccess` | **活-unchanged** |
| `com/tencent/ams/fusion/dynamic/SplashAdDynamicEngineManager$2.smali` | classes3 | `public onEngineInitializeError(I)V` | 80 | `Lcom/tencent/ams/fusion/dynamic/SplashAdDynamicReporter;->reportEngineInitFailed` | **活-unchanged** |
| `com/tencent/ams/fusion/dynamic/SplashAdDynamicEngineManager$2.smali` | classes3 | `public onWillCreateEngine()V` | 289 | `Lcom/tencent/ams/fusion/dynamic/SplashAdDynamicReporter;->reportEngineInitStart` | **活-unchanged** |
| `com/tencent/ams/fusion/dynamic/SplashAdDynamicEngineManager$2.smali` | classes3 | `public onEngineInitialized()V` | 147 | `Lcom/tencent/ams/fusion/dynamic/SplashAdDynamicReporter;->reportEngineInitSuccess` | **活-unchanged** |
| `com/tencent/ams/fusion/dynamic/SplashAdDynamicEngineManager$2.smali` | classes3 | `public onSoLoadFailed(I)V` | 190 | `Lcom/tencent/ams/fusion/dynamic/SplashAdDynamicReporter;->reportSoLoadFinish` | **活-unchanged** |
| `com/tencent/ams/fusion/dynamic/SplashAdDynamicEngineManager$2.smali` | classes3 | `public onSoLoadStart()V` | 218 | `Lcom/tencent/ams/fusion/dynamic/SplashAdDynamicReporter;->reportSoLoadStart` | **活-unchanged** |
| `com/tencent/ams/fusion/dynamic/SplashAdDynamicEngineManager.smali` | classes3 | `public preWarmMosaicEngine(Landroid/content/Context;Lcom/tencent/ams/fusion/dyna` | 194 | `Lcom/tencent/ams/fusion/dynamic/SplashAdDynamicConfig;->getAppName` | **活-unchanged** |
| `com/tencent/ams/fusion/dynamic/SplashAdDynamicEngineManager.smali` | classes3 | `public preWarmMosaicEngine(Ljava/lang/String;Landroid/content/Context;Lcom/tence` | 253 | `Lcom/tencent/ams/fusion/dynamic/SplashAdDynamicConfig;->getIpAddress` | **活-unchanged** |
| `com/tencent/ams/fusion/dynamic/SplashAdDynamicEngineManager.smali` | classes3 | `public preWarmMosaicEngine(Ljava/lang/String;Landroid/content/Context;Lcom/tence` | 274 | `Lcom/tencent/ams/fusion/dynamic/SplashAdDynamicConfig;->isIsDebugJs` | **活-unchanged** |
| `com/tencent/ams/fusion/dynamic/SplashAdDynamicEngineManager.smali` | classes3 | `public preWarmMosaicEngine(Ljava/lang/String;Landroid/content/Context;Lcom/tence` | 304 | `Lcom/tencent/ams/fusion/dynamic/SplashAdDynamicConfig;->isIsDebugMode` | **活-unchanged** |
| `com/tencent/ams/fusion/dynamic/SplashAdDynamicEngineManager.smali` | classes3 | `public preWarmMosaicEngine(Ljava/lang/String;Landroid/content/Context;Lcom/tence` | 285 | `Lcom/tencent/ams/fusion/dynamic/SplashAdDynamicConfig;->isIsDebugTemplate` | **活-unchanged** |
| `com/tencent/ams/fusion/dynamic/SplashAdDynamicEngineManager.smali` | classes3 | `public init(Landroid/content/Context;Lcom/tencent/ams/fusion/dynamic/SplashAdDyn` | 184 | `Lcom/tencent/ams/fusion/dynamic/SplashAdDynamicEngineManager;->getMosaicEngine` | **活-unchanged** |
| `com/tencent/ams/fusion/dynamic/SplashAdDynamicEngineManager.smali` | classes3 | `public init(Landroid/content/Context;Lcom/tencent/ams/fusion/dynamic/SplashAdDyn` | 177 | `Lcom/tencent/ams/fusion/dynamic/SplashAdDynamicEngineManager;->preWarmMosaicEngine` | **活-unchanged** |
| `com/tencent/ams/fusion/dynamic/SplashAdDynamicEngineManager.smali` | classes3 | `private getMosaicEngine(Lcom/tencent/ams/fusion/dynamic/SplashAdDynamicEngineMan` | 157 | `Lcom/tencent/ams/fusion/dynamic/SplashAdDynamicEngineManager$InitCallback;->onInitFailed` | **活-unchanged** |
| `com/tencent/ams/fusion/dynamic/SplashAdDynamicEngineManager.smali` | classes3 | `private getMosaicEngine(Lcom/tencent/ams/fusion/dynamic/SplashAdDynamicEngineMan` | 149 | `Lcom/tencent/ams/fusion/dynamic/SplashAdDynamicEngineManager$InitCallback;->onInitSuccess` | **活-unchanged** |
| `com/tencent/ams/fusion/dynamic/SplashAdDynamicReporter.smali` | classes3 | `public static reportEngineInitFailed(IJ)V` | 45 | `Lcom/tencent/ams/fusion/dynamic/SplashAdDynamicEngineManager;->getInstance` | **活-unchanged** |
| `com/tencent/ams/fusion/dynamic/SplashAdDynamicReporter.smali` | classes3 | `public static reportEngineInitFailed(IJ)V` | 50 | `Lcom/tencent/ams/fusion/dynamic/SplashAdDynamicEngineManager;->getStartShowTimeMillis` | **活-unchanged** |
| `com/tencent/ams/fusion/dynamic/SplashAdDynamicView$3.smali` | classes3 | `public onViewCreate(Landroid/view/View;I)V` | 181 | `Lcom/tencent/ams/fusion/dynamic/SplashAdDynamicReporter;->reportViewCreateFailed` | **活-unchanged** |
| `com/tencent/ams/fusion/dynamic/SplashAdDynamicView$3.smali` | classes3 | `public onViewCreateStart()V` | 238 | `Lcom/tencent/ams/fusion/dynamic/SplashAdDynamicReporter;->reportViewCreateStart` | **活-unchanged** |
| `com/tencent/ams/fusion/dynamic/SplashAdDynamicView$3.smali` | classes3 | `public onViewInitialized()V` | 365 | `Lcom/tencent/ams/fusion/dynamic/SplashAdDynamicReporter;->reportViewCreateSuccess` | **活-unchanged** |
| `com/tencent/ams/fusion/dynamic/SplashAdDynamicView$3.smali` | classes3 | `public onViewCreate(Landroid/view/View;I)V` | 114 | `Lcom/tencent/ams/fusion/dynamic/SplashAdDynamicView$3;->getEventCenter` | **活-unchanged** |
| `com/tencent/ams/fusion/dynamic/SplashAdDynamicView$6.smali` | classes3 | `public invoke(Lcom/tencent/ams/dsdk/core/DKEngine;Ljava/lang/String;Lorg/json/JS` | 646 | `Lcom/tencent/ams/fusion/dynamic/SplashAdDynamicReporter;->reportSplashClicked` | **活-unchanged** |
| `com/tencent/ams/fusion/dynamic/SplashAdDynamicView$6.smali` | classes3 | `public invoke(Lcom/tencent/ams/dsdk/core/DKEngine;Ljava/lang/String;Lorg/json/JS` | 872 | `Lcom/tencent/ams/fusion/dynamic/SplashAdDynamicReporter;->reportSplashSkipped` | **活-unchanged** |
| `com/tencent/ams/fusion/dynamic/SplashAdDynamicView$7.smali` | classes3 | `public invoke(Lcom/tencent/ams/dsdk/core/DKEngine;Ljava/lang/String;Lorg/json/JS` | 192 | `Lcom/tencent/ams/fusion/dynamic/SplashAdDynamicReporter;->reportViewRenderFinish` | **活-unchanged** |
| `com/tencent/ams/fusion/dynamic/SplashAdDynamicView.smali` | classes3 | `private createDynamicViewFromMosaicEngine(Lcom/tencent/ams/dsdk/core/mosaic/DKMo` | 270 | `Lcom/tencent/ams/fusion/dynamic/SplashAdDynamicConfig;->getAdInfo` | **活-unchanged** |
| `com/tencent/ams/fusion/dynamic/SplashAdDynamicView.smali` | classes3 | `private createDynamicViewFromMosaicEngine(Lcom/tencent/ams/dsdk/core/mosaic/DKMo` | 290 | `Lcom/tencent/ams/fusion/dynamic/SplashAdDynamicConfig;->getLocalAssetPath` | **活-unchanged** |
| `com/tencent/ams/fusion/dynamic/SplashAdDynamicView.smali` | classes3 | `private createDynamicViewFromMosaicEngine(Lcom/tencent/ams/dsdk/core/mosaic/DKMo` | 281 | `Lcom/tencent/ams/fusion/dynamic/SplashAdDynamicConfig;->getLocalFilePath` | **活-unchanged** |
| `com/tencent/ams/fusion/dynamic/SplashAdDynamicView.smali` | classes3 | `private createDynamicViewFromMosaicEngine(Lcom/tencent/ams/dsdk/core/mosaic/DKMo` | 235 | `Lcom/tencent/ams/fusion/dynamic/SplashAdDynamicConfig;->getTid` | **活-unchanged** |
| `com/tencent/ams/fusion/dynamic/SplashAdDynamicView.smali` | classes3 | `private showDynamicView()V` | 554 | `Lcom/tencent/ams/fusion/dynamic/SplashAdDynamicEngineManager;->getInstance` | **活-unchanged** |
| `com/tencent/ams/fusion/dynamic/SplashAdDynamicView.smali` | classes3 | `private showDynamicView()V` | 566 | `Lcom/tencent/ams/fusion/dynamic/SplashAdDynamicEngineManager;->init` | **活-unchanged** |
| `com/tencent/ams/fusion/dynamic/SplashAdDynamicView.smali` | classes3 | `public onEvent(Lcom/tencent/ams/mosaic/MosaicEvent;)V` | 694 | `Lcom/tencent/ams/fusion/dynamic/SplashAdDynamicReporter;->reportEngineRunError` | **活-unchanged** |
| `com/tencent/ams/fusion/dynamic/SplashAdDynamicView.smali` | classes3 | `private createDynamicViewFromMosaicEngine(Lcom/tencent/ams/dsdk/core/mosaic/DKMo` | 151 | `Lcom/tencent/ams/fusion/dynamic/SplashAdDynamicView;->createDynamicViewFromMosaicEngine` | **活-unchanged** |
| `com/tencent/ams/fusion/dynamic/SplashAdDynamicView.smali` | classes3 | `static synthetic access$400(Lcom/tencent/ams/fusion/dynamic/SplashAdDynamicView;` | 122 | `Lcom/tencent/ams/fusion/dynamic/SplashAdDynamicView;->recycleImpl` | **活-unchanged** |
| `com/tencent/ams/fusion/dynamic/SplashAdDynamicView.smali` | classes3 | `static synthetic access$100(Lcom/tencent/ams/fusion/dynamic/SplashAdDynamicView;` | 90 | `Lcom/tencent/ams/fusion/dynamic/SplashAdDynamicView;->setupEngine` | **活-unchanged** |
| `com/tencent/ams/fusion/dynamic/SplashAdDynamicView.smali` | classes3 | `public showSplashAd()V` | 792 | `Lcom/tencent/ams/fusion/dynamic/SplashAdDynamicView;->showDynamicView` | **活-unchanged** |
| `com/tencent/ams/fusion/service/dynamic/impl/DynamicServiceImpl$1.smali` | classes3 | `public onEngineInitialized()V` | 94 | `Lcom/tencent/ams/fusion/dynamic/SplashAdDynamicEngineManager;->getInstance` | **活-unchanged** |
| `com/tencent/ams/fusion/service/dynamic/impl/DynamicServiceImpl$1.smali` | classes3 | `public onEngineInitialized()V` | 100 | `Lcom/tencent/ams/fusion/dynamic/SplashAdDynamicEngineManager;->tryGetMosaicEngine` | **活-unchanged** |
| `com/tencent/ams/fusion/service/dynamic/impl/DynamicServiceImpl.smali` | classes3 | `public getEngine(Ljava/lang/String;J)Lcom/tencent/ams/dsdk/core/mosaic/DKMosaicE` | 147 | `Lcom/tencent/ams/fusion/dynamic/SplashAdDynamicEngineManager;->getInstance` | **活-unchanged** |
| `com/tencent/ams/fusion/service/dynamic/impl/DynamicServiceImpl.smali` | classes3 | `public getEngine(Ljava/lang/String;J)Lcom/tencent/ams/dsdk/core/mosaic/DKMosaicE` | 183 | `Lcom/tencent/ams/fusion/dynamic/SplashAdDynamicEngineManager;->preWarmMosaicEngine` | **活-unchanged** |
| `com/tencent/ams/fusion/service/dynamic/impl/DynamicServiceImpl.smali` | classes3 | `public getEngine(Ljava/lang/String;J)Lcom/tencent/ams/dsdk/core/mosaic/DKMosaicE` | 151 | `Lcom/tencent/ams/fusion/dynamic/SplashAdDynamicEngineManager;->tryGetMosaicEngine` | **活-unchanged** |
| `fo1/a.smali` | classes5 | `public final jumpToCustomLandingPage(Landroid/content/Context;Ljava/lang/String;` | 37 | `Lcom/tencentmusic/ad/adapter/ams/AMSSplashAdapter;->e` | **活-unchanged** |
| `fo1/b.smali` | classes5 | `public final invoke()Ljava/lang/Object;` | 31 | `Lcom/tencentmusic/ad/adapter/ams/AMSSplashAdapter;->f` | **活-unchanged** |
| `fo1/c.smali` | classes5 | `public final run()V` | 31 | `Lcom/tencentmusic/ad/adapter/ams/AMSSplashAdapter;->g` | **活-unchanged** |
| `fo1/d.smali` | classes5 | `public final run()V` | 37 | `Lcom/tencentmusic/ad/adapter/ams/AMSSplashAdapter;->h` | **活-unchanged** |
| `fo1/e.smali` | classes5 | `public final run()V` | 49 | `Lcom/tencentmusic/ad/adapter/ams/AMSSplashAdapter;->d` | **活-unchanged** |
| `go1/a.smali` | classes5 | `public final run()V` | 37 | `Lcom/tencentmusic/ad/adapter/ams/nativead/AMSNativeAdAdapter$a;->a` | **活-unchanged** |
| `ho1/a.smali` | classes6 | `public final invoke()Ljava/lang/Object;` | 31 | `Lcom/tencentmusic/ad/adapter/common/BaseAdAdapter;->b` | **活-unchanged** |
| `ho1/b.smali` | classes6 | `public final invoke()Ljava/lang/Object;` | 31 | `Lcom/tencentmusic/ad/adapter/common/BaseAdAdapter;->c` | **活-unchanged** |
| `ho1/c.smali` | classes6 | `public final run()V` | 37 | `Lcom/tencentmusic/ad/adapter/common/BaseAdAdapter;->a` | **活-unchanged** |
| `io1/a.smali` | classes6 | `public final invoke()Ljava/lang/Object;` | 43 | `Lcom/tencentmusic/ad/adapter/mad/nativead/MADNativeAdAdapter;->d` | **活-unchanged** |
| `io1/b.smali` | classes6 | `public final run()V` | 49 | `Lcom/tencentmusic/ad/adapter/mad/nativead/MADNativeAdAdapter;->e` | **活-unchanged** |
| `jo1/a.smali` | classes6 | `public final handleMessage(Landroid/os/Message;)Z` | 31 | `Lcom/tencentmusic/ad/adapter/mad/reward/MADRewardVideoAdAdapter;->k` | **活-unchanged** |
| `jo1/b.smali` | classes6 | `public final onReceiveValue(Ljava/lang/Object;)V` | 51 | `Lcom/tencentmusic/ad/adapter/mad/reward/MADRewardVideoAdAdapter;->j` | **活-unchanged** |
| `jo1/c.smali` | classes6 | `public final invoke()Ljava/lang/Object;` | 31 | `Lcom/tencentmusic/ad/adapter/mad/reward/MADRewardVideoAdAdapter;->i` | **活-unchanged** |
| `jo1/d.smali` | classes6 | `public final invoke()Ljava/lang/Object;` | 37 | `Lcom/tencentmusic/ad/adapter/mad/reward/MADRewardVideoAdAdapter;->e` | **活-unchanged** |
| `jo1/e.smali` | classes6 | `public final invoke()Ljava/lang/Object;` | 43 | `Lcom/tencentmusic/ad/adapter/mad/reward/MADRewardVideoAdAdapter;->f` | **活-unchanged** |
| `jo1/f.smali` | classes6 | `public final invoke()Ljava/lang/Object;` | 55 | `Lcom/tencentmusic/ad/adapter/mad/reward/MADRewardVideoAdAdapter;->g` | **活-unchanged** |
| `jo1/g.smali` | classes6 | `public final invoke()Ljava/lang/Object;` | 37 | `Lcom/tencentmusic/ad/adapter/mad/reward/MADRewardVideoAdAdapter;->d` | **活-unchanged** |
| `jo1/h.smali` | classes6 | `public final invoke()Ljava/lang/Object;` | 39 | `Lcom/tencentmusic/ad/adapter/mad/reward/MADRewardVideoAdAdapter;->h` | **活-unchanged** |
| `jo1/i.smali` | classes6 | `public final invoke()Ljava/lang/Object;` | 49 | `Lcom/tencentmusic/ad/adapter/mad/reward/MADRewardVideoAdAdapter$b;->a` | **活-unchanged** |
| `jo1/j.smali` | classes6 | `public final invoke()Ljava/lang/Object;` | 31 | `Lcom/tencentmusic/ad/adapter/mad/reward/MADRewardVideoAdAdapter$b;->a` | **活-unchanged** |
| `jo1/k.smali` | classes6 | `public final invoke()Ljava/lang/Object;` | 31 | `Lcom/tencentmusic/ad/adapter/mad/reward/MADRewardVideoAdAdapter$b;->b` | **活-unchanged** |
| `jo1/l.smali` | classes6 | `public final invoke()Ljava/lang/Object;` | 37 | `Lcom/tencentmusic/ad/adapter/mad/reward/MADRewardVideoAdAdapter$b;->a` | **活-unchanged** |
| `ko1/a.smali` | classes6 | `public final onReceiveValue(Ljava/lang/Object;)V` | 41 | `Lcom/tencentmusic/ad/adapter/mad/splash/MADBaseSplashAdapter;->d` | **活-unchanged** |
| `ko1/b.smali` | classes6 | `public final invoke()Ljava/lang/Object;` | 31 | `Lcom/tencentmusic/ad/adapter/mad/splash/MADBaseSplashAdapter;->f` | **活-unchanged** |
| `ko1/c.smali` | classes6 | `public final invoke()Ljava/lang/Object;` | 37 | `Lcom/tencentmusic/ad/adapter/mad/splash/MADBaseSplashAdapter;->e` | **活-unchanged** |
| `ko1/d.smali` | classes6 | `public final invoke()Ljava/lang/Object;` | 31 | `Lcom/tencentmusic/ad/adapter/mad/splash/MADBaseSplashAdapter$c;->a` | **活-unchanged** |
| `ko1/e.smali` | classes6 | `public final invoke()Ljava/lang/Object;` | 31 | `Lcom/tencentmusic/ad/adapter/mad/splash/MADBaseSplashAdapter$c;->b` | **活-unchanged** |
| `ko1/f.smali` | classes6 | `public final invoke(Ljava/lang/Object;)Ljava/lang/Object;` | 37 | `Lcom/tencentmusic/ad/adapter/mad/splash/MADBaseSplashAdapter$c;->a` | **活-unchanged** |
| `ko1/g.smali` | classes6 | `public final run()V` | 39 | `Lcom/tencentmusic/ad/adapter/mad/splash/MADBaseSplashAdapter$c;->c` | **活-unchanged** |
| `ko1/h.smali` | classes6 | `public final run()V` | 67 | `Lcom/tencentmusic/ad/adapter/mad/splash/MADExpoSplashAdapter;->h` | **活-unchanged** |
| `ko1/i.smali` | classes6 | `public final run()V` | 67 | `Lcom/tencentmusic/ad/adapter/mad/splash/MADExpoSplashAdapter;->g` | **活-unchanged** |
| `lo1/a.smali` | classes6 | `public final invoke()Ljava/lang/Object;` | 79 | `Lcom/tencentmusic/ad/adapter/madams/splash/OperBaseSplashAdapter;->d` | **活-unchanged** |
| `lo1/b.smali` | classes6 | `public final onReceiveValue(Ljava/lang/Object;)V` | 33 | `Lcom/tencentmusic/ad/adapter/madams/splash/OperExpertSplashAdapter;->s` | **活-unchanged** |
| `lo1/c.smali` | classes6 | `public final invoke()Ljava/lang/Object;` | 39 | `Lcom/tencentmusic/ad/adapter/madams/splash/OperExpertSplashAdapter;->u` | **活-unchanged** |
| `lo1/d.smali` | classes6 | `public final run()V` | 31 | `Lcom/tencentmusic/ad/adapter/madams/splash/OperExpertSplashAdapter;->e` | **活-unchanged** |
| `lo1/e.smali` | classes6 | `public final run()V` | 31 | `Lcom/tencentmusic/ad/adapter/madams/splash/OperExpertSplashAdapter;->f` | **活-unchanged** |
| `lo1/f.smali` | classes6 | `public final run()V` | 31 | `Lcom/tencentmusic/ad/adapter/madams/splash/OperExpertSplashAdapter;->t` | **活-unchanged** |
| `lo1/g.smali` | classes6 | `public final run()V` | 43 | `Lcom/tencentmusic/ad/adapter/madams/splash/OperExpertSplashAdapter;->i` | **活-unchanged** |
| `lo1/h.smali` | classes6 | `public final run()V` | 43 | `Lcom/tencentmusic/ad/adapter/madams/splash/OperExpertSplashAdapter;->k` | **活-unchanged** |
| `lo1/i.smali` | classes6 | `public final run()V` | 43 | `Lcom/tencentmusic/ad/adapter/madams/splash/OperExpertSplashAdapter;->o` | **活-unchanged** |
| `lo1/j.smali` | classes6 | `public final onReceiveValue(Ljava/lang/Object;)V` | 39 | `Lcom/tencentmusic/ad/adapter/madams/splash/OperExpertSplashAdapter;->r` | **活-unchanged** |
| `lo1/k.smali` | classes6 | `public final onReceiveValue(Ljava/lang/Object;)V` | 45 | `Lcom/tencentmusic/ad/adapter/madams/splash/OperExpertSplashAdapter;->h` | **活-unchanged** |
| `lo1/l.smali` | classes6 | `public final onReceiveValue(Ljava/lang/Object;)V` | 39 | `Lcom/tencentmusic/ad/adapter/madams/splash/OperExpertSplashAdapter;->l` | **活-unchanged** |
| `lo1/m.smali` | classes6 | `public final invoke()Ljava/lang/Object;` | 31 | `Lcom/tencentmusic/ad/adapter/madams/splash/OperExpertSplashAdapter;->j` | **活-unchanged** |
| `lo1/n.smali` | classes6 | `public final invoke()Ljava/lang/Object;` | 43 | `Lcom/tencentmusic/ad/adapter/madams/splash/OperExpertSplashAdapter;->g` | **活-unchanged** |
| `lo1/o.smali` | classes6 | `public final invoke()Ljava/lang/Object;` | 37 | `Lcom/tencentmusic/ad/adapter/madams/splash/OperExpertSplashAdapter;->p` | **活-unchanged** |
| `lo1/p.smali` | classes6 | `public final invoke()Ljava/lang/Object;` | 67 | `Lcom/tencentmusic/ad/adapter/madams/splash/OperExpertSplashAdapter;->n` | **活-unchanged** |
| `lo1/q.smali` | classes6 | `public final invoke()Ljava/lang/Object;` | 43 | `Lcom/tencentmusic/ad/adapter/madams/splash/OperExpertSplashAdapter;->q` | **活-unchanged** |
| `lo1/r.smali` | classes6 | `public final invoke()Ljava/lang/Object;` | 39 | `Lcom/tencentmusic/ad/adapter/madams/splash/OperExpertSplashAdapter;->m` | **活-unchanged** |
| `lo1/s.smali` | classes6 | `public final onReceiveValue(Ljava/lang/Object;)V` | 39 | `Lcom/tencentmusic/ad/adapter/madams/splash/OperExpertSplashAdapter$b;->a` | **活-unchanged** |
| `qd/e.smali` | classes9 | `public static f()I` | 149 | `Lcom/tencentmusic/ad/TMEAds;->checkSplashInterval` | **活-unchanged** |
| `ra/e.smali` | classes8 | `protected d(Ljava/lang/String;Ljava/lang/String;Lorg/xml/sax/Attributes;)V` | 5645 | `Lcn/kuwo/base/bean/shieldadinfo/SplashAdShakeShieldInfo;->setThreshold` | **活-changed仍调** |
| `ra/e.smali` | classes8 | `protected d(Ljava/lang/String;Ljava/lang/String;Lorg/xml/sax/Attributes;)V` | 5697 | `Lcn/kuwo/base/bean/shieldadinfo/SplashAdShakeShieldInfo;->setWeights` | **活-changed仍调** |
| `z6/a.smali` | classes8 | `b()V` | 91 | `Lcom/tencentmusic/ad/TMEAds;->getPosConfig` | **活-unchanged** |
| `z6/b.smali` | classes8 | `private static f(Ljava/util/List;)Ljava/lang/String;` | 227 | `Lcom/tencentmusic/ad/TMEAds;->getVersionName` | **活-changed仍调** |

## 表② 埋点 init 存活表（rif / fireeye / xcstat / Statistic 系）

| caller 类 | dex | 所在方法 | 官方行 | 埋点类 | 方法 | mod 现状 |
|---|---|---|---|---|---|---|
| `b3/a.smali` | classes | `public b()V` | 370 | `Lcom/tme/rif/config/ConfigManager` | init | **活-unchanged** |
| `b3/a.smali` | classes | `public b()V` | 375 | `Lcom/tme/rif/service/ServiceManager` | init | **活-unchanged** |
| `sd/d$c.smali` | classes9 | `public attachBusinessInfo()Ljava/util/Map;` | 51 | `Lcom/tme/fireeye/memory/common/MemoryEventAdapter` | attach | **断?** |
| `sd/d.smali` | classes9 | `public b(Landroid/content/Context;Ljava/lang/String;)V` | 590 | `Lcom/tme/fireeye/crash/export/anr/ANRReport` | start | **断?** |
| `sd/d.smali` | classes9 | `public b(Landroid/content/Context;Ljava/lang/String;)V` | 544 | `Lcom/tme/fireeye/crash/export/eup/CrashReport` | init | **断?** |
| `sd/d.smali` | classes9 | `public b(Landroid/content/Context;Ljava/lang/String;)V` | 635 | `Lcom/tme/fireeye/lib/base/FireEye` | init | **活-unchanged** |
| `sd/d.smali` | classes9 | `public b(Landroid/content/Context;Ljava/lang/String;)V` | 642 | `Lcom/tme/fireeye/lib/base/FireEye` | start | **活-unchanged** |

## 表③ 掐点候选（存活 caller，风险自注，非判决）

> 口径=表①②「活」条目按 caller 类去重；风险自注=mod 侧该类文件是否含 VIP/破解链引用（tian0/s2/vipnew/mod/peculiar）。

| caller 类 | dex | 所在方法 | 示例调用 | 风险自注 |
|---|---|---|---|---|
| `b3/a.smali` | classes | `public b()V` | `Lcom/tme/rif/config/ConfigManager;->init` | 独立业务 caller(未见 VIP 链引用)——波及面最小 |
| `cn/kuwo/mod/mobilead/n.smali` | classes8 | `public F(Landroid/view/ViewGroup;Landroid/view/View;Lcn/kuwo` | `Lcom/tencentmusic/ad/TMEAds;->updateLastShowSplashTimeForClient` | 混挂VIP特征——掐该caller先审 VIP 依赖链，防 P3 式崩会员 |
| `cn/kuwo/mod/mobilead/tmead/TMESplashOneshotExt.smali` | classes8 | `public static final x(Lcom/tencentmusic/ad/integration/opera` | `Lcom/tencentmusic/ad/integration/operationsplash/operationSplash/TMEOperSplashAdAsset;->getSplashSource` | 混挂VIP特征——掐该caller先审 VIP 依赖链，防 P3 式崩会员 |
| `cn/kuwo/mod/mobilead/tmead/c.smali` | classes8 | `public static h()V` | `Lcom/tencentmusic/ad/TMEAds;->init` | 混挂VIP特征——掐该caller先审 VIP 依赖链，防 P3 式崩会员 |
| `cn/kuwo/mod/mobilead/tmead/u$a.smali` | classes8 | `public onADDismissed()V` | `Lcom/tencentmusic/ad/integration/operationsplash/operationSplash/TMEOperSplashAdAsset;->getSplashType` | 混挂VIP特征——掐该caller先审 VIP 依赖链，防 P3 式崩会员 |
| `cn/kuwo/mod/mobilead/tmead/u.smali` | classes8 | `public Wa(Landroid/app/Activity;Ljava/lang/String;ILqc/b$b;)` | `Lcom/tencentmusic/ad/TMEAds;->isInitialized` | 混挂VIP特征——掐该caller先审 VIP 依赖链，防 P3 式崩会员 |
| `cn/kuwo/mod/mobilead/z.smali` | classes8 | `public constructor <init>()V` | `Lcn/kuwo/base/bean/shieldadinfo/SplashAdShakeShieldInfo;->getThreshold` | 混挂VIP特征——掐该caller先审 VIP 依赖链，防 P3 式崩会员 |
| `cn/kuwo/player/activities/EntryActivity$d.smali` | classes9 | `public a(IZ)V` | `Lcom/tencentmusic/ad/TMEAds;->updateLastShowSplashTimeForClient` | 混挂VIP特征——掐该caller先审 VIP 依赖链，防 P3 式崩会员 |
| `cn/kuwo/ui/search/i.smali` | classes10 | `public static a(Ljava/lang/String;)Z` | `Lcom/tencentmusic/ad/TMEAds;->forceUpdatePosConfig` | 混挂VIP特征——掐该caller先审 VIP 依赖链，防 P3 式崩会员 |
| `cn/kuwo/ui/settings/FeedBackSetInfoFragment.smali` | classes10 | `public onClick(Landroid/view/View;)V` | `Lcom/tencentmusic/ad/TMEAds;->forceUpdatePosConfig` | 混挂VIP特征——掐该caller先审 VIP 依赖链，防 P3 式崩会员 |
| `cn/kuwo/ui/settings/SettingSubFragment$g.smali` | classes10 | `public a(Lgl/z;ZI)V` | `Lcom/tencentmusic/ad/TMEAds;->setInteractiveAdPrivacyConfig` | 独立业务 caller(未见 VIP 链引用)——波及面最小 |
| `cn/kuwo/ui/settings/SettingSubViewModel$getTMEAdsInteractiveAbilityEnabled$2.smali` | classes10 | `public final invokeSuspend(Ljava/lang/Object;)Ljava/lang/Obj` | `Lcom/tencentmusic/ad/TMEAds;->getInteractiveAdPrivacyConfig` | 独立业务 caller(未见 VIP 链引用)——波及面最小 |
| `com/kugou/fanxing/modul/ad/view/AdBannerView$a.smali` | classes15 | `public final onClick(Landroid/view/View;)V` | `Lcom/kugou/fanxing/modul/ad/view/AdBannerView;->setAdVisibible` | 独立业务 caller(未见 VIP 链引用)——波及面最小 |
| `com/kugou/fanxing/modul/ad/view/AdBannerView$c.smali` | classes15 | `public onADStatusChanged()V` | `Lcom/kugou/fanxing/modul/ad/view/AdBannerView;->a` | 独立业务 caller(未见 VIP 链引用)——波及面最小 |
| `com/kugou/fanxing/modul/ad/view/AdBannerView.smali` | classes15 | `public final setAdVisibible(Z)V` | `Lcom/kugou/fanxing/modul/ad/view/AdBannerView;->c` | 独立业务 caller(未见 VIP 链引用)——波及面最小 |
| `com/kugou/fanxing/modul/shortplay/delegate/e$c.smali` | classes2 | `public final run()V` | `Lcom/kugou/fanxing/modul/ad/view/AdBannerView;->setAdVisibible` | 独立业务 caller(未见 VIP 链引用)——波及面最小 |
| `com/kugou/fanxing/modul/shortplay/delegate/e.smali` | classes2 | `public onDestroy()V` | `Lcom/kugou/fanxing/modul/ad/view/AdBannerView;->c` | 独立业务 caller(未见 VIP 链引用)——波及面最小 |
| `com/qq/e/comm/managers/plugin/a.smali` | classes3 | `public final a()V` | `Lcom/tencent/ams/fusion/dynamic/SplashAdDynamicEngineManager;->getInstance` | 独立业务 caller(未见 VIP 链引用)——波及面最小 |
| `com/qq/e/comm/plugin/tangramsplash/a/a.smali` | classes3 | `public static a(Ljava/lang/String;)V` | `Lcom/tencent/ams/fusion/dynamic/SplashAdDynamicConfig;->setAdInfo` | 独立业务 caller(未见 VIP 链引用)——波及面最小 |
| `com/qq/e/comm/plugin/tangramsplash/a/b$1.smali` | classes3 | `public run()V` | `Lcom/tencent/ams/fusion/dynamic/SplashAdDynamicEngineManager;->getInstance` | 独立业务 caller(未见 VIP 链引用)——波及面最小 |
| `com/qq/e/comm/plugin/tangramsplash/a/b$3.smali` | classes3 | `public run()V` | `Lcom/tencent/ams/fusion/dynamic/SplashAdDynamicView;->recycleMosaicEngine` | 独立业务 caller(未见 VIP 链引用)——波及面最小 |
| `com/qq/e/comm/plugin/tangramsplash/a/b.smali` | classes3 | `private ab()V` | `Lcom/tencent/ams/fusion/dynamic/SplashAdDynamicView;->getEngine` | 独立业务 caller(未见 VIP 链引用)——波及面最小 |
| `com/qq/e/comm/plugin/tangramsplash/d/d.smali` | classes3 | `private h(Ljava/lang/String;Z)V` | `Lcom/tencent/ams/fusion/dynamic/SplashAdDynamicEngineManager;->getInstance` | 独立业务 caller(未见 VIP 链引用)——波及面最小 |
| `com/qq/e/tg/splash/TGSplashAD$ADListenerAdapter.smali` | classes3 | `public onADEvent(Lcom/qq/e/comm/adevent/ADEvent;)V` | `Lcom/qq/e/tg/splash/TGSplashAdListener;->onADClicked` | 独立业务 caller(未见 VIP 链引用)——波及面最小 |
| `com/qq/e/tg/splash/TGSplashAD.smali` | classes3 | `private static a(Lcom/qq/e/tg/splash/TGSplashAdListener;I)V` | `Lcom/qq/e/tg/splash/TGSplashAdListener;->onNoAD` | 独立业务 caller(未见 VIP 链引用)——波及面最小 |
| `com/tencent/ams/fusion/dynamic/SplashAdDynamicEngineManager$1.smali` | classes3 | `public onEngineInitializeError(I)V` | `Lcom/tencent/ams/fusion/dynamic/SplashAdDynamicEngineManager$InitCallback;->onInitFailed` | 独立业务 caller(未见 VIP 链引用)——波及面最小 |
| `com/tencent/ams/fusion/dynamic/SplashAdDynamicEngineManager$2.smali` | classes3 | `public onEngineInitializeError(I)V` | `Lcom/tencent/ams/fusion/dynamic/SplashAdDynamicReporter;->reportEngineInitFailed` | 独立业务 caller(未见 VIP 链引用)——波及面最小 |
| `com/tencent/ams/fusion/dynamic/SplashAdDynamicEngineManager.smali` | classes3 | `public preWarmMosaicEngine(Landroid/content/Context;Lcom/ten` | `Lcom/tencent/ams/fusion/dynamic/SplashAdDynamicConfig;->getAppName` | 独立业务 caller(未见 VIP 链引用)——波及面最小 |
| `com/tencent/ams/fusion/dynamic/SplashAdDynamicReporter.smali` | classes3 | `public static reportEngineInitFailed(IJ)V` | `Lcom/tencent/ams/fusion/dynamic/SplashAdDynamicEngineManager;->getInstance` | 独立业务 caller(未见 VIP 链引用)——波及面最小 |
| `com/tencent/ams/fusion/dynamic/SplashAdDynamicView$3.smali` | classes3 | `public onViewCreate(Landroid/view/View;I)V` | `Lcom/tencent/ams/fusion/dynamic/SplashAdDynamicReporter;->reportViewCreateFailed` | 独立业务 caller(未见 VIP 链引用)——波及面最小 |
| `com/tencent/ams/fusion/dynamic/SplashAdDynamicView$6.smali` | classes3 | `public invoke(Lcom/tencent/ams/dsdk/core/DKEngine;Ljava/lang` | `Lcom/tencent/ams/fusion/dynamic/SplashAdDynamicReporter;->reportSplashClicked` | 独立业务 caller(未见 VIP 链引用)——波及面最小 |
| `com/tencent/ams/fusion/dynamic/SplashAdDynamicView$7.smali` | classes3 | `public invoke(Lcom/tencent/ams/dsdk/core/DKEngine;Ljava/lang` | `Lcom/tencent/ams/fusion/dynamic/SplashAdDynamicReporter;->reportViewRenderFinish` | 独立业务 caller(未见 VIP 链引用)——波及面最小 |
| `com/tencent/ams/fusion/dynamic/SplashAdDynamicView.smali` | classes3 | `private createDynamicViewFromMosaicEngine(Lcom/tencent/ams/d` | `Lcom/tencent/ams/fusion/dynamic/SplashAdDynamicConfig;->getAdInfo` | 独立业务 caller(未见 VIP 链引用)——波及面最小 |
| `com/tencent/ams/fusion/service/dynamic/impl/DynamicServiceImpl$1.smali` | classes3 | `public onEngineInitialized()V` | `Lcom/tencent/ams/fusion/dynamic/SplashAdDynamicEngineManager;->getInstance` | 独立业务 caller(未见 VIP 链引用)——波及面最小 |
| `com/tencent/ams/fusion/service/dynamic/impl/DynamicServiceImpl.smali` | classes3 | `public getEngine(Ljava/lang/String;J)Lcom/tencent/ams/dsdk/c` | `Lcom/tencent/ams/fusion/dynamic/SplashAdDynamicEngineManager;->getInstance` | 独立业务 caller(未见 VIP 链引用)——波及面最小 |
| `fo1/a.smali` | classes5 | `public final jumpToCustomLandingPage(Landroid/content/Contex` | `Lcom/tencentmusic/ad/adapter/ams/AMSSplashAdapter;->e` | 独立业务 caller(未见 VIP 链引用)——波及面最小 |
| `fo1/b.smali` | classes5 | `public final invoke()Ljava/lang/Object;` | `Lcom/tencentmusic/ad/adapter/ams/AMSSplashAdapter;->f` | 独立业务 caller(未见 VIP 链引用)——波及面最小 |
| `fo1/c.smali` | classes5 | `public final run()V` | `Lcom/tencentmusic/ad/adapter/ams/AMSSplashAdapter;->g` | 独立业务 caller(未见 VIP 链引用)——波及面最小 |
| `fo1/d.smali` | classes5 | `public final run()V` | `Lcom/tencentmusic/ad/adapter/ams/AMSSplashAdapter;->h` | 独立业务 caller(未见 VIP 链引用)——波及面最小 |
| `fo1/e.smali` | classes5 | `public final run()V` | `Lcom/tencentmusic/ad/adapter/ams/AMSSplashAdapter;->d` | 独立业务 caller(未见 VIP 链引用)——波及面最小 |
| `go1/a.smali` | classes5 | `public final run()V` | `Lcom/tencentmusic/ad/adapter/ams/nativead/AMSNativeAdAdapter$a;->a` | 独立业务 caller(未见 VIP 链引用)——波及面最小 |
| `ho1/a.smali` | classes6 | `public final invoke()Ljava/lang/Object;` | `Lcom/tencentmusic/ad/adapter/common/BaseAdAdapter;->b` | 独立业务 caller(未见 VIP 链引用)——波及面最小 |
| `ho1/b.smali` | classes6 | `public final invoke()Ljava/lang/Object;` | `Lcom/tencentmusic/ad/adapter/common/BaseAdAdapter;->c` | 独立业务 caller(未见 VIP 链引用)——波及面最小 |
| `ho1/c.smali` | classes6 | `public final run()V` | `Lcom/tencentmusic/ad/adapter/common/BaseAdAdapter;->a` | 独立业务 caller(未见 VIP 链引用)——波及面最小 |
| `io1/a.smali` | classes6 | `public final invoke()Ljava/lang/Object;` | `Lcom/tencentmusic/ad/adapter/mad/nativead/MADNativeAdAdapter;->d` | 独立业务 caller(未见 VIP 链引用)——波及面最小 |
| `io1/b.smali` | classes6 | `public final run()V` | `Lcom/tencentmusic/ad/adapter/mad/nativead/MADNativeAdAdapter;->e` | 独立业务 caller(未见 VIP 链引用)——波及面最小 |
| `jo1/a.smali` | classes6 | `public final handleMessage(Landroid/os/Message;)Z` | `Lcom/tencentmusic/ad/adapter/mad/reward/MADRewardVideoAdAdapter;->k` | 独立业务 caller(未见 VIP 链引用)——波及面最小 |
| `jo1/b.smali` | classes6 | `public final onReceiveValue(Ljava/lang/Object;)V` | `Lcom/tencentmusic/ad/adapter/mad/reward/MADRewardVideoAdAdapter;->j` | 独立业务 caller(未见 VIP 链引用)——波及面最小 |
| `jo1/c.smali` | classes6 | `public final invoke()Ljava/lang/Object;` | `Lcom/tencentmusic/ad/adapter/mad/reward/MADRewardVideoAdAdapter;->i` | 独立业务 caller(未见 VIP 链引用)——波及面最小 |
| `jo1/d.smali` | classes6 | `public final invoke()Ljava/lang/Object;` | `Lcom/tencentmusic/ad/adapter/mad/reward/MADRewardVideoAdAdapter;->e` | 独立业务 caller(未见 VIP 链引用)——波及面最小 |
| `jo1/e.smali` | classes6 | `public final invoke()Ljava/lang/Object;` | `Lcom/tencentmusic/ad/adapter/mad/reward/MADRewardVideoAdAdapter;->f` | 独立业务 caller(未见 VIP 链引用)——波及面最小 |
| `jo1/f.smali` | classes6 | `public final invoke()Ljava/lang/Object;` | `Lcom/tencentmusic/ad/adapter/mad/reward/MADRewardVideoAdAdapter;->g` | 独立业务 caller(未见 VIP 链引用)——波及面最小 |
| `jo1/g.smali` | classes6 | `public final invoke()Ljava/lang/Object;` | `Lcom/tencentmusic/ad/adapter/mad/reward/MADRewardVideoAdAdapter;->d` | 独立业务 caller(未见 VIP 链引用)——波及面最小 |
| `jo1/h.smali` | classes6 | `public final invoke()Ljava/lang/Object;` | `Lcom/tencentmusic/ad/adapter/mad/reward/MADRewardVideoAdAdapter;->h` | 独立业务 caller(未见 VIP 链引用)——波及面最小 |
| `jo1/i.smali` | classes6 | `public final invoke()Ljava/lang/Object;` | `Lcom/tencentmusic/ad/adapter/mad/reward/MADRewardVideoAdAdapter$b;->a` | 独立业务 caller(未见 VIP 链引用)——波及面最小 |
| `jo1/j.smali` | classes6 | `public final invoke()Ljava/lang/Object;` | `Lcom/tencentmusic/ad/adapter/mad/reward/MADRewardVideoAdAdapter$b;->a` | 独立业务 caller(未见 VIP 链引用)——波及面最小 |
| `jo1/k.smali` | classes6 | `public final invoke()Ljava/lang/Object;` | `Lcom/tencentmusic/ad/adapter/mad/reward/MADRewardVideoAdAdapter$b;->b` | 独立业务 caller(未见 VIP 链引用)——波及面最小 |
| `jo1/l.smali` | classes6 | `public final invoke()Ljava/lang/Object;` | `Lcom/tencentmusic/ad/adapter/mad/reward/MADRewardVideoAdAdapter$b;->a` | 独立业务 caller(未见 VIP 链引用)——波及面最小 |
| `ko1/a.smali` | classes6 | `public final onReceiveValue(Ljava/lang/Object;)V` | `Lcom/tencentmusic/ad/adapter/mad/splash/MADBaseSplashAdapter;->d` | 独立业务 caller(未见 VIP 链引用)——波及面最小 |
| `ko1/b.smali` | classes6 | `public final invoke()Ljava/lang/Object;` | `Lcom/tencentmusic/ad/adapter/mad/splash/MADBaseSplashAdapter;->f` | 独立业务 caller(未见 VIP 链引用)——波及面最小 |
| `ko1/c.smali` | classes6 | `public final invoke()Ljava/lang/Object;` | `Lcom/tencentmusic/ad/adapter/mad/splash/MADBaseSplashAdapter;->e` | 独立业务 caller(未见 VIP 链引用)——波及面最小 |
| `ko1/d.smali` | classes6 | `public final invoke()Ljava/lang/Object;` | `Lcom/tencentmusic/ad/adapter/mad/splash/MADBaseSplashAdapter$c;->a` | 独立业务 caller(未见 VIP 链引用)——波及面最小 |
| `ko1/e.smali` | classes6 | `public final invoke()Ljava/lang/Object;` | `Lcom/tencentmusic/ad/adapter/mad/splash/MADBaseSplashAdapter$c;->b` | 独立业务 caller(未见 VIP 链引用)——波及面最小 |
| `ko1/f.smali` | classes6 | `public final invoke(Ljava/lang/Object;)Ljava/lang/Object;` | `Lcom/tencentmusic/ad/adapter/mad/splash/MADBaseSplashAdapter$c;->a` | 独立业务 caller(未见 VIP 链引用)——波及面最小 |
| `ko1/g.smali` | classes6 | `public final run()V` | `Lcom/tencentmusic/ad/adapter/mad/splash/MADBaseSplashAdapter$c;->c` | 独立业务 caller(未见 VIP 链引用)——波及面最小 |
| `ko1/h.smali` | classes6 | `public final run()V` | `Lcom/tencentmusic/ad/adapter/mad/splash/MADExpoSplashAdapter;->h` | 独立业务 caller(未见 VIP 链引用)——波及面最小 |
| `ko1/i.smali` | classes6 | `public final run()V` | `Lcom/tencentmusic/ad/adapter/mad/splash/MADExpoSplashAdapter;->g` | 独立业务 caller(未见 VIP 链引用)——波及面最小 |
| `lo1/a.smali` | classes6 | `public final invoke()Ljava/lang/Object;` | `Lcom/tencentmusic/ad/adapter/madams/splash/OperBaseSplashAdapter;->d` | 独立业务 caller(未见 VIP 链引用)——波及面最小 |
| `lo1/b.smali` | classes6 | `public final onReceiveValue(Ljava/lang/Object;)V` | `Lcom/tencentmusic/ad/adapter/madams/splash/OperExpertSplashAdapter;->s` | 独立业务 caller(未见 VIP 链引用)——波及面最小 |
| `lo1/c.smali` | classes6 | `public final invoke()Ljava/lang/Object;` | `Lcom/tencentmusic/ad/adapter/madams/splash/OperExpertSplashAdapter;->u` | 独立业务 caller(未见 VIP 链引用)——波及面最小 |
| `lo1/d.smali` | classes6 | `public final run()V` | `Lcom/tencentmusic/ad/adapter/madams/splash/OperExpertSplashAdapter;->e` | 独立业务 caller(未见 VIP 链引用)——波及面最小 |
| `lo1/e.smali` | classes6 | `public final run()V` | `Lcom/tencentmusic/ad/adapter/madams/splash/OperExpertSplashAdapter;->f` | 独立业务 caller(未见 VIP 链引用)——波及面最小 |
| `lo1/f.smali` | classes6 | `public final run()V` | `Lcom/tencentmusic/ad/adapter/madams/splash/OperExpertSplashAdapter;->t` | 独立业务 caller(未见 VIP 链引用)——波及面最小 |
| `lo1/g.smali` | classes6 | `public final run()V` | `Lcom/tencentmusic/ad/adapter/madams/splash/OperExpertSplashAdapter;->i` | 独立业务 caller(未见 VIP 链引用)——波及面最小 |
| `lo1/h.smali` | classes6 | `public final run()V` | `Lcom/tencentmusic/ad/adapter/madams/splash/OperExpertSplashAdapter;->k` | 独立业务 caller(未见 VIP 链引用)——波及面最小 |
| `lo1/i.smali` | classes6 | `public final run()V` | `Lcom/tencentmusic/ad/adapter/madams/splash/OperExpertSplashAdapter;->o` | 独立业务 caller(未见 VIP 链引用)——波及面最小 |
| `lo1/j.smali` | classes6 | `public final onReceiveValue(Ljava/lang/Object;)V` | `Lcom/tencentmusic/ad/adapter/madams/splash/OperExpertSplashAdapter;->r` | 独立业务 caller(未见 VIP 链引用)——波及面最小 |
| `lo1/k.smali` | classes6 | `public final onReceiveValue(Ljava/lang/Object;)V` | `Lcom/tencentmusic/ad/adapter/madams/splash/OperExpertSplashAdapter;->h` | 独立业务 caller(未见 VIP 链引用)——波及面最小 |
| `lo1/l.smali` | classes6 | `public final onReceiveValue(Ljava/lang/Object;)V` | `Lcom/tencentmusic/ad/adapter/madams/splash/OperExpertSplashAdapter;->l` | 独立业务 caller(未见 VIP 链引用)——波及面最小 |
| `lo1/m.smali` | classes6 | `public final invoke()Ljava/lang/Object;` | `Lcom/tencentmusic/ad/adapter/madams/splash/OperExpertSplashAdapter;->j` | 独立业务 caller(未见 VIP 链引用)——波及面最小 |
| `lo1/n.smali` | classes6 | `public final invoke()Ljava/lang/Object;` | `Lcom/tencentmusic/ad/adapter/madams/splash/OperExpertSplashAdapter;->g` | 独立业务 caller(未见 VIP 链引用)——波及面最小 |
| `lo1/o.smali` | classes6 | `public final invoke()Ljava/lang/Object;` | `Lcom/tencentmusic/ad/adapter/madams/splash/OperExpertSplashAdapter;->p` | 独立业务 caller(未见 VIP 链引用)——波及面最小 |
| `lo1/p.smali` | classes6 | `public final invoke()Ljava/lang/Object;` | `Lcom/tencentmusic/ad/adapter/madams/splash/OperExpertSplashAdapter;->n` | 独立业务 caller(未见 VIP 链引用)——波及面最小 |
| `lo1/q.smali` | classes6 | `public final invoke()Ljava/lang/Object;` | `Lcom/tencentmusic/ad/adapter/madams/splash/OperExpertSplashAdapter;->q` | 独立业务 caller(未见 VIP 链引用)——波及面最小 |
| `lo1/r.smali` | classes6 | `public final invoke()Ljava/lang/Object;` | `Lcom/tencentmusic/ad/adapter/madams/splash/OperExpertSplashAdapter;->m` | 独立业务 caller(未见 VIP 链引用)——波及面最小 |
| `lo1/s.smali` | classes6 | `public final onReceiveValue(Ljava/lang/Object;)V` | `Lcom/tencentmusic/ad/adapter/madams/splash/OperExpertSplashAdapter$b;->a` | 独立业务 caller(未见 VIP 链引用)——波及面最小 |
| `qd/e.smali` | classes9 | `public static f()I` | `Lcom/tencentmusic/ad/TMEAds;->checkSplashInterval` | 混挂VIP特征——掐该caller先审 VIP 依赖链，防 P3 式崩会员 |
| `ra/e.smali` | classes8 | `protected d(Ljava/lang/String;Ljava/lang/String;Lorg/xml/sax` | `Lcn/kuwo/base/bean/shieldadinfo/SplashAdShakeShieldInfo;->setThreshold` | 混挂VIP特征——掐该caller先审 VIP 依赖链，防 P3 式崩会员 |
| `sd/d.smali` | classes9 | `public b(Landroid/content/Context;Ljava/lang/String;)V` | `Lcom/tme/fireeye/lib/base/FireEye;->init` | 独立业务 caller(未见 VIP 链引用)——波及面最小 |
| `z6/a.smali` | classes8 | `b()V` | `Lcom/tencentmusic/ad/TMEAds;->getPosConfig` | 独立业务 caller(未见 VIP 链引用)——波及面最小 |
| `z6/b.smali` | classes8 | `private static f(Ljava/util/List;)Ljava/lang/String;` | `Lcom/tencentmusic/ad/TMEAds;->getVersionName` | 混挂VIP特征——掐该caller先审 VIP 依赖链，防 P3 式崩会员 |

> 真机基线（老马 PJD110：外联仅腾讯系 443 正常业务面）：存活表=Java 静态口径，最终掐点组合等老马点位表 + 真机复验。

