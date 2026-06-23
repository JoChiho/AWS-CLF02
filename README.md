# AWS CLF-C02 认证考试刷题系统

> **高效备考 AWS Certified Cloud Practitioner (CLF-C02) 的中文练习工具**  
> 320 道高质量题目（181 单选 + 139 多选）+ 领域分类练习 + 自定义练习 + 模拟考试 + 完整持久化进度追踪

---

## ✨ 功能亮点

- **320 道精选题目**（181 单选 + 139 多选），全部配有详细解析和「重点考点」补充；Cloud / Security 领域已针对性补题
- **模拟考试模式**（65 题 / 90 分钟 / 按官方领域权重抽题 / 严格无解析 / 70% 及格线）
- **自定义练习**：随机抽 10 / 20 / 30 / 50 题；可按全部/单选/多选/领域练习；支持「从未做过」「正确率低于阈值」筛选
- **解析区术语标注**：仅在「答案解析」中为 AWS 英文术语追加中文（如 `Cost Explorer（成本分析器）`）；题干、选项与模拟考试保持纯英文
- **解析富文本 UI**：分区显示（正确答案 / 错误选项分析 / 重点考点）；`**关键词**` 蓝色加粗；支持展开/收起与 A−/A+ 字体调节（偏好写入 `user_data.json`）
- **按官方四大领域分类练习**（云概念、安全与合规、技术与服务、账单定价与支持）
- **知识点覆盖审计**：关键词覆盖率 **100%**（202/202），报告见 `docs/keyword_coverage_gap_report.txt`
- **完整持久化系统**：
  - 最近 10 次练习历史记录（模式、得分、正确率、用时）
  - 增强错题本（全量列表、领域筛选、练 Top 10 / 单题、连续答对自动掌握）
  - 正确率趋势统计 + 简单进步提示
- 响应式暗色 GUI（选项/题干自动换行，窗口缩放与字体自适应）
- 多选题需主动「提交答案」后才显示完整正误解析（更接近真实考试）
- 保留传统 CLI 模式（`--cli`），与 GUI 共用 `user_data.json` 持久化
- **Windows 打包**：可生成免装 Python 的 `AWS-CLF-C02-Quiz.exe`

---

## 🚀 快速开始

### 图形界面（推荐）

```bash
# 1. 创建并激活虚拟环境（推荐，venv/ 已在 .gitignore 中忽略）
python -m venv venv
# Windows:  venv\Scripts\activate
# macOS/Linux:  source venv/bin/activate

# 2. 安装依赖
pip install -r requirements.txt

# 3. 启动程序（默认进入 GUI）
python main.py
```

### 运行测试（可选）

```bash
python -m pytest tests/ -v
# 或
python -m unittest discover -s tests -v
```

当前 **76** 项自动化回归测试。

### 命令行模式

```bash
python main.py --cli
```

首次完成任意一套练习后，系统会自动在项目根目录生成 `user_data.json`，用于保存你的历史记录和错题统计（该文件已加入 `.gitignore`，不会随 Git 提交）。

### Windows 打包（免装 Python）

```bash
pip install -r requirements-dev.txt
python build/build_windows.py
```

将 `dist/AWS-CLF-C02-Quiz/` **整个文件夹**复制到目标机器，运行 `AWS-CLF-C02-Quiz.exe` 即可。学习进度保存在 exe 同级目录的 `user_data.json`。

---

## 📊 当前题库状态（2026-06）

- **总规模**：320 题（181 单选 + 139 多选）
- **ID 范围**：单选 S01–S186，多选 M01–M139
- **领域分布**（更接近 CLF-C02 官方权重 24% / 30% / 34% / 12%）：

| 领域 | 单选 | 多选 | 总计 | 占比 |
|------|------|------|------|------|
| Cloud Concepts（云概念） | 40 | 37 | 77 | 24.1% |
| Security and Compliance（安全与合规） | 55 | 40 | 95 | 29.7% |
| Technology and Services（技术与服务） | 61 | 36 | 97 | 30.3% |
| Billing, Pricing, and Support（账单定价与支持） | 25 | 26 | 51 | 15.9% |
| **总计** | **181** | **139** | **320** | 100% |

- **质量状态**：选项长度审计 **0 问题**；干扰项 High/Medium **0 道**；多选题「选择 N 项」与答案数量一致性已校验
- **特色文档**：
  - 《AWS-CLF-C02 考试完整知识点关键词清单》（`docs/AWS-CLF-C02_All_Knowledge_Points.md`）
  - 关键词覆盖率报告（`docs/keyword_coverage_gap_report.txt`）
  - 改善路线图（`docs/改善建议与路线图.md`）

---

## 📖 使用说明

### 主菜单结构

1. **模拟考试**（主菜单置顶入口）
   - 65 题随机抽题（云 24% / 安全 30% / 技术 34% / 账单 12%）
   - 90 分钟倒计时，到时自动交卷
   - 答题期间不显示解析；交卷后查看得分、领域分项与错题

2. **自定义练习**（紫色入口）
   - 题量：10 / 20 / 30 / 50
   - 范围：全部 / 单选 / 多选 / 按领域
   - 筛选：不限 / 从未做过 / 正确率低于阈值

3. **传统模式**
   - 单选题题库（181 题）
   - 多选题题库（139 题）
   - 全部题目（320 题）

