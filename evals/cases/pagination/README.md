# pagination：不满一页的数据没有计入总页数

任务类型：`boundary`；开发集；人工构造。机器入口为 [case.json](case.json)，原始需求快照为 [issue.md](issue.md)。

## 复现

从固定提交 `410270f8f4d96a3973978c9be22f4c0d6b0a84ed` 导出干净工作区，先安装锁定依赖；将本目录的 `reproduce.py` 复制到工作区后执行：

```sh
python reproduce.py
```

修复前输出 `items=(5,); total_pages=2; expected=3`，以 AssertionError 退出（退出码 1）；修复后退出码 0。
不要直接用当前 main 作为基线，也不要在同一工作区连续修复三个案例。

## 验收

- 5 条记录、每页 2 条时总页数为 3，末页为 (5,)。
- 非空但不足一页计为 1 页。
- 空输入总页数为 0。
- 超出范围的页返回空 items，保留真实总页数。
- 保持页码从 1 开始以及参数校验。

同时运行全部公开测试与宿主提供的本案例隐藏测试。已知基线为 4 failed、23 passed，参考补丁后为 27 passed。
详细运行证据由宿主评测目录保存；公开仓库不分发参考补丁、修复 commit 或隐藏测试。
