/*
 * KUWO-R2a：酷我净化版「QQ频道：新时代，天天免费」弹窗注入桥动态定位
 * 目标：cn.kuwo.player 12.2.2.0 净化版（kuwo3-round1）
 * 用法（PJD110 root + frida-server 已在 /data/local/tmp，需先启动）：
 *   adb shell "su -c '/data/local/tmp/frida-server -D &'"
 *   frida -U -f cn.kuwo.player -l kuwo_r2a_bubble_hook.js --no-pause -o /tmp/kw_r2a_out.txt
 *   （已跑起的进程改用：frida -U -n cn.kuwo.player -l ... ）
 * houdini 注意：x86_64 宿主转译 arm64——Java 层 hook 走 ART 桥不受影响；脚本必须可重跑，
 *   所有 hook 包 try/catch，单点失败不影响其余 hook；输出带时间戳与调用栈。
 * hook 清单（派单 R2a）：
 *   ① s2.E(String,[B) 返回值 —— bubble config 响应解密总入口
 *   ② s2.U3() 返回值 —— URL 构造（freemium/automatic/bubble）
 *   ③ bubble config 解析/字段填充点：buttonUrl/buttonVIPText/channel（String.equals/contains 反查调用栈）
 *   ④ Dialog.show / PopupWindow / TextView.setText 含「频道」文案 → 打印完整 Java 调用栈
 * 后门排查（东哥②问）：记录 bubble 响应体完整 URL 与字段，确认下发源域名（官方=kuwo.cn 系 / 第三方=立即上报）
 */

'use strict';

var MAX_STACK = 25;          // 每次命中最多打印栈帧
var HITS_LIMIT = 40;         // 全局命中上限（防刷屏；弹窗触发后够用）
var hits = 0;

function ts() {
    return new Date().toISOString().slice(11, 23);
}

function log(tag, msg) {
    console.log('[' + ts() + '][' + tag + '] ' + msg);
}

function safeStack(thread) {
    try {
        var st = thread.getStackTrace();
        var out = [];
        for (var i = 0; i < st.length && i < MAX_STACK; i++) {
            out.push('    at ' + st[i]);
        }
        return out.join('\n');
    } catch (e) {
        return '    <stack unavailable: ' + e + '>';
    }
}

function hitBudget(tag) {
    if (hits >= HITS_LIMIT) {
        return false;
    }
    hits++;
    if (hits === HITS_LIMIT) {
        log(tag, '!! 达到全局命中上限 ' + HITS_LIMIT + '，后续命中不再打印（脚本仍运行）');
    }
    return true;
}

