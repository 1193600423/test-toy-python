# 开发案例清单

这三个案例供阶段 0–2 开发使用，不是留出评测集。它们从相同的固定基线分别开始：
`410270f8f4d96a3973978c9be22f4c0d6b0a84ed`。

| case_id | 类型 | 详细记录 | Issue 快照 | 最小复现 |
|---|---|---|---|---|
| discount | 普通逻辑错误 | [case.json](discount/case.json) | [issue.md](discount/issue.md) | [reproduce.py](discount/reproduce.py) |
| pagination | 边界条件错误 | [case.json](pagination/case.json) | [issue.md](pagination/issue.md) | [reproduce.py](pagination/reproduce.py) |
| order-quantity | 两个文件的修复 | [case.json](order-quantity/case.json) | [issue.md](order-quantity/issue.md) | [reproduce.py](order-quantity/reproduce.py) |

每条 `case.json` 包括来源、不可变提交、Issue 快照哈希、环境构建约定、依赖锁文件哈希、
复现命令、实际与期望结果、验证命令、超时、测试计数、验收条件、修改约束与已知局限。
三个 Issue 都是本地构造的任务，目前没有对应的 GitHub Issue URL。

## 在干净工作区复现单条案例

在仓库根目录执行；下面以 discount 为例。选择一个尚不存在的任务目录：

```sh
git worktree add --detach ../toy-discount-run 410270f8f4d96a3973978c9be22f4c0d6b0a84ed
cp evals/cases/discount/reproduce.py ../toy-discount-run/reproduce.py
cd ../toy-discount-run
uv sync --locked
uv run --no-sync python reproduce.py
```

最后一条命令在原始版本应因 AssertionError 返回 1。环境安装失败不能算复现成功。
完成使用后先保存必要修改与日志，再处理工作区；不要复用这个工作区运行另一条案例。

## 公开信息与私有材料

公开目录包含需求与最小复现，不包含答案。参考补丁、参考修复 commit、独立隐藏测试和日志由宿主管理。
Agent 应只收到选中案例的 Issue 和任务工作区，不应看到其他任务或整个宿主评测目录。
最小复现脚本可以交给 Agent，但不能替代独立隐藏验证。

宿主完成依赖安装和环境构建后，应分别验证：

1. 固定基线：最小复现失败，公开测试通过，本案例隐藏测试出现预期断言失败。
2. 干净基线应用参考补丁：同一复现和同一套公开、隐藏测试全部通过。
3. 保存 base commit、参考 commit、补丁及测试哈希、环境身份、命令、退出码和完整日志。

宿主脚本默认本地 Python 验证；Docker 模式负责禁网、非 root、只读源码和资源限制。
当前本地前后对照已重复通过两轮，完整隐藏测试的容器前后对照仍待有容器运行时的宿主执行。
