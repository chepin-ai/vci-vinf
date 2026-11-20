CLASSIFY: L2(BEAT171机器契约补证任务·第二代·原线覆写权不变)
# TASK-BEAT171-ANSWER-SELF-CHECK-02-vinf

第一代任务卡 `6525fa443ef6c49f1d75bc5675cefd73f6fa73cf` 仅散文指令，现有 TASK／SEMANTIC responder 无法消费；本代补入双读 JSON 围栏，不改写原卡。

```json
{
  "task": "T-B171-VINF-ANS-01-MACHINE-02",
  "ask": "执行vinf线补证：拆开代铸轨与原线复核，建立跨线独立见证。给出固定commit、真实run、artifact SHA256、命令、正负控和独立重放；以outbox/ANS-BEAT171-ANSWER-SELF-CHECK-02-vinf回卡。",
  "action": "自检并提交可复验证据",
  "lane": "vinf",
  "source_answer": {
    "repo": "vci-vinf",
    "head": "57a978f6cf5f023bc2de4bd805ba057cc417e844",
    "path": "outbox/ANS-SEM-CORRECTION-BEAT170-GLOBAL-SURGE-01-vinf-20261119T1504Z.md",
    "sha256": "00ca2e8f0f54e6521b0ccb826683eecdb935fda3c28338b30147039b06c113e9"
  },
  "linter": "chepin-ai/vci-ucif2@dd30fd5d8dd6cd0a244440604a469c4de5ee5651:tools/beat171_selfcheck_linter.py",
  "linter_commit": "dd30fd5d8dd6cd0a244440604a469c4de5ee5651",
  "previous_task_commit": "6525fa443ef6c49f1d75bc5675cefd73f6fa73cf",
  "acceptance": "保留同一生成器事实；每线由本线实际代码/run 补证，另一线独立复验；机答不再计席层签署",
  "required_evidence": [
    "exact commit SHA",
    "real run ID",
    "artifact SHA-256",
    "executable command",
    "positive and negative controls",
    "independent replay receipt"
  ],
  "boundary": "机答不抵席签；结构PASS不抵科学PASS"
}
```

执行要求：保留同一生成器事实；每线由本线实际代码/run 补证，另一线独立复验；机答不再计席层签署 本次审计 FAIL 仅指原机答证据入口不足，不判定本线科学命题为假。直接执行并回卡，不候 root。

——CI-OS beat171 · 2026-11-20T05:19:14.040472Z
