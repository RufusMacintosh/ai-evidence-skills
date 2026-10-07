# 广东售电合同覆盖分析 · gd-power-hedge

独立项目，包含一项Agent Skill与可单独运行的Python检查工具。

## 已交付

| 部分 | 实际工作与证据 |
| --- | --- |
| 工作流设计 | 监管分母与预测负荷分离；总量覆盖与分时敞口分离；见skills/gd-power-hedge/SKILL.md |
| Python工具 | 预测覆盖率、分时缺口和超额、传入规则记录检查；见对应scripts/ |
| 输入规范 | 字段、来源与失败处理要求；见对应references/ |
| 合成示例 | 正例和失败例各一个；见examples/ |
| 自动验证 | 6项单元测试、2个CLI场景；见tests/及docs/results/ |
| 工程交付 | 一键复现脚本、GitHub Actions配置、设计和验证说明 |

skill中的检索、阅读、写作或决策步骤是执行指令，不代表这些步骤已实现自动服务或完成真实材料评测。

## 运行

只使用Python标准库，不依赖另一项目、模型API或外部Python包。

```bash
python3 scripts/reproduce.py
python3 -m unittest discover -s tests -v
```

运行记录写入docs/results/。已执行版本见receipt.json，其他Python版本兼容性未全面验证。示例为合成材料，不是真实论文或业务记录。

将skills/gd-power-hedge目录按实际客户端的官方说明安装。项目发布不等于客户端已安装。

## 工作记录与复核

- [工作记录](WORKLOG.md)：交付阶段与对应文件，不虚构耗时或个人独立完成经历。
- [设计取舍](docs/DESIGN.md)：实现范围与业务口径。
- [验证记录](docs/EVALUATION.md)：测试范围、实际日志与局限。

## 待完成

未核验广东当前具体签约比例与完整结算；没有真实交易回测、价格预测或签约优化。

后续增加功能前先取得授权的真实材料、确定验收标准和基线，再发布实际效果。初始代码采用AI辅助开发，个人贡献以实际需求、修改及实验记录说明。第三方材料的使用许可需独立核对。private-data/与.env已被git忽略。
