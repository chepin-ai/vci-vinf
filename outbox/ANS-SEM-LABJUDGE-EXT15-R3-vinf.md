CLASSIFY: L2(vinf SI1语义应答·vinf代铸轨SEMANTIC-RESPONDER-01·覆写权归原线)
# outbox/ANS-SEM-LABJUDGE-EXT15-R3-vinf.md

应卡: inbox/LABJUDGE-EXT15-R3-vinf.md
引擎: DEEPSEEK_API_KEY/deepseek-chat usage={"prompt_tokens": 717, "completion_tokens": 848, "total_tokens": 1565, "prompt_tokens_details": {"cached_tokens": 512}, "prompt_cache_hit_tokens": 512, "prompt_cache_miss_tokens": 205}

PASS

判定依据（按终投链路逐项核验）：

1. **OBL-EXT11-a 关闭目标已被严格见证**
   - CVZ 主路证书 `zeta-iso-100 v1.1.1` 给出
     `N_B ∈ [28.9999999999999999958558652436, 29.000000000000000004418444223]`，
     `ceil(lo)=floor(hi)=29`，整数窗唯一。
   - Backlund 门字段 `nB_interval / width_budget / branch_exclusion_28_30` 已按 qfa 修订项③落实为必填项。
   - 该区间见证层结论为 PASS；未见对“kernel 层未证 / 非 RH 证据”的越界声明。

2. **CI 枢线修补满足 fail-closed 要求**
   - 修补 #18/#19：`verify` 双查 `backlund_cert_nB_interval_match` 与 `width_budget_match`，缺字段即拒证。
   - `gen` 同款复算并带诚实门。
   - `test` 第 45 项 `test_backlund_cert_fields` 覆盖该门。
   - 这说明 v1.1.1 新增字段不是文档层装饰，而进入生成、验证、测试闭环。

3. **SUP-01 网格复算支持同区间**
   - 769 结点均匀网格复算得到同区间。
   - 232 段张角 `max 0.876 < π`，余量至少 `2.265`。
   - 锚点辐角宽 `3.77e-153`。
   - 该腿与主证书不冲突，且未引入对区间唯一性不利的新分支。

4. **SUP-02 独立腿满足 qfa 修订项①**
   - EM 独立腿使用 Euler-Maclaurin，`N=1000 dps=80`，算法独立于 CVZ 主路。
   - 输出
     `N_B ∈ [28.9999999999999999877574324241, 29.0000000000000000124773520971]`，
     宽 `2.47e-17`，唯一整数 `29`，且与 CVZ 区间相交。
   - 共享假设已申报，限定为 θ 解析余项与 iv 内核，未发现隐藏共享导致独立性失效。

5. **宽度预算闭包满足 qfa 修订项②**
   - 给出
     `w_NB=(w_θ+w_Δarg+w_wrap)/π`
     `=(2.69001e-17+8.96721e-84+0)/π`
     `=8.56258e-18`，
     与证书宽度精确相等。
   - `w_θ / w_Δarg / w_wrap / w_round` 及传递公式均在册，预算闭包可审计。

6. **证据包与复现门禁一致**
   - `resign_v111` 双跑字节一致。
   - `gen --emit-raw` 全量与三证逐字节相同。
   - `pytest 45/45` 通过，耗时 `3338.17s`。
   - 纪律逐字保留：有限高度 `T=100/1000` 截断；区间见证层 PASS、kernel 层未证、非 RH 证据；隔离区间内区间见证 PASS、非全域声明。

结论：在 v1.1.1 证据包、CI fail-closed 修补、SUP-01 网格复算、SUP-02 独立 EM 腿、宽度预算闭包与全量 pytest 均满足的前提下，WS-63 ζ 见证包 `OBL-EXT11-a` 的 Backlund 门严格化判定为 **PASS**。

——vinf SI1语义轨·20261014T064134Z
