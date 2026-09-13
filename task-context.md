# KUWO 净化线 · task-context（跨会话状态，2026-09-13）

## 当前进度
- ✅ KUWO-0 作者归属核验（老马，01:17-01:33）：结论=**非番茄/红果壳作者**，直接改包重签路线。详见 KUWO-0-作者归属核验.md
- ✅ 样本存证：callacat/kuwo-purify Release samples，sha256=f2f20005e7234025383a517053703a922173fd05dbc7d6a48d09c62fe9b8732b
- 🔄 KUWO-1 已派码农（01:33 inbound 实锤，worker spawn b6ebb06c）：官方 12.2.2.0 基线 + 全量 dex diff + 端点/动态加载/敏感API/so 四素材，CI 执行
- ⏭ KUWO-2（等产物）：老马 A/B/C/D 分类判定 → 蓝图点位表
- ⏭ KUWO-3：净化重打包（自签 keystore，作者私钥不可得；装机需先卸载天天版）
- ⏭ KUWO-4：老马真机四判据实测（金丝雀基线先行；测试机=PJD110 或 ACE5）→ force-stop 收尾 → 汇报东哥

## Loop
- task_id=kuwo-purify（registry + dispatcher */5 tick；rules v2 observe_only=false，N1=CI success+kuwo1产物→通知老马分类）
- actioner.sh */5 cron（flock /tmp/kuwo-action.lock）：CI 失败→拉日志归案后催单重派（预算2）；无 run 且 60min 无文件活动→催单（预算2 后死信）
- 状态文件 actioner-state.json（redispatch_count/nudged/closed）

## 关键事实（勿重复劳动）
- 酷我 mod 证书 `CN=xinshidai0` SHA-256 4f0a1e41…；番茄/红果壳 `CN=L` eae34eaf… —— 两人两路线
- "天天"署名=酷我 mod 系列作者（论坛佐证：KW音乐 xxx会员版-天天.apk 系列；同帖还有"东明"变体文案）
- v1 完整重签（META-INF/新时代.SF），15 dex，无 Tinker/无内嵌原包，zip 无 Overlapped 损伤
- Java 层端点初扫：api.ktvdaren.com ×2 = C 类头号嫌疑；无卡密/设备码 UI 关键词；native 未深审
- APKPure 无 12.2.2.0（只到 11.3.x）→ 官方基线源候选 APKCombo/豌豆荚/应用宝/酷我官网（码农 KUWO-1 内解决）

## 踩坑登记
- 飞书 Range 分片下载 requests 版一次成功（feishu_dl.py 可复用）
- terminal notify=true 报 schema 错（该环境不接受 boolean？用 background 无 notify + 主动 poll 兜底）

## 🏁🏁 线收官（09-50）
- KUWO-3b2 构建：CI 三败（同一根因：bash -e 下 grep -c 0 误炸 R 赋值行，码农修 || true）→ run 34730840890 绿
- 产物：Release kuwo3-round1 / kuwo-12.2.2.0-purified-r1.apk 242,125,949B / sha256 9acc52da…c92869b（本机+CI digest 双对拍）/ v1v2v3 全签 / 自签 CN=KUWO-Purify
- 反解证据：patch-evidence.txt（P1 return-void + P2 rif 2 行 + P3 fireeye 2 行全落位）
- 老马 PJD110 四判据：装机✓（卸天天版）隐私弹窗 2 轮✓ 首页✓无开屏 播放出流✓ crash=0 外联=联通 CDN 业务面✓ 稳定 60s+ force-stop✓
- **全任务交付待东哥拍板**；loop lifecycle=done 自停；接力 cron 已清

## 🏁🏁🏁 全线收官（09-13 15:4x，东哥验收通过）
- R2 最终态：kuwo3-round6（CI 07:37 绿，B2 撤销+B1 值过滤保留+P2/P3 保留），东哥 ACE5 实测成功（弹窗消失+不闪退+VIP 正常）
- round5 必崩归因归档：B2（q1.b.a init nop）切断 mobilead 初始化依赖链 → BirthScreenHelper.o() NPE（crash 实锤 15:12/15:13）
- 最终产物：Release kuwo3-round6 / kuwo-12.2.2.0-purified-r6.apk / 242,125,949B / digest 725fe780… / 自签 CN=KUWO-Purify
- 净化清单（相对天天 mod）：R2b 双桥掐断（uilib.m.F「QQ频道」值过滤 + specialdialogconfig config 喂入口 nop）+ R1 P2/P3 埋点 init nop + 作者开屏 2 刀保留
- 本机已清：样本/旧轮 APK/解码树/调试帧（权威源=Release 各 tag），剩 r6 产物+证据+文档
- 教训沉淀：掐 bridge 桥类（q1.b.a）会殃及同链无关初始化——掐点必须验证依赖面（r4/r5 两轮实锤）

## 临时文件清理纪律（09-13 东哥定调）
- 任务完成即清：样本副本/旧轮 APK/解码树/调试帧/临时脚本——同轮清完，不留到下次
- 保留判据：实物凭证（最终产物+sha256 清单+验收截图+patch-evidence+判定书+task-context）
- 手机侧：frida-server 等注入工具用完即卸（`rm /data/local/tmp/frida-server`），重启虽可清但主动删是本分
- 权威源=GitHub Release 各 tag（samples/artifacts/round1-round6），本机副本可再生即删
- 本机清理后：1.9G→16M；/tmp 全净（91 项临时文件清除）；手机侧 frida-server 已删+重启验证网络恢复
