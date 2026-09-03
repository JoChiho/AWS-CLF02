# -*- coding: utf-8 -*-
"""薄弱点突击题库：针对错 ≥4 次且正确率 ≤25% 的考点重出新题。"""
from __future__ import annotations

D1 = "Cloud Concepts"
D2 = "Security and Compliance"
D3 = "Technology and Services"
D4 = "Billing, Pricing, and Support"


def _s(seq: int, topic: str, question: str, options: list[str], correct_idx: int, explanation: str, domain: str) -> dict:
    letters = "ABCD"
    formatted = [f"{letters[i]}. {opt}" for i, opt in enumerate(options)]
    return {
        "id": f"WP-S{seq:03d}",
        "question": question,
        "options": formatted,
        "correct_answers": [letters[correct_idx]],
        "explanation": explanation,
        "domain": domain,
        "is_multi": False,
        "source": "weak_point_drill",
        "topic": topic,
    }


def _m(seq: int, topic: str, question: str, options: list[str], correct_idxs: list[int], explanation: str, domain: str) -> dict:
    letters = "ABCDE" if len(options) == 5 else "ABCD"
    formatted = [f"{letters[i]}. {opt}" for i, opt in enumerate(options)]
    return {
        "id": f"WP-M{seq:03d}",
        "question": question,
        "options": formatted,
        "correct_answers": [letters[i] for i in correct_idxs],
        "explanation": explanation,
        "domain": domain,
        "is_multi": True,
        "source": "weak_point_drill",
        "topic": topic,
    }


