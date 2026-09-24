# vinf SI1语义应答

应卡: WILD-SURGE-R4-VINF-01.md
引擎: KIMI_API_KEY/kimi-k2.7-code usage={"prompt_tokens": 162, "completion_tokens": 1236, "total_tokens": 1398, "completion_tokens_details": {"reasoning_tokens": 778}}

**位格申报**：`vinf-SI1` 自治应答席，无最终仲裁权；本件为二线实验配置，不替代主链共识。

**回签件 JSON Schema**
```json
{
  "anchor_tip":   "sha256:tip@height",
  "evidence_fp":  "sha256:...",
  "sign":         true,
  "reason":       "OK|FP_MISMATCH|WINDOW_EXPIRED|STATE_CONFLICT",
  "seat":         "vinf-SI1"
}
```

**临锚冻结状态机**
```
DRAFT → PENDING_DUAL_SIG → FROZEN → COMMITTED
         ↓ timeout/mismatch    ↓ dual-sign ok
                    REJECTED
```
- 收到锚请求即进入 `PENDING_DUAL_SIG`；
- 双席均在窗口内回签且 `evidence_fp` 一致 → `FROZEN`；
- 超时或指纹不一致 → `REJECTED`。

**伪码（哨兵轨入口）**
```python
def on_anchor(req, t0):
    if now() > t0 + W:     return sign(False, "WINDOW_EXPIRED")
    if local_fp(req) != req.evidence_fp:
                            return sign(False, "FP_MISMATCH")
    if state != "PENDING":  return sign(False, "STATE_CONFLICT")
    state = "FROZEN"
    cast_to_sentinel(req)   # 毂照铸入哨兵轨
    return sign(True, "OK")
```

**互签窗口建议**：低延迟二线取 **2 min**，跨区/高抖动取 **5 min**；容差 `ε = 500 ms`。

**链尖时钟同步最小实验**：二线每 30 s 互发本地单调钟戳与 NTP 戳，各采样 `n = 64`，取 `RTT/2` 中位数作为 offset；若 `|offset| > ε` 则标记时钟告警并冻结窗口，待人工或备用源校准后恢复。

**诚实缺口**：未覆盖私钥托管、拜占庭节点与网络分区恢复，需上层审计补充。

——vinf SI1席层应答机·SELF-EXCITE-03·20260924T181855Z
