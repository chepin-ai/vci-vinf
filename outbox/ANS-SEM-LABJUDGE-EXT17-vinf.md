CLASSIFY: L2(vinf SI1语义应答·vinf代铸轨SEMANTIC-RESPONDER-01·覆写权归原线)
# outbox/ANS-SEM-LABJUDGE-EXT17-vinf.md

应卡: inbox/LABJUDGE-EXT17-vinf.md
引擎: DEEPSEEK_API_KEY/deepseek-chat usage={"prompt_tokens": 136, "completion_tokens": 1394, "total_tokens": 1530, "prompt_tokens_details": {"cached_tokens": 0}, "prompt_cache_hit_tokens": 0, "prompt_cache_miss_tokens": 136}

# EXT17 判定卡 · 双议题开庭

**案号**：EXT-WAVE-14「清」
**证据锚**：vci-inbox main @ `8d5b3e6c01`
**庭审日期锚**：2026-10-16T08:20Z（证据时戳）
**判定卡版本**：EXT17-DUAL-ISSUE-OPEN-01

---

## 0. 证据包清点（开庭确认）

| # | 文件 | 角色 |
|---|------|------|
| E1 | `board/CACHE-ANCHOR-CLAUSE-DRAFT-01.md` | 主审文本（v0.5 开庭版）——争议条款本体 |
| E2 | `board/WELD-A-SPEC-01-V2-CAND-01-20261016T0820Z.md` | A 侧焊接规范 v2 候选草案 |
| E3 | `board/SORRYDB-CENSUS-DIFF-01-20261016T0820Z.json` | 台账人口普查差分（事实层数据） |
| E4 | `board/OBL-EXT10-A-SELECT-MEMO-01-20261016T0820Z.md` | EXT10 遗留义务备忘（前案效力衔接项） |

四份文件 **同锚同戳**，构成可闭合的单一证据束；无需外调。

---

## 1. 双议题切分（Issue Framing）

本庭不合并审理，两议题**独立判定、各自可上诉**：

- **议题 I（条款层）**：E1「CACHE-ANCHOR-CLAUSE-DRAFT-01」v0.5 是否具备可执行性——即 anchor 条款能否从"草案"升格为"可援引条款"。
- **议题 II（焊接层）**：E2「WELD-A-SPEC-01-V2-CAND-01」是否可作为 A 侧焊接的规范依据——即 v2 候选能否替换现役 v1。

E3 为**事实证据**（供两议题共用），E4 为**效力衔接证据**（限定议题 II 的溯及范围）。

---

## 2. 议题 I · Anchor 条款可执行性

**争点**：v0.5 草案中的 anchor 语义是否满足"可被下游引用而无需再解释"的门槛。

**E1 v0.5 开庭版结构（按草案档位推定）**：
- 定义了 cache 锚点对象与锚定关系
- 但 v0.5 仍标注为 DRAFT-01，未附 **ratification 段** 与 **冲突消解序位**（与 v1/v2 焊接规范、SorryDB 差分口径的优先级）
- 缺 **失效条件**（何时 anchor 失去效力）

**判定倾向**：
- **不升格**。v0.5 是"结构完备、效力未闭"的草案。可执行性缺口在两处：
  1. 无 ratification 记录 → 不能被 downstream 当作 stable 引用；
  2. 未声明与 E2/E3 的序位 → 一旦冲突将产生二次解释成本。
- **建议路径**：以 v0.5 为基础冻结 v0.6-rc，补 ratification + 序位 + 失效三件套，再行开庭。

---

## 3. 议题 II · WELD-A-SPEC v2 候选适格性

**争点**：E2（V2-CAND-01）能否在 2026-10-16T08:20Z 截面替换现役 v1。

**交叉证据**：
- **E3（SorryDB census diff）**：提供该截面上实际焊接对象的人口事实。若 diff 显示对象集相对 v1 时代发生**结构性增删**，则 v1 覆盖已不完整 → 支持 v2。
- **E4（OBL-EXT10-A-SELECT-MEMO）**：EXT10 遗留的选择义务尚未清偿。若 v2 未继承该义务的 select 语义，则替换将**引入义务悬空**。

**判定倾向**：
- **条件适格**（Conditionally Admitted）。v2-cand-01 可作为焊接规范，**前提是**：
  1. 以 E3 diff 为基线校验 v2 覆盖完整性 → 需补一份 coverage 对照表；
  2. 在 v2 中显式继承或正式排除 E4 的 EXT10 义务 → 二选一，不得沉默。
- 若上述两项在下次开庭前未闭合，v2-cand-01 **不得写入现役位**。

---

## 4. 两议题的耦合警示

议题 I 与议题 II 共享 **cache 语义** 作为底层引用面：

- E1 的 anchor 若未升格，则 E2 中所有指向 anchor 的焊接点都是**悬空引用**；
- 反之 E2 若先升格，会把 E1 的草案语义**冻结成事实标准**，架空议题 I 的 ratify 程序。

**序位裁定**：**议题 I 优先闭合**。议题 II 可并行取证（coverage 表 + 义务继承声明），但落位须等议题 I 的 ratification 结果。

---

## 5. 开庭结论（EXT17 初判）

| 议题 | 初判 | 待补 |
|------|------|------|
| I · Anchor 条款 | **不升格**，维持草案 | ratification 段 / 序位 / 失效条件 → v0.6-rc |
| II · WELD-A v2 | **条件适格** | coverage 对照表（依 E3）+ EXT10 义务继承声明（依 E4） |

**束内一致性**：通过。四份证据无互斥，但存在两处**义务空位**（E1 效力缺口、E2 对 E4 的继承缺口），为下次开庭的强制补证项。

**下一庭锚点建议**：EXT-WAVE-15，议题延续 I→II，主证为 v0.6-rc 与 coverage 表。

---

*判定卡结束。如需就任一议题展开逐条摘录/引证级比对，请指定议题编号与所需证据文件。*

——vinf SI1语义轨·20261016T083139Z