4. **按考试领域分类练习**（官方四大领域）

5. **我的学习**（持久化功能）
   - **历史记录（近 10 次）**
   - **错题本（增强）**：全量列表、领域筛选、练 Top 10 / 单题、连续答对自动掌握
   - **我的统计与趋势**

### 答题流程

- **练习模式**：题干与选项为纯英文；单选点击即显示解析；多选需「提交答案」；解析区自动附中文术语标注
- **解析面板**：答对/答错徽章、你的答案与正确答案、分区富文本解析；可「收起 ▲ / 展开 ▼」；顶栏 A− / A+ 调节字体
- **模拟考试**：全程无解析、无中文术语标注，交卷后统一查看结果
- 随时可「上一题 / 下一题」翻阅；「完成测试」后自动保存进度

---

## 🗂 项目结构

```
aws-clf02-sim/
├── main.py                 # 入口（默认 GUI，可加 --cli）
├── app_paths.py            # 开发/打包模式路径解析
├── requirements.txt        # 运行依赖
├── requirements-dev.txt    # 开发 + PyInstaller 打包依赖
├── .gitignore              # 忽略 venv、缓存、user_data.json 等
├── build/
│   ├── clf_quiz.spec       # PyInstaller 配置
│   └── build_windows.py    # 一键打包脚本
├── gui/
│   ├── app.py              # 应用入口（组合各 Mixin）
│   ├── menu.py             # 主菜单
│   ├── quiz_view.py        # 练习模式答题 UI
│   ├── custom_practice_view.py  # 自定义练习弹窗
│   ├── explanation_formatter.py # 解析分区与富文本渲染
│   ├── wrapped_label.py    # 题干/选项自动换行
│   ├── stats_view.py       # 历史 / 统计
│   ├── mock_exam.py        # 模拟考试 UI
│   ├── wrong_book_view.py  # 增强错题本
│   ├── term_glossary.py    # 解析区术语中文标注
│   └── constants.py        # GUI 共享常量
├── core/
│   ├── engine.py           # CLI 核心引擎
│   └── parser.py           # 输入解析
├── data/
│   ├── __init__.py         # 数据层统一出口
│   ├── single_choice.py    # 181 道单选题
│   ├── multi_choice.py     # 139 道多选题
│   ├── custom_practice.py  # 自定义练习抽题与筛选
│   ├── mock_exam.py        # 模拟考试抽题与计分逻辑
│   └── progress.py         # 持久化（user_data.json）
├── tests/                  # 自动化回归测试（76 项）
├── tools/                  # 题库审计与维护脚本
└── docs/                   # 知识点清单、审计报告、路线图
```

---

## 🛠 维护工具（`tools/`）

| 脚本 | 用途 |
|------|------|
| `audit_keyword_coverage.py` | 关键词覆盖率审计 |
| `audit_term_glossary.py` | 术语表覆盖缺口扫描 |
| `analyze_option_lengths.py` | 选项长度均衡性审计 |
| `audit_question_bank.py` | 题库 ID / 领域一致性检查 |
| `check_explanations.py` | 解析格式与字母依赖检查 |
| `print_question.py` | 按 ID 打印题目（如 `python tools/print_question.py S24`） |

---

## 💾 进度数据说明

- 历史记录、错题统计、练习字体比例保存在 `user_data.json`（已 `.gitignore`，仅保留在本地）
- 可随意备份、复制到其他机器继续使用
- 删除该文件即可清空所有进度
- 只保留最近 10 次会话；题目累计统计永久保存

---

## 🔧 Git / SourceTree 协作说明

`.gitignore` 已配置忽略以下内容，**无需在 SourceTree 中手动排除**：

- `venv/`、`.venv/` 等虚拟环境目录
- `__pycache__/`、`*.pyc` 等 Python 缓存
- `.pytest_cache/`、`.mypy_cache/` 等测试/检查缓存
- `dist/`、`build/clf_quiz/` 等打包中间产物
- `user_data.json` 个人学习进度
- `mcps/`、`terminals/` 本地工具链目录

若 SourceTree 仍显示已跟踪的缓存文件，在项目根目录执行一次：

```bash
git rm -r --cached __pycache__ data/__pycache__ gui/__pycache__ tests/__pycache__ tools/__pycache__ 2>nul
git rm --cached user_data.json 2>nul
```

然后在 SourceTree 中提交此次变更，之后新生成的缓存将不再出现在待提交列表。

---

## 🛠 技术栈

- Python 3.9+
- customtkinter（现代暗色 GUI 框架）
- pytest / unittest（自动化测试）
- 分层架构：gui / core / data

---

## 📝 题库与内容

题目基于 AWS CLF-C02 官方 Exam Guide 整理。2026-06 完成 31 道关键词补题（S142–S160 / M110–M120）及 65 道 Medium 干扰项修复，关键词覆盖率 100%。

---

## 🤝 贡献与反馈

欢迎补充新题目、改进解析或提交 Bug / 功能建议。提 PR 或 Issue 均可。

---

## 📄 License

本项目目前未指定开源协议。如需商用或二次分发请先联系作者确认。

---

**祝你早日通过 AWS CLF-C02 考试！** 🚀

详细规划见 `docs/改善建议与路线图.md`。