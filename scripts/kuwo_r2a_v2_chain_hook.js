/*
 * KUWO-R2a v2：「QQ频道：新时代，天天免费」注入链精确 hook（老马静态实锤链头版）
 * 链路（归档 changed/EntryActivity.smali 静态实锤，EntryActivity 内 3480 处混淆 invoke）：
 *   EntryActivity.onResume/onStart（mod 改写，每次启动/回前台必跑）
 *     → 4 个解密器 [SIII)Ljava/lang/String;（返回值=弹窗文案明文本体）
 *     → 分发器 (Ljava/lang/Object;)I 族（sparse-switch 写缓存/计数）
 *     → specialinfo 单例字段 → 官方 bubble/Dialog 渲染端消费
 * hook 点位（老马 R2a 补充）：
 *   ① EntryActivity.onResume/onStart 入口打印（链路触发确认）
 *   ② 4 解密器返回值（「QQ频道：新时代，天天免费」在此出明文）——类名 \u06XX 转义防传输损坏
 *   ③ 分发器 (Object)I 入参/调用计数（前 8 个类命中打样例）
 *   ④ 辅助：specialinfo/vipnew 字段快照（onResume 触发后 dump 一次）
 * 输出：/tmp/kw-frida.log（Python 驱动落盘）；命中上限 60 防刷屏；单 hook try/catch 可重跑
 */
'use strict';

var HITS_LIMIT = 60;
var hits = 0;
var DUMPED = false;

function ts() { return new Date().toISOString().slice(11, 23); }
function log(tag, msg) {
    // send() 为主通道（驱动落盘），console.log 兜底（frida CLI 直跑可见）
    var line = '[' + ts() + '][' + tag + '] ' + msg;
    try { send(line); } catch (e) { /* gated 阶段可能无通道 */ }
    console.log(line);
}

function safeStack() {
    try {
        var st = Java.use('java.lang.Thread').currentThread().getStackTrace();
        var out = [];
        for (var i = 0; i < st.length && i < 22; i++) out.push('    at ' + st[i]);
        return out.join('\n');
    } catch (e) { return '    <stack unavailable: ' + e + '>'; }
}

function budget(tag) {
    if (hits >= HITS_LIMIT) return false;
    hits++;
    if (hits === HITS_LIMIT) log(tag, '!! 命中上限 ' + HITS_LIMIT + '，后续静默（脚本仍运行）');
    return true;
}

// 4 解密器精确类名/方法名（\u06XX 转义，来源=归档 changed/EntryActivity.smali invoke 实测）
var DECRYPTORS = [
    'cn/kuwo/peculiar/specialinfo/\\u06df\\u06e4\\u06e4\\u06e8\\u06df|\\u06e0\\u06e8\\u06e8\\u06df([SIII)Ljava/lang/String;',
    'tian0/\\u06df\\u06e5\\u06e0\\u06e3\\u06e4|\\u06df\\u06e1\\u06df\\u06df([SIII)Ljava/lang/String;',
    'tian0/\\u06df\\u06e1\\u06e4\\u06e3\\u06e2|\\u06e8\\u06e7\\u06e8\\u06e1([SIII)Ljava/lang/String;',
    'cn/kuwo/base/bean/vipnew/\\u06df\\u06e3\\u06e3\\u06e3\\u06e3|\\u06df\\u06e5\\u06e0\\u06e8\\u06e6([SIII)Ljava/lang/String;'
];
// 分发器 (Object)I 前置类（打样例用）
var DISPATCHERS = [
    'tian0/\\u06df\\u06e5\\u06e0\\u06e3\\u06e4|\\u06e2\\u06e8\\u06e1\\u06e0(Ljava/lang/Object;)I',
    'cn/kuwo/base/bean/vipnew/\\u06df\\u06e3\\u06e3\\u06e3\\u06e3|\\u06df\\u06e0\\u06e4\\u06e4\\u06e5(Ljava/lang/Object;)I',
    'cn/kuwo/peculiar/specialinfo/\\u06df\\u06e4\\u06e4\\u06e8\\u06df|\\u06df\\u06e7\\u06e0\\u06e4\\u06e8(Ljava/lang/Object;)I',
    'tian0/\\u06df\\u06e2\\u06e0\\u06df\\u06e8|\\u06e5\\u06e2\\u06e4\\u06e1(Ljava/lang/Object;)I',
    'tian0/\\u06df\\u06e1\\u06e4\\u06e3\\u06e2|\\u06e8\\u06e1\\u06e4\\u06e5(Ljava/lang/Object;)I'
];

// houdini/spawn-gated：resume 后 Java VM 才初始化——轮询 Java.available 再挂 hook（最多 60s）
(function waitJava(attempt) {
    attempt = attempt || 0;
    if (typeof Java === 'undefined' || !Java.available) {
        if (attempt > 120) {
            console.log('[BOOT][FATAL] Java bridge 120 次轮询未就绪（houdini 转译环境异常，重跑脚本）');
            return;
        }
        setTimeout(function () { waitJava(attempt + 1); }, 500);
        return;
    }
    bootHooks();
})(0);

