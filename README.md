# test-toy-python

供 `issue-agent` 学习与评测使用的小型 Python 订单项目。它有意保留三个已知缺陷，
用于观察 Agent 阅读、复现、修复与验证的完整过程，不用于真实交易。

## 安装与测试

需要 Python 3.11+ 和 uv；项目没有运行时第三方依赖。

```sh
uv sync --locked
uv run --no-sync pytest
uv run --no-sync python -c 'from toy_orders import apply_discount; print(apply_discount(1000, 20))'
```

最后一个命令在原始版本输出 200，而业务要求为 800。
`uv.lock` 固定构建与测试依赖。离线执行任务前，应由宿主完成依赖安装。

## 代码与任务

```text
src/toy_orders/
  pricing.py       折扣计算，金额统一使用整数分
  pagination.py    页码从 1 开始的分页
  models.py        商品行与行金额
  orders.py        订单汇总与运费
tests/             公开基础测试
issues/            三条可单独交给 Agent 的问题描述
Dockerfile         预装依赖的验证环境
```

| 本地任务 ID | Issue 文件 | 类型 |
|---|---|---|
| discount | `issues/001-discount.md` | 普通逻辑错误 |
| pagination | `issues/002-pagination.md` | 边界条件错误 |
| order-quantity | `issues/003-order-quantity.md` | 涉及两个文件的修复 |

公开基础测试在原始版本通过，但未覆盖全部业务要求；通过公开测试不代表任务完成。
修复时应增加针对 Issue 的回归测试，并由宿主进行独立验证。
三条任务可从相同的固定 base commit 分别开始，每次使用独立工作区，避免前次修改影响后续结果。

参考补丁、隐藏测试和评测日志保存在本仓库以外，由评测端管理，不应挂载到 Agent 工作区。
仓库 Git 历史不保存参考修复。固定提交、镜像身份与验证结果由外部评测记录保存。

## 容器验证

宿主先联网构建，再离线运行。镜像使用非 root 用户，不需要挂载宿主目录或 Docker socket。

```sh
docker build -t test-toy-python:baseline .
docker run --rm --network none --cpus 1 --memory 256m --pids-limit 64 \
  --read-only --tmpfs /tmp:rw,noexec,nosuid,size=64m test-toy-python:baseline
```

镜像默认执行公开测试；补丁的独立验证应从固定提交重建干净工作区后应用补丁。
Dockerfile 固定了 Python 版本，但镜像标签不是不可变 digest，正式评测必须额外记录实际镜像 ID。

## 开发约定

- 金额使用整数分，避免浮点货币计算。
- 修复应保持现有 API 与输入校验，添加回归测试后运行全部公开测试。
- 每个任务保留 base commit、补丁、测试退出码与完整日志。
- 本项目只提供修复目标，不实现模型循环、权限策略或 PR 发布。
