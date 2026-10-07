# 证据结构
JSON对象含papers数组。每项：id、title、authors（非空字符串数组）、year（整数）、source_url、abstract_text、quote、quote_location、reason。
abstract_text为合法取得的真实摘要快照，不是AI生成摘要。quote为摘要中一条完整原句，允许空白差异，不改写、不截断、不用翻译代替。位置示例：Abstract，第3句。reason按Unicode字符计1—10字，含标点。
可选：doi、source_accessed_at、version、translation、supports、limitations、fulltext_evidence（页码、章节、原文及来源）、license。
脚本通过不能证明文献真实、句子完整、论点获支持或期刊合规。失败项进入待核验表。关键论点映射和语义检查另行完成。
期刊表含：要求、强制/建议/未知、官方来源、访问日期、位置、结果。范文观察表独立，不升级为硬性要求。
