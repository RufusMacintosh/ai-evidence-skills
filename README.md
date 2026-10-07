# AI Evidence Skills

两项可追溯AI工作流：研究论文文献综述章节写作，以及广东售电公司的中长期合同覆盖分析。面向AI Agent应用开发的作品集第一版。

## 当前能力

| Skill | 工作流 | 可运行工具 |
| --- | --- | --- |
| review-with-evidence | 区分范文/证据/官方指南，分析论证结构，生成章节及证据映射 | 核对本地摘要原句匹配、必要字段、理由≤10字符和重复文献ID |
| gd-power-hedge | 核验适用规则、区分监管比例与预测覆盖、组织情景分析 | 计算MWh合同覆盖、分时缺口与超额，检查传入规则记录的适用字段及算术 |

这是skill与确定性工具的第一版，不是已经部署的全自动检索、论文投稿或电力交易系统。阅读和推理需支持skills的AI执行环境；两个Python工具可独立运行，不依赖模型API或第三方Python包。

## 运行示例

需要Python 3.10+。在仓库根目录执行：

```bash
python3 skills/review-with-evidence/scripts/verify_evidence.py examples/evidence-synthetic.json
python3 skills/gd-power-hedge/scripts/analyze_coverage.py examples/power-synthetic.json
python3 -m unittest discover -s tests -v
```

示例全部为合成数据，不是真实论文或市场交易。电力示例总量覆盖率100%，但仍有50MWh分时缺口和50MWh分时超额；这不是监管合规结论。

在支持Agent Skills的客户端中，将`skills/`里的两个目录分别放入该客户端规定的skills目录，按客户端官方说明加载；安装路径与兼容性需按实际客户端确认。在此对话中生成文件不等于已安装。

示例调用：

- “使用 $review-with-evidence，读取我的期刊指南、范文与来源文献，先生成主题提纲和证据表，再写相关工作章节。”
- “使用 $gd-power-hedge，读取广东售电公司的合同与预测负荷，先核验规则，再分析分时敞口。”

## 验证边界

摘要文本匹配不能证明论文真实、原句完整或论点有语义支持。原文真实性、句界、书目信息和语义支持需另行核对。

规则的verified字段为人工标记，不是自动法律核验。本版本没有内置广东签约比例、现货预测、完整结算、签约优化或交易申报。没有真实市场回测，不声称收益提高。

目标期刊、论文主题和范文尚未提供；不能声明已满足某一期刊要求。

## 项目结构

技能目录保持精简；README、测试、演示及CI放在仓库层。10项测试覆盖虚构引文、理由超长、重复ID、错地区规则、失效规则、监管分母与预测分母分离、分时错配、零负荷和非法数值。

真实业务数据请放到被git忽略的`private-data/`；不提交密钥、客户负荷或合同原件。第三方论文、规则和数据不因本仓库发布而获得再分发许可。

下一阶段见 PROJECT_PLAN.md。
