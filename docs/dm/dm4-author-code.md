# DM-1 W4：东明版作者自有类反编译八组汇总（jadx，CI 自动产物）

- 样本：dongming-kuwo-12.2.2.0.apk（sha256 50251119906266d50b872af8de4372c95b40548e175630b85af918e985d43588）
- 反编译：jadx --no-res --no-debug-info --no-imports --show-bad-code，单 dex 直喂 classes9/16/17/18.dex
- 口径：仅陈述「该方法在此类、该正则在此行命中」级事实；**不判 A/B/C/D、不做安全定性**。
- 网络面命中口径 = 派单给定正则（URL/okhttp/java.net/Socket/loadLibrary/WebView/getAssets/SharedPreferences/SQLite/ContentProvider·Resolver/telephony/getDeviceId/ANDROID_ID/Build.MODEL/Base64/Cipher/SecretKey/MessageDigest/MD5/SHA 等），命中=仅此正则，非仅此正则即无风险。

## 总表

| 组 | 源 dex | 路径前缀 | 文件数 | 行数 | 方法/字段声明 | 网络面命中 |
|---|---|---|---:|---:|---:|---:|
| G1_com_dm_dia | classes18.dex | com/dm/dia | 29 | 1466 | 360 | 21 |
| G2_com_vip_yf | classes17.dex | com/vip/yf | 2 | 431 | 93 | 6 |
| G3_com_kw_cj | classes17.dex | com/kw/cj | 3 | 327 | 80 | 8 |
| G4_njggg | classes17.dex | njggg | 2 | 170 | 40 | 1 |
| G5_abcdefgaaa | classes18.dex | abcdefgaaa | 2 | 22 | 3 | 1 |
| G6_kwpass | classes17.dex | kwpass | 1 | 11 | 1 | 0 |
| G7_rj_lddne | classes9.dex | rj/lddne | 1 | 112 | 6 | 5 |
| G8_nt_phkc | classes16.dex | nt/phkc | 1 | 52 | 5 | 1 |
| **合计** | | | **41** | **2591** | | **43** |

## G1_com_dm_dia（classes18.dex，前缀 com/dm/dia）

### 文件清单

| 文件 | 行数 | 声明数 | 命中数 |
|---|---:|---:|---:|
| com/dm/dia/i.java | 36 | 13 | 0 |
| com/dm/dia/l.java | 47 | 12 | 1 |
| com/dm/dia/o$$ExternalSyntheticLambda0.java | 19 | 5 | 0 |
| com/dm/dia/o$$ExternalSyntheticLambda1.java | 17 | 4 | 0 |
| com/dm/dia/o$$ExternalSyntheticLambda10.java | 9 | 1 | 0 |
| com/dm/dia/o$$ExternalSyntheticLambda11.java | 23 | 7 | 0 |
| com/dm/dia/o$$ExternalSyntheticLambda12.java | 9 | 1 | 0 |
| com/dm/dia/o$$ExternalSyntheticLambda13.java | 9 | 1 | 0 |
| com/dm/dia/o$$ExternalSyntheticLambda14.java | 9 | 1 | 0 |
| com/dm/dia/o$$ExternalSyntheticLambda15.java | 31 | 11 | 0 |
| com/dm/dia/o$$ExternalSyntheticLambda16.java | 19 | 5 | 0 |
| com/dm/dia/o$$ExternalSyntheticLambda17.java | 9 | 1 | 0 |
| com/dm/dia/o$$ExternalSyntheticLambda18.java | 17 | 4 | 0 |
| com/dm/dia/o$$ExternalSyntheticLambda19.java | 17 | 4 | 0 |
| com/dm/dia/o$$ExternalSyntheticLambda2.java | 19 | 5 | 0 |
| com/dm/dia/o$$ExternalSyntheticLambda20.java | 11 | 2 | 0 |
| com/dm/dia/o$$ExternalSyntheticLambda21.java | 9 | 1 | 0 |
| com/dm/dia/o$$ExternalSyntheticLambda22.java | 11 | 2 | 0 |
| com/dm/dia/o$$ExternalSyntheticLambda23.java | 21 | 6 | 0 |
| com/dm/dia/o$$ExternalSyntheticLambda3.java | 11 | 2 | 0 |
| com/dm/dia/o$$ExternalSyntheticLambda4.java | 9 | 1 | 0 |
| com/dm/dia/o$$ExternalSyntheticLambda5.java | 17 | 4 | 0 |
| com/dm/dia/o$$ExternalSyntheticLambda6.java | 11 | 2 | 0 |
| com/dm/dia/o$$ExternalSyntheticLambda7.java | 9 | 1 | 0 |
| com/dm/dia/o$$ExternalSyntheticLambda8.java | 9 | 1 | 0 |
| com/dm/dia/o$$ExternalSyntheticLambda9.java | 9 | 1 | 0 |
| com/dm/dia/o.java | 750 | 214 | 7 |
| com/dm/dia/u.java | 256 | 42 | 6 |
| com/dm/dia/v.java | 43 | 6 | 7 |

### 方法/字段声明粗提取（public|private|protected|static|final|native 等，前 120 字符）

