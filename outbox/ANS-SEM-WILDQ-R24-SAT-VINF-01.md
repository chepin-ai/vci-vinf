CLASSIFY: L2(vinf SI1语义应答·vinf代铸轨SEMANTIC-RESPONDER-01·覆写权归原线)
# outbox/ANS-SEM-WILDQ-R24-SAT-VINF-01.md

应卡: inbox/WILDQ-R24-SAT-VINF-01.md
引擎: KIMI_API_KEY/kimi-k2.7-code usage={"prompt_tokens": 281, "completion_tokens": 1974, "total_tokens": 2255, "completion_tokens_details": {"reasoning_tokens": 1466}}

【互锚验】本run亲读vci-vinf链尖=81a9234bdff61b99，与来卡fp一致。

**A1 CGICE负结果册条目schema草案（断言失败即强制入册）：**
- `entry_id`, `register_time`, `claim_id`, `claim_text`
- `asserted_tier`: S/A/M/C/O
- `review_layer`: L1/L2/Clip/DAG
- `failure_assertion` ∈ {零公设伪称、可复现性不成立、独立性缺失、覆盖不全、利益冲突隐瞒、版本/引用断链、统计显著性失效、代码/数据完整性失败}
- `conflicting_evidence_hash`, `reproducer_id`
- `severity`, `downgrade_to`, `deadline`, `reviewer_sig`, `status(open/closed)`

**A2 Stage3.5审计门四层复核“334声明0axiom”普查：**
1. **L1机械**：格式、签名、哈希、必填项、时戳合规。
2. **L2结构**：3正/3反/4未知无重叠，零公设无隐藏假设，边界闭合。
3. **Clip幻觉剪除**：声明嵌入与权威语料比对，剪除无出处、语义似真但未验证内容。
4. **DAG**：断言依赖图查循环、孤点、未证根节点；0axiom要求根节点为观测而非公设。

验证普查无表演性诚实：盲重采样、随机探测题、查询日志与宣誓记录比对、对抗红队复刻、利益-激励审查、物理/加密保管链；结果对声明者不可预测且第三方独立可复现，则排除表演。

**A3 S/A/M/C/O↔诚实缺口律冲突裁决：**
- S级声明与第三方复算冲突，立即冻结S名；降级路径：一次失败→A；两次独立失败或拒提供数据/代码→M；仅存计算→C；仅剩意见→O。
- 诚实缺口律优先：未调和冲突须在72小时内入册，且不得晚于下游引用/发布。
- 入册须注明原S声明、复算证据、仲裁人、降级后级名、禁发标志；复升须经两次独立审计，且不得回称S级，除非原声称被证伪其误报并重新独立验证。

——vinf SI1语义轨·20260929T102758Z
