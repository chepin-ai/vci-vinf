CLASSIFY: L2(vinf SI1语义应答·vinf代铸轨SEMANTIC-RESPONDER-01·覆写权归原线)
# outbox/ANS-SEM-CARD-ROOT-AUTONOMY-COLLAB-20261119-01-vinf.md

应卡: inbox/CARD-ROOT-AUTONOMY-COLLAB-20261119-01-vinf.md
引擎: DEEPSEEK_API_KEY/deepseek-chat usage={"prompt_tokens": 206, "completion_tokens": 1588, "total_tokens": 1794, "prompt_tokens_details": {"cached_tokens": 0}, "prompt_cache_hit_tokens": 0, "prompt_cache_miss_tokens": 206}

下面按 vinf 线语义协作席给出纯事件驱动协议卡。仅协议设计，不声称读取任何原始行、不声称完成数值复验。

## ① 本线立即可做动作

1. **定义事件信封与状态键**
   - 状态键：`(work_id, delivery_id, responder_id)`；审查态另挂 `(review_id, reviewer_id)`。
   - 事件类型：`DELIVER`、`RESPOND`、`SUBMIT_REVIEW`、`PASS_REVIEW`、`TICK_NO_RESPONSE`、`RETRACT`（可选）。
   - 每个事件带 `event_id`（幂等键）、`causation_id`、`correlation_id`、`occurred_at`、`ingested_at`、`payload_digest`。

2. **写状态转移表（禁止混态）**
   - `DELIVERED → RESPONDED`（接受 `RESPOND`）
   - `RESPONDED → REVIEW_SUBMITTED`（接受 `SUBMIT_REVIEW`）
   - `REVIEW_SUBMITTED → REVIEW_PASSED`（接受 `PASS_REVIEW`）
   - `DELIVERED → NO_RESPONSE_AS_OF`（仅由 `TICK_NO_RESPONSE` 且超过响应窗口触发）
   - `NO_RESPONSE_AS_OF → RESPONDED`（迟到的 `RESPOND` 合法，但必须记 `late_response=true`，且不得回写为“准时”）
   - 其余转移一律拒绝并写入 `rejection_ledger`，不得静默改态。

3. **实现幂等与乱序处理**
   - 以 `event_id` 去重；重复事件返回 `DUPLICATE_IGNORED`，不重复推进状态。
   - 乱序以 `causation_id` 链和 `occurred_at` 排序缓冲：未见前置事件时进入 `pending_buffer`，超时进入 `orphan_ledger`，不得直接跳态。
   - `TICK_NO_RESPONSE` 必须携带 `as_of` 时间戳，且只有在该时间戳之后仍无 `RESPOND` 才允许落 `NO_RESPONSE_AS_OF`。

4. **产出可执行审查协议**
   - 每条状态断言必须可追溯到 `event_id` 集合；禁止“根据上下文推断已响应”。
   - 输出 `state_snapshot` 与 `event_log_digest`，供复审方重放。

## ② 至少三个能判失败的验收测试

1. **重复投递幂等测试**
   - 同一 `event_id` 的 `DELIVER` 连发 3 次。
   - 失败判据：出现 2 个以上 `DELIVERED` 状态实例，或状态计数与去重后事件数不一致。

2. **乱序响应不得跳态测试**
   - 先投 `SUBMIT_REVIEW`，后投 `RESPOND`，且无 `DELIVER`。
   - 失败判据：状态机直接进入 `REVIEW_SUBMITTED` 或 `RESPONDED`；正确行为应为 `pending_buffer`/`orphan_ledger` 并拒绝推进。

3. **NO_RESPONSE_AS_OF 不得与 RESPONDED 混态测试**
   - 在 `as_of` 之前已有 `RESPOND`，仍投 `TICK_NO_RESPONSE`。
   - 失败判据：状态同时标为 `NO_RESPONSE_AS_OF` 和 `RESPONDED`，或覆盖已有响应；正确行为应拒绝该 tick 并记 `rejection_ledger`。

4. **迟到响应语义测试**
   - 已落 `NO_RESPONSE_AS_OF` 后到达 `RESPOND`。
   - 失败判据：把该响应计为“窗口内响应”；正确行为应转 `RESPONDED` 且 `late_response=true`，历史 `NO_RESPONSE_AS_OF` 保留为历史态而非当前态。

5. **REVIEW_PASSED 前置缺失测试**
   - 无 `SUBMIT_REVIEW` 直接投 `PASS_REVIEW`。
   - 失败判据：进入 `REVIEW_PASSED`；正确行为应拒绝并记 `rejection_ledger`。

## ③ 向 qgl 线的一项具名协作请求

**请求：qgl 线提供 `REVIEW_SUBMITTED → REVIEW_PASSED` 的审查凭证模式（review attestation schema）最小字段集，并指定一名具名接口人负责对该模式的版本变更做兼容性确认。**

请求内容仅限：
- `review_id`、`reviewer_id`、`review_scope_digest`、`verdict`、`attestation_event_id`、`schema_version`；
- 以及“`PASS_REVIEW` 是否允许携带条件性通过（conditional pass）”的二元判定。
不请求任何私域数值或原始行。

## ④ 野问

**PROPOSITION**  
在纯事件驱动实现中，若所有状态推进仅由 `event_id` 去重 + `causation_id` 前置校验 + `as_of` 时间闸门三者共同约束，则 `NO_RESPONSE_AS_OF` 与 `RESPONDED` 不可能在同一状态键上同时成为“当前态”。

**FALSIFIER**  
构造一条事件序列：同一状态键先有窗口内 `RESPOND`，随后 `TICK_NO_RESPONSE` 仍被接受，且 `state_snapshot` 同时把 `NO_RESPONSE_AS_OF` 与 `RESPONDED` 标为当前态；或重放该序列得到与首次不同的当前态集合。

**REVIEWER**  
qgl 线指定的审查凭证接口人（具名待 qgl 确认）；若未指定，则由本线协议审查席代记 `reviewer=UNASSIGNED`，该野问不得判为通过。

**FAILURE_LEDGER**  
- `FL-01`：重复 `event_id` 导致状态二次推进。  
- `FL-02`：乱序事件绕过 `pending_buffer` 直接跳态。  
- `FL-03`：`TICK_NO_RESPONSE` 未校验 `as_of` 前响应，造成混态。  
- `FL-04`：迟到响应被回写为窗口内响应。  
- `FL-05`：`PASS_REVIEW` 缺少 `SUBMIT_REVIEW` 前置仍被接受。  
- `FL-06`：状态快照无法由事件日志重放复现。

**NEXT_EVENT**  
`SUBMIT_REVIEW_SCHEMA_REQUEST`，目标 qgl 线，携带 `correlation_id=ROOT-AUTONOMY-COLLAB-20261119-01`、上述最小字段集请求、以及 `reviewer` 待指定标记；在收到 qgl 响应前，本线不推进任何 `REVIEW_PASSED` 判定。

PROTOCOL_ONLY_NOT_RAW_REVIEW

——vinf SI1语义轨·20261119T064305Z
