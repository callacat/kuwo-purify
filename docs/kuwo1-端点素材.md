# KUWO-1 端点素材（mod 全 dex URL 常量集 − 官方基线 URL 常量集）

> 集合口径红线：双侧同为全量 classes*.dex 反编译后 const-string 提取，同 regex 同过滤。
> 本表只是素材清单，定性判定权在老马。

## 1. 差集总览

- mod URL 常量: 2079 处 / 去重 1071 个
- base URL 常量: 2133 处 / 去重 1072 个
- **新增 URL（mod 有 base 无）: 0 个**（非官方域 0 + 官方域 0）
- 基线 URL 在 mod 消失: 47 个
- **新增裸域名（非 URL 字符串）: 0 个**（非官方 0）

## 2. 新增 URL —— 非官方域嫌疑区（重点素材）

| URL | 引用类 |
|---|---|

## 3. 新增 URL —— 官方域（信息项）


## 4. 新增裸域名 —— 非官方域（重点素材）


## 5. 基线 URL 在 mod 中消失清单（信息项）

- `http://artistfeeds.tencentmusic.com`
- `http://artistpicserver.kuwo.cn/pic.web?type=ugc_artist_pic&`
- `http://artistpicserver.kuwo.cn/sscrn.s?`
- `http://dataplan.kuwo.cn/mobileflow/flow/domain`
- `http://down.shouji.kuwo.cn/star/mobile/kwplayer_ar_vr.apk`
- `http://jx.kuwo.cn/kuwolive/jsp/alone/store/index.jsp?`
- `http://kwmatch.kuwo.cn/music_match?`
- `http://m.kuwo.cn/static/page/newuser/newusersonglist.html?d=`
- `http://mlyric.kuwo.cn/mobi.s?f=kuwo&q=`
- `http://mobi.kuwo.cn/mobi.s?f=kuwo&q=`
- `http://mobi.tencentmusic.com`
- `http://mobile.kuwo.cn/mpage/shouji/xchelp/index_help.html`
- `http://mobile.kuwo.cn/mpage/sjfk`
- `http://mobilebasedata.kuwo.cn/basedata.s?type=get_album_mc_list&albumid=`
- `http://mobileinterfaces.kuwo.cn/er.s?type=get_cache_times&f=web`
- `http://mobileinterfaces.kuwo.cn/er.s?type=get_slbq_list&f=web&qq-pf-to=pcqq.temporaryc2c`
- `http://musicpay.kuwo.cn/music.pay?`
- `http://ncomment.kuwo.cn/com.s?type=get_comment_num&f=web&digest=15&aapiver=1&sid=`
- `http://nmobi.kuwo.cn/mobi.s?f=kuwo&q=`
- `http://nmsearch.kuwo.cn/mobi.s?f=kuwo&q=`
- `http://nmsublist.kuwo.cn/mobi.s?f=kuwo&q=`
- `http://proxy.kuwo.cn/replace?`
- `http://rich.kuwo.cn/ecomresourceserver/authoronline/isonline?`
- `http://vip1.kuwo.cn`
- `http://vip1.kuwo.cn/vip/v2/user/vip?op=gvsi&uid=`
- `http://wapi.kuwo.cn/feedback.s?cmd=feedback&`
- `http://wapi.kuwo.cn/openapi/v1/radio/listenbar/getradiotypelist?`
- `http://wapi.tencentmusic.com`
- `http://www.kuwo.cn`
- `http://xcstat.kuwo.cn`
- `https://abt-kuwo.tencentmusic.com/kuwo/ui/info?`
- `https://baby.kuwo.cn/payment/api/advert/native/cloumn?`
- `https://beian.miit.gov.cn`
- `https://h5app.kuwo.cn/3000021/staralliance.html?passid=`
- `https://h5app.kuwo.cn/m/dolbyintro/index.html?module_ids=73781`
- `https://h5app.kuwo.cn/pay/canplayvippackage/index.html?packageid=`
- `https://h5app.kuwo.cn/pay/ultrahighquality/index.html`
- `https://imagexc.kuwo.cn`
- `https://m.kuwo.cn/newh5/cd/index#`
- `https://privacy.qq.com/document/preview/0b0dc16a0f004a35b77b7fd48a0b125b`
- `https://search.kuwo.cn/r.s?`
- `https://treehole.tencentmusic.com/tmp-sign-url?appid=x2fjyqpzt0`
- `https://treehole.tencentmusic.com/video-info?appid=x2fjyqpzt0`
- `https://vip1.kuwo.cn/vip_html/digitalarea/72/02/57202.html?mbox_webclose=1&dark=2&sharebtn=1`
- `https://y.qq.com/forest/akqav5oruelxz3s-/index.html`
- `https://y.tencentmusic.com/h5/reg_search_bar?platformtoken=`
- `https://y.tencentmusic.com/h5/register?platformtoken=`

## 6. 头号嫌疑 api.ktvdaren.com 引用上下文（老马初扫 2 次命中）

### `classes8/nb/i.smali` L305
```smali
    .line 1
    new-instance v0, Ljava/util/ArrayList;

    invoke-direct {v0}, Ljava/util/ArrayList;-><init>()V

    .line 2
    new-instance v1, Ljava/lang/StringBuilder;

    const-string v2, "http://api.ktvdaren.com/hot?appid="

    invoke-direct {v1, v2}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    const-string v2, "72980E5609254C1585A4F915925515E4"

    .line 3
    invoke-virtual {v1, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;
```

### `classes8/nb/i.smali` L350
```smali
.end method

.method private static h(Ljava/lang/String;I)Ljava/lang/String;
    .registers 4

    .line 1
    new-instance v0, Ljava/lang/StringBuilder;

    const-string v1, "http://api.ktvdaren.com/search?appid="

    invoke-direct {v0, v1}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    :try_start_7
    const-string v1, "72980E5609254C1585A4F915925515E4"

    .line 2
    invoke-virtual {v0, v1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;
```

