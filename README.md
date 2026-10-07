# 两个独立的AI工作流项目

这里是展示入口。文献综述和广东售电项目分别维护各自的代码、示例、设计说明、工作记录和测试；两者没有代码依赖。

## ① ReviewWithEvidence · 文献综述章节助手

[进入文献综述项目](projects/review-with-evidence/README.md)

服务研究论文中的文献综述章节。已实现文献字段检查、摘要快照中的原句匹配、十字以内参考理由和重复ID检查；skill定义范文分析、主题组织及论点证据追溯流程。

- [工作记录](projects/review-with-evidence/WORKLOG.md)
- [设计说明](projects/review-with-evidence/docs/DESIGN.md)
- [验证记录](projects/review-with-evidence/docs/EVALUATION.md)：4项单元测试、2个合成CLI场景。
- [Skill入口](projects/review-with-evidence/skills/review-with-evidence/SKILL.md)

## ② PowerHedge · 广东售电合同覆盖分析

[进入广东电力项目](projects/gd-power-hedge/README.md)

服务售电公司的中长期合同覆盖分析。已实现预测覆盖率、分时缺口与超额、传入规则记录的范围和阈值检查；skill定义官方规则核验及数据充分时的候选方案分析流程。

- [工作记录](projects/gd-power-hedge/WORKLOG.md)
- [设计说明](projects/gd-power-hedge/docs/DESIGN.md)
- [验证记录](projects/gd-power-hedge/docs/EVALUATION.md)：6项单元测试、2个合成CLI场景。
- [Skill入口](projects/gd-power-hedge/skills/gd-power-hedge/SKILL.md)

## 结构与验证

两个projects/目录均为可单独运行、可迁移到独立repository的完整项目。GitHub Actions为两者分别运行检查，日志以各自项目名展示。当前它们仍位于同一repository，不能称为两个独立仓库。

在对应项目目录运行python3 scripts/reproduce.py，即可重跑该项目的示例与测试。初始实现采用AI辅助开发；工作量按已交付任务与文件记录呈现，不虚构耗时、个人独立编码经历或业务效果。拆分沿用已有实现，不计作新增研发功能。

示例均为合成材料。真实文献来源、目标期刊要求、广东当期签约比例与完整结算规则仍需相应原文和材料核验。没有真实业务回测或投稿效果证明。

## 迁移记录

原型的混合展示已被独立项目目录替代。历史版本保留在Git历史和split-review-with-evidence、split-gd-power-hedge分支中。创建独立仓库的操作尚未完成；一旦该能力可用，可直接迁移对应projects/目录，保留清楚的来源记录。
