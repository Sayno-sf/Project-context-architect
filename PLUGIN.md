# 插件分发

本目录同时提供可直接安装的 skill 和 Claude Code plugin。两条安装路径分别验证，不能以自检通过代替平台安装成功。

## Codex 用户接入

在支持本地 skills 的 Codex 中，请求内置 skill-installer 从以下仓库安装，或将完整目录复制到该环境的 skills 目录，目录名使用 `project-context-architect`：

[GitHub 仓库](https://github.com/Sayno-sf/Project-context-architect)

保留 `SKILL.md`、`references/`、`examples/` 和 `agents/openai.yaml`。执行回归时保留完整仓库。托管 ChatGPT 与本地 Codex 的安装能力不同；不承诺任意账号都能通过 Plugins 界面安装此仓库。

## Claude Code marketplace

唯一清单位于 [.claude-plugin/marketplace.json](.claude-plugin/marketplace.json)，含市场名称、owner 和相对仓库根的插件源 `./`。插件清单 [.claude-plugin/plugin.json](.claude-plugin/plugin.json) 自己声明根目录 skill，不依赖 marketplace 额外补齐。

```bash
claude plugin marketplace add Sayno-sf/Project-context-architect
claude plugin install project-context-architect@project-context-architect-marketplace
```

这些命令读取 GitHub 版本；本地修改必须发布后才影响该安装路径。

## 本地验证与试载

已安装 Claude Code 时，在仓库根执行：

```bash
claude plugin validate .
claude --plugin-dir .
```

随后确认 skill 被发现并执行一个只读 CHECK。发布者应使用隔离配置测试完整 marketplace 添加/安装过程，记录平台版本与结果。平台验证会检查其支持的格式；本仓库 lint 只检查已使用的配置结构。

官方参考：[创建 marketplace](https://code.claude.com/docs/en/plugin-marketplaces)、[插件清单](https://code.claude.com/docs/en/plugins-reference)。向官方目录提交是独立发布步骤，GitHub 公开不代表已获官方收录。

## 发布前检查

- 运行 [回归脚本](scripts/README.md)，检查示例链接和保全反例。
- 依照 [行为演练](fixtures/README.md) 核验只读、漂移与交接行为。
- 验证实际安装/加载路径；未执行的项目明确标为未验证。
- 插件版本与 CHANGELOG 一致，避免修改后仍使用旧缓存版本。