WEAK_POINT_QUESTIONS = [
    # ----- Direct Connect -----
    _s(1, "AWS Direct Connect",
       "某公司需要把本地数据中心与 AWS 用一条专用、私有的网络连接起来，并且这条连接通常要在合作的托管机房里交给网络服务商落地。应选择哪项服务？",
       ["AWS Site-to-Site VPN", "AWS Direct Connect", "互联网网关 (Internet Gateway)", "Amazon CloudFront"],
       1,
       "正确答案：\n\nAWS Direct Connect 在合作的托管设施中通过专用线路接入 AWS，不走公共互联网。\n\n错误选项分析：\n\n「A. AWS Site-to-Site VPN」是错误：VPN 走加密的公共互联网，不需要托管机房专用端口。\n\n「C. 互联网网关」是错误：IGW 只让 VPC 进出公网。\n\n「D. Amazon CloudFront」是错误：这是 CDN，不是专线接入。\n\n重点考点：\n- Direct Connect = 专用网络 + 托管设施/ISP\n- VPN ≠ Direct Connect",
       D3),
    _s(2, "AWS Direct Connect",
       "实施 AWS Direct Connect 时，客户通常还必须具备哪两项外部条件？",
       ["一台 Direct Connect 网关和一台 NAT 网关", "互联网服务提供商 (ISP) 以及托管设施 (colocation)", "AWS Outposts 机架和 Local Zone", "Transit Gateway 附件和 VPC 对等"],
       1,
       "正确答案：\n\nDirect Connect 要在 AWS 合作的 colocation 机房由 ISP/网络服务商提供专线端口。\n\n错误选项分析：\n\n「A. Direct Connect 网关和 NAT 网关」是错误：DX Gateway 是可选架构组件，NAT 网关与专线落地无关。\n\n「C. Outposts 和 Local Zone」是错误：那是把 AWS 算力放到本地/都会区，不是专线接入条件。\n\n「D. Transit Gateway 和 VPC 对等」是错误：它们是 VPC 互联方式，不是 DX 落地前提。\n\n重点考点：\n- 落地条件：ISP + colocation facility",
       D3),
    _s(3, "AWS Direct Connect",
       "与 AWS Site-to-Site VPN 相比，AWS Direct Connect 最主要的差异是什么？",
       ["Direct Connect 默认提供加密，VPN 不加密", "Direct Connect 走专用网络，VPN 通常经公共互联网加密传输", "Direct Connect 只能连接 Amazon S3，VPN 只能连接 EC2", "Direct Connect 是全球 DNS 服务"],
       1,
       "正确答案：\n\nDirect Connect 是专用连接；Site-to-Site VPN 把流量封装后走互联网。\n\n错误选项分析：\n\n「A. Direct Connect 默认提供加密」是错误：DX 本身不自动等同于 VPN 那种 IPsec 加密，常与 VPN 叠加。\n\n「C. 只能连接 S3 / EC2」是错误：两者都可通到 VPC 等资源。\n\n「D. 全球 DNS」是错误：那是 Route 53。\n\n重点考点：\n- 专用线路 vs 公网 VPN",
       D3),
    _m(1, "AWS Direct Connect",
       "关于 AWS Direct Connect，下列哪些描述正确？（选择两项）",
       ["需要在合作托管设施中由网络服务商提供连接", "流量走公共互联网并自动使用 IPsec", "可提供更可预测的网络性能，而不依赖公共互联网质量", "等同于互联网网关，用于给 EC2 分配公网 IP", "是 CloudFront 边缘站点的另一种名称"],
       [0, 2],
       "正确答案：\n\nDirect Connect 在 colocation 落地，专用网络性能更可预期。\n\n错误选项分析：\n\n「B. 走公共互联网并自动 IPsec」是错误：那是 Site-to-Site VPN。\n\n「D. 等同于互联网网关」是错误：IGW 是 VPC 的公网入口。\n\n「E. CloudFront 边缘站点」是错误：边缘站用于 CDN。\n\n重点考点：\n- colocation + 专用性能",
       D3),

    # ----- Service Catalog -----
    _s(4, "AWS Service Catalog",
       "组织希望让员工只能从预先批准的产品清单里一键部署 IT 服务（例如标准 VPC、获批的 EC2 镜像）。应使用哪项服务？",
       ["AWS Marketplace", "AWS Service Catalog", "AWS CloudFormation Designer", "Amazon API Gateway"],
       1,
       "正确答案：\n\nService Catalog 把已批准的 IT 产品组织起来，供最终用户自助部署，便于治理。\n\n错误选项分析：\n\n「A. AWS Marketplace」是错误：那是买卖第三方软件的商店，不是企业内部获批目录。\n\n「C. CloudFormation Designer」是错误：那是画模板的工具，不是面向业务用户的产品目录。\n\n「D. API Gateway」是错误：那是发布 API。\n\n重点考点：\n- Service Catalog = 组织内部获批 IT 产品的目录与治理",
       D3),
    _s(5, "AWS Service Catalog",
       "AWS Service Catalog 主要解决哪类问题？",
       ["给开发人员用熟悉的编程语言声明全部基础设施", "快速检索每项 AWS 服务的官方产品页和定价计算器", "简化和治理组织内常用 IT 服务的发布与部署", "在多个 AWS 账户之间复制 IAM 用户"],
       2,
       "正确答案：\n\n它简化常用部署的组织与管理，让用户只能启动获批产品。\n\n错误选项分析：\n\n「A. 用编程语言声明基础设施」是错误：那更接近 CDK / 编程式 IaC。\n\n「B. 检索服务描述和定价」是错误：那是文档与 Pricing Calculator，不是 Service Catalog。\n\n「D. 复制 IAM 用户」是错误：那是身份管理/组织策略范畴。\n\n重点考点：\n- 不要把 Service Catalog 当成「服务说明书」或 CDK",
       D3),
    _s(6, "AWS Service Catalog",
       "安全团队要求开发人员不得随意创建任意资源，只能启动经过审查的 CloudFormation 产品。哪项服务最直接满足？",
       ["AWS Config 规则", "AWS Service Catalog", "Amazon Inspector", "AWS Trusted Advisor"],
       1,
       "正确答案：\n\n把审查过的模板封装成产品，由 Service Catalog 控制谁能启动。\n\n错误选项分析：\n\n「A. Config 规则」是错误：Config 评估已有资源配置是否合规，不是自助产品目录。\n\n「C. Inspector」是错误：漏洞扫描。\n\n「D. Trusted Advisor」是错误：最佳实践检查与建议。\n\n重点考点：\n- 获批产品自助 vs 事后合规扫描",
       D3),

    # ----- Audit Manager -----
    _s(7, "AWS Audit Manager",
       "哪项服务会按框架自动收集 AWS 使用与活动证据，并整理成评估报告，从而减轻审计准备负担？",
       ["AWS CloudTrail", "AWS Audit Manager", "AWS Trusted Advisor", "AWS Security Hub"],
       1,
       "正确答案：\n\nAudit Manager 持续收集证据并映射到合规框架，输出评估报告。\n\n错误选项分析：\n\n「A. CloudTrail」是错误：它记录 API 调用日志，本身不是按框架出审计评估报告的服务。\n\n「C. Trusted Advisor」是错误：给出成本/安全/性能建议，不是审计证据包。\n\n「D. Security Hub」是错误：聚合安全发现，不是按审计框架整理证据。\n\n重点考点：\n- Audit Manager = 自动收集证据 + 评估报告\n- CloudTrail 是日志源，不是审计报告产品",
       D2),
    _s(8, "AWS Audit Manager",
       "审计员需要一份对照 SOC 2 或类似框架、由系统自动归集的证据包。优先看哪项 AWS 服务？",
       ["AWS CloudTrail Lake", "AWS Audit Manager", "AWS Cost Explorer", "Amazon Macie"],
       1,
       "正确答案：\n\nAudit Manager 内置常见合规框架，自动归集证据。\n\n错误选项分析：\n\n「A. CloudTrail Lake」是错误：用于查询事件数据，不会按框架打包审计证据。\n\n「C. Cost Explorer」是错误：成本可视化。\n\n「D. Macie」是错误：发现敏感数据。\n\n重点考点：\n- 框架化证据收集 → Audit Manager",
       D2),
    _s(9, "AWS Audit Manager",
       "下列哪项最能说明 AWS CloudTrail 与 AWS Audit Manager 的分工？",
       ["CloudTrail 生成评估报告，Audit Manager 记录每一次 API 调用", "CloudTrail 记录账户活动，Audit Manager 把证据映射到审计控件并生成评估", "两者功能相同，只是区域不同", "Audit Manager 只能用于账单争议"],
       1,
       "正确答案：\n\nCloudTrail 提供活动记录；Audit Manager 用这些及其他数据源做合规评估。\n\n错误选项分析：\n\n「A.」把两者职责说反了。\n\n「C. 功能相同」是错误。\n\n「D. 只能用于账单争议」是错误：那不是 Audit Manager 的定位。\n\n重点考点：\n- 日志 vs 审计评估",
       D2),

    # ----- Inspector + Config -----
    _s(10, "Amazon Inspector",
       "哪项服务会自动扫描 Amazon EC2 和容器镜像等，查找软件漏洞与意外网络暴露？",
       ["Amazon GuardDuty", "Amazon Inspector", "AWS Config", "AWS WAF"],
       1,
       "正确答案：\n\nInspector 做漏洞和网络可达性扫描。\n\n错误选项分析：\n\n「A. GuardDuty」是错误：智能威胁检测（异常/可疑活动），不是 CVE 扫描器。\n\n「C. Config」是错误：记录配置并评估是否符合规则。\n\n「D. WAF」是错误：Web 应用防火墙。\n\n重点考点：\n- Inspector = 漏洞/暴露扫描\n- GuardDuty = 威胁检测",
       D2),
    _s(11, "AWS Config",
       "哪项服务持续记录 AWS 资源的配置变更，并能用规则评估这些配置是否符合企业或监管要求？",
       ["AWS CloudTrail", "AWS Config", "Amazon Inspector", "AWS Compute Optimizer"],
       1,
       "正确答案：\n\nConfig 是配置历史 + 合规规则引擎。\n\n错误选项分析：\n\n「A. CloudTrail」是错误：谁在何时调用了 API，不是资源当前/历史配置快照。\n\n「C. Inspector」是错误：漏洞扫描。\n\n「D. Compute Optimizer」是错误：实例规格建议。\n\n重点考点：\n- Config = 配置记录与合规评估",
       D2),
    _m(2, "Amazon Inspector / AWS Config",
       "安全团队要同时做「工作负载漏洞分析」和「资源配置是否持续合规」。应组合哪些服务？（选择两项）",
       ["Amazon Inspector", "AWS Trusted Advisor", "AWS Batch", "Amazon ECS", "AWS Config"],
       [0, 4],
       "正确答案：\n\nInspector 负责漏洞/暴露分析，Config 负责配置合规。二者常一起出现在安全分析与合规审计场景。\n\n错误选项分析：\n\n「B. Trusted Advisor」是错误：高层次建议清单，不是专用漏洞扫描或配置库存。\n\n「C. Batch」是错误：批处理计算。\n\n「D. ECS」是错误：容器编排，不是审计工具。\n\n重点考点：\n- 安全分析 + 合规审计 ≈ Inspector + Config\n- 不要选计算/编排服务来「做审计」",
       D2),

    # ----- Professional Services + APN -----
    _s(12, "AWS 专业服务",
       "企业要把一套复杂遗留应用迁上云，希望 AWS 专家团队帮忙评估现状并给出迁移方案。应优先联系？",
       ["AWS 专业服务 (AWS Professional Services)", "Amazon Inspector", "AWS Secrets Manager", "AWS Systems Manager"],
       0,
       "正确答案：\n\nProfessional Services 是 AWS 的咨询/专家团队，协助迁移与转型。\n\n错误选项分析：\n\n「B. Inspector」是错误：漏洞扫描。\n\n「C. Secrets Manager」是错误：保管密钥。\n\n「D. Systems Manager」是错误：运维枢纽（补丁、清单、会话等），不是迁移评估咨询。\n\n重点考点：\n- 迁云评估：人/伙伴，不是运维工具",
       D1),
    _s(13, "AWS 合作伙伴网络",
       "公司希望由具备 AWS 能力认证的第三方系统集成商来评估并实施迁云。应通过什么网络寻找这类合作伙伴？",
       ["AWS Marketplace Seller 计划", "AWS 合作伙伴网络 (APN)", "AWS IQ 仅限内部员工", "Amazon Mechanical Turk"],
       1,
       "正确答案：\n\nAPN（现常称 AWS Partner Network）汇集咨询与技术合作伙伴。\n\n错误选项分析：\n\n「A. Marketplace Seller」是错误：卖软件产品，不是找实施迁云的 SI。\n\n「C. AWS IQ 仅限内部员工」是错误：IQ 是找独立专家的市场，题干强调有能力认证的伙伴网络。\n\n「D. Mechanical Turk」是错误：众包人力。\n\n重点考点：\n- 迁云评估：APN 合作伙伴",
       D1),
    _m(3, "迁移评估",
       "评估应用程序能否以及如何迁到 AWS 时，下列哪些资源最直接有帮助？（选择两项）",
       ["AWS Trusted Advisor 的服务限额检查", "AWS 专业服务", "AWS Systems Manager Session Manager", "AWS 合作伙伴网络 (APN)", "AWS Secrets Manager"],
       [1, 3],
       "正确答案：\n\n专业服务团队与 APN 合作伙伴专门做迁移评估与实施。\n\n错误选项分析：\n\n「A. Trusted Advisor 服务限额」是错误：限额提醒帮不了应用迁云可行性评估。\n\n「C. Session Manager」是错误：安全登录实例。\n\n「E. Secrets Manager」是错误：密钥管理。\n\n重点考点：\n- 迁云评估 = Professional Services + APN\n- 不要选运维/密钥类服务",
       D1),

    # ----- Compute Optimizer -----
    _s(14, "AWS Compute Optimizer",
       "哪项服务会分析 Amazon EC2 的配置和利用率指标，并推荐更合适的实例类型？",
       ["Amazon Inspector", "AWS Compute Optimizer", "AWS Config", "AWS Cost Explorer"],
       1,
       "正确答案：\n\nCompute Optimizer 基于 CloudWatch 利用率等指标做权利化（rightsizing）建议。\n\n错误选项分析：\n\n「A. Inspector」是错误：安全漏洞，不是规格建议。\n\n「C. Config」是错误：配置合规。\n\n「D. Cost Explorer」是错误：看花费趋势、可做预留建议，但不分析 EC2 利用率来推荐实例类型。\n\n重点考点：\n- Compute Optimizer = 利用率 → 实例类型建议\n- Cost Explorer = 成本可视化，不是规格引擎",
       D4),
    _s(15, "AWS Compute Optimizer",
       "FinOps 希望根据 CPU/内存利用率把一批过大的 EC2 换成更小规格。哪项服务最贴合？",
       ["AWS Budgets", "AWS Compute Optimizer", "Amazon CloudWatch Alarms 本身", "AWS Pricing Calculator"],
       1,
       "正确答案：\n\nCompute Optimizer 专门做计算资源权利化建议。\n\n错误选项分析：\n\n「A. Budgets」是错误：预算告警。\n\n「C. CloudWatch Alarms」是错误：告警机制，不会系统性地推荐实例族/大小。\n\n「D. Pricing Calculator」是错误：估算未来成本，不读取你账户里的实际利用率。\n\n重点考点：\n- 权利化 → Compute Optimizer",
       D4),
    _s(16, "AWS Compute Optimizer",
       "为什么「用 Amazon Inspector 来推荐 EC2 实例类型」是错误做法？",
       ["Inspector 只能扫描 Lambda，不能看 EC2", "Inspector 关注漏洞与网络暴露，不基于利用率推荐规格", "Inspector 已更名为 Compute Optimizer", "Inspector 只能在 GovCloud 使用"],
       1,
       "正确答案：\n\nInspector 是安全扫描；规格建议是 Compute Optimizer。\n\n错误选项分析：\n\n「A. 只能扫描 Lambda」是错误：Inspector 也覆盖 EC2/ECR 等。\n\n「C. 已更名」是错误：两个独立服务。\n\n「D. 只能 GovCloud」是错误。\n\n重点考点：\n- 易混：Inspector ≠ Compute Optimizer ≠ Cost Explorer",
       D4),

    # ----- Performance efficiency -----
    _s(17, "性能效率",
       "Well-Architected「性能效率」支柱强调：尽量让 AWS 替你管理底层，用什么架构方式最能体现这一点？",
       ["在所有层应用最小权限", "使用无服务器架构", "启用账户级 CloudTrail 审计日志", "删除所有安全组规则以降低延迟"],
       1,
       "正确答案：\n\n无服务器让 AWS 承担容量、扩展与底层运维，是性能效率的典型实践。\n\n错误选项分析：\n\n「A. 最小权限」是错误：这是安全支柱。\n\n「C. 审计日志」是错误：安全/合规。\n\n「D. 删除安全组」是错误：牺牲安全换延迟，不是支柱建议。\n\n重点考点：\n- 性能效率：无服务器、托管服务、全球化\n- 安全实践不要答进性能效率",
       D1),
    _s(18, "性能效率",
       "为了让全球用户获得更低延迟，性能效率支柱常建议采用哪种做法？",
       ["只在一个可用区部署，避免跨 AZ 流量", "构建多区域架构以更好服务全球客户", "把所有对象存储改成实例存储", "关闭 CloudFront 以免缓存过期"],
       1,
       "正确答案：\n\n多区域（以及边缘网络）让计算和内容更靠近用户。\n\n错误选项分析：\n\n「A. 单 AZ」是错误：那损害可用性，也不解决全球延迟。\n\n「C. 实例存储」是错误：临时盘，不是全球加速方案。\n\n「D. 关闭 CloudFront」是错误：CDN 正是降延迟的手段。\n\n重点考点：\n- 性能效率：Go global in minutes / 多区域",
       D1),
    _m(4, "性能效率",
       "下列哪些设计原则属于 AWS Well-Architected 的性能效率？（选择两项）",
       ["构建多区域架构，更好服务全球客户", "在所有层应用安全性", "实施强大的身份和访问控制", "使用无服务器架构", "启用审核日志记录"],
       [0, 3],
       "正确答案：\n\n全球化（多区域）与无服务器是性能效率支柱的典型原则。\n\n错误选项分析：\n\n「B. 在所有层应用安全性」是错误：安全支柱。\n\n「C. 身份和访问控制」是错误：安全支柱。\n\n「E. 审核日志」是错误：安全/合规。\n\n重点考点：\n- 性能效率 ≠ 安全\n- 看到「全层安全 / IAM / 审计日志」就不要选进性能效率",
       D1),
]