Java.perform(function () {
    log('BOOT', 'KUWO-R2a hook 载入，目标 cn.kuwo.player（houdini 环境可重跑版）');

    // 当前线程工具（前向定义，全部 hook 复用）
    function JavaThread() {
        try {
            return Java.use('java.lang.Thread').currentThread();
        } catch (e) {
            return null;
        }
    }

    // ---------- ① s2.E(String,[B) 解密总入口 ----------
    try {
        var S2 = Java.use('cn.kuwo.base.utils.s2');
        // E(String,[B) 具体签名未知处走 overload 枚举兜底
        var overloads = S2.E.overloads;
        log('S2', 's2.E overload 数: ' + overloads.length);
        overloads.forEach(function (ov, idx) {
            ov.implementation = function () {
                var ret = ov.apply(this, arguments);
                try {
                    if (hitBudget('S2.E')) {
                        var preview = (ret === null || ret === undefined) ? 'null' : String(ret).slice(0, 400);
                        log('S2.E', 'overload#' + idx + ' ret=' + preview);
                        if (preview.indexOf('bubble') >= 0 || preview.indexOf('freemium') >= 0 ||
                            preview.indexOf('频道') >= 0 || preview.indexOf('qq.com') >= 0 ||
                            preview.indexOf('buttonUrl') >= 0 || preview.indexOf('新时代') >= 0) {
                            log('S2.E', '!! bubble 关键串命中，调用栈:\n' + safeStack(JavaThread()));
                        }
                    }
                } catch (e) {
                    log('S2.E', 'ret 处理异常(不影响 hook): ' + e);
                }
                return ret;
            };
        });
    } catch (e) {
        log('S2', '!! s2.E hook 失败(不阻塞其余): ' + e);
    }

    // ---------- ② s2.U3() URL 构造 ----------
    try {
        var S2b = Java.use('cn.kuwo.base.utils.s2');
        S2b.U3.overloads.forEach(function (ov) {
            ov.implementation = function () {
                var ret = ov.apply(this, arguments);
                try {
                    if (hitBudget('S2.U3')) {
                        log('S2.U3', 'ret=' + ((ret === null || ret === undefined) ? 'null' : String(ret).slice(0, 300)));
                    }
                } catch (e) { /* 兜底 */ }
                return ret;
            };
        });
    } catch (e) {
        log('S2', '!! s2.U3 hook 失败(不阻塞其余): ' + e);
    }

    // ---------- ③ bubble config 字段填充点：String.equals 反查 ----------
    // 文案运行时解密产出后必经字符串比较/赋值；hook equals 含目标文案时打栈
    try {
        var Str = Java.use('java.lang.String');
        var NEEDLES = ['频道', '新时代', '天天免费', 'buttonUrl', 'buttonVIPText', 'mqqLandingPage', 'mqq_landing_page'];
        Str.equals.overload('java.lang.Object').implementation = function (other) {
            var r = this.equals(other);
            try {
                if (r && hits < HITS_LIMIT) {
                    var s = String(this);
                    for (var i = 0; i < NEEDLES.length; i++) {
                        if (s.indexOf(NEEDLES[i]) >= 0) {
                            if (hitBudget('EQ')) {
                                log('EQ', 'String.equals 命中「' + NEEDLES[i] + '」: ' + s.slice(0, 200) + '\n' + safeStack(JavaThread()));
                            }
                            break;
                        }
                    }
                }
            } catch (e) { /* 兜底 */ }
            return r;
        };
    } catch (e) {
        log('EQ', '!! String.equals hook 失败(不阻塞其余): ' + e);
    }

    // ---------- ④ 弹窗渲染面：Dialog.show / PopupWindow / TextView.setText ----------
    function JavaThread() {
        try {
            return Java.use('java.lang.Thread').currentThread();
        } catch (e) {
            return null;
        }
    }

    try {
        var Dialog = Java.use('android.app.Dialog');
        Dialog.show.implementation = function () {
            try {
                if (hitBudget('DLG')) {
                    log('DLG', 'Dialog.show 调用:\n' + safeStack(JavaThread()));
                }
            } catch (e) { /* 兜底 */ }
            return this.show();
        };
    } catch (e) {
        log('DLG', '!! Dialog.show hook 失败(不阻塞其余): ' + e);
    }

    try {
        var Popup = Java.use('android.widget.PopupWindow');
        Popup.showAtLocation.overload('android.view.View', 'int', 'int', 'int').implementation = function (v, g, x, y) {
            try {
                if (hitBudget('POP')) {
                    log('POP', 'PopupWindow.showAtLocation:\n' + safeStack(JavaThread()));
                }
            } catch (e) { /* 兜底 */ }
            return this.showAtLocation(v, g, x, y);
        };
    } catch (e) {
        log('POP', '!! PopupWindow hook 失败(不阻塞其余): ' + e);
    }

    try {
        var TV = Java.use('android.widget.TextView');
        TV.setText.overload('java.lang.CharSequence').implementation = function (cs) {
            try {
                if (cs !== null && hits < HITS_LIMIT) {
                    var s = String(cs);
                    if (s.indexOf('频道') >= 0 || s.indexOf('新时代') >= 0 || s.indexOf('免费') >= 0) {
                        if (hitBudget('TXT')) {
                            log('TXT', 'TextView.setText 命中文案: ' + s.slice(0, 200) + '\n' + safeStack(JavaThread()));
                        }
                    }
                }
            } catch (e) { /* 兜底 */ }
            return this.setText(cs);
        };
    } catch (e) {
        log('TXT', '!! TextView.setText hook 失败(不阻塞其余): ' + e);
    }

    log('BOOT', '全部 hook 注册完成（单点失败不影响其余）。老马操作提示：登录酷我账号 → 切后台 → 回登录页触发弹窗；命中行带 [S2.E]/[S2.U3]/[EQ]/[DLG]/[POP]/[TXT] 标签');
});
