# CloudCertPrep 题库集成说明

## 概述

本系统将 [CloudCertPrep](https://github.com/nastaso/cloudcertprep)（MIT 协议）的 CLF-C02 题库作为**完全独立板块**集成，与自建 320 题互不干扰。

| 项目 | 自建题库 | CloudCertPrep |
|------|----------|---------------|
| 数据目录 | `data/single_choice.py` + `multi_choice.py` | `data/cloudcertprep/` |
| 题目 ID | S01 / M01 | CCP-S001 / CCP-M001 |
| 进度存储 | `user_data.json` 顶层 | `user_data.json` → `cloudcertprep` 键 |
| 主菜单 | 默认入口 | 「CloudCertPrep 题库」独立子菜单 |

## 更新题库

```bash
# 1. 安装导入依赖（仅开发/更新时需要）
pip install deep-translator

# 2. 下载最新 JSON 并翻译生成中文题库
python tools/import_cloudcertprep.py

# 验证用：仅处理前 50 题
python tools/import_cloudcertprep.py --limit 50

# 调试：不调用翻译 API（仅用缓存）
python tools/import_cloudcertprep.py --no-translate

# 仅重排已有题库的错误选项分段（无需重新翻译）
python tools/reformat_cloudcertprep_explanations.py
```

### 输出文件

- `data/cloudcertprep/single_choice.py` — 单选题
- `data/cloudcertprep/multi_choice.py` — 多选题
- `tools/cloudcertprep_translation_cache.json` — 翻译缓存（可重复运行加速）
- `docs/cloudcertprep_import_report.txt` — 题量与领域分布报告

## 中文化规则

- 题干、选项、`explanation` 全文翻译为考试级中文
- **服务品牌名保留英文**（如 Amazon S3、Amazon EC2、AWS Lambda、IAM、Amazon CloudWatch）
- **官方简体中文考试会翻译的考点词用中文**，与考试指南一致，例如：按需型实例、预留实例、竞价型实例、可用区、边缘站点、安全组、网络 ACL、责任共担模式、AWS 管理控制台、服务配额、多重身份验证
- 解析保留「正确答案 / 错误选项分析」两段结构
- 错误选项按选项分段：`「A. 选项文字」是错误的：原因说明`（与自建题库一致）
- 解析区可通过 `term_glossary` 追加术语中文括号；题干/选项不追加服务品牌的中文释义

## 功能对齐

CloudCertPrep 子菜单支持：

- 模拟考试（65 题 / 90 分钟 / 官方权重）
- 自定义练习（10/20/30/50 题 + 筛选）
- 按四大领域练习
- 单选 / 多选 / 全部题库
- 历史记录、错题本、统计趋势（独立进度）

## 数据来源与许可

- 仓库：https://github.com/nastaso/cloudcertprep
- 许可：MIT
- 原始 JSON：`src/data/clf-c02/domain1.json` ~ `domain4.json`