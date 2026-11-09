# 验证脚本

Python 3.10+，仅标准库；验证脚本只读，回归测试仅操作自动清理的临时目录。`check_discovery.py --online` 额外读取公开 GitHub 元数据和 skills.sh 搜索结果。

```bash
python -B scripts/lint_skill.py
python -B scripts/check_discovery.py
python -B scripts/check_fixture.py
python -B -m unittest discover -s scripts -p "test_*.py" -v
```

- `lint_skill.py`：检查必需文件、UTF-8、frontmatter、发布配置，以及文档相对链接和章节锚点；示例也纳入检查。不通过固定措辞判断规则质量。
- `check_fixture.py`：确认原夹具仍然故意损坏，未被误当成真实项目整理。
- `verify_refactor.py <dir>`：仅验收 **fixtures/messy 的重构副本**。逐项核对四份历史材料、保留正文、所有非 Markdown 原件（包括测试及依赖）的字节、协议所有者、章节与链接。不能用于任意项目。
- `test_validation.py`：验证正确样例通过，同时拒绝档案丢失、正文丢失、代码改动、测试删除、失效链接等反例。

## 发布发现检查

`check_discovery.py` 默认离线检查本 skill 的名称/描述、规范来源、仓库元数据配置，以及中英文安装入口。使用 `--online` 只读查询 GitHub 与 skills.sh；同名结果必须匹配仓库，网络失败与未命中分开报告。使用 `--json` 输出机器可读结果。它不安装 skill，也不评估 Agent 的实际触发效果。

`test_discovery.py` 用模拟公开接口响应覆盖同名碰撞、大小写、空结果、错误响应和失败退出码；不依赖线上排名。联网入口、可选严格门槛和结果解释见 [PLUGIN.md](../PLUGIN.md#discovery-checks)。

## 检查真实项目

`check_project_context.py` 适用于实际项目，默认只读根目录 Agent 入口及 `.architect/` 内的指定权威文件，不扫描整个仓库，不追随仓库外链接。

```bash
python -B scripts/check_project_context.py /path/to/project
python -B scripts/check_project_context.py /path/to/project --baseline-ref HEAD --json
```

缺文件、缺章节和断链属于错误；体量、增长、重复段落及可能的新旧状态冲突只提示复核。返回结果始终标注语义与运行状态未验证。自定义命名、中文章节、退出码、提交/CI 接入以及独立交接验收见 [真实项目检查说明](../references/project-checks.md)。

## 演练

PowerShell 7（先选择一个不存在的临时目标目录）：

```powershell
Copy-Item -LiteralPath ./fixtures/messy -Destination "$env:TEMP/context-refactor-demo" -Recurse
# 对副本执行 REFACTOR，保留历史文件名；不要修改原夹具。
python -B scripts/verify_refactor.py "$env:TEMP/context-refactor-demo"
```

其他系统可用 `cp -R fixtures/messy /tmp/context-refactor-demo`。自定义协议入口可传 `--convention TEAM.md`。同一仓库可以保留引用唯一协议所有者的平台适配入口；脚本不证明平台实际自动加载了它。

## 验证边界

结构及保全通过不等于语义通过。七问答案必须附文件位置，确认产品意图、冲突处理和运行状态仍需 agent 核验。只读 CHECK 还需比较前后文件是否未改。Markdown 检查覆盖本仓库使用的行内链接、ATX 标题和显式 HTML id/name 锚点；引用式链接、特殊渲染器语法需要人工检查。

行为演练见 [fixtures/README.md](../fixtures/README.md)。同一 agent 自查应明确标注，不能声称进行了独立新会话验收。
