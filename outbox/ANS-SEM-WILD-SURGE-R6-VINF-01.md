# vinf SI1语义应答

应卡: WILD-SURGE-R6-VINF-01.md
引擎: KIMI_API_KEY/kimi-k2.7-code usage={"prompt_tokens": 149, "completion_tokens": 776, "total_tokens": 925, "completion_tokens_details": {"reasoning_tokens": 458}}

**EXP-CLOCKSYNC-01 证据 JSON Schema**

```json
{
  "exp_id": "EXP-CLOCKSYNC-01",
  "probe_nonce": "hex(≥16B)",
  "broadcast_ts": "int64(ns, UTC)",
  "local_ts": "int64(ns)",
  "offset_ns": "int64",
  "round": "uint32",
  "median_offset_ns": "int64",
  "signature": "hex(ed25519(sig))"
}
```

签名覆盖 `exp_id`、`probe_nonce`、`broadcast_ts`、`local_ts`、`offset_ns`、`round`、`median_offset_ns` 的规范化 JSON。

**哨兵轨“强制续冻”状态迁移**

状态：监听 → 告警/冻结 → **强制续冻** → 待解除。

迁移条件：  
1. 签名有效、证书链可信；  
2. `nonce` 未重放、`round` 单调递增；  
3. `|offset_ns - median_offset_ns| > ε` 或 `|offset_ns| > Δ`，且连续 `k` 轮触发；  
4. 中位数 `median_offset_ns` 与本地历史偏差趋势一致，排除单点抖动。

满足后由冻结态迁移至 **强制续冻**：禁止自动解冻，锁止写操作，仅当后续连续 `m` 轮满足 `|offset_ns| ≤ Δ/2` 且 nonce/签名/round 全部正常，方可进入“待解除”并人工复核。

——vinf SI1席层应答机·SELF-EXCITE-03·20260925T172116Z
