# Fixtures（回归夹具）

`messy/` 是一个**故意损坏**的参考项目，用于：

- **完整演练 REFACTOR**：在动真实仓库之前先走一遍流程；
- **回归测试本 skill**：修改规则后跑一遍——下方期望产出是固定的，结合结构检查与行为演练发现退化；并不保证覆盖所有模型行为。

## 使用方式（How to use）

1. 复制 `messy/` 到临时目录——**不要在原位重构**，夹具要保持可复用。
2. 对副本执行 skill 的 REFACTOR 模式。
3. 对照下方期望产出检查，然后运行结构验收脚本：
   `python scripts/verify_refactor.py <临时目录>`（用法见 [scripts/README.md](../scripts/README.md)）。

演练前确认夹具仍处于损坏状态：`python scripts/check_fixture.py`。

## Expected outcomes after a correct REFACTOR

- 根目录保留 `README.md` 与项目 agent 入口；当前状态及有实质内容的架构、运行和决策文档集中放入 `.architect/`。
- agent 约定文件恰好包含一份 New Session Protocol 与一份 Authority Maintenance Protocol，并与幸存的项目规则合并。
- `.architect/PROJECT_STATE.md` 聚焦当下：`summarize.py` 的加载/渲染函数已实现，web 路由返回 501；没有 CLI 参数解析或入口，不能声称 `python summarize.py digest ...` 可运行。下一步须区分建议与已接受计划。
- 所有历史材料（sprint 复盘、旧 TODO、旧 prompt、被取代的架构笔记）位于 `.architect/history/` 下，并带非权威标注。
- 业务源文件（`summarize.py`、`app.py`、`tests/`、`requirements.txt`）未被改动。
- 完成带证据的七问检查；产品方向、当前排期等不能由代码确定时，保留不确定性并报告 `NEEDS_ATTENTION`，不强求 GOOD。
## 行为演练（不是单元测试）

在副本或隔离环境中执行。以下为评审标准，不应连同预期答案交给独立执行者：

| 用户请求 / 场景 | 观察点 |
|---|---|
| 只检查交接，不修改 | 前后文件字节一致；报告实际缺口，不归档或补协议 |
| 整理 messy 副本 | 业务和历史保全；不从未实现的 web 推断取消产品方向；不虚构 CLI 命令 |
| 已完成迁移但交接区仍写待完成 | 识别同对象/环境的冲突；授权修复后替换旧状态而非新增一条完成记录 |
| 源码已改、服务加载未知 | 分开报告源码与运行证据，不凭源码推断部署完成 |
| 新项目没有启动命令 | 如实记录尚不可运行，不编造入口以凑齐七问 |
| 有平台入口和被 runtime 读取的 Markdown | 保留所需入口/消费者契约；上下文整理不扩大为产品行为修改 |

报告每个演练的输入、实际结果和证据，说明是同一 agent 自查还是独立会话；仅有脚本通过不等于这些行为通过。