- `com/dm/dia/i.java:5` private static android.content.SharedPreferences sp;
- `com/dm/dia/i.java:12` private i() {
- `com/dm/dia/i.java:15` static native void aa(android.content.Context context);
- `com/dm/dia/i.java:17` static native boolean ab(java.lang.String str, boolean z);
- `com/dm/dia/i.java:19` static native void ac(java.lang.String str, boolean z);
- `com/dm/dia/i.java:21` static native long ad(java.lang.String str, long j);
- `com/dm/dia/i.java:23` static native void ae(java.lang.String str, long j);
- `com/dm/dia/i.java:25` static native int af(java.lang.String str, int i);
- `com/dm/dia/i.java:27` static native void ag(java.lang.String str, int i);
- `com/dm/dia/i.java:29` private static native void ah(android.content.Context context);
- `com/dm/dia/i.java:31` private static native java.lang.String ai(java.lang.String str);
- `com/dm/dia/i.java:33` private static native java.lang.String aj(java.lang.String str);
- `com/dm/dia/i.java:35` private static native void ak(java.lang.String str, java.lang.String str2);
- `com/dm/dia/l.java:5` static final boolean cryptoOk;
- `com/dm/dia/l.java:6` static final boolean loaded;
- `com/dm/dia/l.java:27` private l() {
- `com/dm/dia/l.java:30` private static native boolean aa();
- `com/dm/dia/l.java:32` static native byte[] ab(byte[] bArr);
- `com/dm/dia/l.java:34` static native byte[] ac(byte[] bArr, byte[] bArr2);
- `com/dm/dia/l.java:36` static native java.lang.String ad();
- `com/dm/dia/l.java:38` static native java.lang.String ae(java.lang.String str);
- `com/dm/dia/l.java:40` static native byte[] af(byte[] bArr);
- `com/dm/dia/l.java:42` static native byte[] ag(byte[] bArr);
- `com/dm/dia/l.java:44` static native boolean ah(android.graphics.Bitmap bitmap, int i);
- `com/dm/dia/l.java:46` static native boolean ai(android.graphics.Bitmap bitmap, float f);
- `com/dm/dia/o$$ExternalSyntheticLambda0.java:5` public final /* synthetic */ boolean[] f$0;
- `com/dm/dia/o$$ExternalSyntheticLambda0.java:6` public final /* synthetic */ android.view.View f$1;
- `com/dm/dia/o$$ExternalSyntheticLambda0.java:7` public final /* synthetic */ java.lang.Runnable f$2;
- `com/dm/dia/o$$ExternalSyntheticLambda0.java:9` public /* synthetic */ o$$ExternalSyntheticLambda0(boolean[] zArr, android.view.View view, java.lang.Runnable runnable)…
- `com/dm/dia/o$$ExternalSyntheticLambda0.java:16` public final void run() {
- `com/dm/dia/o$$ExternalSyntheticLambda1.java:5` public final /* synthetic */ android.widget.ScrollView f$0;
- `com/dm/dia/o$$ExternalSyntheticLambda1.java:6` public final /* synthetic */ int f$1;
- `com/dm/dia/o$$ExternalSyntheticLambda1.java:8` public /* synthetic */ o$$ExternalSyntheticLambda1(android.widget.ScrollView scrollView, int i) {
- `com/dm/dia/o$$ExternalSyntheticLambda1.java:14` public final void onLayoutChange(android.view.View view, int i, int i2, int i3, int i4, int i5, int i6, int i7, int i8)…
- `com/dm/dia/o$$ExternalSyntheticLambda10.java:6` public final void run() {
- `com/dm/dia/o$$ExternalSyntheticLambda11.java:5` public final /* synthetic */ android.app.Activity f$0;
- `com/dm/dia/o$$ExternalSyntheticLambda11.java:6` public final /* synthetic */ int f$1;
- `com/dm/dia/o$$ExternalSyntheticLambda11.java:7` public final /* synthetic */ int f$2;
- `com/dm/dia/o$$ExternalSyntheticLambda11.java:8` public final /* synthetic */ com.dm.dia.u f$3;
- `com/dm/dia/o$$ExternalSyntheticLambda11.java:9` public final /* synthetic */ int[] f$4;
- `com/dm/dia/o$$ExternalSyntheticLambda11.java:11` public /* synthetic */ o$$ExternalSyntheticLambda11(android.app.Activity activity, int i, int i2, com.dm.dia.u uVar, in…
- `com/dm/dia/o$$ExternalSyntheticLambda11.java:20` public final void run() {
- `com/dm/dia/o$$ExternalSyntheticLambda12.java:6` public final void run() {
- `com/dm/dia/o$$ExternalSyntheticLambda13.java:6` public final void run() {
- `com/dm/dia/o$$ExternalSyntheticLambda14.java:6` public final void run() {
- `com/dm/dia/o$$ExternalSyntheticLambda15.java:5` public final /* synthetic */ boolean f$0;
- `com/dm/dia/o$$ExternalSyntheticLambda15.java:6` public final /* synthetic */ com.dm.dia.o.UpdateCheckCallback f$1;
- `com/dm/dia/o$$ExternalSyntheticLambda15.java:7` public final /* synthetic */ int f$2;
- `com/dm/dia/o$$ExternalSyntheticLambda15.java:8` public final /* synthetic */ java.lang.String f$3;
- `com/dm/dia/o$$ExternalSyntheticLambda15.java:9` public final /* synthetic */ long f$4;
- `com/dm/dia/o$$ExternalSyntheticLambda15.java:10` public final /* synthetic */ java.lang.String f$5;
- `com/dm/dia/o$$ExternalSyntheticLambda15.java:11` public final /* synthetic */ java.lang.String f$6;
- `com/dm/dia/o$$ExternalSyntheticLambda15.java:12` public final /* synthetic */ long f$7;
- `com/dm/dia/o$$ExternalSyntheticLambda15.java:13` public final /* synthetic */ java.lang.String f$8;
- `com/dm/dia/o$$ExternalSyntheticLambda15.java:15` public /* synthetic */ o$$ExternalSyntheticLambda15(boolean z, com.dm.dia.o.UpdateCheckCallback updateCheckCallback, in…
- `com/dm/dia/o$$ExternalSyntheticLambda15.java:28` public final void run() {
- `com/dm/dia/o$$ExternalSyntheticLambda16.java:5` public final /* synthetic */ android.graphics.Bitmap f$0;
- `com/dm/dia/o$$ExternalSyntheticLambda16.java:6` public final /* synthetic */ com.dm.dia.u f$1;
- `com/dm/dia/o$$ExternalSyntheticLambda16.java:7` public final /* synthetic */ int[] f$2;
- `com/dm/dia/o$$ExternalSyntheticLambda16.java:9` public /* synthetic */ o$$ExternalSyntheticLambda16(android.graphics.Bitmap bitmap, com.dm.dia.u uVar, int[] iArr) {
- `com/dm/dia/o$$ExternalSyntheticLambda16.java:16` public final void run() {
- `com/dm/dia/o$$ExternalSyntheticLambda17.java:6` public final void onCancel(android.content.DialogInterface dialogInterface) {
- `com/dm/dia/o$$ExternalSyntheticLambda18.java:5` public final /* synthetic */ java.util.concurrent.atomic.AtomicInteger f$0;
- `com/dm/dia/o$$ExternalSyntheticLambda18.java:6` public final /* synthetic */ java.util.concurrent.CountDownLatch f$1;
- `com/dm/dia/o$$ExternalSyntheticLambda18.java:8` public /* synthetic */ o$$ExternalSyntheticLambda18(java.util.concurrent.atomic.AtomicInteger atomicInteger, java.util.…
- `com/dm/dia/o$$ExternalSyntheticLambda18.java:14` public final void onPixelCopyFinished(int i) {
- `com/dm/dia/o$$ExternalSyntheticLambda19.java:5` public final /* synthetic */ android.app.Activity f$0;
- `com/dm/dia/o$$ExternalSyntheticLambda19.java:6` public final /* synthetic */ java.lang.String f$1;
- `com/dm/dia/o$$ExternalSyntheticLambda19.java:8` public /* synthetic */ o$$ExternalSyntheticLambda19(android.app.Activity activity, java.lang.String str) {
- `com/dm/dia/o$$ExternalSyntheticLambda19.java:14` public final void onClick(android.view.View view) {
- `com/dm/dia/o$$ExternalSyntheticLambda2.java:5` public final /* synthetic */ android.view.View f$0;
- `com/dm/dia/o$$ExternalSyntheticLambda2.java:6` public final /* synthetic */ android.app.Activity f$1;
- `com/dm/dia/o$$ExternalSyntheticLambda2.java:7` public final /* synthetic */ com.dm.dia.u f$2;
- `com/dm/dia/o$$ExternalSyntheticLambda2.java:9` public /* synthetic */ o$$ExternalSyntheticLambda2(android.view.View view, android.app.Activity activity, com.dm.dia.u …
- `com/dm/dia/o$$ExternalSyntheticLambda2.java:16` public final void run() {
- `com/dm/dia/o$$ExternalSyntheticLambda20.java:5` public final /* synthetic */ long f$0;
- `com/dm/dia/o$$ExternalSyntheticLambda20.java:8` public final void onClick(android.view.View view) {
- `com/dm/dia/o$$ExternalSyntheticLambda21.java:6` public final void onCancel(android.content.DialogInterface dialogInterface) {
- `com/dm/dia/o$$ExternalSyntheticLambda22.java:5` public final /* synthetic */ com.dm.dia.o.UpdateCheckCallback f$0;
- `com/dm/dia/o$$ExternalSyntheticLambda22.java:8` public final void run() {
- `com/dm/dia/o$$ExternalSyntheticLambda23.java:5` public final /* synthetic */ java.lang.String f$0;
- `com/dm/dia/o$$ExternalSyntheticLambda23.java:6` public final /* synthetic */ java.lang.String f$1;
- `com/dm/dia/o$$ExternalSyntheticLambda23.java:7` public final /* synthetic */ long f$2;
- `com/dm/dia/o$$ExternalSyntheticLambda23.java:8` public final /* synthetic */ com.dm.dia.o.UpdateCheckCallback f$3;
- `com/dm/dia/o$$ExternalSyntheticLambda23.java:10` public /* synthetic */ o$$ExternalSyntheticLambda23(java.lang.String str, java.lang.String str2, long j, com.dm.dia.o.U…
- `com/dm/dia/o$$ExternalSyntheticLambda23.java:18` public final void run() {
- `com/dm/dia/o$$ExternalSyntheticLambda3.java:5` public final /* synthetic */ java.lang.Runnable f$0;
- `com/dm/dia/o$$ExternalSyntheticLambda3.java:8` public final void onClick(android.view.View view) {
- `com/dm/dia/o$$ExternalSyntheticLambda4.java:6` public final void run() {
- `com/dm/dia/o$$ExternalSyntheticLambda5.java:5` public final /* synthetic */ android.app.Activity f$0;
- `com/dm/dia/o$$ExternalSyntheticLambda5.java:6` public final /* synthetic */ java.lang.String f$1;
- `com/dm/dia/o$$ExternalSyntheticLambda5.java:8` public /* synthetic */ o$$ExternalSyntheticLambda5(android.app.Activity activity, java.lang.String str) {
- `com/dm/dia/o$$ExternalSyntheticLambda5.java:14` public final void run() {
- `com/dm/dia/o$$ExternalSyntheticLambda6.java:5` public final /* synthetic */ long f$0;
- `com/dm/dia/o$$ExternalSyntheticLambda6.java:8` public final void run() {
- `com/dm/dia/o$$ExternalSyntheticLambda7.java:6` public final void run() {
- `com/dm/dia/o$$ExternalSyntheticLambda8.java:6` public final void run() {
- `com/dm/dia/o$$ExternalSyntheticLambda9.java:6` public final void run() {
- `com/dm/dia/o.java:5` private static final int COMPACT_WIDTH_DP = 600;
- `com/dm/dia/o.java:6` private static final int EXPANDED_WIDTH_DP = 1200;
- `com/dm/dia/o.java:7` private static final char[] HEX = null;
- `com/dm/dia/o.java:8` private static final long HOUR_IN_MILLIS = 3600000;
- `com/dm/dia/o.java:9` private static final java.lang.String KEY_LAST_UPDATE_VERSION = "last_update_version_code";
- `com/dm/dia/o.java:10` private static final java.lang.String KEY_REQUEST_COUNT = "request_count";
- `com/dm/dia/o.java:11` private static final java.lang.String KEY_REQUEST_WINDOW_START = "request_window_start";
- `com/dm/dia/o.java:12` private static final int MAX_REQUESTS_PER_HOUR = 10;
- `com/dm/dia/o.java:13` private static final int MAX_RESPONSE_LENGTH = 524288;
- `com/dm/dia/o.java:14` private static final int MEDIUM_WIDTH_DP = 840;
- `com/dm/dia/o.java:15` private static final int PENDING_AGREEMENT = 1;
- `com/dm/dia/o.java:16` private static final int PENDING_NONE = 0;
- `com/dm/dia/o.java:17` private static final int PENDING_UPDATE = 2;
- `com/dm/dia/o.java:18` private static final java.util.concurrent.ExecutorService executor = null;
- `com/dm/dia/o.java:19` private static java.lang.ref.WeakReference<android.app.Activity> sCurrentActivityRef;
- `com/dm/dia/o.java:20` private static final java.util.concurrent.atomic.AtomicLong sCurrentRequestId = null;
- `com/dm/dia/o.java:21` private static java.util.concurrent.Future<?> sCurrentUpdateTask;
- `com/dm/dia/o.java:22` private static android.app.Dialog sDialog;
- `com/dm/dia/o.java:23` private static boolean sFlowStarted;
- `com/dm/dia/o.java:24` private static android.app.Application.ActivityLifecycleCallbacks sLifecycleCallbacks;
- `com/dm/dia/o.java:25` private static final android.os.Handler sMainHandler = null;
- `com/dm/dia/o.java:26` private static int sPendingDialog;
- `com/dm/dia/o.java:27` private static java.lang.String sPendingDownloadUrl;
- `com/dm/dia/o.java:28` private static boolean sPendingForce;
- `com/dm/dia/o.java:29` private static java.lang.String sPendingUpdateLog;
- `com/dm/dia/o.java:30` private static long sPendingVersionCode;
- `com/dm/dia/o.java:31` private static java.lang.String sPendingVersionName;
- `com/dm/dia/o.java:32` private static boolean sRegistered;
- `com/dm/dia/o.java:33` private static com.dm.dia.o.ThemeColors sThemeColors;
- `com/dm/dia/o.java:41` public void onActivityCreated(android.app.Activity activity, android.os.Bundle bundle) {
- `com/dm/dia/o.java:45` public void onActivityDestroyed(android.app.Activity activity) {
- `com/dm/dia/o.java:54` public void onActivityPaused(android.app.Activity activity) {
- `com/dm/dia/o.java:58` public void onActivityResumed(android.app.Activity activity) {
- `com/dm/dia/o.java:63` public void onActivitySaveInstanceState(android.app.Activity activity, android.os.Bundle bundle) {
- `com/dm/dia/o.java:67` public void onActivityStarted(android.app.Activity activity) {
- `com/dm/dia/o.java:71` public void onActivityStopped(android.app.Activity activity) {
- `com/dm/dia/o.java:77` final /* synthetic */ long val$newRequestId;
- `com/dm/dia/o.java:84` public void cg(int i, java.lang.String str, long j, java.lang.String str2, java.lang.String str3, long j2, java.lang.St…
- `com/dm/dia/o.java:115` public void ch() {
- `com/dm/dia/o.java:130` final /* synthetic */ java.lang.Runnable val$onEnd;
- `com/dm/dia/o.java:137` public void onAnimationEnd(android.animation.Animator animator) {
- `com/dm/dia/o.java:144` final /* synthetic */ android.view.View val$decor;
- `com/dm/dia/o.java:145` final /* synthetic */ java.lang.Runnable val$doCapture;
- `com/dm/dia/o.java:153` public void onViewAttachedToWindow(android.view.View view) {
- `com/dm/dia/o.java:159` public void onViewDetachedFromWindow(android.view.View view) {
- `com/dm/dia/o.java:165` final /* synthetic */ android.view.View val$decor;
- `com/dm/dia/o.java:166` final /* synthetic */ java.lang.Runnable val$doCapture;
- `com/dm/dia/o.java:167` final /* synthetic */ boolean[] val$fired;
- `com/dm/dia/o.java:168` final /* synthetic */ android.view.ViewTreeObserver val$vto;
- `com/dm/dia/o.java:178` public /* synthetic */ void lambda$onDraw$0(android.view.ViewTreeObserver viewTreeObserver) {
- `com/dm/dia/o.java:183` public void onDraw() {
- `com/dm/dia/o.java:190` final android.view.ViewTreeObserver viewTreeObserver = this.val$vto;
- `com/dm/dia/o.java:193` public final void run() {
- `com/dm/dia/o.java:203` private static final int TRI_COUNT = 3;
- `com/dm/dia/o.java:204` private final android.animation.ValueAnimator animator;
- `com/dm/dia/o.java:205` private final android.graphics.Paint paint;
- `com/dm/dia/o.java:206` private final android.graphics.Path path;
- `com/dm/dia/o.java:207` private float phase;
- `com/dm/dia/o.java:223` public final void onAnimationUpdate(android.animation.ValueAnimator valueAnimator) {
- `com/dm/dia/o.java:230` public /* synthetic */ void lambda$new$0(android.animation.ValueAnimator valueAnimator) {
- `com/dm/dia/o.java:236` protected void onAttachedToWindow() {
- `com/dm/dia/o.java:242` protected void onDetachedFromWindow() {
- `com/dm/dia/o.java:248` protected void onDraw(android.graphics.Canvas canvas) {
- `com/dm/dia/o.java:274` private android.animation.ValueAnimator anim;
- `com/dm/dia/o.java:275` private float animFromProgress;
- `com/dm/dia/o.java:276` private float animFromTx;
- `com/dm/dia/o.java:277` private float animFromTy;
- `com/dm/dia/o.java:278` private final android.graphics.Path clipPath;
- `com/dm/dia/o.java:279` private float downX;
- `com/dm/dia/o.java:280` private float downY;
- `com/dm/dia/o.java:281` private final android.graphics.Paint hlPaint;
- `com/dm/dia/o.java:282` private float pressProgress;
- `com/dm/dia/o.java:283` private final android.graphics.RectF rect;
- `com/dm/dia/o.java:284` private float spotX;
- `com/dm/dia/o.java:285` private float spotY;
- `com/dm/dia/o.java:294` private void ci(float f, float f2) {
- `com/dm/dia/o.java:314` private void cj(final float f, long j) {
- `com/dm/dia/o.java:328` public final void onAnimationUpdate(android.animation.ValueAnimator valueAnimator2) {
- `com/dm/dia/o.java:336` public /* synthetic */ void lambda$cj$0(float f, android.animation.ValueAnimator valueAnimator) {
- `com/dm/dia/o.java:350` protected void onDraw(android.graphics.Canvas canvas) {
- `com/dm/dia/o.java:380` public boolean onTouchEvent(android.view.MotionEvent motionEvent) {
- `com/dm/dia/o.java:404` private final boolean dark;
- `com/dm/dia/o.java:405` private final android.graphics.Paint paint = new android.graphics.Paint(com.dm.dia.o.PENDING_AGREEMENT);
- `com/dm/dia/o.java:406` private final android.graphics.Paint strokePaint = new android.graphics.Paint(com.dm.dia.o.PENDING_AGREEMENT);
- `com/dm/dia/o.java:407` private final android.graphics.RectF rect = new android.graphics.RectF();
- `com/dm/dia/o.java:414` public void draw(android.graphics.Canvas canvas) {
- `com/dm/dia/o.java:435` public int getOpacity() {
- `com/dm/dia/o.java:440` public void setAlpha(int i) {
- `com/dm/dia/o.java:444` public void setColorFilter(android.graphics.ColorFilter colorFilter) {
- `com/dm/dia/o.java:457` public final int ch;
- `com/dm/dia/o.java:458` public final int error;
- `com/dm/dia/o.java:459` public final int onPrimary;
- `com/dm/dia/o.java:460` public final int onPrimaryContainer;
- `com/dm/dia/o.java:461` public final int onSecondary;
- `com/dm/dia/o.java:462` public final int onSecondaryContainer;
- `com/dm/dia/o.java:463` public final int onSurface;
- `com/dm/dia/o.java:464` public final int onSurfaceVariant;
- `com/dm/dia/o.java:465` public final int onTertiary;
- `com/dm/dia/o.java:466` public final int onTertiaryContainer;
- `com/dm/dia/o.java:467` public final int outline;
- `com/dm/dia/o.java:468` public final int outlineVariant;
- `com/dm/dia/o.java:469` public final int primary;
- `com/dm/dia/o.java:470` public final int primaryContainer;
- `com/dm/dia/o.java:471` public final int secondary;
- `com/dm/dia/o.java:472` public final int secondaryContainer;
- `com/dm/dia/o.java:473` public final int surface;
- `com/dm/dia/o.java:474` public final int surfaceVariant;
- `com/dm/dia/o.java:475` public final int tertiary;
- `com/dm/dia/o.java:476` public final int tertiaryContainer;
- `com/dm/dia/o.java:478` public ThemeColors(int i, int i2, int i3, int i4, int i5, int i6, int i7, int i8, int i9, int i10, int i11, int i12, in…
- `com/dm/dia/o.java:516` static native /* bridge */ /* synthetic */ java.lang.ref.WeakReference m0$$Nest$sfgetsCurrentActivityRef();
- `com/dm/dia/o.java:519` static native /* bridge */ /* synthetic */ java.util.concurrent.atomic.AtomicLong m1$$Nest$sfgetsCurrentRequestId();
- `com/dm/dia/o.java:522` static native /* bridge */ /* synthetic */ int m2$$Nest$sfgetsPendingDialog();
- `com/dm/dia/o.java:525` static native /* bridge */ /* synthetic */ java.lang.String m3$$Nest$sfgetsPendingDownloadUrl();
- `com/dm/dia/o.java:528` static native /* bridge */ /* synthetic */ boolean m4$$Nest$sfgetsPendingForce();
- `com/dm/dia/o.java:531` static native /* bridge */ /* synthetic */ java.lang.String m5$$Nest$sfgetsPendingUpdateLog();
- `com/dm/dia/o.java:534` static native /* bridge */ /* synthetic */ long m6$$Nest$sfgetsPendingVersionCode();
- `com/dm/dia/o.java:537` static native /* bridge */ /* synthetic */ java.lang.String m7$$Nest$sfgetsPendingVersionName();
- `com/dm/dia/o.java:540` static native /* bridge */ /* synthetic */ void m8$$Nest$sfputsPendingDialog(int i);
- `com/dm/dia/o.java:543` static native /* bridge */ /* synthetic */ void m9$$Nest$sfputsPendingDownloadUrl(java.lang.String str);
- `com/dm/dia/o.java:546` static native /* bridge */ /* synthetic */ void m10$$Nest$sfputsPendingForce(boolean z);
- `com/dm/dia/o.java:549` static native /* bridge */ /* synthetic */ void m11$$Nest$sfputsPendingUpdateLog(java.lang.String str);
- `com/dm/dia/o.java:552` static native /* bridge */ /* synthetic */ void m12$$Nest$sfputsPendingVersionCode(long j);
- `com/dm/dia/o.java:555` static native /* bridge */ /* synthetic */ void m13$$Nest$sfputsPendingVersionName(java.lang.String str);
- `com/dm/dia/o.java:558` static native /* bridge */ /* synthetic */ void m14$$Nest$sfputsThemeColors(com.dm.dia.o.ThemeColors themeColors);
- `com/dm/dia/o.java:561` static native /* bridge */ /* synthetic */ void m15$$Nest$smah(android.app.Activity activity);
- `com/dm/dia/o.java:564` static native /* bridge */ /* synthetic */ boolean m16$$Nest$smar(android.app.Activity activity);
- `com/dm/dia/o.java:567` static native /* bridge */ /* synthetic */ void m17$$Nest$smbo();
- `com/dm/dia/o.java:570` static native /* bridge */ /* synthetic */ int m18$$Nest$smbp(android.content.Context context, int i);
- `com/dm/dia/o.java:573` static native /* bridge */ /* synthetic */ void m19$$Nest$smbu(android.app.Activity activity);
- `com/dm/dia/o.java:576` static native /* bridge */ /* synthetic */ void m20$$Nest$smbv(android.app.Activity activity, java.lang.String str, jav…
- `com/dm/dia/o.java:579` static native /* bridge */ /* synthetic */ void m21$$Nest$smbx(android.view.View view, java.lang.Runnable runnable);
- `com/dm/dia/o.java:582` static native /* bridge */ /* synthetic */ com.dm.dia.o.ThemeColors m22$$Nest$smce(android.content.Context context);
- `com/dm/dia/o.java:589` private static native java.util.Map<java.lang.String, java.lang.String> aa(java.lang.String str, long j);
- `com/dm/dia/o.java:591` private static native byte[] ab(byte[] bArr);
- `com/dm/dia/o.java:593` private static native java.lang.String ac(java.lang.String str, java.lang.String str2);
- `com/dm/dia/o.java:595` private static native java.lang.String ad(byte[] bArr);
- `com/dm/dia/o.java:597` public static native void ag(android.app.Application application);
- `com/dm/dia/o.java:599` private static native void ah(android.app.Activity activity);
- `com/dm/dia/o.java:601` private static native void ai(android.app.Activity activity);
- `com/dm/dia/o.java:603` private static native boolean aj();
- `com/dm/dia/o.java:605` public static native void ak(android.app.Activity activity);
- `com/dm/dia/o.java:607` private static native com.dm.dia.o.WindowSizeClass al(android.content.Context context);
- `com/dm/dia/o.java:609` private static native com.dm.dia.o.ScreenType am(android.content.Context context);
- `com/dm/dia/o.java:611` private static native int an(android.content.Context context);
- `com/dm/dia/o.java:613` private static native boolean ao(android.content.Context context);
- `com/dm/dia/o.java:615` private static native boolean ap(android.content.Context context);
- `com/dm/dia/o.java:617` private static native boolean aq(android.content.Context context);
- `com/dm/dia/o.java:619` private static native boolean ar(android.app.Activity activity);
- `com/dm/dia/o.java:621` private static native void as(android.app.Dialog dialog);
- `com/dm/dia/o.java:623` private static native void at(android.app.Dialog dialog, java.lang.Runnable runnable);
- `com/dm/dia/o.java:625` private static native android.app.Dialog au(android.app.Activity activity);
- …（截断：全组共 360 条声明，完整清单见 tar.gz 全文）

### 网络面命中专节（文件:行号 + 行内容前 160 字符）

| 位置 | 内容 |
|---|---|
| com/dm/dia/l.java:12 | java.lang.System.loadLibrary("diacore"); |
| com/dm/dia/o.java:27 | private static java.lang.String sPendingDownloadUrl; |
| com/dm/dia/o.java:97 | com.dm.dia.o.m9$$Nest$sfputsPendingDownloadUrl(str2); |
| com/dm/dia/o.java:109 | com.dm.dia.o.m20$$Nest$smbv(activity, com.dm.dia.o.m3$$Nest$sfgetsPendingDownloadUrl(), com.dm.dia.o.m5$$Nest$sfgetsPendingUpdateLog(), com.dm.dia.o.m7$$Nest$s… |
| com/dm/dia/o.java:524 | /* JADX INFO: renamed from: -$$Nest$sfgetsPendingDownloadUrl, reason: not valid java name */ |
| com/dm/dia/o.java:525 | static native /* bridge */ /* synthetic */ java.lang.String m3$$Nest$sfgetsPendingDownloadUrl(); |
| com/dm/dia/o.java:542 | /* JADX INFO: renamed from: -$$Nest$sfputsPendingDownloadUrl, reason: not valid java name */ |
| com/dm/dia/o.java:543 | static native /* bridge */ /* synthetic */ void m9$$Nest$sfputsPendingDownloadUrl(java.lang.String str); |
| com/dm/dia/u.java:10 | private static final float SHADOW_OFFSET_Y_DP = 4.0f; |
| com/dm/dia/u.java:11 | private static final float SHADOW_RADIUS_DP = 24.0f; |
| com/dm/dia/u.java:36 | private static final int SHADOW_COLOR = android.graphics.Color.argb(26, 0, 0, 0); |
| com/dm/dia/u.java:62 | float f4 = (f2 * SHADOW_OFFSET_Y_DP) + f3; |
| com/dm/dia/u.java:73 | float f3 = f * SHADOW_OFFSET_Y_DP; |
| com/dm/dia/u.java:78 | this.shadowPaint.setColor(SHADOW_COLOR); |
| com/dm/dia/v.java:4 | public class v extends android.content.ContentProvider { |
| com/dm/dia/v.java:5 | @Override // android.content.ContentProvider |
| com/dm/dia/v.java:10 | @Override // android.content.ContentProvider |
| com/dm/dia/v.java:15 | @Override // android.content.ContentProvider |
| com/dm/dia/v.java:20 | @Override // android.content.ContentProvider |
| com/dm/dia/v.java:34 | @Override // android.content.ContentProvider |
| com/dm/dia/v.java:39 | @Override // android.content.ContentProvider |

### 重点点名

**v.java attachBaseContext/onCreate**

- `com/dm/dia/v.java`
  - 21: public boolean onCreate() {

**o.java UpdateCheckCallback 关键字段/方法**

- `com/dm/dia/o.java`
  - 11: private static final java.lang.String KEY_REQUEST_WINDOW_START = "request_window_start";
  - 12: private static final int MAX_REQUESTS_PER_HOUR = 10;
  - 27: private static java.lang.String sPendingDownloadUrl;
  - 525: static native /* bridge */ /* synthetic */ java.lang.String m3$$Nest$sfgetsPendingDownloadUrl();
  - 543: static native /* bridge */ /* synthetic */ void m9$$Nest$sfputsPendingDownloadUrl(java.lang.String str);
  - 675: private static native void bt(android.app.Activity activity, boolean z, com.dm.dia.o.UpdateCheckCallback updateCheckCal…
  - 737: static native /* synthetic */ void lambda$bt$16(boolean z, com.dm.dia.o.UpdateCheckCallback updateCheckCallback, int i,…

> Java 全文见 Release `dm1-artifacts` / `dm4-author-java.tar.gz` → `java/G1_com_dm_dia/`。

## G2_com_vip_yf（classes17.dex，前缀 com/vip/yf）

### 文件清单

| 文件 | 行数 | 声明数 | 命中数 |
|---|---:|---:|---:|
| com/vip/yf/JsonModifiers.java | 408 | 89 | 6 |
| com/vip/yf/JsonUtils.java | 23 | 4 | 0 |

### 方法/字段声明粗提取（public|private|protected|static|final|native 等，前 120 字符）

- `com/vip/yf/JsonModifiers.java:13` public native void modifyJsonArray(org.json.JSONArray jSONArray) throws org.json.JSONException;
- `com/vip/yf/JsonModifiers.java:16` public native void modifyJsonObject(org.json.JSONObject jSONObject) throws org.json.JSONException;
- `com/vip/yf/JsonModifiers.java:26` public native void modifyJsonArray(org.json.JSONArray jSONArray) throws org.json.JSONException;
- `com/vip/yf/JsonModifiers.java:29` public native void modifyJsonObject(org.json.JSONObject jSONObject) throws org.json.JSONException;
- `com/vip/yf/JsonModifiers.java:39` public native void modifyJsonArray(org.json.JSONArray jSONArray) throws org.json.JSONException;
- `com/vip/yf/JsonModifiers.java:42` public native void modifyJsonObject(org.json.JSONObject jSONObject) throws org.json.JSONException;
- `com/vip/yf/JsonModifiers.java:52` public native void modifyJsonArray(org.json.JSONArray jSONArray) throws org.json.JSONException;
- `com/vip/yf/JsonModifiers.java:55` public native void modifyJsonObject(org.json.JSONObject jSONObject) throws org.json.JSONException;
- `com/vip/yf/JsonModifiers.java:65` public native void modifyJsonArray(org.json.JSONArray jSONArray) throws org.json.JSONException;
- `com/vip/yf/JsonModifiers.java:68` public native void modifyJsonObject(org.json.JSONObject jSONObject) throws org.json.JSONException;
- `com/vip/yf/JsonModifiers.java:78` public native void modifyJsonArray(org.json.JSONArray jSONArray) throws org.json.JSONException;
- `com/vip/yf/JsonModifiers.java:81` public native void modifyJsonObject(org.json.JSONObject jSONObject) throws org.json.JSONException;
- `com/vip/yf/JsonModifiers.java:91` public native void modifyJsonArray(org.json.JSONArray jSONArray) throws org.json.JSONException;
- `com/vip/yf/JsonModifiers.java:94` public native void modifyJsonObject(org.json.JSONObject jSONObject) throws org.json.JSONException;
- `com/vip/yf/JsonModifiers.java:104` public native void modifyJsonArray(org.json.JSONArray jSONArray) throws org.json.JSONException;
- `com/vip/yf/JsonModifiers.java:107` public native void modifyJsonObject(org.json.JSONObject jSONObject) throws org.json.JSONException;
- `com/vip/yf/JsonModifiers.java:117` public native void modifyJsonArray(org.json.JSONArray jSONArray) throws org.json.JSONException;
- `com/vip/yf/JsonModifiers.java:120` public native void modifyJsonObject(org.json.JSONObject jSONObject) throws org.json.JSONException;
- `com/vip/yf/JsonModifiers.java:130` public native void modifyJsonArray(org.json.JSONArray jSONArray) throws org.json.JSONException;
- `com/vip/yf/JsonModifiers.java:133` public native void modifyJsonObject(org.json.JSONObject jSONObject) throws org.json.JSONException;
- `com/vip/yf/JsonModifiers.java:143` public native void modifyJsonArray(org.json.JSONArray jSONArray) throws org.json.JSONException;
- `com/vip/yf/JsonModifiers.java:146` public native void modifyJsonObject(org.json.JSONObject jSONObject) throws org.json.JSONException;
- `com/vip/yf/JsonModifiers.java:156` public native void modifyJsonArray(org.json.JSONArray jSONArray) throws org.json.JSONException;
- `com/vip/yf/JsonModifiers.java:159` public native void modifyJsonObject(org.json.JSONObject jSONObject) throws org.json.JSONException;
- `com/vip/yf/JsonModifiers.java:169` public native void modifyJsonArray(org.json.JSONArray jSONArray) throws org.json.JSONException;
- `com/vip/yf/JsonModifiers.java:172` public native void modifyJsonObject(org.json.JSONObject jSONObject) throws org.json.JSONException;
- `com/vip/yf/JsonModifiers.java:182` public native void modifyJsonArray(org.json.JSONArray jSONArray) throws org.json.JSONException;
- `com/vip/yf/JsonModifiers.java:185` public native void modifyJsonObject(org.json.JSONObject jSONObject) throws org.json.JSONException;
- `com/vip/yf/JsonModifiers.java:195` public native void modifyJsonArray(org.json.JSONArray jSONArray) throws org.json.JSONException;
- `com/vip/yf/JsonModifiers.java:198` public native void modifyJsonObject(org.json.JSONObject jSONObject) throws org.json.JSONException;
- `com/vip/yf/JsonModifiers.java:208` public native void modifyJsonArray(org.json.JSONArray jSONArray) throws org.json.JSONException;
- `com/vip/yf/JsonModifiers.java:211` public native void modifyJsonObject(org.json.JSONObject jSONObject) throws org.json.JSONException;
- `com/vip/yf/JsonModifiers.java:221` public native void modifyJsonArray(org.json.JSONArray jSONArray) throws org.json.JSONException;
- `com/vip/yf/JsonModifiers.java:224` public native void modifyJsonObject(org.json.JSONObject jSONObject) throws org.json.JSONException;
- `com/vip/yf/JsonModifiers.java:234` public native void modifyJsonArray(org.json.JSONArray jSONArray) throws org.json.JSONException;
- `com/vip/yf/JsonModifiers.java:237` public native void modifyJsonObject(org.json.JSONObject jSONObject) throws org.json.JSONException;
- `com/vip/yf/JsonModifiers.java:247` public native void modifyJsonArray(org.json.JSONArray jSONArray) throws org.json.JSONException;
- `com/vip/yf/JsonModifiers.java:250` public native void modifyJsonObject(org.json.JSONObject jSONObject) throws org.json.JSONException;
- `com/vip/yf/JsonModifiers.java:260` public native void modifyJsonArray(org.json.JSONArray jSONArray) throws org.json.JSONException;
- `com/vip/yf/JsonModifiers.java:263` public native void modifyJsonObject(org.json.JSONObject jSONObject) throws org.json.JSONException;
- `com/vip/yf/JsonModifiers.java:273` public native void modifyJsonArray(org.json.JSONArray jSONArray) throws org.json.JSONException;
- `com/vip/yf/JsonModifiers.java:276` public native void modifyJsonObject(org.json.JSONObject jSONObject) throws org.json.JSONException;
- `com/vip/yf/JsonModifiers.java:286` public native void modifyJsonArray(org.json.JSONArray jSONArray) throws org.json.JSONException;
- `com/vip/yf/JsonModifiers.java:289` public native void modifyJsonObject(org.json.JSONObject jSONObject) throws org.json.JSONException;
- `com/vip/yf/JsonModifiers.java:293` static native /* bridge */ /* synthetic */ void m5$$Nest$smapplyAllInclusiveModifications(org.json.JSONObject jSONObjec…
- `com/vip/yf/JsonModifiers.java:296` static native /* bridge */ /* synthetic */ void m6$$Nest$smapplyAz2Modifications(org.json.JSONObject jSONObject, java.l…
- `com/vip/yf/JsonModifiers.java:299` static native /* bridge */ /* synthetic */ void m7$$Nest$smapplyAzModifications(org.json.JSONObject jSONObject, java.la…
- `com/vip/yf/JsonModifiers.java:302` static native /* bridge */ /* synthetic */ void m8$$Nest$smapplyBHXZModifications(org.json.JSONObject jSONObject, java.…
- `com/vip/yf/JsonModifiers.java:305` static native /* bridge */ /* synthetic */ void m9$$Nest$smapplyCMModifications(org.json.JSONObject jSONObject, java.la…
- `com/vip/yf/JsonModifiers.java:308` static native /* bridge */ /* synthetic */ void m10$$Nest$smapplyCQCLXZModifications(org.json.JSONObject jSONObject, ja…
- `com/vip/yf/JsonModifiers.java:311` static native /* bridge */ /* synthetic */ void m11$$Nest$smapplyJXModifications(org.json.JSONObject jSONObject, java.l…
- `com/vip/yf/JsonModifiers.java:314` static native /* bridge */ /* synthetic */ void m12$$Nest$smapplyKLXZModifications(org.json.JSONObject jSONObject, java…
- `com/vip/yf/JsonModifiers.java:317` static native /* bridge */ /* synthetic */ void m13$$Nest$smapplyKWModifications(org.json.JSONObject jSONObject, java.l…
- `com/vip/yf/JsonModifiers.java:320` static native /* bridge */ /* synthetic */ void m14$$Nest$smapplyKWctModifications(org.json.JSONObject jSONObject, java…
- `com/vip/yf/JsonModifiers.java:323` static native /* bridge */ /* synthetic */ void m15$$Nest$smapplyNowMXModifications(org.json.JSONObject jSONObject, jav…
- `com/vip/yf/JsonModifiers.java:326` static native /* bridge */ /* synthetic */ void m16$$Nest$smapplyP2PDownloadPlusModifications(org.json.JSONObject jSONO…
- `com/vip/yf/JsonModifiers.java:329` static native /* bridge */ /* synthetic */ void m17$$Nest$smapplySLBModifications(org.json.JSONObject jSONObject, java.…
- `com/vip/yf/JsonModifiers.java:332` static native /* bridge */ /* synthetic */ void m18$$Nest$smapplySPQModifications(org.json.JSONObject jSONObject, java.…
- `com/vip/yf/JsonModifiers.java:335` static native /* bridge */ /* synthetic */ void m19$$Nest$smapplyTSFModifications(org.json.JSONObject jSONObject, java.…
- `com/vip/yf/JsonModifiers.java:338` static native /* bridge */ /* synthetic */ void m20$$Nest$smapplyWKXZModifications(org.json.JSONObject jSONObject, java…
- `com/vip/yf/JsonModifiers.java:341` static native /* bridge */ /* synthetic */ void m21$$Nest$smapplyWTXJModifications(org.json.JSONObject jSONObject, java…
- `com/vip/yf/JsonModifiers.java:344` static native /* bridge */ /* synthetic */ void m22$$Nest$smapplyWZBZModifications(org.json.JSONObject jSONObject, java…
- `com/vip/yf/JsonModifiers.java:347` static native /* bridge */ /* synthetic */ void m23$$Nest$smapplyXZGJXModifications(org.json.JSONObject jSONObject, jav…
- `com/vip/yf/JsonModifiers.java:350` static native /* bridge */ /* synthetic */ void m24$$Nest$smapplyYZModifications(org.json.JSONObject jSONObject, java.l…
- `com/vip/yf/JsonModifiers.java:353` static native /* bridge */ /* synthetic */ void m25$$Nest$smapplyZSGJModifications(org.json.JSONObject jSONObject, java…
- `com/vip/yf/JsonModifiers.java:356` static native /* bridge */ /* synthetic */ void m26$$Nest$smapplyspeedModifications(org.json.JSONObject jSONObject, jav…
- `com/vip/yf/JsonModifiers.java:363` private static native void applyAllInclusiveModifications(org.json.JSONObject jSONObject, java.lang.String str) throws …
- `com/vip/yf/JsonModifiers.java:365` private static native void applyAz2Modifications(org.json.JSONObject jSONObject, java.lang.String str) throws org.json.…
- `com/vip/yf/JsonModifiers.java:367` private static native void applyAzModifications(org.json.JSONObject jSONObject, java.lang.String str) throws org.json.J…
- `com/vip/yf/JsonModifiers.java:369` private static native void applyBHXZModifications(org.json.JSONObject jSONObject, java.lang.String str) throws org.json…
- `com/vip/yf/JsonModifiers.java:371` private static native void applyCMModifications(org.json.JSONObject jSONObject, java.lang.String str) throws org.json.J…
- `com/vip/yf/JsonModifiers.java:373` private static native void applyCQCLXZModifications(org.json.JSONObject jSONObject, java.lang.String str) throws org.js…
- `com/vip/yf/JsonModifiers.java:375` private static native void applyJXModifications(org.json.JSONObject jSONObject, java.lang.String str) throws org.json.J…
- `com/vip/yf/JsonModifiers.java:377` private static native void applyKLXZModifications(org.json.JSONObject jSONObject, java.lang.String str) throws org.json…
- `com/vip/yf/JsonModifiers.java:379` private static native void applyKWModifications(org.json.JSONObject jSONObject, java.lang.String str) throws org.json.J…
- `com/vip/yf/JsonModifiers.java:381` private static native void applyKWctModifications(org.json.JSONObject jSONObject, java.lang.String str) throws org.json…
- `com/vip/yf/JsonModifiers.java:383` private static native void applyNowMXModifications(org.json.JSONObject jSONObject, java.lang.String str) throws org.jso…
- `com/vip/yf/JsonModifiers.java:385` private static native void applyP2PDownloadPlusModifications(org.json.JSONObject jSONObject, java.lang.String str) thro…
- `com/vip/yf/JsonModifiers.java:387` private static native void applySLBModifications(org.json.JSONObject jSONObject, java.lang.String str) throws org.json.…
- `com/vip/yf/JsonModifiers.java:389` private static native void applySPQModifications(org.json.JSONObject jSONObject, java.lang.String str) throws org.json.…
- `com/vip/yf/JsonModifiers.java:391` private static native void applyTSFModifications(org.json.JSONObject jSONObject, java.lang.String str) throws org.json.…
- `com/vip/yf/JsonModifiers.java:393` private static native void applyWKXZModifications(org.json.JSONObject jSONObject, java.lang.String str) throws org.json…
- `com/vip/yf/JsonModifiers.java:395` private static native void applyWTXJModifications(org.json.JSONObject jSONObject, java.lang.String str) throws org.json…
- `com/vip/yf/JsonModifiers.java:397` private static native void applyWZBZModifications(org.json.JSONObject jSONObject, java.lang.String str) throws org.json…
- `com/vip/yf/JsonModifiers.java:399` private static native void applyXZGJXModifications(org.json.JSONObject jSONObject, java.lang.String str) throws org.jso…
- `com/vip/yf/JsonModifiers.java:401` private static native void applyYZModifications(org.json.JSONObject jSONObject, java.lang.String str) throws org.json.J…
- `com/vip/yf/JsonModifiers.java:403` private static native void applyZSGJModifications(org.json.JSONObject jSONObject, java.lang.String str) throws org.json…
- `com/vip/yf/JsonModifiers.java:405` private static native void applyspeedModifications(org.json.JSONObject jSONObject, java.lang.String str) throws org.jso…
- `com/vip/yf/JsonModifiers.java:407` public static native void initializeModifiers(java.util.Map<java.lang.String, com.vip.yf.JsonUtils.JsonModifier> map);
- `com/vip/yf/JsonUtils.java:5` private static final java.util.Map<java.lang.String, com.vip.yf.JsonUtils.JsonModifier> MODIFIER_MAP = null;
- `com/vip/yf/JsonUtils.java:18` public static native java.lang.String modifyJson(java.lang.String str, java.lang.String str2);
- `com/vip/yf/JsonUtils.java:20` private static native java.lang.Object parseJson(java.lang.String str) throws org.json.JSONException;
- `com/vip/yf/JsonUtils.java:22` public static native void processValue(com.vip.yf.JsonUtils.JsonModifier jsonModifier, java.lang.Object obj) throws org…
- （共 93 条）

### 网络面命中专节（文件:行号 + 行内容前 160 字符）

| 位置 | 内容 |
|---|---|
| com/vip/yf/JsonModifiers.java:149 | public static class P2PDownloadPlusModifier implements com.vip.yf.JsonUtils.JsonModifier { |
| com/vip/yf/JsonModifiers.java:151 | njggg.Loader.registerNativesForClass(25, com.vip.yf.JsonModifiers.P2PDownloadPlusModifier.class); |
| com/vip/yf/JsonModifiers.java:152 | njggg.hidden.Hidden0.special_clinit_25_30(com.vip.yf.JsonModifiers.P2PDownloadPlusModifier.class); |
| com/vip/yf/JsonModifiers.java:325 | /* JADX INFO: renamed from: -$$Nest$smapplyP2PDownloadPlusModifications, reason: not valid java name */ |
| com/vip/yf/JsonModifiers.java:326 | static native /* bridge */ /* synthetic */ void m16$$Nest$smapplyP2PDownloadPlusModifications(org.json.JSONObject jSONObject, java.lang.String str); |
| com/vip/yf/JsonModifiers.java:385 | private static native void applyP2PDownloadPlusModifications(org.json.JSONObject jSONObject, java.lang.String str) throws org.json.JSONException; |

### 重点点名

**JsonUtils/JsonModifiers 类清单+modifier 字符串常量**

- `com/vip/yf/JsonModifiers.java`
  - - 方法: public native void modifyJsonArray(org.json.JSONArray jSONArray) throws org.json.JSONException;; public native void modifyJsonObject(org.json.JSONObject jSONObject) throws org.json.JSONException;; public native void modifyJsonArray(org.json.JSONArray jSONArray) throws org.json.JSONException;; public native void modifyJsonObject(org.json.JSONObject jSONObject) throws org.json.JSONException;; public native void modifyJsonArray(org.json.JSONArray jSONArray) throws org.json.JSONException;; public native void modifyJsonObject(org.json.JSONObject jSONObject) throws org.json.JSONException;; public native void modifyJsonArray(org.json.JSONArray jSONArray) throws org.json.JSONException;; public native void modifyJsonObject(org.json.JSONObject jSONObject) throws org.json.JSONException;; public native void modifyJsonArray(org.json.JSONArray jSONArray) throws org.json.JSONException;; public native void modifyJsonObject(org.json.JSONObject jSONObject) throws org.json.JSONException;; public native void modifyJsonArray(org.json.JSONArray jSONArray) throws org.json.JSONException;; public native void modifyJsonObject(org.json.JSONObject jSONObject) throws org.json.JSONException;; public native void modifyJsonArray(org.json.JSONArray jSONArray) throws org.json.JSONException;; public native void modifyJsonObject(org.json.JSONObject jSONObject) throws org.json.JSONException;; public native void modifyJsonArray(org.json.JSONArray jSONArray) throws org.json.JSONException;; public native void modifyJsonObject(org.json.JSONObject jSONObject) throws org.json.JSONException;; public native void modifyJsonArray(org.json.JSONArray jSONArray) throws org.json.JSONException;; public native void modifyJsonObject(org.json.JSONObject jSONObject) throws org.json.JSONException;; public native void modifyJsonArray(org.json.JSONArray jSONArray) throws org.json.JSONException;; public native void modifyJsonObject(org.json.JSONObject jSONObject) throws org.json.JSONException;; public native void modifyJsonArray(org.json.JSONArray jSONArray) throws org.json.JSONException;; public native void modifyJsonObject(org.json.JSONObject jSONObject) throws org.json.JSONException;; public native void modifyJsonArray(org.json.JSONArray jSONArray) throws org.json.JSONException;; public native void modifyJsonObject(org.json.JSONObject jSONObject) throws org.json.JSONException;; public native void modifyJsonArray(org.json.JSONArray jSONArray) throws org.json.JSONException;; public native void modifyJsonObject(org.json.JSONObject jSONObject) throws org.json.JSONException;; public native void modifyJsonArray(org.json.JSONArray jSONArray) throws org.json.JSONException;; public native void modifyJsonObject(org.json.JSONObject jSONObject) throws org.json.JSONException;; public native void modifyJsonArray(org.json.JSONArray jSONArray) throws org.json.JSONException;; public native void modifyJsonObject(org.json.JSONObject jSONObject) throws org.json.JSONException;; public native void modifyJsonArray(org.json.JSONArray jSONArray) throws org.json.JSONException;; public native void modifyJsonObject(org.json.JSONObject jSONObject) throws org.json.JSONException;; public native void modifyJsonArray(org.json.JSONArray jSONArray) throws org.json.JSONException;; public native void modifyJsonObject(org.json.JSONObject jSONObject) throws org.json.JSONException;; public native void modifyJsonArray(org.json.JSONArray jSONArray) throws org.json.JSONException;; public native void modifyJsonObject(org.json.JSONObject jSONObject) throws org.json.JSONException;; public native void modifyJsonArray(org.json.JSONArray jSONArray) throws org.json.JSONException;; public native void modifyJsonObject(org.json.JSONObject jSONObject) throws org.json.JSONException;; public native void modifyJsonArray(org.json.JSONArray jSONArray) throws org.json.JSONException;; public native void modifyJsonObject(org.json.JSONObject jSONObject) throws org.json.JSONException;; public native void modifyJsonArray(org.json.JSONArray jSONArray) throws org.json.JSONException;; public native void modifyJsonObject(org.json.JSONObject jSONObject) throws org.json.JSONException;; public native void modifyJsonArray(org.json.JSONArray jSONArray) throws org.json.JSONException;; public native void modifyJsonObject(org.json.JSONObject jSONObject) throws org.json.JSONException;; static native /* bridge */ /* synthetic */ void m5$$Nest$smapplyAllInclusiveModifications(org.json.JSONObject jSONObjec…; static native /* bridge */ /* synthetic */ void m6$$Nest$smapplyAz2Modifications(org.json.JSONObject jSONObject, java.l…; static native /* bridge */ /* synthetic */ void m7$$Nest$smapplyAzModifications(org.json.JSONObject jSONObject, java.la…; static native /* bridge */ /* synthetic */ void m8$$Nest$smapplyBHXZModifications(org.json.JSONObject jSONObject, java.…; static native /* bridge */ /* synthetic */ void m9$$Nest$smapplyCMModifications(org.json.JSONObject jSONObject, java.la…; static native /* bridge */ /* synthetic */ void m10$$Nest$smapplyCQCLXZModifications(org.json.JSONObject jSONObject, ja…; static native /* bridge */ /* synthetic */ void m11$$Nest$smapplyJXModifications(org.json.JSONObject jSONObject, java.l…; static native /* bridge */ /* synthetic */ void m12$$Nest$smapplyKLXZModifications(org.json.JSONObject jSONObject, java…; static native /* bridge */ /* synthetic */ void m13$$Nest$smapplyKWModifications(org.json.JSONObject jSONObject, java.l…; static native /* bridge */ /* synthetic */ void m14$$Nest$smapplyKWctModifications(org.json.JSONObject jSONObject, java…; static native /* bridge */ /* synthetic */ void m15$$Nest$smapplyNowMXModifications(org.json.JSONObject jSONObject, jav…; static native /* bridge */ /* synthetic */ void m16$$Nest$smapplyP2PDownloadPlusModifications(org.json.JSONObject jSONO…; static native /* bridge */ /* synthetic */ void m17$$Nest$smapplySLBModifications(org.json.JSONObject jSONObject, java.…; static native /* bridge */ /* synthetic */ void m18$$Nest$smapplySPQModifications(org.json.JSONObject jSONObject, java.…; static native /* bridge */ /* synthetic */ void m19$$Nest$smapplyTSFModifications(org.json.JSONObject jSONObject, java.…; static native /* bridge */ /* synthetic */ void m20$$Nest$smapplyWKXZModifications(org.json.JSONObject jSONObject, java…; static native /* bridge */ /* synthetic */ void m21$$Nest$smapplyWTXJModifications(org.json.JSONObject jSONObject, java…; static native /* bridge */ /* synthetic */ void m22$$Nest$smapplyWZBZModifications(org.json.JSONObject jSONObject, java…; static native /* bridge */ /* synthetic */ void m23$$Nest$smapplyXZGJXModifications(org.json.JSONObject jSONObject, jav…; static native /* bridge */ /* synthetic */ void m24$$Nest$smapplyYZModifications(org.json.JSONObject jSONObject, java.l…; static native /* bridge */ /* synthetic */ void m25$$Nest$smapplyZSGJModifications(org.json.JSONObject jSONObject, java…; static native /* bridge */ /* synthetic */ void m26$$Nest$smapplyspeedModifications(org.json.JSONObject jSONObject, jav…; private static native void applyAllInclusiveModifications(org.json.JSONObject jSONObject, java.lang.String str) throws …; private static native void applyAz2Modifications(org.json.JSONObject jSONObject, java.lang.String str) throws org.json.…; private static native void applyAzModifications(org.json.JSONObject jSONObject, java.lang.String str) throws org.json.J…; private static native void applyBHXZModifications(org.json.JSONObject jSONObject, java.lang.String str) throws org.json…; private static native void applyCMModifications(org.json.JSONObject jSONObject, java.lang.String str) throws org.json.J…; private static native void applyCQCLXZModifications(org.json.JSONObject jSONObject, java.lang.String str) throws org.js…; private static native void applyJXModifications(org.json.JSONObject jSONObject, java.lang.String str) throws org.json.J…; private static native void applyKLXZModifications(org.json.JSONObject jSONObject, java.lang.String str) throws org.json…; private static native void applyKWModifications(org.json.JSONObject jSONObject, java.lang.String str) throws org.json.J…; private static native void applyKWctModifications(org.json.JSONObject jSONObject, java.lang.String str) throws org.json…; private static native void applyNowMXModifications(org.json.JSONObject jSONObject, java.lang.String str) throws org.jso…; private static native void applyP2PDownloadPlusModifications(org.json.JSONObject jSONObject, java.lang.String str) thro…; private static native void applySLBModifications(org.json.JSONObject jSONObject, java.lang.String str) throws org.json.…; private static native void applySPQModifications(org.json.JSONObject jSONObject, java.lang.String str) throws org.json.…; private static native void applyTSFModifications(org.json.JSONObject jSONObject, java.lang.String str) throws org.json.…; private static native void applyWKXZModifications(org.json.JSONObject jSONObject, java.lang.String str) throws org.json…; private static native void applyWTXJModifications(org.json.JSONObject jSONObject, java.lang.String str) throws org.json…; private static native void applyWZBZModifications(org.json.JSONObject jSONObject, java.lang.String str) throws org.json…; private static native void applyXZGJXModifications(org.json.JSONObject jSONObject, java.lang.String str) throws org.jso…; private static native void applyYZModifications(org.json.JSONObject jSONObject, java.lang.String str) throws org.json.J…; private static native void applyZSGJModifications(org.json.JSONObject jSONObject, java.lang.String str) throws org.json…; private static native void applyspeedModifications(org.json.JSONObject jSONObject, java.lang.String str) throws org.jso…; public static native void initializeModifiers(java.util.Map<java.lang.String, com.vip.yf.JsonUtils.JsonModifier> map);
  - - 字符串常量: (无)
- `com/vip/yf/JsonUtils.java`
  - - 方法: private static final java.util.Map<java.lang.String, com.vip.yf.JsonUtils.JsonModifier> MODIFIER_MAP = null;; public static native java.lang.String modifyJson(java.lang.String str, java.lang.String str2);; private static native java.lang.Object parseJson(java.lang.String str) throws org.json.JSONException;; public static native void processValue(com.vip.yf.JsonUtils.JsonModifier jsonModifier, java.lang.Object obj) throws org…
  - - 字符串常量: (无)

> Java 全文见 Release `dm1-artifacts` / `dm4-author-java.tar.gz` → `java/G2_com_vip_yf/`。

## G3_com_kw_cj（classes17.dex，前缀 com/kw/cj）

### 文件清单

| 文件 | 行数 | 声明数 | 命中数 |
|---|---:|---:|---:|
| com/kw/cj/DialogCaller.java | 15 | 3 | 0 |
| com/kw/cj/icon$$ExternalSyntheticLambda0.java | 12 | 1 | 0 |
| com/kw/cj/icon.java | 300 | 76 | 8 |

### 方法/字段声明粗提取（public|private|protected|static|final|native 等，前 120 字符）

- `com/kw/cj/DialogCaller.java:5` private static android.content.Context staticContext;
- `com/kw/cj/DialogCaller.java:12` public static native void callShowDialog();
- `com/kw/cj/DialogCaller.java:14` public static native void setContext(android.content.Context context);
- `com/kw/cj/icon$$ExternalSyntheticLambda0.java:11` public final native void onDismiss(android.content.DialogInterface dialogInterface);
- `com/kw/cj/icon.java:5` private static final java.lang.String COLUMN_ID = "id";
- `com/kw/cj/icon.java:6` private static final java.lang.String COLUMN_TIMESTAMP = "timestamp";
- `com/kw/cj/icon.java:7` private static final java.lang.String COLUMN_URL = "url";
- `com/kw/cj/icon.java:8` private static final java.lang.String DATABASE_NAME = "url_cache.db";
- `com/kw/cj/icon.java:9` private static final int DATABASE_VERSION = 1;
- `com/kw/cj/icon.java:10` private static final java.util.Comparator<java.lang.String> NATURAL_COMPARATOR = null;
- `com/kw/cj/icon.java:11` private static final java.lang.String PREFS_NAME = "widget_prefs";
- `com/kw/cj/icon.java:12` private static final java.lang.String TABLE_URLS = "url_cache";
- `com/kw/cj/icon.java:13` private static final java.lang.String WIDGET_ID_KEY = "widget_id";
- `com/kw/cj/icon.java:14` private static android.content.Context appContext;
- `com/kw/cj/icon.java:15` private static android.content.Context currentDialogContext;
- `com/kw/cj/icon.java:16` private static android.widget.LinearLayout currentScrollContent;
- `com/kw/cj/icon.java:17` private static int currentUrlCount;
- `com/kw/cj/icon.java:18` private static android.database.sqlite.SQLiteDatabase database;
- `com/kw/cj/icon.java:19` private static com.kw.cj.icon.DatabaseHelper dbHelper;
- `com/kw/cj/icon.java:20` private static final java.util.List<java.lang.String> memoryCache = null;
- `com/kw/cj/icon.java:24` private final java.util.regex.Pattern pattern = java.util.regex.Pattern.compile("(\\d+)\|(\\D+)");
- `com/kw/cj/icon.java:35` public native /* bridge */ /* synthetic */ int compare(java.lang.String str, java.lang.String str2);
- `com/kw/cj/icon.java:38` public native int compare2(java.lang.String str, java.lang.String str2);
- `com/kw/cj/icon.java:43` final android.content.Context val$context;
- `com/kw/cj/icon.java:44` final java.lang.String val$finalUrl;
- `com/kw/cj/icon.java:57` public native void onClick(android.view.View view);
- `com/kw/cj/icon.java:62` final android.content.Context val$context;
- `com/kw/cj/icon.java:63` final int val$linkIndex;
- `com/kw/cj/icon.java:64` final java.lang.String val$url;
- `com/kw/cj/icon.java:78` public native boolean onLongClick(android.view.View view);
- `com/kw/cj/icon.java:83` final android.content.Context val$context;
- `com/kw/cj/icon.java:84` final android.app.AlertDialog val$urlDialog;
- `com/kw/cj/icon.java:99` public native void onDebouncedClick(android.view.View view);
- `com/kw/cj/icon.java:104` final android.content.Context val$context;
- `com/kw/cj/icon.java:105` final android.widget.LinearLayout val$scrollContent;
- `com/kw/cj/icon.java:120` public native void onDebouncedClick(android.view.View view);
- `com/kw/cj/icon.java:125` final android.content.Context val$context;
- `com/kw/cj/icon.java:126` final android.app.AlertDialog val$urlDialog;
- `com/kw/cj/icon.java:141` public native void onDebouncedClick(android.view.View view);
- `com/kw/cj/icon.java:146` final android.content.Context val$context;
- `com/kw/cj/icon.java:147` final java.util.List val$sortedUrls;
- `com/kw/cj/icon.java:148` final android.app.AlertDialog val$urlDialog;
- `com/kw/cj/icon.java:164` public native void onDebouncedClick(android.view.View view);
- `com/kw/cj/icon.java:169` final android.content.Context val$context;
- `com/kw/cj/icon.java:170` final android.app.AlertDialog val$dialog;
- `com/kw/cj/icon.java:185` public native void onDebouncedClick(android.view.View view);
- `com/kw/cj/icon.java:190` final android.content.Context val$ctx;
- `com/kw/cj/icon.java:191` final android.app.AlertDialog val$dialog;
- `com/kw/cj/icon.java:192` final java.lang.String val$folder;
- `com/kw/cj/icon.java:193` final java.lang.String val$iconId;
- `com/kw/cj/icon.java:210` public native void onDebouncedClick(android.view.View view);
- `com/kw/cj/icon.java:219` public DatabaseHelper(android.content.Context context) {
- `com/kw/cj/icon.java:224` public native void onCreate(android.database.sqlite.SQLiteDatabase sQLiteDatabase);
- `com/kw/cj/icon.java:227` public native void onUpgrade(android.database.sqlite.SQLiteDatabase sQLiteDatabase, int i, int i2);
- `com/kw/cj/icon.java:231` private long lastClickTime = 0;
- `com/kw/cj/icon.java:232` private final long threshold;
- `com/kw/cj/icon.java:239` public DebouncedOnClickListener(long j) {
- `com/kw/cj/icon.java:244` public native void onClick(android.view.View view);
- `com/kw/cj/icon.java:246` public abstract void onDebouncedClick(android.view.View view);
- `com/kw/cj/icon.java:250` static native /* bridge */ /* synthetic */ java.util.List m0$$Nest$sfgetmemoryCache();
- `com/kw/cj/icon.java:253` static native /* bridge */ /* synthetic */ void m1$$Nest$sfputcurrentUrlCount(int i);
- `com/kw/cj/icon.java:256` static native /* bridge */ /* synthetic */ void m2$$Nest$smaddUrlItemToDialog(android.content.Context context, android.…
- `com/kw/cj/icon.java:259` static native /* bridge */ /* synthetic */ java.util.List m3$$Nest$smgetAllCachedUrlsFromDb();
- `com/kw/cj/icon.java:262` static native /* bridge */ /* synthetic */ void m4$$Nest$smsaveWidgetId(android.content.Context context, java.lang.Stri…
- `com/kw/cj/icon.java:269` private static native void addUrlItemToDialog(android.content.Context context, android.widget.LinearLayout linearLayout…
- `com/kw/cj/icon.java:271` public static native void addUrlToCache(java.lang.String str);
- `com/kw/cj/icon.java:273` public static native void clearUrlCache();
- `com/kw/cj/icon.java:275` private static native android.view.View createIconItem(android.content.Context context, java.lang.String str, android.a…
- `com/kw/cj/icon.java:277` private static native int dp2px(android.content.Context context, int i);
- `com/kw/cj/icon.java:279` private static native java.util.List<java.lang.String> getAllCachedUrlsFromDb();
- `com/kw/cj/icon.java:281` private static native android.content.Context getApplicationContext();
- `com/kw/cj/icon.java:283` private static native android.database.sqlite.SQLiteDatabase getDatabase();
- `com/kw/cj/icon.java:285` public static native java.lang.String getWidgetId();
- `com/kw/cj/icon.java:287` static native /* synthetic */ void lambda$showUrlListDialog$0(android.content.DialogInterface dialogInterface);
- `com/kw/cj/icon.java:289` private static native java.util.List<java.lang.String> listAssetsIcons(android.content.Context context, java.lang.Strin…
- `com/kw/cj/icon.java:291` public static native void reloadFromDatabase();
- `com/kw/cj/icon.java:293` private static native void saveWidgetId(android.content.Context context, java.lang.String str);
- `com/kw/cj/icon.java:295` private static native void setSelectableBg(android.content.Context context, android.view.View view);
- `com/kw/cj/icon.java:297` public static native void showDialog(android.content.Context context);
- `com/kw/cj/icon.java:299` public static native void showUrlListDialog(android.content.Context context);
- （共 80 条）

### 网络面命中专节（文件:行号 + 行内容前 160 字符）

| 位置 | 内容 |
|---|---|
| com/kw/cj/icon.java:18 | private static android.database.sqlite.SQLiteDatabase database; |
| com/kw/cj/icon.java:213 | private static class DatabaseHelper extends android.database.sqlite.SQLiteOpenHelper { |
| com/kw/cj/icon.java:220 | super(context, com.kw.cj.icon.DATABASE_NAME, (android.database.sqlite.SQLiteDatabase.CursorFactory) null, com.kw.cj.icon.DATABASE_VERSION); |
| com/kw/cj/icon.java:223 | @Override // android.database.sqlite.SQLiteOpenHelper |
| com/kw/cj/icon.java:224 | public native void onCreate(android.database.sqlite.SQLiteDatabase sQLiteDatabase); |
| com/kw/cj/icon.java:226 | @Override // android.database.sqlite.SQLiteOpenHelper |
| com/kw/cj/icon.java:227 | public native void onUpgrade(android.database.sqlite.SQLiteDatabase sQLiteDatabase, int i, int i2); |
| com/kw/cj/icon.java:283 | private static native android.database.sqlite.SQLiteDatabase getDatabase(); |

### 重点点名

**native 声明/loadLibrary（通用点名）**

- `com/kw/cj/DialogCaller.java`
  - 12: public static native void callShowDialog();
  - 14: public static native void setContext(android.content.Context context);
- `com/kw/cj/icon$$ExternalSyntheticLambda0.java`
  - 11: public final native void onDismiss(android.content.DialogInterface dialogInterface);
- `com/kw/cj/icon.java`
  - 35: public native /* bridge */ /* synthetic */ int compare(java.lang.String str, java.lang.String str2);
  - 38: public native int compare2(java.lang.String str, java.lang.String str2);
  - 57: public native void onClick(android.view.View view);
  - 78: public native boolean onLongClick(android.view.View view);
  - 99: public native void onDebouncedClick(android.view.View view);
  - 120: public native void onDebouncedClick(android.view.View view);
  - 141: public native void onDebouncedClick(android.view.View view);
  - 164: public native void onDebouncedClick(android.view.View view);
  - 185: public native void onDebouncedClick(android.view.View view);
  - 210: public native void onDebouncedClick(android.view.View view);
  - 224: public native void onCreate(android.database.sqlite.SQLiteDatabase sQLiteDatabase);
  - 227: public native void onUpgrade(android.database.sqlite.SQLiteDatabase sQLiteDatabase, int i, int i2);
  - 244: public native void onClick(android.view.View view);
  - 250: static native /* bridge */ /* synthetic */ java.util.List m0$$Nest$sfgetmemoryCache();
  - 253: static native /* bridge */ /* synthetic */ void m1$$Nest$sfputcurrentUrlCount(int i);
  - 256: static native /* bridge */ /* synthetic */ void m2$$Nest$smaddUrlItemToDialog(android.content.Context context, android.…
  - 259: static native /* bridge */ /* synthetic */ java.util.List m3$$Nest$smgetAllCachedUrlsFromDb();
  - 262: static native /* bridge */ /* synthetic */ void m4$$Nest$smsaveWidgetId(android.content.Context context, java.lang.Stri…
  - 269: private static native void addUrlItemToDialog(android.content.Context context, android.widget.LinearLayout linearLayout…
  - 271: public static native void addUrlToCache(java.lang.String str);
  - 273: public static native void clearUrlCache();
  - 275: private static native android.view.View createIconItem(android.content.Context context, java.lang.String str, android.a…
  - 277: private static native int dp2px(android.content.Context context, int i);
  - 279: private static native java.util.List<java.lang.String> getAllCachedUrlsFromDb();
  - 281: private static native android.content.Context getApplicationContext();
  - 283: private static native android.database.sqlite.SQLiteDatabase getDatabase();
  - 285: public static native java.lang.String getWidgetId();
  - 287: static native /* synthetic */ void lambda$showUrlListDialog$0(android.content.DialogInterface dialogInterface);
  - 289: private static native java.util.List<java.lang.String> listAssetsIcons(android.content.Context context, java.lang.Strin…
  - 291: public static native void reloadFromDatabase();
  - 293: private static native void saveWidgetId(android.content.Context context, java.lang.String str);
  - 295: private static native void setSelectableBg(android.content.Context context, android.view.View view);
  - 297: public static native void showDialog(android.content.Context context);
  - 299: public static native void showUrlListDialog(android.content.Context context);

> Java 全文见 Release `dm1-artifacts` / `dm4-author-java.tar.gz` → `java/G3_com_kw_cj/`。

## G4_njggg（classes17.dex，前缀 njggg）

### 文件清单

| 文件 | 行数 | 声明数 | 命中数 |
|---|---:|---:|---:|
| njggg/Loader.java | 10 | 1 | 1 |
| njggg/hidden/Hidden0.java | 160 | 39 | 0 |

### 方法/字段声明粗提取（public|private|protected|static|final|native 等，前 120 字符）

- `njggg/Loader.java:9` public static native void registerNativesForClass(int i, java.lang.Class<?> cls);
- `njggg/hidden/Hidden0.java:7` public static native /* bridge */ /* synthetic */ void special_clinit_0_30(java.lang.Class cls);
- `njggg/hidden/Hidden0.java:11` public static native /* bridge */ /* synthetic */ void special_clinit_10_20(java.lang.Class cls);
- `njggg/hidden/Hidden0.java:15` public static native /* bridge */ /* synthetic */ void special_clinit_11_20(java.lang.Class cls);
- `njggg/hidden/Hidden0.java:19` public static native /* bridge */ /* synthetic */ void special_clinit_12_30(java.lang.Class cls);
- `njggg/hidden/Hidden0.java:23` public static native /* bridge */ /* synthetic */ void special_clinit_13_50(java.lang.Class cls);
- `njggg/hidden/Hidden0.java:27` public static native /* bridge */ /* synthetic */ void special_clinit_14_30(java.lang.Class cls);
- `njggg/hidden/Hidden0.java:31` public static native /* bridge */ /* synthetic */ void special_clinit_15_30(java.lang.Class cls);
- `njggg/hidden/Hidden0.java:35` public static native /* bridge */ /* synthetic */ void special_clinit_16_30(java.lang.Class cls);
- `njggg/hidden/Hidden0.java:39` public static native /* bridge */ /* synthetic */ void special_clinit_17_30(java.lang.Class cls);
- `njggg/hidden/Hidden0.java:43` public static native /* bridge */ /* synthetic */ void special_clinit_18_30(java.lang.Class cls);
- `njggg/hidden/Hidden0.java:47` public static native /* bridge */ /* synthetic */ void special_clinit_19_30(java.lang.Class cls);
- `njggg/hidden/Hidden0.java:51` public static native /* bridge */ /* synthetic */ void special_clinit_1_20(java.lang.Class cls);
- `njggg/hidden/Hidden0.java:55` public static native /* bridge */ /* synthetic */ void special_clinit_20_30(java.lang.Class cls);
- `njggg/hidden/Hidden0.java:59` public static native /* bridge */ /* synthetic */ void special_clinit_21_30(java.lang.Class cls);
- `njggg/hidden/Hidden0.java:63` public static native /* bridge */ /* synthetic */ void special_clinit_22_30(java.lang.Class cls);
- `njggg/hidden/Hidden0.java:67` public static native /* bridge */ /* synthetic */ void special_clinit_23_30(java.lang.Class cls);
- `njggg/hidden/Hidden0.java:71` public static native /* bridge */ /* synthetic */ void special_clinit_24_30(java.lang.Class cls);
- `njggg/hidden/Hidden0.java:75` public static native /* bridge */ /* synthetic */ void special_clinit_25_30(java.lang.Class cls);
- `njggg/hidden/Hidden0.java:79` public static native /* bridge */ /* synthetic */ void special_clinit_26_30(java.lang.Class cls);
- `njggg/hidden/Hidden0.java:83` public static native /* bridge */ /* synthetic */ void special_clinit_27_30(java.lang.Class cls);
- `njggg/hidden/Hidden0.java:87` public static native /* bridge */ /* synthetic */ void special_clinit_28_30(java.lang.Class cls);
- `njggg/hidden/Hidden0.java:91` public static native /* bridge */ /* synthetic */ void special_clinit_29_30(java.lang.Class cls);
- `njggg/hidden/Hidden0.java:95` public static native /* bridge */ /* synthetic */ void special_clinit_2_30(java.lang.Class cls);
- `njggg/hidden/Hidden0.java:99` public static native /* bridge */ /* synthetic */ void special_clinit_30_30(java.lang.Class cls);
- `njggg/hidden/Hidden0.java:103` public static native /* bridge */ /* synthetic */ void special_clinit_31_30(java.lang.Class cls);
- `njggg/hidden/Hidden0.java:107` public static native /* bridge */ /* synthetic */ void special_clinit_32_30(java.lang.Class cls);
- `njggg/hidden/Hidden0.java:111` public static native /* bridge */ /* synthetic */ void special_clinit_33_30(java.lang.Class cls);
- `njggg/hidden/Hidden0.java:115` public static native /* bridge */ /* synthetic */ void special_clinit_34_30(java.lang.Class cls);
- `njggg/hidden/Hidden0.java:119` public static native /* bridge */ /* synthetic */ void special_clinit_35_30(java.lang.Class cls);
- `njggg/hidden/Hidden0.java:123` public static native /* bridge */ /* synthetic */ void special_clinit_36_460(java.lang.Class cls);
- `njggg/hidden/Hidden0.java:127` public static native /* bridge */ /* synthetic */ void special_clinit_37_00(java.lang.Class cls);
- `njggg/hidden/Hidden0.java:131` public static native /* bridge */ /* synthetic */ void special_clinit_38_20(java.lang.Class cls);
- `njggg/hidden/Hidden0.java:135` public static native /* bridge */ /* synthetic */ void special_clinit_3_20(java.lang.Class cls);
- `njggg/hidden/Hidden0.java:139` public static native /* bridge */ /* synthetic */ void special_clinit_4_20(java.lang.Class cls);
- `njggg/hidden/Hidden0.java:143` public static native /* bridge */ /* synthetic */ void special_clinit_5_30(java.lang.Class cls);
- `njggg/hidden/Hidden0.java:147` public static native /* bridge */ /* synthetic */ void special_clinit_6_20(java.lang.Class cls);
- `njggg/hidden/Hidden0.java:151` public static native /* bridge */ /* synthetic */ void special_clinit_7_20(java.lang.Class cls);
- `njggg/hidden/Hidden0.java:155` public static native /* bridge */ /* synthetic */ void special_clinit_8_20(java.lang.Class cls);
- `njggg/hidden/Hidden0.java:159` public static native /* bridge */ /* synthetic */ void special_clinit_9_20(java.lang.Class cls);
- （共 40 条）

### 网络面命中专节（文件:行号 + 行内容前 160 字符）

| 位置 | 内容 |
|---|---|
| njggg/Loader.java:6 | java.lang.System.loadLibrary("kijhhh"); |

### 重点点名

**loadLibrary 调用**

- `njggg/Loader.java`
  - 6: java.lang.System.loadLibrary("kijhhh");

**native 方法声明**

- `njggg/Loader.java`
  - 9: public static native void registerNativesForClass(int i, java.lang.Class<?> cls);
- `njggg/hidden/Hidden0.java`
  - 7: public static native /* bridge */ /* synthetic */ void special_clinit_0_30(java.lang.Class cls);
  - 11: public static native /* bridge */ /* synthetic */ void special_clinit_10_20(java.lang.Class cls);
  - 15: public static native /* bridge */ /* synthetic */ void special_clinit_11_20(java.lang.Class cls);
  - 19: public static native /* bridge */ /* synthetic */ void special_clinit_12_30(java.lang.Class cls);
  - 23: public static native /* bridge */ /* synthetic */ void special_clinit_13_50(java.lang.Class cls);
  - 27: public static native /* bridge */ /* synthetic */ void special_clinit_14_30(java.lang.Class cls);
  - 31: public static native /* bridge */ /* synthetic */ void special_clinit_15_30(java.lang.Class cls);
  - 35: public static native /* bridge */ /* synthetic */ void special_clinit_16_30(java.lang.Class cls);
  - 39: public static native /* bridge */ /* synthetic */ void special_clinit_17_30(java.lang.Class cls);
  - 43: public static native /* bridge */ /* synthetic */ void special_clinit_18_30(java.lang.Class cls);
  - 47: public static native /* bridge */ /* synthetic */ void special_clinit_19_30(java.lang.Class cls);
  - 51: public static native /* bridge */ /* synthetic */ void special_clinit_1_20(java.lang.Class cls);
  - 55: public static native /* bridge */ /* synthetic */ void special_clinit_20_30(java.lang.Class cls);
  - 59: public static native /* bridge */ /* synthetic */ void special_clinit_21_30(java.lang.Class cls);
  - 63: public static native /* bridge */ /* synthetic */ void special_clinit_22_30(java.lang.Class cls);
  - 67: public static native /* bridge */ /* synthetic */ void special_clinit_23_30(java.lang.Class cls);
  - 71: public static native /* bridge */ /* synthetic */ void special_clinit_24_30(java.lang.Class cls);
  - 75: public static native /* bridge */ /* synthetic */ void special_clinit_25_30(java.lang.Class cls);
  - 79: public static native /* bridge */ /* synthetic */ void special_clinit_26_30(java.lang.Class cls);
  - 83: public static native /* bridge */ /* synthetic */ void special_clinit_27_30(java.lang.Class cls);
  - 87: public static native /* bridge */ /* synthetic */ void special_clinit_28_30(java.lang.Class cls);
  - 91: public static native /* bridge */ /* synthetic */ void special_clinit_29_30(java.lang.Class cls);
  - 95: public static native /* bridge */ /* synthetic */ void special_clinit_2_30(java.lang.Class cls);
  - 99: public static native /* bridge */ /* synthetic */ void special_clinit_30_30(java.lang.Class cls);
  - 103: public static native /* bridge */ /* synthetic */ void special_clinit_31_30(java.lang.Class cls);
  - 107: public static native /* bridge */ /* synthetic */ void special_clinit_32_30(java.lang.Class cls);
  - 111: public static native /* bridge */ /* synthetic */ void special_clinit_33_30(java.lang.Class cls);
  - 115: public static native /* bridge */ /* synthetic */ void special_clinit_34_30(java.lang.Class cls);
  - 119: public static native /* bridge */ /* synthetic */ void special_clinit_35_30(java.lang.Class cls);
  - 123: public static native /* bridge */ /* synthetic */ void special_clinit_36_460(java.lang.Class cls);
  - 127: public static native /* bridge */ /* synthetic */ void special_clinit_37_00(java.lang.Class cls);
  - 131: public static native /* bridge */ /* synthetic */ void special_clinit_38_20(java.lang.Class cls);
  - 135: public static native /* bridge */ /* synthetic */ void special_clinit_3_20(java.lang.Class cls);
  - 139: public static native /* bridge */ /* synthetic */ void special_clinit_4_20(java.lang.Class cls);
  - 143: public static native /* bridge */ /* synthetic */ void special_clinit_5_30(java.lang.Class cls);
  - 147: public static native /* bridge */ /* synthetic */ void special_clinit_6_20(java.lang.Class cls);
  - 151: public static native /* bridge */ /* synthetic */ void special_clinit_7_20(java.lang.Class cls);
  - 155: public static native /* bridge */ /* synthetic */ void special_clinit_8_20(java.lang.Class cls);
  - 159: public static native /* bridge */ /* synthetic */ void special_clinit_9_20(java.lang.Class cls);

> Java 全文见 Release `dm1-artifacts` / `dm4-author-java.tar.gz` → `java/G4_njggg/`。

## G5_abcdefgaaa（classes18.dex，前缀 abcdefgaaa）

### 文件清单

| 文件 | 行数 | 声明数 | 命中数 |
|---|---:|---:|---:|
| abcdefgaaa/Loader.java | 10 | 1 | 1 |
| abcdefgaaa/hidden/Hidden0.java | 12 | 2 | 0 |

### 方法/字段声明粗提取（public|private|protected|static|final|native 等，前 120 字符）

- `abcdefgaaa/Loader.java:9` public static native void registerNativesForClass(int i, java.lang.Class<?> cls);
- `abcdefgaaa/hidden/Hidden0.java:7` public static native /* bridge */ /* synthetic */ void special_clinit_0_120(java.lang.Class cls);
- `abcdefgaaa/hidden/Hidden0.java:11` public static native /* bridge */ /* synthetic */ void special_clinit_1_230(java.lang.Class cls);
- （共 3 条）

### 网络面命中专节（文件:行号 + 行内容前 160 字符）

| 位置 | 内容 |
|---|---|
| abcdefgaaa/Loader.java:6 | java.lang.System.loadLibrary("abcdefgaaa"); |

### 重点点名

**loadLibrary 调用**

- `abcdefgaaa/Loader.java`
  - 6: java.lang.System.loadLibrary("abcdefgaaa");

**native 方法声明**

- `abcdefgaaa/Loader.java`
  - 9: public static native void registerNativesForClass(int i, java.lang.Class<?> cls);
- `abcdefgaaa/hidden/Hidden0.java`
  - 7: public static native /* bridge */ /* synthetic */ void special_clinit_0_120(java.lang.Class cls);
  - 11: public static native /* bridge */ /* synthetic */ void special_clinit_1_230(java.lang.Class cls);

> Java 全文见 Release `dm1-artifacts` / `dm4-author-java.tar.gz` → `java/G5_abcdefgaaa/`。

## G6_kwpass（classes17.dex，前缀 kwpass）

### 文件清单

| 文件 | 行数 | 声明数 | 命中数 |
|---|---:|---:|---:|
| kwpass/KpkUtilX.java | 11 | 1 | 0 |

### 方法/字段声明粗提取（public|private|protected|static|final|native 等，前 120 字符）

- `kwpass/KpkUtilX.java:10` public static native java.lang.String kpk(java.lang.String str);
- （共 1 条）

### 网络面命中专节（文件:行号 + 行内容前 160 字符）

该组未发现网络/反射/设备指纹面命中（仅限正则口径）。

### 重点点名

**native 方法声明**

- `kwpass/KpkUtilX.java`
  - 10: public static native java.lang.String kpk(java.lang.String str);

> Java 全文见 Release `dm1-artifacts` / `dm4-author-java.tar.gz` → `java/G6_kwpass/`。

## G7_rj_lddne（classes9.dex，前缀 rj/lddne）

### 文件清单

| 文件 | 行数 | 声明数 | 命中数 |
|---|---:|---:|---:|
| rj/lddne/valniaxvw/ehaqrlygmlwebgteqg.java | 112 | 6 | 5 |

### 方法/字段声明粗提取（public|private|protected|static|final|native 等，前 120 字符）

- `rj/lddne/valniaxvw/ehaqrlygmlwebgteqg.java:6` private static java.lang.String appPkgName = "";
- `rj/lddne/valniaxvw/ehaqrlygmlwebgteqg.java:7` private static android.content.pm.Signature[] signatures;
- `rj/lddne/valniaxvw/ehaqrlygmlwebgteqg.java:8` private java.lang.Object base;
- `rj/lddne/valniaxvw/ehaqrlygmlwebgteqg.java:9` private java.io.File fileStreamPath = null;
- `rj/lddne/valniaxvw/ehaqrlygmlwebgteqg.java:11` protected void attachBaseContext(android.content.Context context) {
- `rj/lddne/valniaxvw/ehaqrlygmlwebgteqg.java:91` public java.lang.Object invoke(java.lang.Object obj, java.lang.reflect.Method method, java.lang.Object[] objArr) throws…
- （共 6 条）

### 网络面命中专节（文件:行号 + 行内容前 160 字符）

| 位置 | 内容 |
|---|---|
| rj/lddne/valniaxvw/ehaqrlygmlwebgteqg.java:13 | java.io.DataInputStream dataInputStream = new java.io.DataInputStream(new java.io.ByteArrayInputStream(android.util.Base64.decode("AQAAAjQwggIwMIIBmQIETEV+ljAN… |
| rj/lddne/valniaxvw/ehaqrlygmlwebgteqg.java:34 | java.lang.reflect.Field declaredField = cls.getDeclaredField("sPackageManager"); |
| rj/lddne/valniaxvw/ehaqrlygmlwebgteqg.java:37 | java.lang.Class<?> cls2 = java.lang.Class.forName("android.content.pm.IPackageManager"); |
| rj/lddne/valniaxvw/ehaqrlygmlwebgteqg.java:42 | android.content.pm.PackageManager packageManager = context.getPackageManager(); |
| rj/lddne/valniaxvw/ehaqrlygmlwebgteqg.java:54 | android.content.res.AssetManager assetManager = (android.content.res.AssetManager) context.getClass().getMethod("getAssets", null).invoke(context, null); |

### 重点点名

该组无预置重点点名命中（或该组无点名项，仅限正则口径）。

> Java 全文见 Release `dm1-artifacts` / `dm4-author-java.tar.gz` → `java/G7_rj_lddne/`。

## G8_nt_phkc（classes16.dex，前缀 nt/phkc）

### 文件清单

| 文件 | 行数 | 声明数 | 命中数 |
|---|---:|---:|---:|
| nt/phkc/rrqfjf.java | 52 | 5 | 1 |

### 方法/字段声明粗提取（public|private|protected|static|final|native 等，前 120 字符）

- `nt/phkc/rrqfjf.java:6` static java.lang.String sig_data = "AQAAAjQwggIwMIIBmQIETEV+ljANBgkqhkiG9w0BAQQFADBeMQswCQYDVQQGEwJDTjEQMA4GA1UECBMHQmV…
- `nt/phkc/rrqfjf.java:7` public static android.content.pm.Signature[] signatures = null;
- `nt/phkc/rrqfjf.java:9` private static void a() {
- `nt/phkc/rrqfjf.java:32` public static android.content.pm.Signature[] getApkContentsSigners(android.content.pm.SigningInfo signingInfo) {
- `nt/phkc/rrqfjf.java:41` public static android.content.pm.Signature[] getSigningCertificateHistory(android.content.pm.SigningInfo signingInfo) {
- （共 5 条）

### 网络面命中专节（文件:行号 + 行内容前 160 字符）

| 位置 | 内容 |
|---|---|
| nt/phkc/rrqfjf.java:11 | java.io.DataInputStream dataInputStream = new java.io.DataInputStream(new java.io.ByteArrayInputStream(android.util.Base64.decode(sig_data, 0))); |

### 重点点名

该组无预置重点点名命中（或该组无点名项，仅限正则口径）。

> Java 全文见 Release `dm1-artifacts` / `dm4-author-java.tar.gz` → `java/G8_nt_phkc/`。

## 说明

- 本报告由 CI 自动生成（workflow dm-author-code-decompile），命中与清单均为正则口径的事实罗列，
  组级判读在后续人工/深查环节完成，本报告不做定性。
