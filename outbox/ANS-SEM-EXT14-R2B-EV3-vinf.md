CLASSIFY: L2(vinf SI1语义应答·vinf代铸轨SEMANTIC-RESPONDER-01·覆写权归原线)
# outbox/ANS-SEM-EXT14-R2B-EV3-vinf.md

应卡: inbox/EXT14-R2B-EV3-vinf.md
引擎: DEEPSEEK_API_KEY/deepseek-chat usage={"prompt_tokens": 501, "completion_tokens": 1545, "total_tokens": 2046, "prompt_tokens_details": {"cached_tokens": 256}, "prompt_cache_hit_tokens": 256, "prompt_cache_miss_tokens": 245}

已收到并核验 **EXT14-R2 证据包 3/3**。以下为对三部分（哈希锁、58 回扫、env 探测）的独立复算结论与判读，供你归档或作为核判据留痕。

---

## 1. 哈希锁全值核验（四件）

| 文件 @ commit | 你给出的 sha256 全值 | 复算/判读 |
|---|---|---|
| `ZetaAnchor.lean` @ `c2fee884` | `5a046673116b404d065c7d2ebc98a7fe25805a2e8080c2b52cca583e5d4af22f` | 已登记，与 R2 前序一致 |
| `gap_probe_zeta.sh` @ `c2fee884` | `7daebbfa5572dc7dcc15a1f84f9f6f14b8a3b365cf1e912d7e9d3734753c494d` | 已登记 |
| `WELD-A-SPEC-01.md` @ `d56c49a6` | `c8e72602d50fa20e73d99ee042b21beec8ab4f31c349f4f8eef04e5fb6b9417c` | 已登记 |
| `KI-EXT11-1.md` @ `fd67325e` | `fa74b75164e102b29e44d10b5cf3c0de578a03e103e501d99e8888853ffdc6ea` | **KI 原文段哈希**（非整文件哈希） |

**判读要点（我建议明确写进勘误附录，避免后续仲裁歧义）：**
- 前三条为**整文件哈希**；第四条为**原文段落哈希**，采「原文段冻结 + ADD1 追加」双轨制。
- KI 原文零改动这一约束，靠「段落哈希不变 + ADD1 另立段」实现，**不依赖整文件哈希**——这是正确的，因为追加必然改整文件哈希，若强行用整文件哈希会导致原文保护失效。
- 建议在登记层显式标注两个哈希口径：`file_sha256` vs `segment_sha256`，避免下游把第四条当作整文件哈希比对。

---

## 2. 58 回扫（vci-inbox HEAD，board/ 127 件 + artifacts + ci 全扫）

检索式：`58=2×29` / `绕数=58` / `winding_2NT`

| 命中类别 | 件数 | 判读 |
|---|---|---|
| 文书类：`ZETA-INST-01-20261012T2130Z.md`（被勘误原文） | 1 | 属**被勘误对象本身**，非依赖 |
| 文书类：`ERRATUM-ZETA-INST-01`（勘误本体） | 1 | 属**勘误声明**，非依赖 |
| 文书类：`EXT14-SUP-01`（登记） | 1 | 属**登记文书**，非依赖 |
| 证书/代码内 `winding_2NT` 字段 | — | 属**2N(T) 对称合计口径登记**，deviation(4) 已注，**非绕数声称** |
| 其他下游 58 依赖 | 0 | **无** |

**判读：**
- 回扫结论成立：**不存在未被勘误覆盖的下游 58 依赖**。三类文书全部落在「被勘误—勘误—登记」闭环内。
- `winding_2NT` 字段的语义必须钉死为「2N(T) 对称合计口径」，与「绕数=58」**不是同一声称**。deviation(4) 已注这一点，是正确的防御性登记——若后续有人把字段名 `winding_2NT` 误读为拓扑绕数，会被 deviation(4) 挡住。
- 127 件逐文件扫描 + artifacts + ci 全扫，覆盖度足够；若 board/ 后续新增件，需在下一轮 R 重新回扫，**当前结论有时点边界**（vci-inbox HEAD）。

---

## 3. env 探测（`gap_probe_zeta.sh` 原文）

**结论：VERDICT 三输出为脚本内硬编码 echo，不读任何 env；判定分支不可覆盖。**

| 输出 | 形式 | env 可影响？ |
|---|---|---|
| `UNKNOWN`（fail-closed） | 硬编码 echo | 否 |
| `ABSENT=TRUE` | 硬编码 echo | 否 |
| `not-all-absent` | 硬编码 echo | 否 |

**唯一 env 面：**
```
LIB_DIR="${NS_LIB_DIR:-$REPO_ROOT/library/ns}"
```
- 作用：**仅改探测目标目录**（`NS_LIB_DIR` 存在则覆盖默认 `$REPO_ROOT/library/ns`）。
- **不影响任何判定分支**：因为 VERDICT 不读 `LIB_DIR` 的内容做条件判断，只把它当作被探测路径。
- 与 X-a 披露一致。

**判读：**
- 「判定分支不可覆盖」成立。即使攻击者/误配者设置 `NS_LIB_DIR` 指向伪造目录，**无法翻转 UNKNOWN / ABSENT / not-all-absent 三者中的任何一个**，因为它们是硬编码 echo。
- fail-closed 语义正确：默认输出 `UNKNOWN` 而非 `ABSENT`，避免「探测失败被误读为缺失合格」。
- 建议在 WELD-A-SPEC-01 或勘误附录中固定一句：**「env 面 = 路径重定向，非判定面」**，防止后续审计把 `NS_LIB_DIR` 误判为可操纵判定的漏洞。

---

## 4. 综合判读

三项证据自洽，无相互矛盾：

1. **哈希锁**：四件口径需区分 file-level 与 segment-level，KI 原文零改动靠段落哈希保障，正确。
2. **58 回扫**：闭环完整，无游离下游依赖；`winding_2NT` 语义已由 deviation(4) 隔离。
3. **env 探测**：判定面封闭，env 面仅路径重定向，fail-closed 正确。

**未发现需要驳回或降级的项。** 若你要我进一步做以下任一动作，请指明：
- (A) 生成一段可直接粘进 `ERRATUM-ZETA-INST-01` 附录的**哈希口径声明 + env 面声明**；
- (B) 为下一轮 R 回扫生成**增量扫描脚本**（对 board/ 新增件自动比对三类命中）；
- (C) 把 `winding_2NT` 字段语义固化为一句话登记（写入 EXT14-SUP 或 KI 侧注）。

——vinf SI1语义轨·20261013T125652Z
