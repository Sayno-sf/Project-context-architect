# 插件分发

本目录同时提供可直接安装的 skill 和 Claude Code plugin。各安装路径分别验证，不能以自检通过代替平台安装成功。

## 通用 Skills CLI

需要 Node.js/npm。来源和 skill 名称显式指定，避免同名结果：

```bash
npx skills add Sayno-sf/Project-context-architect --skill project-context-architect
```

按 CLI 提示选择 Agent 和安装范围。`--list` 仅枚举，不安装；能枚举不代表目标 Agent 已成功加载。CLI 的具体支持范围以[官方说明](https://github.com/vercel-labs/skills)为准。

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

<a id="discovery-checks"></a>
## 发现与检索检查（维护者）

这些检查用于发布本 skill，不是用户项目的日常维护流程。仓库简介和 Topics 的期望值保存在 [.github/repository-metadata.json](.github/repository-metadata.json)，并在 GitHub About 中维护；文件本身不会自动修改远端设置。

```bash
# 离线：名称、描述、来源、两份 README 的通用安装入口
python -B scripts/check_discovery.py
# 只读联网：核对 GitHub 元数据；精确作者搜索及场景词搜索
python -B scripts/check_discovery.py --online --json
# 确需把精确检索命中作为门槛时使用
python -B scripts/check_discovery.py --online --require-listed
# 独立确认 GitHub 仓库能被实际 CLI 枚举（不安装）
npx skills add Sayno-sf/Project-context-architect --list
```

输出区分 `PASS`、`FAIL`、`NOT_FOUND`、`UNAVAILABLE`。搜索只在返回结果中按**仓库来源与 skill 标识**匹配；其他仓库的同名项不算通过。未命中不证明目录中绝对不存在，更不能证明 skill 无法直接安装。HTTP 错误、超时、响应格式变化标为 `UNAVAILABLE`，不当作零结果。

退出码：`0` 表示已执行的硬性检查通过（可包含非阻塞 `NOT_FOUND`）；`1` 表示本地/远端元数据不一致或显式要求的精确检索未命中；`2` 表示联网检查未能完成。场景词排名是诊断项，不做强制排名断言。普通 CI 只跑离线检查与模拟响应回归；GitHub Actions 的 **skill-discovery** 工作流可手动运行线上检查并下载 JSON 报告，不定时轮询、不自动安装或制造安装量。

[skills.sh 官方说明](https://skills.sh/docs/faq)称，用户通过 Skills CLI 安装产生的遥测会推动目录收录和排名；可用环境变量 `DISABLE_TELEMETRY=1` 关闭 CLI 遥测。没有即时收录或排名保证。本脚本只发出公开元数据/搜索 GET 请求，不安装、不发送安装事件。检索接口沿用[官方 CLI 的查询入口](https://github.com/vercel-labs/skills/blob/main/src/find.ts)，第三方接口变化可能需要调整。

安装后的选择另行做自然语言试用：例如“准备让另一个 Agent 接手，整理一下当前进度”和“已经修好了，文档却还写着待修复”。也检查普通业务代码请求不会被错误引导为文档重构。它属于行为评估，脚本不以关键词匹配冒充触发准确率。
