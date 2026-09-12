# KUWO-1 补充素材：libtian.so 字节级指纹（码农，2026-09-13 老马判定后秒级轻检）

> 方式：zip 条目字节级 grep 字符串（非反汇编，不触深逆向红线）。样本 Release samples / 本机 mod 副本。

- lib/arm64-v8a/libtian.so：**6,555,475 B**（6.2MB）/ arm64 ELF / sha256 84982a71e8ea7e96…12b9b5（与判定书一致）
- `JNI_OnLoad` ×1（有 native 注册入口，与 tan 注册桥画像吻合）
- `registerNatives` ×0 / `socket` ×0 / `/.so` ×0
- `http` ×2 全上下文：①clang 工具链版本串（android.googlesource.com，编译器残留）②**"Soforge 加固引擎 官网: https://www.soforge.top 简单好用 · 稳稳保护您的程序"**（中文宣传文案）

## 素材结论（定性权在老马/东哥）
**libtian.so = Soforge 商用 so 加固引擎产物**，功能是保护 tian0 那 7 个 Java 类（native 注册解密桥+控制流平坦化解密器）。即作者唯一 native 面=破解代码的保护壳，非独立载荷；其内嵌字符串无任何网络 API/socket 痕迹。
- 对「深审 libtian.so」选项的含义：审的对象本质是第三方加固壳，静态字符串面已见底（无 socket/URL）；native 反混淆深审成本高（Soforge 对抗级），而收益=确认壳内 Java 逻辑与 7 类明文一致——Java 面已明文在手，该收益边际低。
- 「边界开而不追」选项的依据强化：未审角只是加固壳本身，非作者自研 native 逻辑。

（本文件为素材补充，不改判定书原文；判定书 §4 的拍板参考。）
