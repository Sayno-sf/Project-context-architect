# Project Context Architect

**让 AI 编程助手在新会话中更快接上项目。**

整理项目目标、当前工作、架构入口和运行说明，清理过期状态；日常更新只核对受影响的内容。

**中文** | [English](README.en.md)

[![CI](https://github.com/lhq418899-sketch/Project-context-architect/actions/workflows/ci.yml/badge.svg)](https://github.com/lhq418899-sketch/Project-context-architect/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 什么时候用

这是一个供支持本地 skills 的 AI 编程助手使用的 skill。适合这些情况：

- **新会话接不上进度**：每次都要重新解释项目做什么、做到哪里、接下来做什么。
- **文档互相矛盾**：功能已经完成，旧 TODO、问题清单或交接摘要仍然写着“待实现”。
- **项目资料越积越多**：当前规则、历史方案和临时笔记混在一起，不知道该信哪份。

它把当前事实放进少量职责清楚的项目文件，其他摘要指向这些文件。后续事实变化时，更新原位置和相关摘要，避免不断追加新的状态记录。

## 安装

选择你使用的平台。默认安装**完整仓库目录**，保留内部结构；直接安装 skill 时，目录名使用 `project-context-architect`。

### Codex

在支持本地 skills 的 Codex 中发送：

```text
使用 skill-installer，从以下仓库的根目录安装 project-context-architect：
https://github.com/lhq418899-sketch/Project-context-architect
保留完整目录。如果已经安装，先备份旧版再更新，并告诉我实际安装位置。
```

### Claude Code

在终端运行：

```bash
claude plugin marketplace add lhq418899-sketch/Project-context-architect
claude plugin install project-context-architect@project-context-architect-marketplace
```

### 其他支持本地 skills 的助手

从 [Releases](https://github.com/lhq418899-sketch/Project-context-architect/releases) 下载源码包并解压，将完整目录命名为 `project-context-architect`，放进该助手支持的 skills 目录。具体加载方式取决于平台。

安装后确认助手能找到这个 skill，再打开目标项目使用。更多安装与验证说明见 [PLUGIN.md](PLUGIN.md)。

## 第一次使用

下面三条提示词可直接复制到目标项目的会话中。你可以用自然语言说明任务，不必先记住模式名。

### 1. 先检查，不改文件

```text
使用 project-context-architect 检查这个项目的交接文档，只读。
指出过期状态、重复事实和缺失入口，给出文件位置及最小修正建议。
```

你会得到一份注明检查范围的报告。检查本身不会修改文件或归档资料。

### 2. 建立或整理项目文档

```text
使用 project-context-architect 为这个项目建立或整理交接文档。
允许修改相关文档；保留现有项目规则和有价值的历史，不修改业务代码。
把当前状态、架构和运行说明放到合适的位置，证据不足的地方明确标注。
```

助手会复用合适的现有文档，补齐确有需要的内容，并检查新会话能否据此找到当前工作和下一步。

### 3. 完成工作后更新状态

```text
使用 project-context-architect，根据本轮已经验证的改动更新项目文档。
只核对受影响的章节和关联摘要，替换过期事实；没有事实变化就不写回。
```

例如，修复已验证后，相关问题清单和下一步不应继续写“待修复”；上线状态仍需要对应的部署证据。日常小更新不要求每次重读整份文件或执行完整交接检查。

## 会生成或维护什么

具体文件取决于项目已有约定。常见分工如下：

| 文件 | 负责说明 |
|---|---|
| `AGENTS.md` 或现有同类入口 | 协作规则，以及新会话先读什么 |
| `PROJECT_STATE.md` | 当前状态、正在做的事、已知问题和下一步 |
| `ARCHITECTURE.md` | 当前组件、入口、数据流和职责边界 |
| `RUNBOOK.md` | 环境、启动、测试和排查方法 |
| `DECISIONS.md` | 值得长期保留的决策理由 |

新项目从协作入口和当前状态开始；其他文件有实质内容才建立。已有文件名和结构合理时会继续使用。历史资料保留并标明用途，交接摘要优先使用链接，避免再维护一份相同状态。

想看具体样子，可以打开[虚构项目示例](examples/bootstrap/)。其中的功能和验证结果仅用于演示文档写法。

## 使用边界

- **检查默认只读。** 修改或归档须属于你的请求范围；这个 skill 管理项目上下文，不负责业务实现。
- **文档检查不等于事实认证。** 自动脚本检查结构、链接和部分可疑表述；语义、产品意图和线上运行状态仍需对应证据。
- **安装不等于自动接管项目。** 它不会在后台监控仓库，也不会自动替换已有项目的协议或安装 CI。需要时在对应项目中明确提出。

## 进阶使用

日常使用走增量维护；需要明确指定范围时，可使用 `BOOTSTRAP`（建立体系）、`REFACTOR`（整理体系）或 `CHECK`（检查）。

- [增量维护流程](references/maintenance.md) · [文档职责与事实归属](references/authority-model.md)
- [BOOTSTRAP](references/bootstrap.md) · [REFACTOR](references/refactor.md) · [CHECK](references/check.md)
- [完整交接的七问检查](references/fresh-session-test.md)

如果需要脚本检查，在本 skill 的目录中运行（Python 3.10+，仅标准库）：

```bash
python -B scripts/check_project_context.py /path/to/project
```

默认检查约定文件名和章节；使用不同命名时先配置对应关系。配置、结果解释和可选 CI 接入见[真实项目检查说明](references/project-checks.md)。

维护本 skill 的回归命令见 [scripts/README.md](scripts/README.md)。其中 `verify_refactor.py` 仅用于验收演练夹具的重构副本，不能用于任意项目。

[更新记录](CHANGELOG.md) · [贡献指南](CONTRIBUTING.md) · [MIT License](LICENSE)
