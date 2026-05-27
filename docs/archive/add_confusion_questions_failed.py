#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Add new high-frequency confusion/comparison questions (S122-S129 + M90-M95)
Targeted at the gaps identified in the keyword audit (especially section 5).
"""

import ast
import os
from datetime import datetime

# ============== NEW SINGLE CHOICE QUESTIONS (S122 - S129) ==============

NEW_SINGLE = [
    {
        "id": "S122",
        "question": "关于 AWS KMS 中的 Customer Managed Key (CMK) 与 AWS Managed Key，以下哪项说法是正确的？",
        "options": [
            "A. 两者都由 AWS 自动管理密钥轮换，客户无法干预",
            "B. Customer Managed Key 允许客户控制密钥策略、轮换计划和删除操作",
            "C. AWS Managed Key 可以被客户随时禁用或删除",
            "D. CMK 仅用于 S3 服务，AWS Managed Key 用于所有其他服务"
        ],
        "correct_answers": ["B"],
        "explanation": "「Customer Managed Key 允许客户控制密钥策略、轮换计划和删除操作」是正确的。\n\nCustomer Managed Key (CMK) 由客户创建和管理，客户可以定义密钥策略、启用/禁用自动轮换（每年一次）、手动轮换、禁用或删除密钥。而 AWS Managed Key 由 AWS 创建和管理，客户对策略和轮换没有控制权。\n\n其他选项分析：\n\n「两者都由 AWS 自动管理密钥轮换」是错误的：只有 CMK 支持客户控制轮换。\n\n「AWS Managed Key 可以被客户随时禁用或删除」是错误的：AWS Managed Key 客户无法删除或永久禁用。\n\n「CMK 仅用于 S3 服务」是错误的：CMK 可用于多种 AWS 服务（S3、EBS、RDS、Lambda 等）。\n\n**重点考点 / 关键词补充：**\n- CMK（客户托管密钥）：客户完全控制策略、轮换、删除\n- AWS Managed Key：AWS 托管，客户无控制权\n- 自动轮换：CMK 支持每年自动轮换，AWS Managed Key 由 AWS 决定\n-  Envelope Encryption：KMS 始终使用 envelope 加密模式",
        "domain": "Security and Compliance"
    },
    {
        "id": "S123",
        "question": "在 S3 Object Lock 中，Compliance 模式和 Governance 模式的主要区别是什么？",
        "options": [
            "A. Compliance 模式下 Root 用户可以修改保留期，Governance 模式则完全不可修改",
            "B. Compliance 模式下任何用户（包括 Root）在保留期内都无法删除或覆盖对象，Governance 模式允许特定权限的用户修改保留期或提前删除",
            "C. 两者完全相同，只是命名不同",
            "D. Governance 模式仅用于合规审计，Compliance 模式用于日常备份"
        ],
        "correct_answers": ["B"],
        "explanation": "「Compliance 模式下任何用户（包括 Root）在保留期内都无法删除或覆盖对象，Governance 模式允许特定权限的用户修改保留期或提前删除」是正确的。\n\n这是 S3 Object Lock 两种保留模式的经典区别：Compliance 模式极其严格（满足 SEC、FINRA 等最严监管），连 Root 用户也无法在保留期内删除或缩短保留期；Governance 模式相对灵活，拥有 s3:BypassGovernanceRetention 权限的用户可以修改保留设置或提前删除。\n\n其他选项分析：\n\n「Compliance 模式下 Root 用户可以修改保留期」是错误的：Compliance 模式下 Root 也无权修改。\n\n「两者完全相同」是错误的：两者权限控制强度差异极大。\n\n「Governance 模式仅用于合规审计」是错误的：Governance 更适合需要一定灵活性的内部合规场景。\n\n**重点考点 / 关键词补充：**\n- Object Lock 两种模式：Compliance（最严格） vs Governance（可绕过）\n- Compliance：任何人（含 Root）都无法删除/缩短保留期\n- Governance：拥有 s3:BypassGovernanceRetention 权限的用户可修改\n- 常考：Compliance 用于金融、医疗等强监管场景",
        "domain": "Security and Compliance"
    },
    {
        "id": "S124",
        "question": "启用 S3 Block Public Access 后，以下哪种情况仍然可能发生？",
        "options": [
            "A. 存储桶策略允许公共读取某个对象",
            "B. ACL 设置为 public-read 的对象可被匿名访问",
            "C. 存储桶本身对互联网完全不可访问",
            "D. 通过预签名 URL（Presigned URL）临时访问私有对象"
        ],
        "correct_answers": ["D"],
        "explanation": "「通过预签名 URL（Presigned URL）临时访问私有对象」是正确的。\n\nS3 Block Public Access 主要阻止通过存储桶策略、ACL 或公开 URL 的公共访问，但不影响合法的预签名 URL（使用签名凭证的临时访问）。预签名 URL 是私有对象授权访问的标准方式，不属于“公共访问”。\n\n其他选项分析：\n\n「存储桶策略允许公共读取」是错误的：Block Public Access 会阻止此类公共访问，即使策略允许。\n\n「ACL 设置为 public-read」是错误的：Block Public Access 会忽略或阻止公共 ACL。\n\n「存储桶本身对互联网完全不可访问」是错误的：Block Public Access 仅阻止公共访问，私有访问和授权访问仍然正常。\n\n**重点考点 / 关键词补充：**\n- Block Public Access：阻止公共访问（存储桶策略 + ACL + 公开 URL）\n- 不影响：预签名 URL、私有访问、授权访问\n- 推荐：对所有存储桶默认开启，尤其是生产环境\n- 四个设置：BlockPublicAcls、IgnorePublicAcls、BlockPublicPolicy、RestrictPublicBuckets",
        "domain": "Security and Compliance"
    },
    {
        "id": "S125",
        "question": "AWS Wavelength Zones 主要用于解决哪类场景的延迟问题？",
        "options": [
            "A. 全球静态内容分发",
            "B. 5G 边缘计算和超低延迟应用（如 AR/VR、自动驾驶、工业物联网）",
            "C. 跨 Region 灾难恢复",
            "D. 大规模批处理计算任务"
        ],
        "correct_answers": ["B"],
        "explanation": "「5G 边缘计算和超低延迟应用（如 AR/VR、自动驾驶、工业物联网）」是正确的。\n\nWavelength Zones 是 AWS 与电信运营商合作，在 5G 网络边缘部署的 AWS 基础设施扩展，允许客户将应用部署到极靠近移动用户的 5G 边缘，从而实现毫秒级超低延迟，特别适合 5G 时代对延迟极度敏感的应用。\n\n其他选项分析：\n\n「全球静态内容分发」是错误的：这是 Edge Locations + CloudFront 的场景。\n\n「跨 Region 灾难恢复」是错误的：Wavelength Zones 不用于 DR，主要解决边缘延迟。\n\n「大规模批处理计算任务」是错误的：批处理更适合 Spot + 普通 Region 或 Outposts。\n\n**重点考点 / 关键词补充：**\n- Wavelength Zones：AWS + 电信 5G 边缘基础设施\n- 核心价值：5G 超低延迟（<10ms）\n- 典型场景：AR/VR、游戏、自动驾驶、实时工业控制\n- 与 Local Zones 区别：Wavelength 更靠近移动用户（5G 边缘），Local Zones 靠近固定人口中心",
        "domain": "Cloud Concepts"
    },
    {
        "id": "S126",
        "question": "以下哪些 AWS 服务是 Global（全球）级别的服务？（注意：题目为单选，选出最准确的描述）",
        "options": [
            "A. Amazon S3 存储桶和 Amazon EC2 实例",
            "B. AWS IAM、Amazon CloudFront 和 Amazon Route 53",
            "C. Amazon RDS 和 Amazon DynamoDB 表",
            "D. AWS Lambda 函数和 Amazon EBS 卷"
        ],
        "correct_answers": ["B"],
        "explanation": "「AWS IAM、Amazon CloudFront 和 Amazon Route 53」是正确的。\n\nIAM（身份与访问管理）、CloudFront（CDN）和 Route 53（DNS）是典型的 Global 级别服务：其配置和资源不绑定特定 Region，在 AWS 全球范围内生效或可用。而 S3 桶、EC2、RDS、Lambda 等绝大多数资源都是 Region 级别的。\n\n其他选项分析：\n\n「Amazon S3 存储桶和 Amazon EC2 实例」是错误的：两者都是 Region 级资源（S3 桶名全局唯一但存储在特定 Region）。\n\n「Amazon RDS 和 Amazon DynamoDB 表」是错误的：都是 Region 级服务。\n\n「AWS Lambda 函数和 Amazon EBS 卷」是错误的：都是 Region 级资源。\n\n**重点考点 / 关键词补充：**\n- Global 服务典型代表：IAM、CloudFront、Route 53、AWS Organizations、AWS Artifact\n- Region 级服务：EC2、S3、RDS、Lambda、DynamoDB、EBS 等绝大多数\n- 考试常考：IAM 用户/角色/策略是 Global 的，但 EC2 实例是 Region 的\n- S3 桶名全局唯一，但实际数据位于特定 Region",
        "domain": "Cloud Concepts"
    },
    {
        "id": "S127",
        "question": "当 Spot Instance 被中断时，AWS 会提前多久发出通知？中断后 EBS 根卷数据通常会如何处理？",
        "options": [
            "A. 提前 5 分钟通知，EBS 根卷数据会立即丢失",
            "B. 提前 2 分钟通知，EBS 根卷数据默认会保留（除非设置了删除策略）",
            "C. 没有提前通知，实例直接被终止且所有数据丢失",
            "D. 提前 30 分钟通知，EBS 数据会自动备份到 S3"
        ],
        "correct_answers": ["B"],
        "explanation": "「提前 2 分钟通知，EBS 根卷数据默认会保留（除非设置了删除策略）」是正确的。\n\nAWS Spot Instance 中断时通常会提前 2 分钟通过 EC2 实例元数据和 EventBridge 发出中断通知。EBS 根卷（以及附加的 EBS 卷）数据默认会在实例终止后保留（与 On-Demand 行为一致），除非在启动模板或 API 中明确设置了 DeleteOnTermination=true。\n\n其他选项分析：\n\n「提前 5 分钟通知」是错误的：标准是 2 分钟。\n\n「没有提前通知」是错误的：AWS 会提供中断通知以便应用做优雅退出。\n\n「EBS 数据会自动备份到 S3」是错误的：不会自动备份，需要客户自己处理。\n\n**重点考点 / 关键词补充：**\n- Spot 中断通知：提前 2 分钟（通过 instance metadata + EventBridge）\n- EBS 根卷：默认保留（DeleteOnTermination 默认为 false）\n- 实例存储（ephemeral）：中断时数据会丢失\n- 最佳实践：使用 Checkpointing、队列、Auto Scaling 组处理中断",
        "domain": "Technology and Services"
    },
    {
        "id": "S128",
        "question": "CloudWatch、CloudTrail 和 AWS Config 在监控与审计方面的主要职责区别是什么？",
        "options": [
            "A. 三者功能完全相同，只是名称不同",
            "B. CloudWatch 负责性能指标和告警，CloudTrail 负责记录 API 调用审计日志，Config 负责记录资源配置变更和合规评估",
            "C. CloudTrail 负责性能监控，Config 负责安全补丁管理",
            "D. CloudWatch 仅用于日志收集，Config 用于成本监控"
        ],
        "correct_answers": ["B"],
        "explanation": "「CloudWatch 负责性能指标和告警，CloudTrail 负责记录 API 调用审计日志，Config 负责记录资源配置变更和合规评估」是正确的。\n\n这是 CLF-C02 最经典的三者对比：\n- CloudWatch：Metrics（性能数据）、Alarms（告警）、Logs（日志收集分析）\n- CloudTrail：记录所有 AWS API 调用（谁、在何时、对什么资源做了什么操作），用于审计和安全分析\n- AWS Config：持续记录资源配置变更历史，并可进行合规规则评估（如“所有 S3 桶是否开启加密”）\n\n其他选项分析：\n\n「三者功能完全相同」是错误的：职责完全不同。\n\n「CloudTrail 负责性能监控」是错误的：CloudTrail 不做性能指标。\n\n「CloudWatch 仅用于日志收集」是错误的：CloudWatch 核心是 Metrics + Alarms。\n\n**重点考点 / 关键词补充：**\n- CloudWatch：性能 + 告警 + 日志（Metrics, Alarms, Logs）\n- CloudTrail：API 调用审计日志（Who, What, When）\n- Config：资源配置变更历史 + 合规规则评估\n- 常考组合：CloudTrail + Config 一起用于安全合规审计",
        "domain": "Technology and Services"
    },
    {
        "id": "S129",
        "question": "关于 AWS 数据传输费用，以下哪种场景通常是免费或费用最低的？",
        "options": [
            "A. 从 AWS 某个 Region 向互联网传输大量数据",
            "B. 同一 Region 内两个不同 Availability Zone 之间的数据传输",
            "C. 从一个 Region 复制数据到另一个 Region",
            "D. 通过互联网将数据上传到 S3（入方向）"
        ],
        "correct_answers": ["B"],
        "explanation": "「同一 Region 内两个不同 Availability Zone 之间的数据传输」是正确的。\n\nAWS 定价规则：同一 Region 内 AZ 之间的数据传输通常免费或费用极低（部分服务有极低收费）。而跨 Region 传输和出互联网流量则收费较高。入互联网流量（上传到 AWS）大多数情况下是免费的。\n\n其他选项分析：\n\n「从 AWS 某个 Region 向互联网传输」是错误的：出方向流量收费，且通常较贵。\n\n「从一个 Region 复制数据到另一个 Region」是错误的：跨 Region 数据传输通常收费最高。\n\n「通过互联网将数据上传到 S3」是错误的：入方向大多免费，但题目问的是“最低”，AZ 内传输更接近零成本。\n\n**重点考点 / 关键词补充：**\n- 入互联网 → AWS：大多免费\n- 同 Region AZ 间：通常免费或极低\n- 跨 Region：收费（通常最贵）\n- 出互联网：收费\n- 优化建议：善用 CloudFront、Direct Connect、同一 Region 部署减少跨 Region 流量",
        "domain": "Billing, Pricing, and Support"
    }
]

# ============== NEW MULTI CHOICE QUESTIONS (M90 - M95) ==============

NEW_MULTI = [
    {
        "id": "M90",
        "question": "以下哪些服务与描述的匹配是正确的？（选择三项）",
        "options": [
            "A. Amazon GuardDuty —— 智能威胁检测服务，自动分析 CloudTrail、VPC Flow Logs 等发现异常",
            "B. AWS Inspector —— 针对 EC2 实例和容器镜像的漏洞评估与安全扫描",
            "C. Amazon Macie —— 使用机器学习发现和保护 S3 中的敏感数据（如 PII）",
            "D. AWS Security Hub —— 提供对 EC2 实例的实时性能监控和告警",
            "E. AWS WAF —— 集中收集和分析跨多个 AWS 账户的安全数据"
        ],
        "correct_answers": ["A", "B", "C"],
        "explanation": "正确答案：\n\n「Amazon GuardDuty —— 智能威胁检测」\n「AWS Inspector —— 漏洞评估与安全扫描」\n「Amazon Macie —— 发现和保护 S3 中的敏感数据」\n\n错误选项分析：\n\n「AWS Security Hub —— 提供对 EC2 实例的实时性能监控」是错误的：Security Hub 是安全态势聚合与管理平台，不是性能监控（那是 CloudWatch）。\n\n「AWS WAF —— 集中收集和分析跨多个 AWS 账户的安全数据」是错误的：WAF 是 Web 应用防火墙，负责过滤恶意 HTTP 请求；跨账户安全数据聚合是 Security Hub 的职责。\n\n**重点考点 / 关键词补充：**\n- GuardDuty：威胁检测（无代理，分析日志）\n- Inspector：漏洞扫描（EC2 + 容器镜像）\n- Macie：S3 敏感数据发现（ML）\n- Security Hub：安全态势管理 + 聚合多个安全服务发现\n- 常考陷阱：不要把 Security Hub 当成性能监控工具",
        "domain": "Security and Compliance"
    },
    {
        "id": "M91",
        "question": "关于 CloudWatch、CloudTrail 和 AWS Config 的职责，以下哪些说法是正确的？（选择三项）",
        "options": [
            "A. CloudWatch 可以设置告警，当 CPU 使用率超过阈值时自动触发 Auto Scaling",
            "B. CloudTrail 可以记录 IAM 用户在控制台或 API 中执行的所有操作，用于安全审计和取证",
            "C. AWS Config 可以持续跟踪 EC2 安全组规则的历史变更，并在配置偏离合规策略时告警",
            "D. CloudTrail 主要用于收集应用程序的业务日志和性能指标",
            "E. AWS Config 可以替代 CloudWatch 实现对 EC2 实例 CPU 和内存的实时监控"
        ],
        "correct_answers": ["A", "B", "C"],
        "explanation": "正确答案：\n\n「CloudWatch 可以设置告警...自动触发 Auto Scaling」\n「CloudTrail 可以记录 IAM 用户...所有操作」\n「AWS Config 可以持续跟踪...历史变更」\n\n错误选项分析：\n\n「CloudTrail 主要用于收集应用程序的业务日志」是错误的：CloudTrail 只记录 AWS 控制平面 API 调用，不记录应用业务日志（应用日志用 CloudWatch Logs）。\n\n「AWS Config 可以替代 CloudWatch 实现...实时监控」是错误的：Config 不做性能指标实时监控，它关注配置变更历史。\n\n**重点考点 / 关键词补充：**\n- CloudWatch：性能指标 + 告警 + 应用/系统日志\n- CloudTrail：AWS API 调用审计（Who/What/When）\n- Config：资源配置漂移检测 + 合规规则评估\n- 经典组合：CloudTrail + Config 用于安全合规，CloudWatch 用于运维告警",
        "domain": "Technology and Services"
    },
    {
        "id": "M92",
        "question": "以下关于 AWS 存储服务的适用场景描述，哪些是正确的？（选择三项）",
        "options": [
            "A. Amazon EFS 适合多个 EC2 实例需要同时读写同一文件系统的场景（如内容管理系统、开发环境）",
            "B. Amazon EBS 适合需要低延迟块存储的单实例数据库或需要高 IOPS 的应用",
            "C. Amazon S3 适合存储非结构化数据、备份、静态网站和作为数据湖",
            "D. Amazon FSx for Windows 适合运行 Windows 应用且需要原生 SMB 支持的场景",
            "E. Amazon S3 适合作为 EC2 实例的根卷启动磁盘"
        ],
        "correct_answers": ["A", "B", "C", "D"],
        "explanation": "正确答案：\n\n「Amazon EFS 适合多个 EC2 实例需要同时读写同一文件系统」\n「Amazon EBS 适合需要低延迟块存储的单实例数据库」\n「Amazon S3 适合存储非结构化数据、备份、静态网站」\n「Amazon FSx for Windows 适合运行 Windows 应用且需要原生 SMB 支持」\n\n错误选项分析：\n\n「Amazon S3 适合作为 EC2 实例的根卷启动磁盘」是错误的：S3 是对象存储，不能作为 EC2 根卷；根卷必须使用 EBS（或实例存储）。\n\n**重点考点 / 关键词补充：**\n- S3：对象存储，海量非结构化数据、备份、数据湖、静态网站\n- EBS：块存储，单实例低延迟（数据库、OS 卷）\n- EFS：托管 NFS，跨多实例共享文件系统\n- FSx：托管 Windows 文件系统（SMB）或 Lustre（高性能计算）\n- 常考：S3 不能做 EC2 根卷或需要 POSIX 语义的共享文件系统",
        "domain": "Technology and Services"
    },
    {
        "id": "M93",
        "question": "关于 AWS 灾难恢复（DR）策略，以下哪些描述与策略名称匹配正确？（选择三项）",
        "options": [
            "A. Pilot Light：核心基础设施（如数据库）在备用 Region 持续运行，应用层在故障时才启动",
            "B. Warm Standby：备用 Region 运行缩减版的完整生产环境，故障时快速扩容接管流量",
            "C. Multi-Site Active/Active：多个 Region 同时处理生产流量，故障时几乎零停机切换",
            "D. Backup and Restore：最便宜的方案，仅在故障时才从备份恢复整个环境",
            "E. Warm Standby：在故障发生前所有 Region 都完全不运行任何资源"
        ],
        "correct_answers": ["A", "B", "C", "D"],
        "explanation": "正确答案：\n\n「Pilot Light：核心基础设施在备用 Region 持续运行」\n「Warm Standby：运行缩减版的完整生产环境」\n「Multi-Site Active/Active：多个 Region 同时处理生产流量」\n「Backup and Restore：最便宜的方案」\n\n错误选项分析：\n\n「Warm Standby：在故障发生前所有 Region 都完全不运行任何资源」是错误的：这是 Backup and Restore 的特点，Warm Standby 是有缩减版系统在运行的。\n\n**重点考点 / 关键词补充：**\n- Backup & Restore：RTO/RPO 最高，成本最低\n- Pilot Light：核心服务运行，应用层待命（中等 RTO）\n- Warm Standby：缩减版完整系统运行（较低 RTO）\n- Multi-Site Active/Active：RTO 接近 0，成本最高\n- 考试常考：根据 RTO/RPO 要求选择合适策略",
        "domain": "Cloud Concepts"
    },
    {
        "id": "M94",
        "question": "以下关于 AWS 全球基础设施补充形式的描述，哪些是正确的？（选择三项）",
        "options": [
            "A. Local Zones 部署在靠近大型人口中心的位置，允许运行完整的 EC2、EBS、RDS 等服务",
            "B. Wavelength Zones 是与电信运营商合作的 5G 网络边缘基础设施，适合超低延迟移动应用",
            "C. AWS Outposts 是客户本地数据中心部署的 AWS 硬件，用于满足数据主权或低延迟要求",
            "D. Edge Locations 主要用于运行客户自定义的容器化应用和数据库",
            "E. Local Zones 和 Wavelength Zones 都属于 Region 的一部分，可以像普通 AZ 一样使用所有服务"
        ],
        "correct_answers": ["A", "B", "C"],
        "explanation": "正确答案：\n\n「Local Zones 部署在靠近大型人口中心...运行完整的 EC2、EBS、RDS」\n「Wavelength Zones 是与电信运营商合作的 5G 网络边缘」\n「AWS Outposts 是客户本地数据中心部署的 AWS 硬件」\n\n错误选项分析：\n\n「Edge Locations 主要用于运行客户自定义的容器化应用」是错误的：Edge Locations 主要用于 CloudFront 和 Global Accelerator 的内容缓存和加速，不运行通用计算服务。\n\n「Local Zones 和 Wavelength Zones 都属于 Region 的一部分」是错误的：它们是独立于标准 Region/AZ 的补充基础设施形式，使用方式和可用服务都有差异。\n\n**重点考点 / 关键词补充：**\n- Local Zones：靠近人口中心，低延迟运行完整 AWS 服务\n- Wavelength Zones：5G 边缘，超低延迟移动场景\n- Outposts：本地部署 AWS 硬件（混合云）\n- Edge Locations：全球内容分发节点（数量最多）\n- 核心仍是 Region + AZ，这三者是补充",
        "domain": "Cloud Concepts"
    },
    {
        "id": "M95",
        "question": "关于 IAM Permission Boundary 和 AWS Organizations SCP（Service Control Policies），以下哪些说法是正确的？（选择两项）",
        "options": [
            "A. Permission Boundary 是在单个 AWS 账户内为 IAM 用户或角色设置的权限上限",
            "B. SCP 是在 AWS Organizations 组织层面为成员账户设置的权限边界，即使 IAM 策略允许也不能超过",
            "C. Permission Boundary 可以扩大 IAM 实体的权限范围",
            "D. SCP 可以为单个 IAM 用户授予额外权限",
            "E. 两者都只能用于限制权限，不能用于授予权限"
        ],
        "correct_answers": ["A", "B", "E"],
        "explanation": "正确答案：\n\n「Permission Boundary 是在单个 AWS 账户内...设置的权限上限」\n「SCP 是在 AWS Organizations 组织层面...权限边界」\n「两者都只能用于限制权限，不能用于授予权限」\n\n错误选项分析：\n\n「Permission Boundary 可以扩大 IAM 实体的权限范围」是错误的：它只会设置上限（取交集），不会扩大权限。\n\n「SCP 可以为单个 IAM 用户授予额外权限」是错误的：SCP 只能在组织层面设置 Deny 限制，不能授予权限，也不能针对单个用户。\n\n**重点考点 / 关键词补充：**\n- Permission Boundary：账户内 IAM 实体（User/Role）的权限天花板\n- SCP：Organizations 层面针对整个账户/OU 的权限边界（Deny 优先）\n- 两者共同点：都只能限制、不能授予权限\n- 常考：SCP 影响整个账户，Permission Boundary 针对具体 IAM 实体",
        "domain": "Security and Compliance"
    }
]

def load_questions(path, var_name):
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    tree = ast.parse(content)
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign) and getattr(node.targets[0], "id", "") == var_name:
            return ast.literal_eval(node.value), content
    raise ValueError(f"Variable {var_name} not found in {path}")

def save_questions(path, var_name, questions, original_content):
    """
    Robust save: locate the final top-level ']' of the list assignment and insert
    new items before it. This preserves module docstring, encoding declaration, etc.
    """
    # Find the last occurrence of a line that is just "]" (or " ]") after the assignment
    # Strategy: find the position of the LAST "]" in the file that closes the list
    # We will rebuild the content up to the last item, add comma + new items, then ]
    
    lines = original_content.splitlines(keepends=True)
    
    # Find the last line that contains the closing of the list
    last_bracket_idx = None
    for i in range(len(lines)-1, -1, -1):
        stripped = lines[i].strip()
        if stripped == "]":
            last_bracket_idx = i
            break
    
    if last_bracket_idx is None:
        raise RuntimeError(f"Could not find closing ']' in {path}")
    
    # Rebuild content: everything up to (but not including) the final ]
    new_content = "".join(lines[:last_bracket_idx])
    
    # Ensure the previous item ends with a comma
    # (our existing files already have commas after each dict)
    # Now append the new questions
    for q in questions:
        # Use repr and clean up a bit for readability
        q_repr = repr(q)
        # Add proper indentation (4 spaces)
        indented = "    " + q_repr.replace("\n", "\n    ") + ",\n"
        new_content += indented
    
    # Close the list
    new_content += "]\n"
    
    with open(path, "w", encoding="utf-8") as f:
        f.write(new_content)
    
    print(f"Updated {path} with {len(questions)} new questions")

def main():
    print("Adding new confusion/comparison questions...")
    
    # Single choice
    single_qs, single_orig = load_questions("data/single_choice.py", "SINGLE_CHOICE_QUESTIONS")
    print(f"Current single: {len(single_qs)}")
    single_qs.extend(NEW_SINGLE)
    save_questions("data/single_choice.py", "SINGLE_CHOICE_QUESTIONS", single_qs, single_orig)
    
    # Multi choice
    multi_qs, multi_orig = load_questions("data/multi_choice.py", "MULTI_CHOICE_QUESTIONS")
    print(f"Current multi: {len(multi_qs)}")
    multi_qs.extend(NEW_MULTI)
    save_questions("data/multi_choice.py", "MULTI_CHOICE_QUESTIONS", multi_qs, multi_orig)
    
    print(f"\nDone. New totals: Single={len(single_qs)}, Multi={len(multi_qs)}")
    print("New IDs: S122-S129 and M90-M95")

if __name__ == "__main__":
    main()
