#!/usr/bin/env python3
# KUWO-R2a v2 驱动：Python 起 frida attach 净化版进程，60s 超时自动 detach，输出落盘 /tmp/kw-frida.log
# houdini 注意：attach 失败自动重试 attach-by-pid（frida-server pid 325 已在跑，老马验证 frida-ps -U 通）
# 用法（CT110 上跑，设备 PJD110 via adb）：python3 kuwo_r2a_driver.py [--spawn]
#   默认 attach 已跑起的 cn.kuwo.player；--spawn 由 frida 拉起（弹窗链每次启动必跑，attach 也够）
import subprocess, sys, time, os
import frida

TARGET = 'cn.kuwo.player'
SCRIPT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'kuwo_r2a_v2_chain_hook.js')
LOG = '/tmp/kw-frida.log'
TIMEOUT = 120
RETRY = 3

def frida_ps():
    try:
        out = subprocess.run(['frida-ps', '-U'], capture_output=True, text=True, timeout=15).stdout
        return out
    except Exception as e:
        print(f'frida-ps 失败: {e}')
        return ''

def target_pid():
    """只匹配主进程（行以 PID + cn.kuwo.player 结尾，排除 :service/:push 等子进程）。
    houdini 坑：attach 子进程（x86_64 宿主转译）会挂起等 stop 超时，必须主进程或 spawn。"""
    out = frida_ps()
    for line in out.splitlines():
        parts = line.split()
        if len(parts) >= 2 and parts[0].isdigit() and parts[1] == TARGET:
            return int(parts[0])
    return None

def get_device():
    """USB 枚举不稳（adb 重连后需要重试），按 device id 兜底（PKG110=192.168.1.157:6666）。"""
    try:
        return frida.get_usb_device(timeout=5)
    except Exception:
        for d in frida.enumerate_devices():
            if d.type == 'usb':
                return d
        raise RuntimeError('无 usb 设备——先 adb connect 100.64.0.3:5555 再重试')

def run(timeout=TIMEOUT):
    logf = open(LOG, 'a', encoding='utf-8')
    def on_message(message, data):
        try:
            if message.get('type') == 'send':
                logf.write(f"{time.strftime('%H:%M:%S')} {message['payload']}\n")
            elif message.get('type') == 'error':
                logf.write(f"{time.strftime('%H:%M:%S')} [JS-ERROR] {message.get('description','')[:400]}\n")
            logf.flush()
        except Exception:
            pass
    dev = get_device()
    pid = target_pid()
    if pid:
        print(f'attach-by-pid {pid}（{TARGET} 主进程）')
        session = dev.attach(pid)
    else:
        print(f'{TARGET} 主进程未跑起，spawn 拉起（houdini 大 App 启动慢，spawn 由 frida 管理）')
        pid = dev.spawn([TARGET])
        time.sleep(2)
        session = dev.attach(pid)
        dev.resume(pid)
    with open(SCRIPT, encoding='utf-8') as f:
        script = session.create_script(f.read())
    script.on('message', on_message)
    script.load()
    print(f'hook 已挂载，{timeout}s 后自动 detach（老马现在启动/回前台 App 触发 onResume 链）')
    t0 = time.time()
    while time.time() - t0 < timeout:
        time.sleep(1)
    session.detach()
    logf.write(f"{time.strftime('%H:%M:%S')} [DRIVER] detach 完成\n")
    logf.close()
    print(f'完成，输出={LOG}')

def force_stop():
    """spawn 超时/frida 挂起会留僵死主进程（launched-not-resumed 态，再 attach 永远等 stop）——重试前清理。"""
    try:
        subprocess.run(['adb', '-s', '100.64.0.3:5555', 'shell',
                        'su -c "am force-stop cn.kuwo.player"'],
                       capture_output=True, timeout=15)
        time.sleep(1)
    except Exception as e:
        print(f'force-stop 失败(继续): {e}')

if __name__ == '__main__':
    for attempt in range(1, RETRY + 1):
        try:
            run()
            sys.exit(0)
        except Exception as e:
            print(f'第 {attempt}/{RETRY} 次失败: {e}')
            if attempt < RETRY:
                force_stop()
                time.sleep(3)
    print(f' 连续 {RETRY} 次失败——查 frida-server 是否在跑: adb shell "su -c pgrep -fl frida"')
    sys.exit(1)
