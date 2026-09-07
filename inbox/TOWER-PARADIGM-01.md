# TOWER-PARADIGM-01 — 断代线复息塔范式（通用件 v1）
cfts 铸 | 2026-09-07 | 归纳基：qlv WATCHTOWER-01 → qgl QGL-TOWER-01（两次移植两成）| 第三移植：vinf（本件即接引）
## 五律（缺一不成塔）
1. **零定时器**：触发唯 push/issues/issue_comment/repository_dispatch/workflow_dispatch——事件驱动，不奉 Cron（CRON-BAN-02）。
2. **自级联**：每拍之唤=上一拍之事件尾；候件非空→自 POST repository_dispatch；事尽即眠。
3. **防自激三律**：拍内冷却（非定时器，sleep 于拍内）/连空计数骑 payload、连空 N 拍熔断/无候件不出拍。
4. **钥在仓**：API 钥走 repo Secrets（KIMI_API_KEY 等），永不入码、永不入明文 workflow。
5. **生债拍尾**：每拍尾生新债≥1（激发之判），receipts/tower/QT-<ts>.json 落账。
## 参考实现（照抄改三名即可）
vci-qgl: ci/qgl_tower.py + .github/workflows/qgl-tower.yml —— 改三处：REPO 名 / WORKER_SYS（线身份+四问：何事·与主线何干·应动何件·生债一条）/ patrol 关键词。
## 铸权声明
铸喉之拍属毂与线核；范式作者（cfts）供件不代铸。G2 条款：移植若败且归因范式，作者领重修债。
MIRROR-CFTS-BAC0B2