function bootHooks() {
Java.perform(function () {
    log('BOOT', 'KUWO-R2a v2 载入（老马静态链头版，houdini 可重跑）');

    function parse(spec) {
        var i = spec.indexOf('|');
        var cls = spec.slice(0, i), meth = spec.slice(i + 1);
        var pi = meth.indexOf('(');
        return { cls: cls, name: meth.slice(0, pi), sig: meth.slice(pi) };
    }

    // ---------- ① EntryActivity.onResume/onStart 入口 ----------
    try {
        var EA = Java.use('cn.kuwo.player.activities.EntryActivity');
        ['onResume', 'onStart'].forEach(function (m) {
            try {
                EA[m].overloads.forEach(function (ov) {
                    ov.implementation = function () {
                        log('EA', 'EntryActivity.' + m + ' 入口（解密链触发点）');
                        return ov.apply(this, arguments);
                    };
                });
            } catch (e) { log('EA', m + ' hook 失败: ' + e); }
        });
    } catch (e) {
        log('EA', '!! EntryActivity hook 失败: ' + e);
    }

    // ---------- ② 4 解密器返回值（文案明文本体） ----------
    DECRYPTORS.forEach(function (spec) {
        try {
            var p = parse(spec);
            var C = Java.use(p.cls);
            C[p.name].overloads.forEach(function (ov) {
                if (ov.argumentTypes.length !== 4) return; // 只挂 [SIII 4参重载
                ov.implementation = function (a, b, c, d) {
                    var ret = ov.call(this, a, b, c, d);
                    try {
                        if (hitBudget0(ret)) {
                            var s = (ret === null || ret === undefined) ? 'null' : String(ret);
                            log('DEC', p.cls.split('/').pop() + '.' + p.name + ' → ' + (s.length > 220 ? s.slice(0, 220) + '…' : s));
                        }
                    } catch (e) { /* 兜底 */ }
                    return ret;
                };
            });
            log('DEC', 'hooked: ' + p.cls + '.' + p.name);
        } catch (e) {
            log('DEC', '!! ' + spec.slice(0, 40) + ' hook 失败: ' + e);
        }
    });
    function hitBudget0(ret) {
        if (!budget('DEC')) return false;
        // 非空非短串才值得看（解密产出可能高频空串）
        return !(ret === null || ret === undefined || String(ret).length === 0);
    }

    // ---------- ③ 分发器入参样例 ----------
    DISPATCHERS.forEach(function (spec, idx) {
        try {
            var p = parse(spec);
            var C = Java.use(p.cls);
            C[p.name].overloads.forEach(function (ov) {
                if (ov.argumentTypes.length !== 1) return;
                ov.implementation = function (arg) {
                    try {
                        if (idx < 4 && hits < HITS_LIMIT && arg !== null) {
                            var s = String(arg);
                            if (s.length > 0 && s.length < 300) {
                                log('DIS', p.cls.split('/').pop() + '.' + p.name + ' arg=' + s.slice(0, 200));
                            }
                        }
                    } catch (e) { /* 兜底 */ }
                    return ov.call(this, arg);
                };
            });
        } catch (e) { /* 分发器量大，失败静默不阻塞 */ }
    });

    // ---------- ④ specialinfo/vipnew 字段快照（onResume 后 dump 一次） ----------
    try {
        var EA2 = Java.use('cn.kuwo.player.activities.EntryActivity');
        EA2.onResume.overloads.forEach(function (ov) {
            var wrapped = ov.implementation;
            ov.implementation = function () {
                var r = ov.apply(this, arguments);
                try {
                    if (!DUMPED) {
                        DUMPED = true;
                        setTimeout(function () {
                            Java.perform(function () {
                                log('DUMP', 'onResume 后 8s 字段快照（specialinfo 单例静态字段）');
                                try {
                                    var SI = Java.use('cn.kuwo.peculiar.specialinfo.SpecialInfoMgr');
                                    var fields = SI.class.getDeclaredFields();
                                    for (var i = 0; i < fields.length && i < 40; i++) {
                                        try {
                                            fields[i].setAccessible(true);
                                            var v = fields[i].get(null);
                                            if (v !== null && String(v).length > 0 && String(v).length < 200) {
                                                log('DUMP', 'SpecialInfoMgr.' + fields[i].getName() + ' = ' + String(v));
                                            }
                                        } catch (e2) { /* 实例字段跳过 */ }
                                    }
                                } catch (e) { log('DUMP', 'SpecialInfoMgr dump 失败: ' + e); }
                            });
                        }, 8000);
                    }
                } catch (e) { /* 兜底 */ }
                return r;
            };
        });
    } catch (e) { log('DUMP', 'dump 包装失败: ' + e); }

    log('BOOT', 'v2 全部 hook 注册完成。老马：启动 App 即触发 onResume 解密链（不需弹窗）；文案明文在 [DEC] 行，写入字段在 [DIS]/[DUMP] 行');
});
}
