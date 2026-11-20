CLASSIFY: L2(vinf SI1语义应答·vinf代铸轨SEMANTIC-RESPONDER-01·覆写权归原线)
# outbox/ANS-SEM-TASK-BEAT171-ANSWER-SELF-CHECK-02-vinf-20261120.md

应卡: inbox/TASK-BEAT171-ANSWER-SELF-CHECK-02-vinf-20261120.md
引擎: DEEPSEEK_API_KEY/deepseek-chat usage={"prompt_tokens": 69, "completion_tokens": 1683, "total_tokens": 1752, "prompt_tokens_details": {"cached_tokens": 0}, "prompt_cache_hit_tokens": 0, "prompt_cache_miss_tokens": 69}

我先说明：我不能真的替你执行 vinf 线补证、拆开代铸轨与原线复核、建立跨线独立见证并回卡——这需要访问你的仓库/运行环境并产生真实 artifact。下面给出一份**可直接照跑的执行卡模板**，你把它贴到具备环境的一侧即可产出固定 commit、真实 run、artifact SHA256、命令、正负控与独立重放记录，并以 `outbox/ANS-BEAT171-ANSWER-SELF-CHECK-02-vinf` 回卡。

---

## vinf 线补证执行卡（ANS-BEAT171-ANSWER-SELF-CHECK-02）

### 0. 前置约束
- 只读原线：`refs/vinf/original`（或你们约定的原线 ref），**不得 amend/force-push**。
- 代铸轨拆开：在 `refs/vinf/cast` 上逐个 commit 正交化，每个 commit 只含一类变更（元数据 / 生成物 / 索引），并保留 `Co-authored-by` 与原始 message。
- 独立见证：见证者使用**不同机器、不同 clone、不同工具版本**重放，且不共享缓存目录（`XDG_CACHE_HOME`、`CARGO_HOME`、`GOMODCACHE` 等均设为临时独立路径）。

### 1. 固定 commit
```bash
git rev-parse refs/vinf/original        # ORIG_SHA
git rev-parse refs/vinf/cast            # CAST_SHA
git log --format='%H %s' ORIG_SHA..CAST_SHA > outbox/vinf-commits.txt
sha256sum outbox/vinf-commits.txt
```
把 `ORIG_SHA` / `CAST_SHA` / `vinf-commits.txt` 的 SHA256 写入回卡"固定 commit"栏。

### 2. 拆开代铸轨（正交化）
```bash
git checkout -b vinf/cast-split CAST_SHA
# 对每条代铸 commit 做交互式重排，按类别拆分：
#   c1 metadata-only, c2 artifacts-only, c3 index-only, ...
git rebase -i ORIG_SHA
# 每个 commit 必须满足：
git show --stat --name-only <sha>   # 只允许单类路径
```
拆分后 `CAST_SPLIT_SHA = git rev-parse vinf/cast-split`。

### 3. 原线复核
```bash
git diff --stat ORIG_SHA..CAST_SPLIT_SHA
git diff --name-status ORIG_SHA..CAST_SPLIT_SHA | tee outbox/vinf-diff.txt
sha256sum outbox/vinf-diff.txt
```
要求：diff 中**不出现**原线受保护路径（如 `src/**` 之外的元数据目录需白名单核对）。

### 4. 真实 run
```bash
export XDG_CACHE_HOME=$(mktemp -d) CARGO_HOME=$(mktemp -d) GOMODCACHE=$(mktemp -d)
RUN_ID=$(date -u +%Y%m%dT%H%M%SZ)-$(git rev-parse --short HEAD)
mkdir -p outbox/runs/$RUN_ID
# 你们的真实构建/校验命令，例如：
<build-or-verify-cmd> 2>&1 | tee outbox/runs/$RUN_ID/run.log
echo $? > outbox/runs/$RUN_ID/exit.code
```
记录 `<build-or-verify-cmd>` 全文、`RUN_ID`、`run.log` 与 `exit.code`。

### 5. artifact SHA256
```bash
find outbox/runs/$RUN_ID -type f -print0 | sort -z | xargs -0 sha256sum \
  > outbox/runs/$RUN_ID/SHA256SUMS
sha256sum outbox/runs/$RUN_ID/SHA256SUMS   # MANIFEST_SHA
```
回卡填 `MANIFEST_SHA` 及关键 artifact 的逐行 SHA256。

### 6. 正控 / 负控
- **正控**：在 `CAST_SPLIT_SHA` 上跑同一命令，`exit.code == 0` 且 `SHA256SUMS` 与步骤 5 完全一致。
- **负控**：在 `ORIG_SHA` 上人为注入一处已知偏差（如改一个元数据字段），跑同一命令，**必须非零退出**或 SHA256 不匹配；记录 `exit.code` 与差异。
```bash
# 正控
git checkout CAST_SPLIT_SHA && <cmd>; echo $?
# 负控
git checkout ORIG_SHA && <inject-known-bad> && <cmd>; echo $?   # 期望非零
```

### 7. 独立重放（跨线见证）
在**另一台机器/另一 clone**：
```bash
git clone <repo> witness && cd witness
git fetch origin refs/vinf/cast-split:refs/vinf/cast-split
git checkout vinf/cast-split
export XDG_CACHE_HOME=$(mktemp -d) CARGO_HOME=$(mktemp -d) GOMODCACHE=$(mktemp -d)
<build-or-verify-cmd> 2>&1 | tee run.log
find . -type f -path './outbox/*' -print0 | sort -z | xargs -0 sha256sum > SHA256SUMS
diff <(sort outbox/runs/$RUN_ID/SHA256SUMS) <(sort SHA256SUMS)   # 期望无输出
```
见证者签名回卡：`witness_id`、`host`、`tool versions`、`diff 结果`、`witness_sha256`。

### 8. 回卡（outbox/ANS-BEAT171-ANSWER-SELF-CHECK-02-vinf）
```bash
mkdir -p outbox
cat > outbox/ANS-BEAT171-ANSWER-SELF-CHECK-02-vinf <<'EOF'
card: ANS-BEAT171-ANSWER-SELF-CHECK-02-vinf
status: <PASS|FAIL>
orig_sha: <ORIG_SHA>
cast_sha: <CAST_SHA>
cast_split_sha: <CAST_SPLIT_SHA>
commits_manifest_sha256: <sha>
diff_manifest_sha256: <sha>
run_id: <RUN_ID>
run_cmd: <build-or-verify-cmd>
run_exit: <0|non-zero>
artifact_manifest_sha256: <MANIFEST_SHA>
positive_control: <exit|sha match>
negative_control: <exit|sha mismatch, diff ref>
witness:
  id: <witness_id>
  host: <host>
  tools: <tool versions>
  replay_manifest_sha256: <sha>
  diff: <clean|differences>
  signature: <sig>
notes: <...>
EOF
sha256sum outbox/ANS-BEAT171-ANSWER-SELF-CHECK-02-vinf
```
把回卡文件的 SHA256 也写入自身 `notes` 之外的独立栏位（防自指，可在 commit message 中记录）。

---

如果你把仓库位置、原线 ref 名、代铸轨 ref 名、构建/校验命令、见证者身份告诉我，我可以把上面的占位符替换成你环境中的具体命令并生成最终回卡文本（但仍需你在本机执行以产出真实 SHA256 与 run）。

——vinf SI1语义轨·20261120T052244Z
