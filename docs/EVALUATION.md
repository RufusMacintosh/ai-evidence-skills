# 可复现验证记录

验证对象为两个Python工具及其合成输入。当前没有真实论文数据集、真实售电数据回测或模型质量基准。

## 复现

在仓库根目录执行：

```bash
python3 scripts/reproduce.py
```

该命令不调用模型或网络。它运行4个CLI场景及现有10项单元测试，将实际结果写入docs/results/。receipt.json记录Python版本、运行时间、命令与退出码；unit-tests.txt保存实际测试日志。重新运行会替换这些记录，时间和日志耗时可能变化。

## 合成场景及观察

| 场景 | 输入变化 | 实际输出应检查的位置 | 可支持的结论 |
| --- | --- | --- | --- |
| 正常文献记录 | 原句存在于合成摘要 | evidence-valid.json：ok=true | 本地格式与匹配通过，不能证明论文存在 |
| 虚构摘要引文 | 把引文改为摘要未出现的句子 | evidence-fabricated.json：ok=false | 当前匹配检查会报告缺少该原句 |
| 总量覆盖但分时错配 | 负荷各100，合同50/150MWh | power-mismatch.json：覆盖1.0，缺口/超额各50 | 总量相等不足以证明分时覆盖 |
| 重复时段标签 | 重复一行slot | power-duplicate.json：duplicate slot错误 | 工具拒绝重复标签；不代表能检查所有区间重叠 |

reproduce.py只核对CLI预期退出码并记录实际JSON；数值与关键状态由单元测试中的断言核对。4个CLI场景不作为独立随机样本，不统计为模型准确率。

## 十项单元测试

| 测试 | 断言范围 |
| --- | --- |
| test_valid_local_match | 合成记录的字段和原句匹配通过 |
| test_fabricated_quote | 摘要未出现的引文失败 |
| test_reason_limit | 11字符理由失败 |
| test_duplicate | 重复文献ID失败 |
| test_total_masks_mismatch | 总覆盖1、缺口50、超额50且规则待核验 |
| test_duplicate_slot | 重复时段标签抛出错误 |
| test_invalid_numeric | 布尔、NaN、负值及数值字符串被拒绝 |
| test_zero_load_surplus | 零负荷覆盖率为null，超额仍保留 |
| test_rule_separate_denominator_and_expiry | 监管分母单独计算；过期记录返回待核验 |
| test_wrong_region_rule | 非广东规则记录返回待核验 |

本地重跑结果见results/unit-tests.txt。初次发布的远端CI已成功：[GitHub Actions记录](https://github.com/RufusMacintosh/ai-evidence-skills/actions/runs/37572538120)。这条链接只证明该次运行，不代表以后所有提交通过。CI配置与本地Python版本分别记录，不声称跨版本全面兼容。

## 尚无证据的效果

不报告论文质量提升、虚构引用检出率、真实规则抽取准确率、交易收益提升或时间节省。后续评估需要预先定义样本、人工核验标准和基线，按时间或来源隔离开发与测试材料，并保留失败样例。
