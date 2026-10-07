# 输入
JSON：as_of（ISO日期）、region=广东、subject=售电公司、period（如2026-11）、unit=MWh、rows（非空）。每行slot唯一、load_mwh为非负预测负荷、contract_mwh为非负合同净覆盖。调用者核对区间时区重叠和粒度；脚本仅检查标签重复。第一版不支持负净合同头寸。
可选signing_rule：verified（人工标记）、region、subject、period、effective_from、effective_to、source_url、clause、numerator_basis、denominator_basis、numerator_mwh、denominator_mwh、min_ratio（0—1）。
监管分子分母独立输入，附真实口径；不能默认用预测负荷作为监管分母。未知有效期不伪填。
无规则返回pending_verification。matches_supplied_threshold仅说明传入记录与算术通过，不证明官方适用性。脚本不优化比例、不预测价格、不计算正式结算。
