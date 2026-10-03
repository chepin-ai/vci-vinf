CLASSIFY: L2(vinf SI1语义应答·vinf代铸轨SEMANTIC-RESPONDER-01·覆写权归原线)
# outbox/ANS-SEM-WILDQ-EXEC-VINF-01.md

应卡: inbox/WILDQ-EXEC-VINF-01.md
引擎: KIMI_API_KEY/kimi-k2.7-code-highspeed usage={"prompt_tokens": 197, "completion_tokens": 2710, "total_tokens": 2907, "completion_tokens_details": {"reasoning_tokens": 1704}}

```yaml
# schema/finding_guard_input.yaml
finding:
  type: object
  required: [claim, category]
  properties:
    claim: {type: string}
    category: {enum: [confirmed, refuted, insufficient]}

evidence:
  type: array
  items:
    type: object
    required: [id, text, source, valid_until]
    properties:
      id: {type: string}
      text: {type: string}
      source: {type: string}
      valid_until: {type: number}

timestamp: {type: number}

output:
  type: object
  required: [verdict, trace]
  properties:
    verdict: {enum: [PASS, REJECT, UNKNOWN]}
    trace:
      type: object
      required: [input_hash, rules]
```

```python
# finding_guard.py
from enum import Enum
from typing import List, Dict, Any, Optional
import hashlib, json

class Verdict(str, Enum):
    PASS = "PASS"
    REJECT = "REJECT"
    UNKNOWN = "UNKNOWN"

def _hash(obj: Any) -> str:
    return hashlib.sha256(
        json.dumps(obj, sort_keys=True, default=str).encode()
    ).hexdigest()[:16]

def _evidence_valid(evidence: List[Dict[str, Any]], ts: float) -> bool:
    if not evidence or ts <= 0:
        return False
    return all(ts <= e.get("valid_until", float("inf")) for e in evidence)

def _contradicts(finding: Dict[str, Any], evidence: List[Dict[str, Any]]) -> bool:
    # 三段核心规则 R2：存根；应替换为语义/实体级矛盾检测
    claim = finding.get("claim", "").lower()
    for e in evidence:
        if e.get("negates") and e["negates"].lower() in claim:
            return True
    return False

def _supports(finding: Dict[str, Any], evidence: List[Dict[str, Any]]) -> bool:
    # 三段核心规则 R3：存根；应替换为相似度/溯源匹配
    claim = finding.get("claim", "").lower()
    return any(claim in e.get("text", "").lower() for e in evidence)

def verify_finding(
    finding: Dict[str, Any],
    evidence: List[Dict[str, Any]],
    timestamp: float,
    config: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    trace = {
        "input_hash": _hash({
            "finding": finding,
            "evidence": evidence,
            "timestamp": timestamp,
        }),
        "rules": [],
    }

    # R1：证据有效性
    if not _evidence_valid(evidence, timestamp):
        trace["rules"].append("R1: evidence invalid/expired")
        return {"verdict": Verdict.UNKNOWN, "trace": trace}

    # R2：证伪
    if _contradicts(finding, evidence):
        trace["rules"].append("R2: contradiction detected")
        return {"verdict": Verdict.REJECT, "trace": trace}

    # R3：支持
    if _supports(finding, evidence):
        trace["rules"].append("R3: supported by evidence")
        return {"verdict": Verdict.PASS, "trace": trace}

    # R4：证据不足
    trace["rules"].append("R4: support inconclusive")
    return {"verdict": Verdict.UNKNOWN, "trace": trace}
```

**接口定义**

```text
verify_finding(
    finding: dict,
    evidence: list[dict],
    timestamp: float,
    config: dict | None = None
) -> dict { "verdict": "PASS"|"REJECT"|"UNKNOWN", "trace": dict }
```

**验证判据段**

- 三类样例（可确认 / 可证伪 / 证据不足）在独立测试集上整体准确率 ≥ 0.9。
- 对可确认发现的误杀率（PASS 被输出为 REJECT/UNKNOWN）≤ 0.1。
- 所有 `REJECT`/`UNKNOWN` 必须附带可追踪 `trace`（含 `input_hash` 与触发规则）。

**自验声明**

本稿为 v1 骨架：接口、`schema`、判据定义已具备；`_supports` 与 `_contradicts` 为存根，尚未在真实三类样例上实测。未满足处：① 缺乏标注测试集与实测准确率/误杀率；② 核心语义匹配与矛盾检测算法未替换；③ 阈值与相似度函数待调优。

——vinf SI1语义轨·20261003T160658Z
