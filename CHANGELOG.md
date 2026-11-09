# Changelog

本项目遵循 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/) 与语义化版本（[SemVer](https://semver.org/lang/zh-CN/)）。

## [Unreleased]

- 计划提交 [Anthropic 官方插件目录](https://github.com/anthropics/claude-plugins-official)（仓库公开后走提交表单）。

## [0.4.0] - 2026-11-09

### Changed

- 默认将项目状态、架构、运行说明、决策和上下文历史集中到 `.architect/`，保留根目录 Agent 入口。
- 检查器、示例、模板和演练验收同步新布局；检查器不再自动使用根目录状态文件，自定义路径仍可显式配置。
- 增加跨平台轻量接力：用户指定接手即承接整合职责，按需核对相关变化，仅实际并行时协调文件范围；不引入锁、看板或额外审批。
- 更新 GitHub 仓库链接至 `Sayno-sf/Project-context-architect`。

## [0.3.1] - 2026-10-22

### Changed

- 日常维护默认增量核对：受影响章节、新证据、关联摘要和批次 diff；不要求每次写入通读全文。
- 完整七问限于初始化、广泛重构与交接验收；局部检查不宣称整体 GOOD，无变化不强制写回或输出空报告。
- 精简主入口和重复规则，按需读取示例及检查器/CI 说明；同步可独立使用的项目协议模板。
- 明确无实现的新项目可以如实声明缺少架构/运行入口，不为通过检查创建空文档。

## [0.3.0] - 2026-10-22

### Added

- 面向真实项目的只读检查器：指定权威范围、章节/链接/入口检查、JSON 输出和 Git 基线增长比较。
- 体量、交付日记、重复段落及待办/完成语言的复核提示；明确机械通过不代表语义或部署通过。
- 可自定义文件名及中文章节的配置、项目内独立安装和 CI 样例；不自动安装 hook 或修改其他项目。
- 真实项目检查器的读取边界、只读性、反例与退出码回归。

### Changed

- 权威维护要求先核对“旧事实 → 新证据 → 需撤下的旧摘要”，再替换当前状态。
- 项目完成协议引用已安装的本地检查命令，并保留独立交接验收与自查的区分。
- 修复并验证 CI 步骤换行，增加真实项目示例检查。

## [0.2.0] - 2026-10-22

### Changed

- CHECK 默认只读，修复须属于用户请求；报告注明范围，允许审计完成但健康度仍待处理。
- 日常维护替换当前事实并清理过期摘要，区分源码、构建、运行与验收；按阅读成本控制上下文。
- 项目协议内置带证据的七问检查，脱离 skill 安装路径仍可使用；保留必要的平台适配入口与运行时消费者契约。
- 示例改为自洽、链接完整的文档集；明确虚构验证标签，不重复手写交接状态。

### Fixed

- REFACTOR 验收逐项核对全部历史正文及业务/测试/依赖原件，支持 GEMINI 和自定义入口。
- 链接检查覆盖章节锚点和示例；以结构及反例回归替换固定措辞检查。
- marketplace 移至 `.claude-plugin/marketplace.json` 并补 owner；插件自带根 skill 路径。修正本地试载和 Windows 副本命令。
- 夹具期望不再虚构可运行 CLI 或强制 GOOD；增加行为演练标准。

## [0.1.0] - 2026-10-11

### Added

- 三种模式：**BOOTSTRAP**（最小权威集建立）、**REFACTOR**（上下文收敛与历史归档）、**CHECK**（交接就绪检查）。
- 权威模型：一事实一主、当前真相与历史分离、分类感知冲突验证、权威完成门。
- Agent 约定文件命名通用化：默认 `AGENTS.md`，可复用平台等价文件（`CLAUDE.md` / `COPILOT.md` / `GEMINI.md` 等），禁止并行约定文件。
- 交接就绪测试：`references/fresh-session-test.md` 7 问清单。
- 金标准示例：`examples/bootstrap/`（虚构 remindr 项目）。
- 回归夹具：`fixtures/messy/` 故意损坏参考项目 + `scripts/` 确定性验收脚本（`lint_skill.py` / `check_fixture.py` / `verify_refactor.py`）。
- 插件分发资产：`.claude-plugin/plugin.json`、`marketplace.json`、`PLUGIN.md`（官方目录 / 自建 marketplace / 本地安装三种接入）。
- 发布配套：README（中英混合、中文为主）、MIT LICENSE、CHANGELOG、CONTRIBUTING、CI workflow。

### Fixed

- `lint_skill.py` 对 `references/authority-model.md` 中指向目标项目根目录的模板示例链接加入显式豁免。
