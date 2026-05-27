# -*- coding: utf-8 -*-
"""Single Choice Questions

Stable IDs: S01 ~ Sxxx (used for progress tracking & wrong book)"""

SINGLE_CHOICE_QUESTIONS = [
    {
        "id": "S01",
        "question": "AWS 全球基础设施中，Edge Location 主要用于什么目的？",
        "options": [
            "A. 提供跨 Region 的高可用性",
            "B. 缓存内容以降低全球用户延迟",
            "C. 托管关系型数据库",
            "D. 运行客户 EC2 实例",
        ],
        "correct_answers": [
            "B",
        ],
        "explanation": "「缓存内容以降低全球用户延迟」是正确的，因为 Edge Location 是 AWS 全球内容分发网络（CDN）和边缘服务的主要接入点，核心功能是就近缓存静态内容（图片、视频、CSS/JS 文件等），从而显著降低全球最终用户的访问延迟。\n\n其他选项分析：\n\n「提供跨 Region 的高可用性」是错误的：跨 Region 高可用主要依靠 Route 53、Global Accelerator 或多 Region 架构实现，Edge Location 本身不提供跨 Region 容灾能力。\n\n「托管关系型数据库」是错误的：这是 Amazon RDS、Aurora 等服务的职责，Edge Location 是内容分发节点，不托管数据库。\n\n「运行客户 EC2 实例」是错误的：EC2 实例运行在 Region 内的 Availability Zone，Edge Location 主要用于缓存和边缘加速，不用于运行通用计算实例。\n\n**重点考点 / 关键词补充：**\n- Edge Location ≠ Availability Zone ≠ Region\n- 主要服务：CloudFront、AWS Global Accelerator\n- 核心价值：降低延迟（Latency Reduction）+ 减轻源站负载",
        "domain": "Cloud Concepts",
    },
    {
        "id": "S02",
        "question": "水平扩展（Scale Out）和垂直扩展（Scale Up）的主要区别是什么？",
        "options": [
            "A. 水平扩展是增加实例数量，垂直扩展是升级单实例规格",
            "B. 两者都是通过增加计算资源来提升系统能力，只是实现方式不同",
            "C. 垂直扩展通常成本更低，且比水平扩展更容易实施",
            "D. 水平扩展主要适用于有状态应用，垂直扩展更适合无状态服务",
        ],
        "correct_answers": [
            "A",
        ],
        "explanation": "「水平扩展是增加实例数量，垂直扩展是升级单实例规格」是正确的。\n\n水平扩展（Scale Out）是通过增加实例数量来提升系统能力，垂直扩展（Scale Up）则是升级单个实例的规格（CPU、内存、存储）。水平扩展通常更具弹性、成本效益更高，尤其适合云原生无状态应用；垂直扩展适合有状态或难以水平扩展的传统应用。\n\n其他选项分析：\n\n「两者都是通过增加计算资源来提升系统能力，只是实现方式不同」是错误的：水平扩展和垂直扩展在成本模型、弹性、容错性、实施复杂度上有本质区别，并非只是实现方式不同。\n\n「垂直扩展通常成本更低，且比水平扩展更容易实施」是错误的：垂直扩展在达到一定规模后成本上升很快，且存在单点故障风险；水平扩展虽然初期更复杂，但长期更具成本效益和弹性。\n\n「水平扩展主要适用于有状态应用，垂直扩展更适合无状态服务」是错误的：实际情况完全相反。水平扩展特别适合无状态应用，垂直扩展通常用于难以水平拆分的有状态应用。\n\n**重点考点 / 关键词补充：**\n- 水平扩展（Scale Out / Horizontal Scaling）：增加实例数量\n- 垂直扩展（Scale Up / Vertical Scaling）：提升单实例规格\n- 云原生推荐优先水平扩展（弹性更好、容错性更高）",
        "domain": "Cloud Concepts",
    },
    {
        "id": "S03",
        "question": "AWS 推荐的“松耦合”架构原则主要带来什么好处？",
        "options": [
            "A. 所有组件必须使用相同的技术栈并同时发布",
            "B. 降低组件间依赖，单个组件故障不会拖垮整个系统",
            "C. 实现高可用架构必须选用最昂贵的硬件",
            "D. 所有服务组件都必须部署在同一台服务器内",
        ],
        "correct_answers": [
            "B",
        ],
        "explanation": "「降低组件间依赖，单个组件故障不会拖垮整个系统」是正确的。\n\n松耦合（Loose Coupling）是 AWS 推荐的架构原则之一，指系统各组件之间尽量减少直接依赖，通过消息队列、事件驱动、API 等间接方式通信。这样当某个组件故障时，不会拖垮整个系统，显著提高弹性和容错能力。\n\n其他选项分析：\n\n「所有组件必须使用相同的技术栈并同时发布」是错误的：松耦合正是为了支持不同组件使用不同技术、独立部署和独立发布。\n\n「实现高可用架构必须选用最昂贵的硬件」是错误的：松耦合通过架构设计实现高可用，通常可以用更普通、廉价的组件组合达到更好效果。\n\n「所有服务组件都必须部署在同一台服务器内」是错误的：松耦合正是为了支持分布式、多服务器、多组件架构，避免单点故障。\n\n**重点考点 / 关键词补充：**\n- 松耦合 vs 紧耦合\n- 实现手段：SQS、SNS、EventBridge、Step Functions、API Gateway\n- 好处：独立扩展、故障隔离、团队并行开发",
        "domain": "Cloud Concepts",
    },
    {
        "id": "S04",
        "question": "使用 On-Demand 实例相比预留实例的主要优势是什么？",
        "options": [
            "A. 在所有 EC2 购买选项中价格最低",
            "B. 无需任何前期承诺，按实际使用付费，灵活性最高",
            "C. 必须提前承诺至少 1 年或 3 年的使用量",
            "D. 实例的计算性能和网络稳定性明显更好",
        ],
        "correct_answers": [
            "B",
        ],
        "explanation": "「无需任何前期承诺，按实际使用付费，灵活性最高」是正确的。\n\nOn-Demand 实例无需任何前期承诺，按实际使用秒级计费，随时可以启动或停止，灵活性最高。这是大多数短期、测试、不可预测流量场景的默认选择。\n\n其他选项分析：\n\n「在所有 EC2 购买选项中价格最低」是错误的：On-Demand 实际上是价格最高的选项，Spot Instances 通常最便宜（但有中断风险）。\n\n「必须提前承诺至少 1 年或 3 年的使用量」是错误的：这是 Reserved Instances 和 Savings Plans 的典型特征，On-Demand 无需任何承诺。\n\n「实例的计算性能和网络稳定性明显更好」是错误的：购买选项不影响底层实例的性能或稳定性，性能由实例类型（t3, m5, c5 等）决定。\n\n**重点考点 / 关键词补充：**\n- On-Demand：最高灵活性，无承诺\n- 适合场景：开发测试、短期项目、流量波动大的工作负载\n- 对比：Spot（最便宜但可中断）、RI/Savings Plans（有承诺但折扣高）",
        "domain": "Cloud Concepts",
    },
    {
        "id": "S05",
        "question": "AWS Artifact 主要用于什么场景？",
        "options": [
            "A. 通过 AWS Marketplace 一键部署合规加固的第三方应用镜像",
            "B. 下载 AWS 合规报告、SOC、PCI、HIPAA 报告及 NDA/BAA 协议",
            "C. 在多个账户和 Region 中集中管理安全组规则和网络 ACL",
            "D. 实时查看并分析所有 AWS 服务的按需使用费用明细",
        ],
        "correct_answers": [
            "B",
        ],
        "explanation": "「下载 AWS 合规报告、SOC、PCI、HIPAA 报告及 NDA/BAA 协议」是正确的。\n\nAWS Artifact 是 AWS 的合规中心，提供各种官方合规报告（SOC、PCI DSS、HIPAA、ISO 等）、NDA/BAA 协议下载，以及合规性自助服务。对金融、医疗、政府等有严格合规要求的客户非常重要。\n\n其他选项分析：\n\n「通过 AWS Marketplace 一键部署合规加固的第三方应用镜像」是错误的：Marketplace 主要用于购买和部署第三方软件/AMI，AWS Artifact 不提供应用部署功能。\n\n「在多个账户和 Region 中集中管理安全组规则和网络 ACL」是错误的：这是 AWS Firewall Manager 或 Security Hub + Config 的职责范围。\n\n「实时查看并分析所有 AWS 服务的按需使用费用明细」是错误的：费用明细和成本分析主要通过 AWS Cost Explorer、AWS Cost and Usage Report (CUR) 和 Billing Console 完成。\n\n**重点考点 / 关键词补充：**\n- Artifact 是“合规证明”的官方来源\n- 常见报告：SOC 1/2/3、PCI、HIPAA、FedRAMP\n- 支持下载 NDA（保密协议）和 BAA（商业伙伴协议）",
        "domain": "Security and Compliance",
    },
    {
        "id": "S06",
        "question": "多因素认证 (MFA) 在 AWS 中的主要作用是？",
        "options": [
            "A. 加速登录速度",
            "B. 即使密码泄露，没有第二因素也无法完成登录",
            "C. 替代所有权限控制",
            "D. 允许 Root 用户日常操作",
        ],
        "correct_answers": [
            "B",
        ],
        "explanation": "「即使密码泄露，没有第二因素也无法完成登录」是正确的。\n\n多因素认证（MFA）要求用户在输入密码后，还需要提供第二因素（通常是手机上的虚拟 MFA 设备或硬件密钥），即使密码泄露，攻击者也无法完成登录。这是保护 AWS 账户（尤其是 Root 和管理员用户）的最重要最佳实践之一。\n\n其他选项分析：\n\n「加速登录速度」是错误的：MFA 反而会增加登录步骤，目的是提高安全性。\n\n「替代所有权限控制」是错误的：MFA 只是身份验证手段，不能替代 IAM 权限策略。\n\n「允许 Root 用户日常操作」是错误的：强烈不推荐使用 Root 日常操作，更不应该只靠 MFA 保护 Root。\n\n**重点考点 / 关键词补充：**\n- MFA 是“多因素认证”的缩写\n- 推荐为所有 IAM 用户（尤其是拥有控制台访问权限的用户）启用\n- 硬件 MFA（YubiKey 等）安全性高于虚拟 MFA",
        "domain": "Security and Compliance",
    },
    {
        "id": "S07",
        "question": "当 EC2 实例需要访问 S3 时，以下哪种方式最符合安全最佳实践？",
        "options": [
            "A. 把 Access Key 硬编码在代码里",
            "B. 将具有最小权限的 IAM Role 附加到 EC2 实例",
            "C. 使用 Root 用户凭证",
            "D. 把 S3 存储桶设为公开",
        ],
        "correct_answers": [
            "B",
        ],
        "explanation": "「将具有最小权限的 IAM Role 附加到 EC2 实例」是正确的。\n\n将具有最小权限的 IAM Role 附加到 EC2 实例后，实例可以通过 Instance Metadata Service 自动获取临时凭证（每小时轮换），无需在代码中硬编码长期 Access Key，这是 AWS 强烈推荐的安全最佳实践。\n\n其他选项分析：\n\n「把 Access Key 硬编码在代码里」是错误的：这是严重的安全反模式，一旦代码泄露，凭证将永久暴露。\n\n「使用 Root 用户凭证」是错误的：Root 用户拥有全部权限，日常操作使用 Root 极度危险。\n\n「把 S3 存储桶设为公开」是错误的：这会让存储桶中的数据被任何人访问，严重违反安全原则。\n\n**重点考点 / 关键词补充：**\n- IAM Role + Instance Profile 是 EC2 访问其他 AWS 服务的推荐方式\n- 临时凭证自动轮换（通常 1 小时）\n- 配合最小权限策略（Least Privilege）使用",
        "domain": "Security and Compliance",
    },
    {
        "id": "S08",
        "question": "以下哪些 EC2 购买选项适合可中断、容错且对成本敏感的工作负载？",
        "options": [
            "A. On-Demand Instances",
            "B. Spot Instances",
            "C. Reserved Instances",
            "D. Savings Plans",
            "E. Dedicated Hosts",
        ],
        "correct_answers": [
            "B",
        ],
        "explanation": "「Spot Instances」是正确的。\n\nSpot Instances 使用 AWS 的富余容量，价格可比 On-Demand 低 90%，但实例可能被中断（通常提前 2 分钟通知）。非常适合可中断、容错设计良好的工作负载（如大数据处理、渲染、CI/CD 等）。\n\n其他选项分析：\n\n「On-Demand Instances」是错误的：On-Demand 价格最高，适合需要稳定运行的场景。\n\n「Reserved Instances」是错误的：RI 需要 1 年或 3 年承诺，适合稳定、长期负载。\n\n「Savings Plans」是错误的：Savings Plans 也需要承诺，适合有可预测计算用量的场景。\n\n「Dedicated Hosts」是错误的：Dedicated Host 价格最高，适合有物理服务器隔离或许可要求的工作负载。\n\n**重点考点 / 关键词补充：**\n- Spot Instance：最便宜，但可中断（2 分钟中断通知）\n- 适合场景：批处理、容器化、容错设计好的应用\n- 必须做好中断处理（Checkpointing、Queue、Auto Scaling 等）",
        "domain": "Technology and Services",
    },
    {
        "id": "S09",
        "question": "S3 Standard、S3 Standard-IA、S3 Glacier Deep Archive 在检索时间和成本上的正确描述是？",
        "options": [
            "A. Standard 最贵，Glacier Deep Archive 最便宜且检索最慢",
            "B. 三种存储类的存储费用和检索性能差异不大",
            "C. Glacier Deep Archive 同样支持毫秒级的快速数据检索",
            "D. Standard-IA 的存储成本高于 Standard 标准存储",
        ],
        "correct_answers": [
            "A",
        ],
        "explanation": "「Standard 最贵，Glacier Deep Archive 最便宜且检索最慢」是正确的。\n\nS3 Standard：频繁访问，毫秒级检索，成本最高。\nS3 Standard-IA：不频繁访问但需要快速检索（毫秒级），有最低 30 天存储要求。\nS3 Glacier Deep Archive：极低成本的长期归档，检索时间最长（12 小时+），适合几乎不访问的冷数据。\n\n其他选项分析：\n\n「三种存储类的存储费用和检索性能差异不大」是错误的：三种存储类的成本差异可达数十倍，检索时间从毫秒级到12小时以上，差异极大。\n\n「Glacier Deep Archive 同样支持毫秒级的快速数据检索」是错误的：Glacier Deep Archive 的检索时间通常为12小时甚至更长，专门用于极冷数据。\n\n「Standard-IA 的存储成本高于 Standard 标准存储」是错误的：Standard-IA 的存储费用明显低于 Standard，但有最低30天存储期限和取回费用。\n\n**重点考点 / 关键词补充：**\n- 访问频率越高 → 越适合 Standard\n- 几乎不访问 + 极致省钱 → Glacier Deep Archive\n- Standard-IA 适合“冷但偶尔要快速访问”的数据",
        "domain": "Technology and Services",
    },
    {
        "id": "S10",
        "question": "Amazon CloudFront 是一个什么类型的服务？",
        "options": [
            "A. 提供海量非结构化数据的对象存储服务",
            "B. 全球内容分发网络 (CDN)",
            "C. 托管兼容 MySQL 和 PostgreSQL 的关系型数据库",
            "D. 提供高吞吐量的分布式消息队列服务",
        ],
        "correct_answers": [
            "B",
        ],
        "explanation": "「全球内容分发网络 (CDN)」是正确的。\n\nAmazon CloudFront 是 AWS 提供的全球内容分发网络（CDN）服务，通过分布在全球的 Edge Location 缓存内容，显著降低用户访问延迟，同时减轻源站（S3、EC2 等）负载。\n\n其他选项分析：\n\n「提供海量非结构化数据的对象存储服务」是错误的：对象存储是 Amazon S3 的核心功能，CloudFront 是内容分发加速网络。\n\n「托管兼容 MySQL 和 PostgreSQL 的关系型数据库」是错误的：这是 Amazon RDS / Aurora 的职责范围。\n\n「提供高吞吐量的分布式消息队列服务」是错误的：消息队列服务对应 Amazon SQS、Amazon MQ 或 SNS。\n\n**重点考点 / 关键词补充：**\n- CloudFront = 全球 CDN\n- 主要功能：缓存加速、降低延迟、安全（WAF 集成）、边缘计算（Lambda@Edge）\n- 常见搭配：S3 + CloudFront（静态网站加速）",
        "domain": "Technology and Services",
    },
    {
        "id": "S11",
        "question": "在 VPC 中，NAT Gateway 的主要作用是什么？",
        "options": [
            "A. 允许私有子网实例访问互联网，同时隐藏其真实 IP",
            "B. 允许互联网直接访问私有子网实例",
            "C. 提供跨 Region 连接",
            "D. 自动分配公网 IP 给所有实例",
        ],
        "correct_answers": [
            "A",
        ],
        "explanation": "「允许私有子网实例访问互联网，同时隐藏其真实 IP」是正确的。\n\nNAT Gateway 允许私有子网中的 EC2 实例通过 NAT 网关访问互联网（出站），但互联网上的主机无法主动访问私有子网内的实例（入站被阻止），同时隐藏了实例的真实私有 IP。\n\n其他选项分析：\n\n「允许互联网直接访问私有子网实例」是错误的：这会破坏私有子网的安全隔离，NAT Gateway 恰恰防止这种访问。\n\n「提供跨 Region 连接」是错误的：跨 Region 连接通常使用 VPC Peering、Transit Gateway 或 Direct Connect。\n\n「自动分配公网 IP 给所有实例」是错误的：这是 Auto-assign Public IP 或 Elastic IP 的功能。\n\n**重点考点 / 关键词补充：**\n- NAT Gateway：有状态，支持数万并发连接\n- 替代方案：NAT Instance（已不推荐）\n- 配合：Private Subnet + Route Table 指向 NAT Gateway",
        "domain": "Technology and Services",
    },
    {
        "id": "S12",
        "question": "S3 Intelligent-Tiering 存储类的最大特点是什么？",
        "options": [
            "A. 需要用户定期分析访问模式并手动切换层级",
            "B. 自动根据访问模式在频繁和不频繁访问层之间移动数据",
            "C. 仅支持将对象存储在单个可用区",
            "D. 无论访问频率如何，检索费用都显著高于其他存储类",
        ],
        "correct_answers": [
            "B",
        ],
        "explanation": "「自动根据访问模式在频繁和不频繁访问层之间移动数据」是正确的。\n\nS3 Intelligent-Tiering 会自动监控对象的访问模式，在频繁访问层（Standard）和不频繁访问层（IA）之间自动移动数据，无需用户手动干预，特别适合访问模式不规律的数据。\n\n其他选项分析：\n\n「需要用户定期分析访问模式并手动切换层级」是错误的：Intelligent-Tiering 的核心价值就是完全自动化，无需任何手动操作或定期分析。\n\n「仅支持将对象存储在单个可用区」是错误的：Standard 和 Standard-IA 均采用多 AZ 持久化存储（One Zone-IA 才是单 AZ）。\n\n「无论访问频率如何，检索费用都显著高于其他存储类」是错误的：Intelligent-Tiering 的检索费用与所处层级一致，自动移动后会降低整体成本，并非一直更高。\n\n**重点考点 / 关键词补充：**\n- Intelligent-Tiering：AWS 推荐的“懒人”存储类\n- 自动在 Standard ↔ Standard-IA 之间移动\n- 适合：访问模式不稳定的数据、日志、备份等",
        "domain": "Technology and Services",
    },
    {
        "id": "S13",
        "question": "Amazon API Gateway 主要用于什么场景？",
        "options": [
            "A. 作为负载均衡器将流量分发到多个后端 EC2 实例和 Lambda 函数",
            "B. 创建、发布、维护、监控和保护 RESTful/WebSocket API",
            "C. 提供完全托管的 GraphQL API 和实时数据订阅能力",
            "D. 自动将入站 HTTP 请求转换为 Lambda 函数调用并处理返回结果",
        ],
        "correct_answers": [
            "B",
        ],
        "explanation": "「创建、发布、维护、监控和保护 RESTful/WebSocket API」是正确的。\n\nAmazon API Gateway 是 AWS 全托管的 API 管理服务，主要用于创建、发布、维护、监控和保护 RESTful API 和 WebSocket API。它支持身份验证（Cognito、IAM、Lambda Authorizer）、限流、缓存、监控、版本控制等功能。\n\n其他选项分析：\n\n「作为负载均衡器将流量分发到多个后端 EC2 实例和 Lambda 函数」是错误的：这是 Application Load Balancer (ALB) 或 API Gateway 本身可以集成的功能，但 API Gateway 的核心定位是 API 管理而非纯负载均衡。\n\n「提供完全托管的 GraphQL API 和实时数据订阅能力」是错误的：这是 AWS AppSync 的主要功能。\n\n「自动将入站 HTTP 请求转换为 Lambda 函数调用并处理返回结果」是错误的：这是 API Gateway 可以集成的能力，但其核心价值在于 API 的全生命周期管理（版本、限流、授权、监控等），而非单纯的 Lambda 代理。\n\n**重点考点 / 关键词补充：**\n- API Gateway 是“API 前门”\n- 常见集成：Lambda、EC2、S3、Step Functions\n- 安全功能：WAF、Throttling、API Keys、Usage Plans",
        "domain": "Technology and Services",
    },
    {
        "id": "S14",
        "question": "Amazon EBS 卷默认情况下数据存储在哪个范围？",
        "options": [
            "A. 单个 Region 内的多个 AZ",
            "B. 单个 Availability Zone",
            "C. 全球所有 Edge Locations",
            "D. 多个 Region",
        ],
        "correct_answers": [
            "B",
        ],
        "explanation": "「单个 Availability Zone」是正确的。\n\nAmazon EBS（Elastic Block Store）卷默认绑定到单个 Availability Zone（可用区）。一旦创建，就只能被同一 AZ 内的 EC2 实例挂载使用，不能直接跨 AZ 挂载。\n\n其他选项分析：\n\n「单个 Region 内的多个 AZ」是错误的：EBS 卷不能跨 AZ 使用。\n\n「全球所有 Edge Locations」是错误的：Edge Location 用于内容分发，不是块存储。\n\n「多个 Region」是错误的：跨 Region 需要使用 EBS 快照复制。\n\n**重点考点 / 关键词补充：**\n- EBS 卷是 AZ 级资源\n- 跨 AZ 高可用方案：使用快照定期复制 + 多 AZ 部署应用\n- 跨 Region 灾难恢复：使用 EBS 快照跨 Region 复制",
        "domain": "Technology and Services",
    },
    {
        "id": "S15",
        "question": "AWS Snowball Edge 相比普通 Snowball 的额外能力是什么？",
        "options": [
            "A. 提供比标准 Snowball 更大的本地存储容量以支持超大规模数据迁移",
            "B. 内置计算能力，可在本地运行 Lambda 或 EC2 实例处理数据",
            "C. 支持更高的网络传输速度和更低的延迟直连 AWS",
            "D. 允许用户在设备上安装任意第三方 Linux 应用程序和自定义脚本",
        ],
        "correct_answers": [
            "B",
        ],
        "explanation": "「内置计算能力，可在本地运行 Lambda 或 EC2 实例处理数据」是正确的。\n\nAWS Snowball Edge 相比普通 Snowball，增加了本地计算能力，支持在设备上直接运行 AWS Lambda 函数或 EC2 实例，对数据进行预处理、过滤、转换后再传回 AWS，大幅减少需要传输的数据量。\n\n其他选项分析：\n\n「提供比标准 Snowball 更大的本地存储容量以支持超大规模数据迁移」是错误的：Snowball Edge 的存储容量和标准 Snowball 相近，其核心差异在于新增的本地计算能力。\n\n「支持更高的网络传输速度和更低的延迟直连 AWS」是错误的：Snowball 系列主要用于离线大规模数据迁移，网络传输速度不是其设计重点。\n\n「允许用户在设备上安装任意第三方 Linux 应用程序和自定义脚本」是错误的：Snowball Edge 支持运行 AWS 提供的 Lambda 和 EC2 实例，但对任意第三方软件的安装和运行有严格限制，并非通用计算设备。\n\n**重点考点 / 关键词补充：**\n- Snowball Edge = 存储 + 计算\n- 适合场景：数据预处理、边缘计算、断网环境下的数据收集\n- 普通 Snowball 只有存储功能",
        "domain": "Technology and Services",
    },
    {
        "id": "S16",
        "question": "Amazon ElastiCache 主要用于什么场景？",
        "options": [
            "A. 用于将不常访问的数据自动归档到低成本存储",
            "B. 提供高性能的内存缓存层，降低数据库负载",
            "C. 托管兼容 MySQL 和 PostgreSQL 的关系型数据库",
            "D. 提供海量非结构化数据的对象存储服务",
        ],
        "correct_answers": [
            "B",
        ],
        "explanation": "「提供高性能的内存缓存层，降低数据库负载」是正确的。\n\nAmazon ElastiCache 是 AWS 全托管的内存缓存服务，支持 Redis 和 Memcached 引擎，主要用于在应用和数据库之间构建高性能缓存层，显著降低数据库负载、提升响应速度。\n\n其他选项分析：\n\n「用于将不常访问的数据自动归档到低成本存储」是错误的：这是 S3 Intelligent-Tiering 或 S3 Glacier 的功能，ElastiCache 是内存级缓存。\n\n「托管兼容 MySQL 和 PostgreSQL 的关系型数据库」是错误的：这是 Amazon RDS / Aurora 的核心职责，ElastiCache 只做缓存，不托管主数据库。\n\n「提供海量非结构化数据的对象存储服务」是错误的：对象存储是 Amazon S3 的功能，与内存缓存完全不同。\n\n**重点考点 / 关键词补充：**\n- ElastiCache = 内存缓存（Redis / Memcached）\n- 常见用途：会话存储、排行榜、缓存查询结果\n- 与 DynamoDB DAX 的区别：DAX 是 DynamoDB 专用的缓存",
        "domain": "Technology and Services",
    },
    {
        "id": "S17",
        "question": "使用 AWS Organizations 进行 Consolidated Billing 的主要财务优势是什么？",
        "options": [
            "A. 每个账户独立享受完整免费套餐",
            "B. 多个账户用量合并计算，更容易达到更高折扣层级",
            "C. 所有服务自动打 50% 折扣",
            "D. 没有任何财务优势",
        ],
        "correct_answers": [
            "B",
        ],
        "explanation": "「多个账户用量合并计算，更容易达到更高折扣层级」是正确的。\n\n使用 AWS Organizations 的 Consolidated Billing 功能后，所有关联账户的用量会被合并计算，更容易达到更高的折扣层级（尤其是数据传输费），同时由主账户统一支付，简化财务管理。\n\n其他选项分析：\n\n「每个账户独立享受完整免费套餐」是错误的：多个账户合并后，免费额度是共享的，并非每个账户都独立享受完整额度。\n\n「所有服务自动打 50% 折扣」是错误的：折扣主要来自用量合并达到更高阶梯，并非固定 50%。\n\n「没有任何财务优势」是错误的：合并计费是 AWS 组织的主要财务优势之一。\n\n**重点考点 / 关键词补充：**\n- Consolidated Billing：合并计费\n- 主要好处：用量合并 → 更高折扣层级 + 统一支付\n- 注意：免费额度在组织内是共享的",
        "domain": "Billing, Pricing, and Support",
    },
    {
        "id": "S18",
        "question": "以下哪些情况下推荐购买 Reserved Instances 或 Savings Plans？",
        "options": [
            "A. 流量极不稳定，每天变化很大",
            "B. 有稳定、可预测的长期工作负载",
            "C. 短期测试项目",
            "D. 完全不关心成本",
        ],
        "correct_answers": [
            "B",
        ],
        "explanation": "「有稳定、可预测的长期工作负载」是正确的。\n\nReserved Instances 或 Savings Plans 适合有稳定、可预测的长期工作负载，可以获得 30%~72% 的折扣，适合有稳定基线负载的场景。\n\n其他选项分析：\n\n「流量极不稳定，每天变化很大」是错误的：这种场景更适合 On-Demand 或 Spot Instances，RI/Savings Plans 需要稳定用量才能发挥价值。\n\n「短期测试项目」是错误的：短期项目通常更适合 On-Demand，RI/Savings Plans 需要长期承诺。\n\n「完全不关心成本」是错误的：完全不关心成本的用户不需要考虑任何折扣方案。\n\n**重点考点 / 关键词补充：**\n- RI / Savings Plans：有承诺换折扣\n- 适合稳定、长期、可预测的计算负载\n- On-Demand：灵活但最贵\n- Spot：最便宜但可中断",
        "domain": "Billing, Pricing, and Support",
    },
    {
        "id": "S19",
        "question": "AWS Support 计划中，Basic Support 主要提供哪些服务？",
        "options": [
            "A. 7x24 技术支持和 <1 小时响应",
            "B. 账户和账单支持 + 有限的 Trusted Advisor 检查",
            "C. Technical Account Manager",
            "D. 架构审查和优化建议",
        ],
        "correct_answers": [
            "B",
        ],
        "explanation": "「账户和账单支持 + 有限的 Trusted Advisor 检查」是正确的。\n\nBasic Support 仅提供基本的账户和账单支持，以及有限的 Trusted Advisor 检查（7 个检查项）。它不提供技术支持，生产环境通常至少需要 Business Support。\n\n其他选项分析：\n\n「7x24 技术支持和 <1 小时响应」是错误的：这是 Business Support 及以上计划才有的服务。\n\n「Technical Account Manager」是错误的：TAM 是 Enterprise Support 的专属服务。\n\n「架构审查和优化建议」是错误的：深度架构审查是 Enterprise Support 的功能。\n\n**重点考点 / 关键词补充：**\n- Basic Support：几乎没有技术支持\n- Business Support：生产环境推荐的最低支持计划（24x7 技术支持）\n- Enterprise Support：有 TAM + 架构审查",
        "domain": "Billing, Pricing, and Support",
    },
    {
        "id": "S20",
        "question": "AWS CloudTrail 主要记录什么？",
        "options": [
            "A. EC2 实例的 CPU 使用率",
            "B. 对 AWS 账户中资源的 API 调用历史",
            "C. S3 对象的访问内容",
            "D. 网络流量详细内容",
        ],
        "correct_answers": [
            "B",
        ],
        "explanation": "「对 AWS 账户中资源的 API 调用历史」是正确的。\n\nAWS CloudTrail 主要记录对 AWS 账户中资源的 API 调用历史，包括通过控制台、CLI、SDK 发起的所有操作，是安全审计、合规取证和事件调查的核心服务。\n\n其他选项分析：\n\n「EC2 实例的 CPU 使用率」是错误的：这是 CloudWatch 的功能。\n\n「S3 对象的访问内容」是错误的：S3 对象内容访问主要由 S3 访问日志或 CloudTrail 数据事件记录。\n\n「网络流量详细内容」是错误的：网络流量详细分析通常使用 VPC Flow Logs。\n\n**重点考点 / 关键词补充：**\n- CloudTrail = API 调用日志（谁在什么时候做了什么）\n- 强烈建议开启所有区域的 CloudTrail\n- 与 CloudWatch 的区别：CloudTrail 关注“做了什么操作”，CloudWatch 关注“资源状态和指标”",
        "domain": "Security and Compliance",
    },
    {
        "id": "S21",
        "question": "以下哪些情况适合使用 Amazon S3 Glacier Instant Retrieval？",
        "options": [
            "A. 需要毫秒级检索的长期归档数据",
            "B. 每天频繁访问的数据",
            "C. 几乎从不访问的冷数据",
            "D. 需要最低存储成本",
        ],
        "correct_answers": [
            "A",
        ],
        "explanation": "「需要毫秒级检索的长期归档数据」是正确的。\n\nS3 Glacier Instant Retrieval 适合需要长期归档但偶尔需要快速（毫秒级）检索的数据，成本比 Standard-IA 低，但比 Glacier Deep Archive 高。\n\n其他选项分析：\n\n「每天频繁访问的数据」是错误的：频繁访问应使用 Standard 或 Intelligent-Tiering。\n\n「几乎从不访问的冷数据」是错误的：几乎不访问的极冷数据更适合 Glacier Deep Archive（成本更低）。\n\n「需要最低存储成本」是错误的：最低成本通常是 Glacier Deep Archive。\n\n**重点考点 / 关键词补充：**\n- Glacier Instant Retrieval：归档但需快速访问\n- 检索时间：毫秒级\n- 成本介于 Standard-IA 和 Glacier Deep Archive 之间",
        "domain": "Technology and Services",
    },
    {
        "id": "S22",
        "question": "AWS Organizations 的 Service Control Policies (SCP) 主要用于什么？",
        "options": [
            "A. 完全替代成员账户中的 IAM 策略来控制所有用户权限",
            "B. 在组织层面设置最大可用权限边界（即使 IAM 允许也不能超过）",
            "C. 自动为组织内的所有账户分配和调整预算额度",
            "D. 实时监控并告警组织内所有账户的 AWS 使用费用",
        ],
        "correct_answers": [
            "B",
        ],
        "explanation": "「在组织层面设置最大可用权限边界（即使 IAM 允许也不能超过）」是正确的。\n\nAWS Organizations 的 Service Control Policies (SCP) 是在组织（Organization）层面设置的权限边界，用于限制成员账户的最大可用权限。即使 IAM 策略允许，SCP 也会生效，是实现合规和安全治理的重要工具。\n\n其他选项分析：\n\n「完全替代成员账户中的 IAM 策略来控制所有用户权限」是错误的：SCP 不能授予权限，只能添加限制（Deny），它是 Organizations 层的边界控制，不能替代 IAM。\n\n「自动为组织内的所有账户分配和调整预算额度」是错误的：预算管理和告警是 AWS Budgets 的功能。\n\n「实时监控并告警组织内所有账户的 AWS 使用费用」是错误的：成本监控和告警主要使用 AWS Cost Explorer 和 AWS Budgets。\n\n**重点考点 / 关键词补充：**\n- SCP 是“最大权限边界”（Deny 优先）\n- 不能授予权限，只能限制\n- 常见用途：防止关闭 CloudTrail、限制使用特定 Region、服务等",
        "domain": "Security and Compliance",
    },
    {
        "id": "S23",
        "question": "AWS Trusted Advisor 主要提供什么价值？",
        "options": [
            "A. 自动检测并一键修复所有安全和成本问题",
            "B. 检查资源并提供优化建议（成本、安全、性能、容错等）",
            "C. 集中管理所有 IAM 用户、角色和权限策略",
            "D. 记录所有 AWS API 调用并生成详细审计日志",
        ],
        "correct_answers": [
            "B",
        ],
        "explanation": "「检查资源并提供优化建议（成本、安全、性能、容错等）」是正确的。\n\nAWS Trusted Advisor 是一个实时指导工具，会自动检查你的 AWS 环境，并针对成本优化、安全、性能、容错、服务限制等方面提供具体建议和最佳实践。\n\n其他选项分析：\n\n「自动检测并一键修复所有安全和成本问题」是错误的：Trusted Advisor 仅提供检查和建议，不会自动执行任何修复操作。\n\n「集中管理所有 IAM 用户、角色和权限策略」是错误的：IAM 用户和权限管理由 AWS Identity and Access Management (IAM) 服务负责。\n\n「记录所有 AWS API 调用并生成详细审计日志」是错误的：API 调用审计是 AWS CloudTrail 的核心功能。\n\n**重点考点 / 关键词补充：**\n- Trusted Advisor 有免费版和付费版（Business/Enterprise 支持更多检查项）\n- 常见检查：未使用的 EBS 卷、开放的 S3 桶、MFA 未启用等\n- 与 AWS Config、Security Hub 的区别",
        "domain": "Billing, Pricing, and Support",
    },
    {
        "id": "S24",
        "question": "Amazon DynamoDB 的计费模式特点是什么？",
        "options": [
            "A. 仅支持预置容量模式，按小时预留 RCU/WCU 计费",
            "B. 支持按需模式，按实际请求次数和存储量计费",
            "C. 必须提前购买 1 年或 3 年预留容量才能使用",
            "D. 无论使用量多少都收取固定月费",
        ],
        "correct_answers": [
            "B",
        ],
        "explanation": "「支持按需模式，按实际请求次数和存储量计费」是正确的。\n\nAmazon DynamoDB 支持两种主要计费模式：按需模式（On-Demand）按实际读写请求次数和存储量计费，极度灵活；预置容量模式则需预先配置 RCU/WCU 并按小时计费，适合稳定负载。\n\n其他选项分析：\n\n「仅支持预置容量模式，按小时预留 RCU/WCU 计费」是错误的：DynamoDB 同时支持按需模式和预置容量模式，按需模式是其默认推荐的灵活模式。\n\n「必须提前购买 1 年或 3 年预留容量才能使用」是错误的：DynamoDB 没有强制预留要求，按需模式可随时使用，无需任何长期承诺。\n\n「无论使用量多少都收取固定月费」是错误的：DynamoDB 没有固定月费，按需模式完全按实际用量计费。\n\n**重点考点 / 关键词补充：**\n- DynamoDB 两种计费模式：按需（On-Demand） vs 预置容量（Provisioned）\n- 按需模式适合流量波动大的场景\n- 预置容量适合稳定、可预测的负载，可以结合 Auto Scaling",
        "domain": "Technology and Services",
    },
    {
        "id": "S25",
        "question": "AWS 客户想把 Oracle 数据库迁移到 AWS，同时尽量减少对现有应用代码的修改，最佳方案是？",
        "options": [
            "A. 直接在 Amazon EC2 上自建 Oracle 数据库并自行管理备份和高可用",
            "B. 使用 AWS Database Migration Service 迁移到 RDS for Oracle 或 Aurora",
            "C. 将 Oracle 数据文件直接上传到 Amazon S3 并使用 Athena 查询",
            "D. 使用 AWS Snowball Edge 将整个 Oracle 实例物理迁移到 AWS",
        ],
        "correct_answers": [
            "B",
        ],
        "explanation": "「使用 AWS Database Migration Service 迁移到 RDS for Oracle 或 Aurora」是正确的。\n\n当客户希望把 Oracle 数据库迁移到 AWS，同时尽量减少对现有应用代码的修改，最佳方案是使用 AWS Database Migration Service (DMS) 将数据迁移到 Amazon RDS for Oracle 或 Aurora（兼容 PostgreSQL/MySQL，但 Oracle 工作负载通常选 RDS for Oracle）。\n\n其他选项分析：\n\n「直接在 Amazon EC2 上自建 Oracle 数据库并自行管理备份和高可用」是错误的：虽然技术上可行，但需要自己负责操作系统补丁、备份、高可用架构等大量运维工作，失去了托管数据库的优势。\n\n「将 Oracle 数据文件直接上传到 Amazon S3 并使用 Athena 查询」是错误的：Athena 是用于查询 S3 中数据的分析服务，无法运行 Oracle 数据库引擎。\n\n「使用 AWS Snowball Edge 将整个 Oracle 实例物理迁移到 AWS」是错误的：Snowball Edge 主要用于离线大数据迁移，不支持将正在运行的 Oracle 数据库实例直接物理迁移。\n\n**重点考点 / 关键词补充：**\n- DMS：支持同构和异构数据库迁移\n- 保持兼容性（最小代码修改）是关键考点\n- RDS for Oracle 提供托管 Oracle 体验",
        "domain": "Technology and Services",
    },
    {
        "id": "S26",
        "question": "以下哪些属于 AWS 的合规性认证或框架？",
        "options": [
            "A. SOC",
            "B. PCI DSS",
            "C. HIPAA",
            "D. ISO 9001",
            "E. 以上全部",
        ],
        "correct_answers": [
            "E",
        ],
        "explanation": "「以上全部」是正确的。\n\nAWS 拥有大量国际和行业合规认证，包括 SOC（1/2/3）、PCI DSS、HIPAA、ISO 9001、ISO 27001、FedRAMP 等。客户可以在 AWS Artifact 中下载对应合规报告用于审计和合规证明。\n\n其他选项分析：\n\n单独列出任何一个（如 SOC、PCI DSS、HIPAA、ISO 9001）都是正确的，但题目问的是“以下哪些”，因此答案是 E（以上全部）。\n\n**重点考点 / 关键词补充：**\n- AWS Artifact 是获取官方合规报告的唯一官方渠道\n- 常见考试组合：SOC + PCI + HIPAA\n- 认证不等于“数据安全由 AWS 完全负责”（仍需客户负责云中安全）",
        "domain": "Security and Compliance",
    },
    {
        "id": "S27",
        "question": "当 Spot Instance 被 AWS 中断时，通常会提前多久发出通知？",
        "options": [
            "A. 立即中断，无通知",
            "B. 通常提前 2 分钟发出中断通知",
            "C. 提前 1 小时通知",
            "D. 永远不会中断",
        ],
        "correct_answers": [
            "B",
        ],
        "explanation": "「通常提前 2 分钟发出中断通知」是正确的。\n\n当 Spot Instance 被 AWS 中断时，AWS 通常会在中断前 2 分钟通过实例元数据和 EventBridge 发出中断通知，让应用有时间做优雅关机、保存状态或进行 Checkpointing。\n\n其他选项分析：\n\n「立即中断，无通知」是错误的：AWS 会提供 2 分钟的宽限期。\n\n「提前 1 小时通知」是错误的：通知时间是 2 分钟，不是 1 小时。\n\n「永远不会中断」是错误的：Spot Instance 的本质就是可中断的。\n\n**重点考点 / 关键词补充：**\n- Spot 中断通知时间：2 分钟（固定）\n- 应用必须做好中断处理才能安全使用 Spot\n- 可以通过 Spot 实例中断处理（Spot Instance Interruption）机制优雅退出",
        "domain": "Technology and Services",
    },
    {
        "id": "S28",
        "question": "AWS Config 主要用于什么？",
        "options": [
            "A. 记录所有 AWS API 调用历史用于审计和取证",
            "B. 持续评估和记录 AWS 资源配置变更，并检查合规性",
            "C. 实时检测和告警可疑的网络入侵行为",
            "D. 通过全球节点缓存静态内容以降低用户延迟",
        ],
        "correct_answers": [
            "B",
        ],
        "explanation": "「持续评估和记录 AWS 资源配置变更，并检查合规性」是正确的。\n\nAWS Config 主要用于持续记录 AWS 资源的配置变更历史，并通过 Config Rules 对资源进行合规性检查和评估，是合规治理和配置管理的重要服务。\n\n其他选项分析：\n\n「记录所有 AWS API 调用历史用于审计和取证」是错误的：这是 AWS CloudTrail 的核心功能（记录谁在什么时候做了什么操作）。\n\n「实时检测和告警可疑的网络入侵行为」是错误的：这是 Amazon GuardDuty、AWS Security Hub 等威胁检测服务的功能。\n\n「通过全球节点缓存静态内容以降低用户延迟」是错误的：这是 Amazon CloudFront 的主要功能。\n\n**重点考点 / 关键词补充：**\n- Config = 配置变更历史 + 合规检查\n- 与 CloudTrail 的区别：Config 关注“资源变成了什么样子”，CloudTrail 关注“谁做了什么操作”\n- Config Rules 可用于自动检测不合规资源",
        "domain": "Security and Compliance",
    },
    {
        "id": "S29",
        "question": "以下哪些情况推荐使用 Savings Plans 而非 On-Demand？",
        "options": [
            "A. 有稳定基线计算需求，希望获得折扣",
            "B. 完全不可预测的突发负载",
            "C. 短期测试项目（少于 1 个月）",
            "D. 只需要偶尔运行的批处理任务",
        ],
        "correct_answers": [
            "A",
        ],
        "explanation": "「有稳定基线计算需求，希望获得折扣」是正确的。\n\nSavings Plans 适合有稳定、可预测的基线计算需求，可以获得比 On-Demand 显著的折扣（通常 30%~72%）。它比传统 Reserved Instances 更灵活。\n\n其他选项分析：\n\n「完全不可预测的突发负载」是错误的：这种场景更适合 On-Demand 或 Spot Instances，Savings Plans 需要有一定可预测的基线用量。\n\n「短期测试项目（少于 1 个月）」是错误的：短期负载通常更适合 On-Demand，Savings Plans 需要一定承诺期才能划算。\n\n「只需要偶尔运行的批处理任务」是错误的：这种场景更适合 Spot Instances。\n\n**重点考点 / 关键词补充：**\n- Savings Plans 比传统 RI 更灵活（可跨实例类型、区域）\n- 适合有稳定基线 + 一定增长的负载\n- Compute Savings Plans 最推荐（灵活性最高）",
        "domain": "Billing, Pricing, and Support",
    },
    {
        "id": "S30",
        "question": "AWS 客户希望获得最快的响应时间和架构优化支持，应该选择哪种支持计划？",
        "options": [
            "A. Basic Support",
            "B. Developer Support",
            "C. Business Support",
            "D. Enterprise Support",
        ],
        "correct_answers": [
            "D",
        ],
        "explanation": "「Enterprise Support」是正确的。\n\nEnterprise Support 提供最快的响应时间（< 15 分钟严重故障）、专属 Technical Account Manager (TAM)、架构审查、主动指导和白手套服务，适合大型关键业务和对支持要求极高的客户。\n\n其他选项分析：\n\n「Basic Support」是错误的：Basic Support 几乎没有技术支持。\n\n「Developer Support」是错误的：Developer Support 响应时间较慢，且只在工作时间提供支持。\n\n「Business Support」是错误的：Business Support 响应时间为 < 1 小时，没有 TAM 和深度架构支持。\n\n**重点考点 / 关键词补充：**\n- Enterprise Support = 最高级别支持计划\n- 核心优势：TAM + 最快响应 + 架构审查 + 主动支持\n- 适合：大型企业、关键生产环境、对合规和架构有严格要求",
        "domain": "Billing, Pricing, and Support",
    },
    {
        "id": "S31",
        "question": "VPC Endpoint 分为哪两种主要类型？",
        "options": [
            "A. Public Endpoint 和 Private Endpoint",
            "B. Gateway Endpoint 和 Interface Endpoint",
            "C. Regional Endpoint 和 Global Endpoint",
            "D. Direct Endpoint 和 Indirect Endpoint",
        ],
        "correct_answers": [
            "B",
        ],
        "explanation": "「Gateway Endpoint 和 Interface Endpoint」是正确的。\n\nAWS VPC Endpoint 主要分为两种类型：\n- Gateway Endpoint：主要用于 S3 和 DynamoDB，通过路由表实现，免费。\n- Interface Endpoint：支持大部分 AWS 服务，通过 Elastic Network Interface (ENI) + Private DNS 实现，需要付费。\n\n其他选项分析：\n\n「Public Endpoint 和 Private Endpoint」是错误的：这不是 VPC Endpoint 的官方分类方式。\n\n「Regional Endpoint 和 Global Endpoint」是错误的：VPC Endpoint 是 Region 级别的概念。\n\n「Direct Endpoint 和 Indirect Endpoint」是错误的：没有这种官方分类。\n\n**重点考点 / 关键词补充：**\n- Gateway Endpoint：仅 S3/DynamoDB，免费，基于路由表\n- Interface Endpoint：大部分服务，收费，基于 ENI\n- 两者都用于在不使用公网的情况下私密访问 AWS 服务",
        "domain": "Technology and Services",
    },
    {
        "id": "S32",
        "question": "Amazon EC2 突增型实例（T3/T3a/T2）使用 CPU 积分（Credit）机制。以下说法正确的是？",
        "options": [
            "A. 积分用完后实例会立即停止",
            "B. 积分用完后实例性能会降到基准性能",
            "C. 积分可以永久积累，没有上限",
            "D. 基准性能以下的 CPU 使用不会消耗积分",
        ],
        "correct_answers": [
            "B",
        ],
        "explanation": "「积分用完后实例性能会降到基准性能」是正确的。\n\nT 系列（突增型）实例使用 CPU 积分机制：在基准性能以下运行时会积累积分，超过基准时会消耗积分。积分用完后，实例性能会自动限制在基准性能，不会停止或被终止。\n\n其他选项分析：\n\n「积分用完后实例会立即停止」是错误的：实例不会停止，只是性能被限制到基准。\n\n「积分可以永久积累，没有上限」是错误的：积分有上限（通常为 24 小时的积累量）。\n\n「基准性能以下的 CPU 使用不会消耗积分」是错误的：基准以下会积累积分，基准以上才消耗。\n\n**重点考点 / 关键词补充：**\n- T 系列适合有突发负载但平均利用率不高的场景\n- 积分用完后性能降至基线（不是停止）\n- 可以通过 Unlimited 模式避免性能受限（会产生额外费用）",
        "domain": "Technology and Services",
    },
    {
        "id": "S33",
        "question": "AWS 跨区域数据传输费用通常比 Region 内部传输费用？",
        "options": [
            "A. 更便宜",
            "B. 更贵",
            "C. 完全免费",
            "D. 取决于服务类型，没有统一规律",
        ],
        "correct_answers": [
            "B",
        ],
        "explanation": "「更贵」是正确的。\n\nAWS 跨 Region 数据传输（尤其是出方向）通常比同一 Region 内部（甚至跨 AZ）的传输费用贵很多，是成本优化和架构设计时的重要考量因素。\n\n其他选项分析：\n\n「更便宜」是错误的：跨 Region 传输几乎总是更贵。\n\n「完全免费」是错误的：跨 Region 数据传输一般都需要收费。\n\n「取决于服务类型，没有统一规律」是错误的：虽然不同服务有细微差异，但总体规律是跨 Region 更贵。\n\n**重点考点 / 关键词补充：**\n- 跨 Region 数据传输是主要成本项之一\n- 建议尽量把相关资源放在同一 Region\n- CloudFront、S3 Transfer Acceleration 等可用于优化跨 Region 访问",
        "domain": "Billing, Pricing, and Support",
    },
    {
        "id": "S34",
        "question": "Amazon Aurora Serverless 的最大优势是什么？",
        "options": [
            "A. 比普通 Aurora 性能更高",
            "B. 自动根据负载调整计算容量，按实际使用量计费",
            "C. 必须手动指定最小最大容量",
            "D. 只支持 MySQL，不支持 PostgreSQL",
        ],
        "correct_answers": [
            "B",
        ],
        "explanation": "「自动根据负载调整计算容量，按实际使用量计费」是正确的。\n\nAmazon Aurora Serverless 的最大优势是完全自动根据实际负载调整计算容量（以 ACU 为单位），用户无需管理数据库实例，按实际使用的计算量付费，特别适合流量波动大或不可预测的工作负载。\n\n其他选项分析：\n\n「比普通 Aurora 性能更高」是错误的：性能主要取决于 ACU 数量，不一定比手动配置的 Aurora 更高。\n\n「必须手动指定最小最大容量」是错误的：虽然可以设置范围，但核心是自动伸缩。\n\n「只支持 MySQL，不支持 PostgreSQL」是错误的：Aurora Serverless 支持 MySQL 和 PostgreSQL 两种引擎。\n\n**重点考点 / 关键词补充：**\n- Aurora Serverless v2：支持更细粒度的自动伸缩\n- 适合：不定期访问的应用、开发测试环境、流量波动大的工作负载\n- 按 ACU 计费（每秒计费）",
        "domain": "Technology and Services",
    },
    {
        "id": "S35",
        "question": "AWS Well-Architected Tool 的主要用途是？",
        "options": [
            "A. 自动根据审查结果为工作负载应用推荐的最佳实践配置",
            "B. 帮助用户根据 Well-Architected Framework 审查自己的工作负载并生成改进建议",
            "C. 对多个 AWS 账户执行统一的安全基准检查和合规性评分",
            "D. 持续监控工作负载的性能指标并在出现异常时自动发送告警",
        ],
        "correct_answers": [
            "B",
        ],
        "explanation": "「帮助用户根据 Well-Architected Framework 审查自己的工作负载并生成改进建议」是正确的。\n\nAWS Well-Architected Tool 是一个免费工具，它引导用户按照 Well-Architected Framework 的五大支柱（卓越运营、安全、可靠性、性能效率、成本优化）对自己的工作负载进行审查，并生成具体的改进建议和最佳实践。\n\n其他选项分析：\n\n「自动根据审查结果为工作负载应用推荐的最佳实践配置」是错误的：Well-Architected Tool 仅提供审查报告和改进建议，不会自动执行任何配置变更或部署操作。\n\n「对多个 AWS 账户执行统一的安全基准检查和合规性评分」是错误的：这是 AWS Security Hub、AWS Config、或 AWS Control Tower 的功能范畴。\n\n「持续监控工作负载的性能指标并在出现异常时自动发送告警」是错误的：实时性能监控和告警属于 Amazon CloudWatch + Amazon SNS / EventBridge 的职责。\n\n**重点考点 / 关键词补充：**\n- Well-Architected Tool 是免费的\n- 审查结果可导出为 PDF\n- 强烈建议在生产工作负载上线前进行审查",
        "domain": "Cloud Concepts",
    },
    {
        "id": "S36",
        "question": "Amazon Lightsail 相比标准 EC2 的主要定位是？",
        "options": [
            "A. 提供更强大的 GPU 性能",
            "B. 面向初学者和简单工作负载，提供固定价格的一键式虚拟服务器",
            "C. 替代 Lambda 的 serverless 服务",
            "D. 专门用于大数据处理",
        ],
        "correct_answers": [
            "B",
        ],
        "explanation": "「面向初学者和简单工作负载，提供固定价格的一键式虚拟服务器」是正确的。\n\nAmazon Lightsail 主要面向初学者、个人开发者和简单工作负载，提供固定价格、开箱即用的一键式虚拟服务器（VPS），管理界面简单，适合快速搭建博客、网站、小型应用等场景。\n\n其他选项分析：\n\n「提供更强大的 GPU 性能」是错误的：Lightsail 的 GPU 选项有限，更强大的 GPU 应使用标准 EC2。\n\n「替代 Lambda 的 serverless 服务」是错误的：Lightsail 仍然是传统虚拟服务器，不是 serverless。\n\n「专门用于大数据处理」是错误的：大数据处理应使用 EMR、Glue 等服务。\n\n**重点考点 / 关键词补充：**\n- Lightsail = 简化版的 EC2 + 托管数据库 + 负载均衡 + CDN\n- 适合快速启动简单项目\n- 超过一定规模后建议迁移到标准 EC2 以获得更多灵活性",
        "domain": "Technology and Services",
    },
    {
        "id": "S37",
        "question": "以下哪些情况最适合使用 AWS Outposts？",
        "options": [
            "A. 需要在本地数据中心运行完全一致的 AWS 服务和 API",
            "B. 希望将所有工作负载从本地数据中心完全迁移到 AWS 云端以降低运维成本",
            "C. 只需要低成本的对象存储服务，且对延迟没有特殊要求",
            "D. 应对短期内突然增加的计算需求，适合使用 Spot 实例",
        ],
        "correct_answers": [
            "A",
        ],
        "explanation": "「需要在本地数据中心运行完全一致的 AWS 服务和 API」是正确的。\n\nAWS Outposts 允许客户在自己的本地数据中心或机房部署与 AWS 云完全一致的基础设施和服务（包括计算、存储、网络），实现真正混合云架构，特别适合有低延迟、数据主权或遗留系统集成要求的场景。\n\n其他选项分析：\n\n「希望将所有工作负载从本地数据中心完全迁移到 AWS 云端以降低运维成本」是错误的：这更适合直接使用标准 AWS 云服务，而不是 Outposts。\n\n「只需要低成本的对象存储服务，且对延迟没有特殊要求」是错误的：对象存储可直接使用标准 S3，不需要部署 Outposts。\n\n「应对短期内突然增加的计算需求，适合使用 Spot 实例」是错误的：短期突发需求更适合使用 On-Demand 或 Spot 实例，而不是长期部署 Outposts。\n\n**重点考点 / 关键词补充：**\n- Outposts = 本地部署的 AWS 基础设施\n- 支持与云端完全一致的 API 和服务\n- 常见场景：低延迟、数据驻留、制造业、医疗、金融等",
        "domain": "Technology and Services",
    },
    {
        "id": "S38",
        "question": "AWS Marketplace 的主要作用是什么？",
        "options": [
            "A. 购买和部署第三方软件和服务的在线商店",
            "B. 管理 AWS 支持案例",
            "C. 估算 AWS 成本",
            "D. 监控安全威胁",
        ],
        "correct_answers": [
            "A",
        ],
        "explanation": "「购买和部署第三方软件和服务的在线商店」是正确的。\n\nAWS Marketplace 是一个在线商店，客户可以在这里查找、购买和快速部署来自第三方厂商的软件、AMI、SaaS 服务和解决方案，大大简化了采购和部署流程。\n\n其他选项分析：\n\n「管理 AWS 支持案例」是错误的：支持案例通过 Support Center 管理。\n\n「估算 AWS 成本」是错误的：成本估算使用 AWS Pricing Calculator。\n\n「监控安全威胁」是错误的：安全威胁监控使用 GuardDuty、Security Hub 等。\n\n**重点考点 / 关键词补充：**\n- Marketplace 支持按小时、按月或按使用量计费\n- 包含大量第三方 AMI 和 SaaS 产品\n- 购买后可直接部署到 AWS 环境",
        "domain": "Technology and Services",
    },
    {
        "id": "S39",
        "question": "AWS CloudWatch 和 AWS CloudTrail 的核心区别是什么？",
        "options": [
            "A. CloudWatch 记录 API 调用历史，CloudTrail 监控性能指标",
            "B. CloudWatch 监控性能指标和日志，CloudTrail 记录 API 调用和账户活动",
            "C. 两者完全相同，只是 AWS 推出的不同产品名称，实际功能没有区别",
            "D. CloudTrail 只能监控 EC2 实例的启动、停止和终止事件",
        ],
        "correct_answers": [
            "B",
        ],
        "explanation": "「CloudWatch 监控性能指标和日志，CloudTrail 记录 API 调用和账户活动」是正确的。\n\nAmazon CloudWatch 主要用于监控资源性能指标、收集日志、设置告警和实现自动化响应。\nAWS CloudTrail 主要用于记录对 AWS 资源的 API 调用历史和账户活动，用于审计、安全分析和合规。\n\n其他选项分析：\n\n「CloudWatch 记录 API 调用历史，CloudTrail 监控性能指标」是错误的：两者功能正好相反。\n\n「两者完全相同，只是 AWS 推出的不同产品名称，实际功能没有区别」是错误的：CloudWatch 专注于性能监控与日志，CloudTrail 专注于 API 调用审计，两者功能定位完全不同。\n\n「CloudTrail 只能监控 EC2 实例的启动、停止和终止事件」是错误的：CloudTrail 记录几乎所有 AWS 服务的 API 调用历史，而非仅限于 EC2 实例的生命周期事件。\n\n**重点考点 / 关键词补充：**\n- CloudWatch：监控 + 日志 + 告警（“资源在做什么”）\n- CloudTrail：API 调用审计（“谁在什么时候做了什么”）\n- 两者经常结合使用实现完整可观测性和安全审计",
        "domain": "Security and Compliance",
    },
    {
        "id": "S40",
        "question": "Amazon DynamoDB 开启 Point-in-Time Recovery (PITR) 后可以恢复到多久之前的时间点？",
        "options": [
            "A. 最近 5 分钟",
            "B. 最近 35 天内的任意时间点",
            "C. 最近 1 年",
            "D. 只能恢复到创建快照的时间点",
        ],
        "correct_answers": [
            "B",
        ],
        "explanation": "「最近 35 天内的任意时间点」是正确的。\n\nAmazon DynamoDB 开启 Point-in-Time Recovery (PITR) 后，可以将表恢复到过去 35 天内任意时间点（精确到秒），无需手动创建备份，极大简化了数据恢复流程。\n\n其他选项分析：\n\n「最近 5 分钟」是错误的：支持范围远不止 5 分钟。\n\n「最近 1 年」是错误的：PITR 只支持 35 天。\n\n「只能恢复到创建快照的时间点」是错误的：PITR 支持任意时间点恢复，不是只能恢复到快照时间。\n\n**重点考点 / 关键词补充：**\n- DynamoDB PITR：连续备份 + 任意时间点恢复\n- 最长支持 35 天\n- 开启后会产生额外存储费用（约表大小的 1.5%~2%）",
        "domain": "Technology and Services",
    },
    {
        "id": "S41",
        "question": "AWS 客户想对 S3 存储桶中的对象自动应用生命周期策略，以降低存储成本。推荐使用什么功能？",
        "options": [
            "A. S3 Versioning",
            "B. S3 Lifecycle Policies",
            "C. S3 Cross-Region Replication",
            "D. S3 Object Lock",
        ],
        "correct_answers": [
            "B",
        ],
        "explanation": "「S3 Lifecycle Policies」是正确的。\n\nS3 Lifecycle Policies 可以根据时间或前缀自动将对象从 Standard 存储类转移到 Standard-IA、Glacier、Glacier Deep Archive 等更便宜的存储类，或者在达到一定天数后自动删除对象，从而有效降低存储成本。\n\n其他选项分析：\n\n「S3 Versioning」是错误的：版本控制主要用于防止误删和恢复历史版本，不会自动降低成本（反而可能增加存储量）。\n\n「S3 Cross-Region Replication」是错误的：跨区域复制主要用于灾难恢复和低延迟访问，不会降低成本。\n\n「S3 Object Lock」是错误的：对象锁定主要用于合规和防勒索，不会自动降低成本。\n\n**重点考点 / 关键词补充：**\n- Lifecycle Policies 是 S3 成本优化的核心功能\n- 常见策略：Standard → IA（30天）→ Glacier（90天）\n- 配合 Intelligent-Tiering 使用效果更好",
        "domain": "Technology and Services",
    },
    {
        "id": "S42",
        "question": "AWS 客户希望在多个 AWS 账户之间共享 Reserved Instance 或 Savings Plans 的折扣，最佳方式是？",
        "options": [
            "A. 把所有关联账户完全合并成一个主 AWS 账户来共享所有折扣",
            "B. 使用 AWS Organizations + Consolidated Billing",
            "C. 在每个成员账户中手动购买相同的 Reserved Instance 或 Savings Plans",
            "D. 使用 AWS Marketplace 将折扣转售给其他关联账户",
        ],
        "correct_answers": [
            "B",
        ],
        "explanation": "「使用 AWS Organizations + Consolidated Billing」是正确的。\n\n通过 AWS Organizations 创建组织，并开启 Consolidated Billing 功能后，Reserved Instances 和 Savings Plans 的折扣可以自动在所有关联账户之间共享，这是 AWS 推荐的最佳实践。\n\n其他选项分析：\n\n「把所有关联账户完全合并成一个主 AWS 账户来共享所有折扣」是错误的：这不是必要操作，且会失去 Organizations 的灵活组织管理优势。\n\n「在每个成员账户中手动购买相同的 Reserved Instance 或 Savings Plans」是错误的：这样无法实现折扣共享，且管理成本极高。\n\n「使用 AWS Marketplace 将折扣转售给其他关联账户」是错误的：Marketplace 主要用于向外部客户转售 RI/Savings Plans，不是组织内共享折扣的最佳方式。\n\n**重点考点 / 关键词补充：**\n- Consolidated Billing 是共享 RI/Savings Plans 折扣的主要方式\n- 必须使用 AWS Organizations\n- 折扣会自动分配给用量最高的账户",
        "domain": "Billing, Pricing, and Support",
    },
    {
        "id": "S43",
        "question": "Amazon EC2 实例的根卷（Root Volume）使用 EBS 还是 Instance Store 时，停止实例后数据会怎样？",
        "options": [
            "A. 无论使用 EBS 还是 Instance Store 作为根卷，停止实例后数据都会保留",
            "B. EBS 根卷停止后数据保留，Instance Store 根卷停止后数据丢失",
            "C. 无论使用哪种存储作为根卷，停止实例后数据都会永久丢失",
            "D. 只有使用 Instance Store 作为根卷时，停止后数据才会保留下来",
        ],
        "correct_answers": [
            "B",
        ],
        "explanation": "「EBS 根卷停止后数据保留，Instance Store 根卷停止后数据丢失」是正确的。\n\n当使用 EBS 作为根卷时，实例停止后数据会保留；当使用 Instance Store 作为根卷时，实例停止或终止后，Instance Store 上的数据会永久丢失。\n\n其他选项分析：\n\n「无论使用 EBS 还是 Instance Store 作为根卷，停止实例后数据都会保留」是错误的：Instance Store 是临时存储，实例停止或终止后数据会立即丢失。\n\n「无论使用哪种存储作为根卷，停止实例后数据都会永久丢失」是错误的：EBS 根卷数据在实例停止后会保留，只有终止且设置了 DeleteOnTermination 才会删除。\n\n「只有使用 Instance Store 作为根卷时，停止后数据才会保留下来」是错误的：实际情况完全相反，Instance Store 数据在停止后必然丢失。\n\n**重点考点 / 关键词补充：**\n- EBS = 持久块存储（停止后保留）\n- Instance Store = 临时存储（停止/终止后丢失）\n- 大多数生产环境推荐使用 EBS 根卷",
        "domain": "Technology and Services",
    },
    {
        "id": "S44",
        "question": "AWS 客户想对 S3 中的敏感数据进行自动发现和分类，推荐使用哪项服务？",
        "options": [
            "A. Amazon GuardDuty",
            "B. Amazon Macie",
            "C. AWS Inspector",
            "D. AWS Shield",
        ],
        "correct_answers": [
            "B",
        ],
        "explanation": "「Amazon Macie」是正确的。\n\nAmazon Macie 是一项安全服务，使用机器学习自动发现、分类和保护 S3 存储桶中的敏感数据（如个人身份信息 PII、财务数据、医疗信息等），帮助客户满足数据保护和合规要求。\n\n其他选项分析：\n\n「Amazon GuardDuty」是错误的：GuardDuty 是智能威胁检测服务。\n\n「AWS Inspector」是错误的：Inspector 是漏洞管理服务。\n\n「AWS Shield」是错误的：Shield 是 DDoS 防护服务。\n\n**重点考点 / 关键词补充：**\n- Macie = 敏感数据发现与保护（S3 专用）\n- 使用机器学习自动识别敏感信息\n- 常见于金融、医疗、需要 GDPR/HIPAA 合规的场景",
        "domain": "Security and Compliance",
    },
    {
        "id": "S45",
        "question": "以下哪些 AWS 服务提供免费的 DDoS 防护？",
        "options": [
            "A. AWS Shield Standard",
            "B. AWS Shield Advanced",
            "C. AWS WAF",
            "D. Amazon GuardDuty",
        ],
        "correct_answers": [
            "A",
        ],
        "explanation": "「AWS Shield Standard」是正确的。\n\nAWS Shield Standard 对所有 AWS 客户免费提供基础的 DDoS 防护（自动防护常见攻击）。Shield Advanced 是付费服务，提供更高级的防护、DDoS 成本保护和 24/7 支持。\n\n其他选项分析：\n\n「AWS Shield Advanced」是错误的：Advanced 是收费服务。\n\n「AWS WAF」是错误的：WAF 是 Web 应用防火墙，主要防护应用层攻击（如 SQL 注入），不是专门的 DDoS 防护。\n\n「Amazon GuardDuty」是错误的：GuardDuty 是威胁检测服务。\n\n**重点考点 / 关键词补充：**\n- Shield Standard：免费，自动启用\n- Shield Advanced：收费，提供额外保护和成本保障\n- WAF 主要防护应用层攻击（L7），Shield 主要防护网络/传输层 DDoS（L3/L4）",
        "domain": "Security and Compliance",
    },
    {
        "id": "S46",
        "question": "Amazon Redshift 主要用于什么工作负载？",
        "options": [
            "A. 实时事务处理 (OLTP)",
            "B. 大规模数据仓库和分析查询 (OLAP)",
            "C. 非结构化文档存储",
            "D. 缓存热点数据",
        ],
        "correct_answers": [
            "B",
        ],
        "explanation": "「大规模数据仓库和分析查询 (OLAP)」是正确的。\n\nAmazon Redshift 是 AWS 的全托管 PB 级数据仓库服务，主要用于大规模数据仓库和复杂分析查询（OLAP）工作负载，适合商业智能、报表和大规模数据分析场景。\n\n其他选项分析：\n\n「实时事务处理 (OLTP)」是错误的：OLTP 更适合使用 RDS、Aurora 或 DynamoDB。\n\n「非结构化文档存储」是错误的：非结构化/文档存储更适合 DynamoDB、DocumentDB 或 S3。\n\n「缓存热点数据」是错误的：缓存服务是 ElastiCache。\n\n**重点考点 / 关键词补充：**\n- Redshift = 数据仓库（OLAP）\n- 适合复杂分析查询和 BI\n- 与 Athena 的区别：Redshift 适合大量结构化数据 + 高并发分析；Athena 适合即席查询 S3 数据",
        "domain": "Technology and Services",
    },
    {
        "id": "S47",
        "question": "AWS Well-Architected Framework 的主要目的是什么？",
        "options": [
            "A. 帮助客户自动优化和修复架构问题",
            "B. 提供一套最佳实践框架，帮助客户设计安全、高效、可靠的云架构",
            "C. 作为云上项目管理的标准化方法论",
            "D. 仅限拥有 AWS Enterprise Support 的客户使用",
        ],
        "correct_answers": [
            "B",
        ],
        "explanation": "「提供一套最佳实践框架，帮助客户设计安全、高效、可靠的云架构」是正确的。\n\nAWS Well-Architected Framework 提供了一套经过验证的最佳实践，围绕五大支柱帮助客户在云上构建安全、可靠、高性能且成本优化的系统。\n\n其他选项分析：\n\n「帮助客户自动优化和修复架构问题」是错误的：框架和 Well-Architected Tool 仅提供检查与建议，不会自动执行任何优化或修复操作。\n\n「作为云上项目管理的标准化方法论」是错误的：Well-Architected Framework 专注于技术架构最佳实践，而非项目管理流程或方法论。\n\n「仅限拥有 AWS Enterprise Support 的客户使用」是错误的：Well-Architected Framework 和 Tool 对所有 AWS 客户完全免费使用。\n\n**重点考点 / 关键词补充：**\n- 五大支柱：卓越运营、安全、可靠性、性能效率、成本优化\n- Well-Architected Tool 是免费的审查工具\n- 建议在生产工作负载上线前进行审查",
        "domain": "Cloud Concepts",
    },
    {
        "id": "S48",
        "question": "在设计高可用架构时，为什么 AWS 推荐在一个 Region 内至少使用两个 Availability Zone？",
        "options": [
            "A. 可以降低数据存储成本",
            "B. 当一个 AZ 发生故障时，应用可以在另一个 AZ 继续运行",
            "C. 可以获得更高的网络带宽",
            "D. 所有 AWS 服务只在多 AZ 部署时才可用",
        ],
        "correct_answers": [
            "B",
        ],
        "explanation": "「当一个 AZ 发生故障时，应用可以在另一个 AZ 继续运行」是正确的。\n\nAvailability Zone 是物理隔离的数据中心。在一个 Region 内跨多个 AZ 部署资源，可以实现真正的故障隔离。当一个 AZ 发生电力、网络或自然灾害故障时，其他 AZ 通常不受影响，从而提高整体可用性。\n\n其他选项分析：\n\n「可以降低数据存储成本」是错误的：多 AZ 部署通常会增加成本（需要复制数据）。\n\n「可以获得更高的网络带宽」是错误的：多 AZ 主要解决可用性，而不是带宽。\n\n「所有 AWS 服务只在多 AZ 部署时才可用」是错误的：大多数服务在单 AZ 也可以使用，只是高可用架构推荐跨 AZ。\n\n**重点考点 / 关键词补充：**\n- AZ = 物理隔离的数据中心（Region 内）\n- 推荐高可用架构至少跨 2 个 AZ\n- 跨 AZ 数据传输通常免费或极低费用",
        "domain": "Cloud Concepts",
    },
    {
        "id": "S49",
        "question": "AWS Key Management Service (KMS) 中，Customer Managed Key 和 AWS Managed Key 的主要区别是什么？",
        "options": [
            "A. Customer Managed Key 只能用于 S3 和 EBS 加密，其他 AWS 服务必须使用 AWS Managed Key",
            "B. Customer Managed Key 由客户完全控制生命周期和访问策略，AWS Managed Key 由 AWS 管理",
            "C. AWS Managed Key 提供更高的安全性和更完善的审计日志记录",
            "D. 两者在功能、控制权和生命周期管理上没有本质区别，只是创建主体不同",
        ],
        "correct_answers": [
            "B",
        ],
        "explanation": "「Customer Managed Key 由客户完全控制生命周期和访问策略，AWS Managed Key 由 AWS 管理」是正确的。\n\nCustomer Managed Keys (CMK) 由客户创建和管理，客户可以控制密钥的启用、禁用、轮换、删除以及访问策略。AWS Managed Keys 由 AWS 创建和管理，客户无法控制其生命周期。\n\n其他选项分析：\n\n「Customer Managed Key 只能用于 S3 和 EBS 加密，其他 AWS 服务必须使用 AWS Managed Key」是错误的：Customer Managed Keys 可以用于几乎所有支持 KMS 的 AWS 服务（RDS、S3、EBS、Lambda 等），远不止 S3 和 EBS。\n\n「AWS Managed Key 提供更高的安全性和更完善的审计日志记录」是错误的：安全性主要取决于如何配置密钥策略和访问控制，而非密钥是由客户还是 AWS 创建。两者产生的 CloudTrail 日志级别相似。\n\n「两者在功能、控制权和生命周期管理上没有本质区别，只是创建主体不同」是错误的：Customer Managed Key 允许客户完全控制启用/禁用、自动轮换、删除计划和密钥策略，而 AWS Managed Key 由 AWS 完全管理，客户控制权非常有限。\n\n**重点考点 / 关键词补充：**\n- Customer Managed Key：客户完全控制（推荐用于敏感数据）\n- AWS Managed Key：AWS 管理，适合一般使用场景\n- 密钥轮换：CMK 支持自动轮换，AWS Managed Key 也支持但客户无法控制",
        "domain": "Security and Compliance",
    },
    {
        "id": "S50",
        "question": "S3 Standard-IA 和 S3 One Zone-IA 的主要区别是什么？",
        "options": [
            "A. Standard-IA 支持毫秒级检索，One Zone-IA 只能支持秒级或更慢的检索",
            "B. Standard-IA 将数据存储在多个可用区，One Zone-IA 只存储在一个可用区",
            "C. One Zone-IA 比 Standard-IA 更贵，因为它提供了更低的可用性",
            "D. 两者在耐久性上完全相同，只是存储成本不同",
        ],
        "correct_answers": [
            "B",
        ],
        "explanation": "「Standard-IA 将数据存储在多个可用区，One Zone-IA 只存储在一个可用区」是正确的。\n\nS3 Standard-IA 将数据冗余存储在同一 Region 的多个可用区，提供更高的可用性（99.9%）。S3 One Zone-IA 仅将数据存储在一个可用区，成本更低，但可用性较低（99.5%），适合可以承受单 AZ 故障的非关键数据。\n\n其他选项分析：\n\n「Standard-IA 支持毫秒级检索，One Zone-IA 只能支持秒级或更慢的检索」是错误的：Standard-IA 和 One Zone-IA 都支持毫秒级数据检索，检索性能没有显著差异。\n\n「One Zone-IA 比 Standard-IA 更贵，因为它提供了更低的可用性」是错误的：One Zone-IA 的存储费用比 Standard-IA 更低（通常低约 20%），代价是更低的可用性。\n\n「两者在耐久性上完全相同，只是存储成本不同」是错误的：两者耐久性完全相同（11 个 9），核心区别在于可用性（Standard-IA 多 AZ vs One Zone-IA 单 AZ）和价格。\n\n**重点考点 / 关键词补充：**\n- One Zone-IA：成本最低的 IA 存储类，适合可承受单 AZ 故障的数据\n- Standard-IA：更平衡的选择，适合需要较高可用性的不频繁访问数据\n- 两者都有最低 30 天存储要求",
        "domain": "Technology and Services",
    },
    {
        "id": "S51",
        "question": "AWS Global Accelerator 与 Amazon CloudFront 的主要区别是什么？",
        "options": [
            "A. Global Accelerator 只能加速 HTTP/HTTPS 流量，不能处理 TCP/UDP 协议",
            "B. Global Accelerator 提供静态 Anycast IP 地址，可加速 TCP/UDP 应用",
            "C. CloudFront 主要用于降低跨 Region 数据传输费用和存储成本",
            "D. 两者功能完全相同，只是 AWS 推出的两个不同产品名称",
        ],
        "correct_answers": [
            "B",
        ],
        "explanation": "「Global Accelerator 提供静态 Anycast IP 地址，可加速 TCP/UDP 应用」是正确的。\n\nAWS Global Accelerator 使用 Anycast IP 地址，通过 AWS 全球骨干网将用户流量路由到最近的健康端点，支持 TCP 和 UDP 协议，适合需要低延迟和全球加速的非 HTTP 应用。\n\n其他选项分析：\n\n「Global Accelerator 只能加速 HTTP/HTTPS 流量，不能处理 TCP/UDP 协议」是错误的：Global Accelerator 的最大特点之一正是支持 TCP 和 UDP 协议加速，而非仅限于 HTTP/HTTPS。\n\n「CloudFront 主要用于降低跨 Region 数据传输费用和存储成本」是错误的：CloudFront 主要用于全球内容分发加速和降低最终用户访问延迟，而非主要为了降低跨 Region 数据传输费用。\n\n「两者功能完全相同，只是 AWS 推出的两个不同产品名称」是错误的：Global Accelerator 专注于基于 Anycast IP 的 TCP/UDP 网络层加速，CloudFront 专注于 HTTP/HTTPS 内容缓存和边缘计算，两者定位和适用场景明显不同。\n\n**重点考点 / 关键词补充：**\n- Global Accelerator：Anycast + 全球骨干网加速（TCP/UDP）\n- CloudFront：CDN 缓存加速（HTTP/HTTPS）\n- 常见组合：两者一起使用实现最佳全球加速效果",
        "domain": "Cloud Concepts",
    },
    {
        "id": "S52",
        "question": "使用 AWS Organizations 的主要优势之一是什么？",
        "options": [
            "A. 可以让所有关联账户共享同一个 Root 用户",
            "B. 可以在组织层面集中管理多个 AWS 账户的权限、策略和账单",
            "C. 自动为所有成员账户开启所有 AWS 服务",
            "D. 可以免费获得无限的 AWS 服务额度",
        ],
        "correct_answers": [
            "B",
        ],
        "explanation": "「可以在组织层面集中管理多个 AWS 账户的权限、策略和账单」是正确的。\n\nAWS Organizations 允许企业创建多个 AWS 账户，并通过 Service Control Policies (SCP)、Consolidated Billing 等功能在组织层面进行统一治理、权限边界设置和成本管理。\n\n其他选项分析：\n\n「可以让所有关联账户共享同一个 Root 用户」是错误的：每个 AWS 账户都有自己独立的 Root 用户，不应共享。\n\n「自动为所有成员账户开启所有 AWS 服务」是错误的：服务默认是关闭的，需要手动启用。\n\n「可以免费获得无限的 AWS 服务额度」是错误的：Organizations 本身不提供额外免费额度。\n\n**重点考点 / 关键词补充：**\n- Organizations 核心功能：账户管理 + SCP + 合并计费\n- SCP 用于设置权限边界（Deny 优先）\n- 强烈推荐用于有多账户需求的企业",
        "domain": "Security and Compliance",
    },
    {
        "id": "S53",
        "question": "Amazon S3 版本控制（Versioning）开启后，如果误删了一个对象，可以如何恢复？",
        "options": [
            "A. 直接从回收站找回",
            "B. 通过查看版本列表，恢复到之前的版本",
            "C. 必须联系 AWS Support",
            "D. 数据会永久丢失，无法恢复",
        ],
        "correct_answers": [
            "B",
        ],
        "explanation": "「通过查看版本列表，恢复到之前的版本」是正确的。\n\n开启 S3 Versioning 后，每次对对象进行修改或删除操作都会保留历史版本。误删或误覆盖后，可以通过 S3 控制台或 API 查看所有版本，并将所需的历史版本恢复为最新版本。\n\n其他选项分析：\n\n「直接从回收站找回」是错误的：S3 没有传统意义上的回收站，恢复依赖版本控制。\n\n「必须联系 AWS Support」是错误的：版本恢复是客户自己操作的。\n\n「数据会永久丢失，无法恢复」是错误的：开启版本控制后可以恢复历史版本。\n\n**重点考点 / 关键词补充：**\n- Versioning 防止误删和误覆盖\n- 删除版本化对象会产生删除标记（Delete Marker）\n- 配合 Lifecycle Policy 可以控制旧版本的存储成本",
        "domain": "Technology and Services",
    },
    {
        "id": "S54",
        "question": "AWS Lambda 的执行环境在函数执行结束后会发生什么？",
        "options": [
            "A. 立即被永久删除，无法复用任何资源或状态",
            "B. 可能被保留一段时间以供后续调用复用（暖启动）",
            "C. 自动转换为 EC2 实例以继续运行更长时间",
            "D. 必须由开发者手动调用 API 释放所有计算资源",
        ],
        "correct_answers": [
            "B",
        ],
        "explanation": "「可能被保留一段时间以供后续调用复用（暖启动）」是正确的。\n\nLambda 执行环境在函数执行结束后不会立即销毁，AWS 可能会保留该环境一段时间（通常几分钟到几小时，取决于负载）。如果后续有相同函数的调用，可以复用该环境，实现更快的「暖启动」。\n\n其他选项分析：\n\n「立即被永久删除，无法复用任何资源或状态」是错误的：Lambda 会保留执行环境一段时间以支持后续调用的暖启动，显著降低延迟。\n\n「自动转换为 EC2 实例以继续运行更长时间」是错误的：Lambda 是完全 serverless 的服务，执行环境与 EC2 实例没有关系，不会自动转换。\n\n「必须由开发者手动调用 API 释放所有计算资源」是错误的：Lambda 的执行环境生命周期完全由 AWS 自动管理，开发者无需手动释放。\n\n**重点考点 / 关键词补充：**\n- 冷启动 vs 暖启动\n- 冷启动时间受运行时、内存、代码包大小影响\n- 使用 Provisioned Concurrency 可以消除冷启动",
        "domain": "Technology and Services",
    },
    {
        "id": "S55",
        "question": "AWS Free Tier 中的「12 个月免费额度」和「永久免费套餐」的区别是什么？",
        "options": [
            "A. 两者完全相同，只是叫法不同，实际使用期限和额度没有区别",
            "B. 12 个月免费额度从账户激活起算，永久免费套餐无时间限制",
            "C. 永久免费套餐（Always Free）仅限教育机构、初创公司或非营利组织使用",
            "D. 12 个月免费额度只能用于 EC2 和 S3，其他 AWS 服务不提供免费额度",
        ],
        "correct_answers": [
            "B",
        ],
        "explanation": "「12 个月免费额度从账户激活起算，永久免费套餐无时间限制」是正确的。\n\n12 个月免费额度从首次激活 AWS 账户开始计算（通常为 12 个月），之后转为正常计费。永久免费套餐（Always Free）则没有时间限制，只要账户保持活跃即可继续使用（如 DynamoDB 25GB、Lambda 每月 100 万次调用等）。\n\n其他选项分析：\n\n「两者完全相同，只是叫法不同，实际使用期限和额度没有区别」是错误的：12 个月免费额度有明确时间限制（激活后 12 个月），而永久免费套餐没有时间限制。\n\n「永久免费套餐（Always Free）仅限教育机构、初创公司或非营利组织使用」是错误的：永久免费套餐对所有新注册的 AWS 账户开放，并非仅限教育或非营利机构。\n\n「12 个月免费额度只能用于 EC2 和 S3，其他 AWS 服务不提供免费额度」是错误的：12 个月免费额度覆盖多个服务（EC2、S3、Lambda、RDS 等），并非仅限 EC2 和 S3。\n\n**重点考点 / 关键词补充：**\n- 12 个月免费：从激活开始算（不是注册日）\n- 永久免费：无时间限制，但用量有上限\n- 免费额度用完后会正常收费，不会自动停止服务",
        "domain": "Billing, Pricing, and Support",
    },
    {
        "id": "S56",
        "question": "AWS 客户希望在多个 AWS 账户之间实施统一的权限策略边界，最佳实践是使用哪项服务？",
        "options": [
            "A. 使用 IAM Identity Center 集中管理所有成员账户的用户和权限",
            "B. AWS Organizations 的 Service Control Policies (SCP)",
            "C. 通过 AWS Resource Access Manager (RAM) 在账户间共享权限策略",
            "D. 在每个成员账户中部署相同 IAM Policy 并用 CloudFormation StackSets 统一更新",
        ],
        "correct_answers": [
            "B",
        ],
        "explanation": "「AWS Organizations 的 Service Control Policies (SCP)」是正确的。\n\nService Control Policies (SCP) 允许在 AWS Organizations 层面为成员账户设置权限边界。即使 IAM 策略允许，SCP 也可以阻止特定操作，是实现多账户治理和合规的重要工具。\n\n其他选项分析：\n\n「使用 IAM Identity Center 集中管理所有成员账户的用户和权限」是错误的：IAM Identity Center 主要用于统一身份认证和单点登录（SSO），它本身不提供跨账户的权限策略边界控制。\n\n「通过 AWS Resource Access Manager (RAM) 在账户间共享权限策略」是错误的：RAM 用于跨账户共享资源（如子网、License 等），而非用于设置权限策略边界。\n\n「在每个成员账户中部署相同 IAM Policy 并用 CloudFormation StackSets 统一更新」是错误的：这是手动或半自动化的做法，无法提供 Organizations 层面强制的、不可绕过的权限边界（SCP 才是真正的边界工具）。\n\n**重点考点 / 关键词补充：**\n- SCP 是“最大权限边界”，采用 Deny 优先\n- 必须在 Organizations 根或 OU 级别附加\n- 常用于禁止关闭 CloudTrail、限制使用特定 Region 等",
        "domain": "Security and Compliance",
    },
    {
        "id": "S57",
        "question": "Amazon CloudFront 的主要功能是什么？",
        "options": [
            "A. 提供跨 Region 的高可用数据库服务，支持全局读写",
            "B. 通过全球 Edge Location 缓存内容，降低用户访问延迟",
            "C. 管理 DNS 记录和全球流量路由，实现智能负载均衡",
            "D. 提供容器编排和自动扩缩容的 Kubernetes 服务",
        ],
        "correct_answers": [
            "B",
        ],
        "explanation": "「通过全球 Edge Location 缓存内容，降低用户访问延迟」是正确的。\n\nAmazon CloudFront 是 AWS 的全球内容分发网络 (CDN) 服务。它通过分布在全球的 Edge Location 缓存静态和动态内容，显著降低最终用户访问延迟，同时减轻源站负载。\n\n其他选项分析：\n\n「提供跨 Region 的高可用数据库服务，支持全局读写」是错误的：这是 Amazon Aurora Global Database 或 RDS Global 的功能，与 CDN 完全无关。\n\n「管理 DNS 记录和全球流量路由，实现智能负载均衡」是错误的：这是 Amazon Route 53 的核心功能，CloudFront 本身不提供 DNS 管理。\n\n「提供容器编排和自动扩缩容的 Kubernetes 服务」是错误的：这是 Amazon EKS / ECS 的功能，CloudFront 是内容分发网络而非容器平台。\n\n**重点考点 / 关键词补充：**\n- CloudFront = 全球 CDN\n- 主要优势：降低延迟 + 减轻源站压力\n- 常与 S3、ALB、API Gateway 配合使用\n- 支持 Lambda@Edge 实现边缘计算",
        "domain": "Technology and Services",
    },
    {
        "id": "S58",
        "question": "AWS 客户希望对 S3 中的数据进行跨 Region 复制以实现灾难恢复，最合适的方案是？",
        "options": [
            "A. 开启 S3 Versioning",
            "B. 配置 S3 Cross-Region Replication (CRR)",
            "C. 使用 S3 Transfer Acceleration",
            "D. 定期手动复制对象到另一个 Region",
        ],
        "correct_answers": [
            "B",
        ],
        "explanation": "「配置 S3 Cross-Region Replication (CRR)」是正确的。\n\nS3 Cross-Region Replication 允许自动、异步地将对象从源存储桶复制到另一个 Region 的目标存储桶，是实现跨 Region 灾难恢复和数据冗余的标准方案。\n\n其他选项分析：\n\n「开启 S3 Versioning」是错误的：版本控制主要防止误删，不能实现跨 Region 复制。\n\n「使用 S3 Transfer Acceleration」是错误的：Transfer Acceleration 主要优化上传速度，不是复制方案。\n\n「定期手动复制对象」是错误的：手动方式不可靠且难以管理，不符合最佳实践。\n\n**重点考点 / 关键词补充：**\n- CRR 是异步复制，通常在几分钟内完成\n- 支持复制加密对象和元数据\n- 常用于合规、灾难恢复和降低跨 Region 访问延迟",
        "domain": "Technology and Services",
    },
    {
        "id": "S59",
        "question": "AWS 客户在设计架构时，希望同时获得 Reserved Instances 的折扣和 Spot Instances 的低价，应该如何结合使用？",
        "options": [
            "A. 混合使用多种购买选项会失去所有折扣，必须选择单一模式全量使用",
            "B. 对稳定基线负载使用 Savings Plans，对可中断负载使用 Spot Instances",
            "C. 只要工作负载可以容忍中断，就可以把所有负载都放在 Spot Instances 上运行",
            "D. 为了保证最大灵活性和稳定性，所有生产负载都应该使用 On-Demand 实例",
        ],
        "correct_answers": [
            "B",
        ],
        "explanation": "「对稳定基线负载使用 Savings Plans，对可中断负载使用 Spot Instances」是正确的。\n\n最佳实践是混合使用：用 Savings Plans 或 Reserved Instances 覆盖稳定的基线负载以获得高折扣，用 Spot Instances 处理可中断、可容错的突发或批处理负载以进一步降低成本。\n\n其他选项分析：\n\n「混合使用多种购买选项会失去所有折扣，必须选择单一模式全量使用」是错误的：AWS 完全支持在同一个账户内同时使用 Savings Plans、Spot、On-Demand 等多种购买选项，且折扣可以叠加。\n\n「只要工作负载可以容忍中断，就可以把所有负载都放在 Spot Instances 上运行」是错误的：即使可以容忍中断，生产环境中的关键服务通常仍需要一定比例的稳定容量作为基础。\n\n「为了保证最大灵活性和稳定性，所有生产负载都应该使用 On-Demand 实例」是错误的：On-Demand 价格最高，对于稳定负载使用 Savings Plans 或 Reserved Instances 能显著降低成本且同样灵活。\n\n**重点考点 / 关键词补充：**\n- 混合购买模型是成本优化的核心策略\n- Savings Plans 比传统 RI 更灵活\n- Spot 适合可中断工作负载（需做好中断处理）",
        "domain": "Billing, Pricing, and Support",
    },
    {
        "id": "S60",
        "question": "AWS 客户希望在不暴露公网 IP 的情况下，让私有子网中的 EC2 实例访问 S3，该最佳实践方案是？",
        "options": [
            "A. 通过 NAT Gateway 访问 S3",
            "B. 配置 VPC Endpoint (Gateway Endpoint) 访问 S3",
            "C. 使用 S3 Transfer Acceleration",
            "D. 把 S3 存储桶设为公开",
        ],
        "correct_answers": [
            "B",
        ],
        "explanation": "「配置 VPC Endpoint (Gateway Endpoint) 访问 S3」是正确的。\n\n通过 VPC Endpoint（Gateway 类型）访问 S3，流量完全在 AWS 内部网络中，不会经过公网，也不需要 NAT Gateway，既安全又能节省数据传输费用。\n\n其他选项分析：\n\n「通过 NAT Gateway 访问 S3」是错误的：虽然可行，但会产生 NAT Gateway 处理费用，且流量仍会经过 AWS 骨干网。\n\n「使用 S3 Transfer Acceleration」是错误的：这主要用于加速跨互联网的上传，不是私有访问方案。\n\n「把 S3 存储桶设为公开」是错误的：严重违反安全最佳实践。\n\n**重点考点 / 关键词补充：**\n- VPC Endpoint for S3 是 Gateway Endpoint（免费）\n- 推荐在私有子网访问 S3 时使用\n- 可以显著降低成本并提高安全性",
        "domain": "Technology and Services",
    },
    {
        "id": "S61",
        "question": "AWS 客户希望将多个 AWS 账户统一管理，并通过一个主账户查看所有关联账户的账单，最佳实践是使用哪项服务？",
        "options": [
            "A. 通过 AWS IAM 跨账户角色实现所有子账户的统一费用查看和支付",
            "B. AWS Organizations + Consolidated Billing",
            "C. 使用 AWS Cost Explorer 的多账户聚合视图功能",
            "D. 配置 AWS Budgets 并开启跨账户成本告警聚合",
        ],
        "correct_answers": [
            "B",
        ],
        "explanation": "「AWS Organizations + Consolidated Billing」是正确的。\n\n通过 AWS Organizations 创建组织结构，并开启 Consolidated Billing 功能后，可以将多个 AWS 账户关联在一起，由主账户统一支付所有关联账户的费用，并在一个地方查看合并后的账单。\n\n其他选项分析：\n\n「通过 AWS IAM 跨账户角色实现所有子账户的统一费用查看和支付」是错误的：IAM 跨账户角色可以授权访问，但无法实现统一的账单支付和 Consolidated Billing 折扣共享。\n\n「使用 AWS Cost Explorer 的多账户聚合视图功能」是错误的：Cost Explorer 可以查看聚合成本，但本身不负责账户的组织结构管理和统一支付。\n\n「配置 AWS Budgets 并开启跨账户成本告警聚合」是错误的：Budgets 主要用于设置成本和使用量告警，不是用于多账户统一管理和 Consolidated Billing。\n\n**重点考点 / 关键词补充：**\n- Organizations 是多账户管理的核心服务\n- Consolidated Billing 允许折扣共享（RI/Savings Plans）\n- 强烈推荐用于有多个环境（开发/测试/生产）的企业",
        "domain": "Billing, Pricing, and Support",
    },
    {
        "id": "S62",
        "question": "在设计多可用区（Multi-AZ）架构时，以下哪种做法最有助于提高应用的高可用性？",
        "options": [
            "A. 将所有资源部署在同一个 Availability Zone",
            "B. 将应用部署在多个 Availability Zone，并使用负载均衡器分发流量",
            "C. 只使用一个 Region 中的一个 Availability Zone",
            "D. 依赖单个 EC2 实例运行整个应用",
        ],
        "correct_answers": [
            "B",
        ],
        "explanation": "「将应用部署在多个 Availability Zone，并使用负载均衡器分发流量」是正确的。\n\n将应用组件部署在同一 Region 的不同 Availability Zone，并配合 Elastic Load Balancing，可以在某个 AZ 发生故障时自动将流量路由到健康的 AZ，从而实现真正的高可用。\n\n其他选项分析：\n\n「将所有资源部署在同一个 Availability Zone」是错误的：这是单点故障设计，AZ 故障会导致整个应用不可用。\n\n「只使用一个 Region 中的一个 Availability Zone」是错误的：这同样存在单 AZ 风险。\n\n「依赖单个 EC2 实例运行整个应用」是错误的：这是最差的高可用设计。\n\n**重点考点 / 关键词补充：**\n- Multi-AZ 是 Region 内的物理隔离\n- 配合 ELB + Auto Scaling 是经典高可用组合\n- 跨 AZ 数据传输通常免费或费用很低",
        "domain": "Cloud Concepts",
    },
    {
        "id": "S63",
        "question": "AWS 客户希望对 IAM 用户执行的操作进行精细控制，例如只允许在特定时间段内访问某些资源，应该使用 IAM Policy 的哪个部分实现？",
        "options": [
            "A. Principal",
            "B. Action",
            "C. Condition",
            "D. Resource",
        ],
        "correct_answers": [
            "C",
        ],
        "explanation": "「Condition」是正确的。\n\nIAM Policy 中的 Condition 块用于添加额外的条件限制，例如限制操作只能在特定 IP 地址、特定时间段（使用 aws:CurrentTime）、或特定请求参数下才能执行，是实现精细权限控制的重要机制。\n\n其他选项分析：\n\n「Principal」是错误的：Principal 用于指定谁可以访问（用户、角色、服务等）。\n\n「Action」是错误的：Action 用于指定允许或拒绝的具体操作（如 s3:GetObject）。\n\n「Resource」是错误的：Resource 用于指定策略适用的 AWS 资源 ARN。\n\n**重点考点 / 关键词补充：**\n- Condition 是实现“上下文感知”权限的关键\n- 常见 Condition 键：aws:CurrentTime、aws:SourceIp、aws:RequestedRegion\n- Condition 块支持多种运算符（StringEquals、DateGreaterThan 等）",
        "domain": "Security and Compliance",
    },
    {
        "id": "S64",
        "question": "Amazon S3 Object Lock 的主要用途是什么？",
        "options": [
            "A. 提高对象检索速度并降低首次字节延迟",
            "B. 防止对象被删除或覆盖，实现 WORM（一次写入多次读取）保护",
            "C. 自动将对象转移到 Glacier 等更便宜的存储类",
            "D. 跨 Region 复制对象实现异地容灾和合规备份",
        ],
        "correct_answers": [
            "B",
        ],
        "explanation": "「防止对象被删除或覆盖，实现 WORM（一次写入多次读取）保护」是正确的。\n\nS3 Object Lock 允许用户以 WORM（Write Once Read Many）模式存储对象，在指定的保留期内防止对象被删除或覆盖。这对于满足监管合规要求（如 SEC、FINRA）或防止勒索软件攻击非常重要。\n\n其他选项分析：\n\n「提高对象检索速度并降低首次字节延迟」是错误的：Object Lock 完全不影响对象检索性能，它只负责防止删除/覆盖。\n\n「自动将对象转移到 Glacier 等更便宜的存储类」是错误的：这是 S3 Lifecycle Policies 的功能，与 Object Lock 完全无关。\n\n「跨 Region 复制对象实现异地容灾和合规备份」是错误的：这是 S3 Cross-Region Replication (CRR) 的功能，Object Lock 关注的是本地对象的不可变保护。\n\n**重点考点 / 关键词补充：**\n- Object Lock 有两种模式：Compliance（严格）和 Governance（可由特定角色修改）\n- 常用于金融、医疗、法律等强合规行业\n- 一旦开启，对象在保留期内无法被任何方式删除（包括 Root 用户）",
        "domain": "Security and Compliance",
    },
    {
        "id": "S65",
        "question": "AWS 客户希望对多个账户的 AWS 使用情况设置统一的预算告警，最佳方案是使用哪项服务？",
        "options": [
            "A. AWS Cost Explorer",
            "B. AWS Budgets",
            "C. AWS Organizations",
            "D. AWS Pricing Calculator",
        ],
        "correct_answers": [
            "B",
        ],
        "explanation": "「AWS Budgets」是正确的。\n\nAWS Budgets 允许用户为成本、用量或预留实例覆盖率设置自定义预算，并配置告警。当实际或预测费用超过预算阈值时，可以通过 SNS、Email 或 Chatbot 发送通知。即使有多个账户，也可以通过 Organizations 集中管理预算。\n\n其他选项分析：\n\n「AWS Cost Explorer」是错误的：Cost Explorer 主要用于分析和可视化历史成本，不是告警工具。\n\n「AWS Organizations」是错误的：Organizations 提供账户管理，但预算告警功能在 Budgets 中。\n\n「AWS Pricing Calculator」是错误的：Pricing Calculator 用于估算未来费用，不是监控工具。\n\n**重点考点 / 关键词补充：**\n- Budgets 支持成本预算、用量预算、预留实例预算等多种类型\n- 可以设置实际费用告警和预测费用告警\n- 支持通过 AWS Chatbot 发送到 Slack/Teams",
        "domain": "Billing, Pricing, and Support",
    },
    {
        "id": "S66",
        "question": "以下关于 AWS Edge Location、Availability Zone 和 Region 的描述，哪一项是正确的？",
        "options": [
            "A. Edge Location 是 Region 内部的物理隔离单元，用于实现高可用性",
            "B. 一个 Region 通常包含多个 Availability Zone，而 Edge Location 主要用于内容缓存和边缘加速",
            "C. Edge Location 可以独立运行 EC2 实例和托管数据库",
            "D. Availability Zone 和 Edge Location 是同一个概念的不同名称",
        ],
        "correct_answers": [
            "B",
        ],
        "explanation": "「一个 Region 通常包含多个 Availability Zone，而 Edge Location 主要用于内容缓存和边缘加速」是正确的。\n\nRegion 是地理区域，内部包含多个物理隔离的 Availability Zone（AZ）；Edge Location 则是分布在全球的边缘节点，主要服务于 CloudFront、Global Accelerator 等，用于就近缓存内容、降低延迟。\n\n其他选项分析：\n\n「Edge Location 是 Region 内部的物理隔离单元」是错误的：这是 Availability Zone 的定义。\n\n「Edge Location 可以独立运行 EC2 实例和托管数据库」是错误的：Edge Location 不提供通用计算和数据库服务。\n\n「Availability Zone 和 Edge Location 是同一个概念」是错误的：两者定位和功能完全不同。\n\n**重点考点 / 关键词补充：**\n- Region > Availability Zone > Edge Location（层级关系）\n- Edge Location 核心价值：Latency Reduction + 全球内容分发\n- 常见搭配：CloudFront + Global Accelerator",
        "domain": "Cloud Concepts",
    },
    {
        "id": "S67",
        "question": "AWS 客户希望在 VPC 内私密访问 Amazon S3 和 DynamoDB，同时要求完全免费且通过路由表实现，最佳方案是使用哪种 VPC Endpoint？",
        "options": [
            "A. Interface Endpoint",
            "B. Gateway Endpoint",
            "C. PrivateLink Endpoint",
            "D. Transit Gateway Endpoint",
        ],
        "correct_answers": [
            "B",
        ],
        "explanation": "「Gateway Endpoint」是正确的。\n\nGateway Endpoint 是 VPC Endpoint 的一种类型，目前仅支持 Amazon S3 和 DynamoDB，通过修改 VPC 路由表实现流量转发，完全免费，且不需要 ENI。\n\n其他选项分析：\n\n「Interface Endpoint」是错误的：Interface Endpoint 支持更多服务，但需要创建 ENI 并产生费用。\n\n「PrivateLink Endpoint」是错误的：PrivateLink 是 Interface Endpoint 的底层实现技术，不是独立类型。\n\n「Transit Gateway Endpoint」是错误的：Transit Gateway 用于连接多个 VPC 和本地网络，不直接提供 S3/DynamoDB 私有访问。\n\n**重点考点 / 关键词补充：**\n- Gateway Endpoint：仅 S3 + DynamoDB + 免费 + 路由表驱动\n- Interface Endpoint：支持绝大多数 AWS 服务 + 收费 + ENI + Private DNS\n- 两者均可实现不经过公网访问 AWS 服务",
        "domain": "Technology and Services",
    },
    {
        "id": "S68",
        "question": "某公司有大量历史日志数据，几乎不会被访问，但必须保留 7 年以满足合规要求，且对检索时间不敏感。推荐使用哪种 S3 存储类？",
        "options": [
            "A. S3 Standard",
            "B. S3 Standard-IA",
            "C. S3 Glacier Deep Archive",
            "D. S3 Intelligent-Tiering",
        ],
        "correct_answers": [
            "C",
        ],
        "explanation": "「S3 Glacier Deep Archive」是正确的。\n\nGlacier Deep Archive 是 AWS 成本最低的存储类，专为长期归档（7-10 年甚至更长）且极少访问的数据设计，检索时间通常为 12 小时以内，存储费用极低，适合合规归档场景。\n\n其他选项分析：\n\n「S3 Standard」是错误的：成本最高，适合频繁访问数据。\n\n「S3 Standard-IA」是错误的：虽然比 Standard 便宜，但仍有最低 30 天存储要求，且费用高于 Deep Archive。\n\n「S3 Intelligent-Tiering」是错误的：适合访问模式不确定的数据，会自动分层，但对于几乎不访问的冷数据成本仍高于 Deep Archive。\n\n**重点考点 / 关键词补充：**\n- 访问频率极低 + 长期保留 → 优先选择 Glacier Deep Archive\n- 检索时间要求：Standard/IA = 毫秒级，Glacier Deep Archive = 小时级\n- 合规场景（7 年+）是 Deep Archive 的典型用例",
        "domain": "Technology and Services",
    },
    {
        "id": "S69",
        "question": "在 AWS KMS 中，如果客户需要能够随时禁用、删除或轮换密钥，并完全控制访问策略，应该创建哪种类型的密钥？",
        "options": [
            "A. AWS Managed Key",
            "B. Customer Managed Key (CMK)",
            "C. AWS Owned Key",
            "D. Data Key",
        ],
        "correct_answers": [
            "B",
        ],
        "explanation": "「Customer Managed Key (CMK)」是正确的。\n\nCustomer Managed Key 由客户完全创建和管理，客户拥有密钥的完整生命周期控制权（启用/禁用、轮换、删除策略、访问策略），适合对密钥有严格控制需求或合规要求的场景。\n\n其他选项分析：\n\n「AWS Managed Key」是错误的：由 AWS 创建和管理，客户无法控制其删除或轮换策略。\n\n「AWS Owned Key」是错误的：这是 AWS 内部使用的密钥，客户完全不可见和不可管理。\n\n「Data Key」是错误的：Data Key 是由 CMK 加密的数据加密密钥，用于实际加密数据，不是长期管理的密钥类型。\n\n**重点考点 / 关键词补充：**\n- 需要完全控制生命周期 → 必须使用 Customer Managed Key\n- AWS Managed Key：适合一般场景，客户无法删除\n- 密钥策略（Key Policy）+ IAM Policy 共同控制 CMK 访问",
        "domain": "Security and Compliance",
    },
    {
        "id": "S70",
        "question": "使用 Amazon EC2 Spot Instance 时，以下哪项是运行容错工作负载时必须考虑的设计要点？",
        "options": [
            "A. 必须使用 Dedicated Hosts 以避免中断",
            "B. 应用程序需要能够处理实例中断（通常提前 2 分钟收到通知）",
            "C. Spot Instance 价格固定且永远不会被中断",
            "D. 只能用于单实例、不可扩展的工作负载",
        ],
        "correct_answers": [
            "B",
        ],
        "explanation": "「应用程序需要能够处理实例中断（通常提前 2 分钟收到通知）」是正确的。\n\nSpot Instance 使用 AWS 富余容量，价格可低至 On-Demand 的 10%，但 AWS 可以在 2 分钟前通过实例元数据和 EventBridge 发送中断通知。容错良好的应用应实现 Checkpointing、队列解耦、Auto Scaling Group 等机制来优雅处理中断。\n\n其他选项分析：\n\n「必须使用 Dedicated Hosts」是错误的：Dedicated Host 价格最高，与 Spot 目标相反。\n\n「Spot Instance 价格固定且永远不会被中断」是错误的：价格随供需浮动，且随时可能被中断。\n\n「只能用于单实例、不可扩展的工作负载」是错误的：Spot 非常适合可水平扩展、容错设计的分布式工作负载。\n\n**重点考点 / 关键词补充：**\n- Spot 中断通知时间固定为 2 分钟\n- 最佳实践：使用 Spot Fleet / Auto Scaling Group + 混合购买选项\n- 适合场景：大数据处理、渲染、CI/CD、容器化无状态应用",
        "domain": "Technology and Services",
    },
    {
        "id": "S71",
        "question": "AWS 客户希望自动将 S3 中 90 天未访问的对象从 Standard 存储类转移到 Glacier Deep Archive 以降低成本，最佳实现方式是什么？",
        "options": [
            "A. 使用 S3 Cross-Region Replication",
            "B. 使用 S3 Lifecycle Policies 配置转换规则",
            "C. 使用 S3 Object Lock 设置保留期",
            "D. 手动使用 AWS CLI 定期执行复制命令",
        ],
        "correct_answers": [
            "B",
        ],
        "explanation": "「使用 S3 Lifecycle Policies 配置转换规则」是正确的。\n\nS3 Lifecycle Policies 可以基于对象年龄、前缀或标签自动执行存储类转换（例如 Standard → Standard-IA → Glacier → Glacier Deep Archive），是实现 S3 成本自动优化的标准做法。\n\n其他选项分析：\n\n「使用 S3 Cross-Region Replication」是错误的：CRR 用于跨区域复制对象，主要解决灾难恢复和低延迟访问，不用于成本优化。\n\n「使用 S3 Object Lock」是错误的：Object Lock 用于防止删除和覆盖，与存储类转换无关。\n\n「手动使用 AWS CLI」是错误的：手动操作不可扩展且容易出错，Lifecycle Policies 是推荐的自动化方案。\n\n**重点考点 / 关键词补充：**\n- Lifecycle Policies 是 S3 成本优化的核心工具\n- 常见转换路径：Standard（0天）→ IA（30天）→ Glacier（90天）→ Deep Archive（180天+）\n- 可配合 S3 Intelligent-Tiering 实现更智能的分层",
        "domain": "Technology and Services",
    },
    {
        "id": "S72",
        "question": "在 VPC 中部署 NAT Gateway 的主要目的是什么？",
        "options": [
            "A. 允许私有子网中的实例访问互联网，同时阻止互联网主动访问这些实例",
            "B. 允许互联网上的主机主动访问私有子网中的实例",
            "C. 为 VPC 中的所有实例自动分配公网 IP 地址",
            "D. 实现跨 Region 的私有网络连接",
        ],
        "correct_answers": [
            "A",
        ],
        "explanation": "「允许私有子网中的实例访问互联网，同时阻止互联网主动访问这些实例」是正确的。\n\nNAT Gateway 是有状态的网关，允许私有子网实例通过它发起出站互联网连接（出站流量被 NAT），但互联网无法主动发起入站连接到私有子网实例，从而在提供互联网访问的同时保持私有子网的安全隔离。\n\n其他选项分析：\n\n「允许互联网上的主机主动访问私有子网中的实例」是错误的：这是 NAT Gateway 明确阻止的行为。\n\n「为 VPC 中的所有实例自动分配公网 IP」是错误的：这是 Auto-assign Public IP 或 Elastic IP 的功能。\n\n「实现跨 Region 的私有网络连接」是错误的：跨 Region 连接通常使用 VPC Peering、Transit Gateway 或 Direct Connect。\n\n**重点考点 / 关键词补充：**\n- NAT Gateway：有状态、支持高并发、每个 AZ 需单独部署实现高可用\n- 替代方案（已不推荐）：NAT Instance\n- 配合 Private Subnet + 路由表指向 NAT Gateway 使用",
        "domain": "Technology and Services",
    },
    {
        "id": "S73",
        "question": "AWS 客户需要下载官方的 SOC、PCI DSS、HIPAA 合规报告以及 NDA/BAA 协议，用于审计和合同签署，最合适的获取渠道是什么？",
        "options": [
            "A. AWS Cost Explorer",
            "B. AWS Artifact",
            "C. AWS Trusted Advisor",
            "D. AWS Security Hub",
        ],
        "correct_answers": [
            "B",
        ],
        "explanation": "「AWS Artifact」是正确的。\n\nAWS Artifact 是 AWS 的官方合规门户，提供各种合规报告（SOC 1/2/3、PCI DSS、HIPAA、ISO、FedRAMP 等）的下载，以及 NDA（保密协议）和 BAA（商业伙伴协议）的自助签署服务，是满足审计和合规要求的标准渠道。\n\n其他选项分析：\n\n「AWS Cost Explorer」是错误的：主要用于成本分析和可视化。\n\n「AWS Trusted Advisor」是错误的：提供最佳实践检查和建议，不提供合规报告。\n\n「AWS Security Hub」是错误的：用于集中安全发现和合规检查，不提供官方报告下载。\n\n**重点考点 / 关键词补充：**\n- Artifact 是获取 AWS 官方合规证明的唯一官方自助渠道\n- 支持 SOC、PCI、HIPAA、ISO 等主流报告\n- 提供 NDA 和 BAA 在线签署功能",
        "domain": "Security and Compliance",
    },
    {
        "id": "S74",
        "question": "以下关于 S3 Versioning 和 S3 Object Lock 的说法，哪一项是正确的？",
        "options": [
            "A. 两者都可以防止对象被删除或覆盖，实现 WORM 保护",
            "B. Versioning 主要用于防止误删和恢复历史版本，Object Lock 主要用于合规防篡改",
            "C. 开启 Versioning 后对象就无法被删除",
            "D. Object Lock 可以替代 Versioning 用于数据恢复",
        ],
        "correct_answers": [
            "B",
        ],
        "explanation": "「Versioning 主要用于防止误删和恢复历史版本，Object Lock 主要用于合规防篡改」是正确的。\n\nS3 Versioning 会保留对象的多个版本，主要用于误删恢复和审计历史变更；S3 Object Lock 则在保留期内强制实施 WORM（一次写入多次读取），防止任何删除或覆盖操作，满足严格的合规要求（如 SEC 17a-4）。\n\n其他选项分析：\n\n「两者都可以防止对象被删除或覆盖」是错误的：Versioning 不会阻止删除，它只是保留旧版本。\n\n「开启 Versioning 后对象就无法被删除」是错误的：Versioning 允许删除，但会保留删除标记和旧版本。\n\n「Object Lock 可以替代 Versioning 用于数据恢复」是错误的：两者目的不同，Object Lock 更侧重不可变性而非版本恢复。\n\n**重点考点 / 关键词补充：**\n- Versioning：数据保护 + 版本历史（可删除但可恢复）\n- Object Lock：合规不可变性（Compliance/Governance 模式）\n- 两者可以同时开启，互补使用",
        "domain": "Security and Compliance",
    },
    {
        "id": "S75",
        "question": "对于一个无状态的 Web 应用，在 AWS 上进行扩展时，通常优先推荐哪种扩展方式？",
        "options": [
            "A. 垂直扩展（Scale Up），因为单台实例性能更好",
            "B. 水平扩展（Scale Out），通过增加实例数量提升容量和弹性",
            "C. 两者效果完全相同，没有优劣之分",
            "D. 只能使用垂直扩展，否则无法保证数据一致性",
        ],
        "correct_answers": [
            "B",
        ],
        "explanation": "「水平扩展（Scale Out），通过增加实例数量提升容量和弹性」是正确的。\n\n无状态应用非常适合水平扩展：通过 Auto Scaling Group、Load Balancer 动态增减实例数量，可实现更好的弹性、容错性和成本效益。云原生架构强烈推荐优先使用水平扩展。\n\n其他选项分析：\n\n「垂直扩展（Scale Up）」是错误的：虽然可行，但单点故障风险高，扩展有上限，且通常成本效益不如水平扩展。\n\n「两者效果完全相同」是错误的：水平扩展在弹性、容错和成本上通常更优。\n\n「只能使用垂直扩展」是错误的：无状态应用正是水平扩展的理想场景。\n\n**重点考点 / 关键词补充：**\n- 无状态应用 → 优先水平扩展（Scale Out / Horizontal Scaling）\n- 有状态应用 → 垂直扩展或分布式架构更合适\n- 水平扩展的核心组件：Auto Scaling + Load Balancer + Stateless Design",
        "domain": "Technology and Services",
    },
    {
        "id": "S76",
        "question": "在 AWS IAM 中，当需要同时控制“谁可以访问”（身份）和“从哪里访问”（条件）时，应该在策略中使用哪个元素来实现精细的上下文控制？",
        "options": [
            "A. Principal",
            "B. Action",
            "C. Condition",
            "D. Resource",
        ],
        "correct_answers": [
            "C",
        ],
        "explanation": "「Condition」是正确的。\n\nIAM Policy 的 Condition 块用于添加额外的上下文限制，例如限制操作只能在特定 IP 范围（aws:SourceIp）、特定时间（aws:CurrentTime）、或特定请求参数下执行，是实现精细化、上下文感知权限控制的关键机制。\n\n其他选项分析：\n\n「Principal」是错误的：Principal 用于指定允许访问的身份（用户、角色、服务等）。\n\n「Action」是错误的：Action 用于指定具体的操作权限（如 s3:GetObject）。\n\n「Resource」是错误的：Resource 用于指定策略适用的资源 ARN。\n\n**重点考点 / 关键词补充：**\n- Condition 是 IAM Policy 中实现“上下文感知”的核心元素\n- 常见键：aws:SourceIp、aws:CurrentTime、aws:RequestedRegion、aws:MultiFactorAuthPresent\n- 支持多种运算符（StringEquals、DateGreaterThan、IpAddress 等）",
        "domain": "Security and Compliance",
    },
    {
        "id": "S77",
        "question": "AWS 客户有一个稳定且可预测的计算工作负载，计划长期使用（1-3 年），希望获得最大折扣。以下哪种购买选项通常能提供最高的成本节省？",
        "options": [
            "A. Spot Instances（虽然有中断风险，但对于稳定负载也能获得极高折扣）",
            "B. On-Demand Instances（无需任何承诺，价格虽然较高但最灵活）",
            "C. Reserved Instances 或 Savings Plans（全预付）",
            "D. Dedicated Hosts（虽然价格最高，但能提供物理隔离和最高折扣）",
        ],
        "correct_answers": [
            "C",
        ],
        "explanation": "「Reserved Instances 或 Savings Plans（全预付）」是正确的。\n\n对于稳定、可预测的长期负载，全预付的 Reserved Instances 或 Compute Savings Plans 通常能提供最高的折扣（可达 70%+），因为客户通过承诺使用换取最大价格优惠。\n\n其他选项分析：\n\n「Spot Instances（虽然有中断风险，但对于稳定负载也能获得极高折扣）」是错误的：Spot 虽然最便宜，但存在中断风险，不适合需要稳定运行的长期工作负载。\n\n「On-Demand Instances（无需任何承诺，价格虽然较高但最灵活）」是错误的：On-Demand 是所有购买选项中价格最高的，适合短期或流量波动的场景。\n\n「Dedicated Hosts（虽然价格最高，但能提供物理隔离和最高折扣）」是错误的：Dedicated Hosts 主要用于满足许可、隔离或物理服务器需求，价格通常高于 On-Demand，并非折扣最高的选择。\n\n**重点考点 / 关键词补充：**\n- 稳定长期负载 → 优先 Reserved Instances / Savings Plans（全预付折扣最高）\n- 灵活性需求高 → Savings Plans 比 RI 更灵活\n- 可预测负载 + 长期承诺 = 最大成本节省",
        "domain": "Billing, Pricing, and Support",
    },
    {
        "id": "S78",
        "question": "AWS 客户希望对 S3 对象实现自动存储成本优化，但又不想自己定义复杂的转换规则。推荐使用哪种功能？",
        "options": [
            "A. S3 Lifecycle Policies",
            "B. S3 Intelligent-Tiering",
            "C. S3 Glacier Deep Archive",
            "D. S3 Versioning",
        ],
        "correct_answers": [
            "B",
        ],
        "explanation": "「S3 Intelligent-Tiering」是正确的。\n\nS3 Intelligent-Tiering 是一种自动分层存储类，它会根据对象的访问模式自动在频繁访问层和不频繁访问层之间移动对象，无需用户定义任何转换规则，适合访问模式难以预测或变化频繁的数据。\n\n其他选项分析：\n\n「S3 Lifecycle Policies」是错误的：需要用户自己定义时间和规则，适合访问模式非常明确的场景。\n\n「S3 Glacier Deep Archive」是错误的：这是极冷归档存储类，不适合需要自动分层的场景。\n\n「S3 Versioning」是错误的：版本控制用于数据保护和恢复，与成本优化无关。\n\n**重点考点 / 关键词补充：**\n- Intelligent-Tiering：自动、无需规则、适合访问模式不确定的数据\n- Lifecycle Policies：需手动配置规则、适合可预测的访问模式\n- 两者可结合使用（Intelligent-Tiering + Lifecycle 归档层）",
        "domain": "Technology and Services",
    },
    {
        "id": "S79",
        "question": "以下关于 S3 Standard-IA 和 S3 One Zone-IA 的说法，哪一项是正确的？",
        "options": [
            "A. 两者在可用性上完全相同，因为都属于 Infrequent Access 存储类",
            "B. One Zone-IA 的可用性低于 Standard-IA，因为数据只存储在一个可用区",
            "C. One Zone-IA 比 Standard-IA 更贵，因为它提供了更高的耐久性和更快的检索性能",
            "D. 两者都不支持毫秒级检索，必须等待几秒到几分钟才能取回数据",
        ],
        "correct_answers": [
            "B",
        ],
        "explanation": "「One Zone-IA 的可用性低于 Standard-IA，因为数据只存储在一个可用区」是正确的。\n\nS3 Standard-IA 将数据跨多个可用区冗余存储（可用性 99.9%），而 S3 One Zone-IA 仅在一个可用区内存储（可用性 99.5%），因此成本更低，但无法承受单 AZ 故障。\n\n其他选项分析：\n\n「两者在可用性上完全相同，因为都属于 Infrequent Access 存储类」是错误的：Standard-IA 跨多个可用区冗余存储（可用性 99.9%），而 One Zone-IA 仅在一个可用区存储（可用性 99.5%），可用性差异是两者最核心的区别。\n\n「One Zone-IA 比 Standard-IA 更贵，因为它提供了更高的耐久性和更快的检索性能」是错误的：One Zone-IA 存储费用明显更低（通常比 Standard-IA 低 20% 左右），但耐久性和可用性也更低。\n\n「两者都不支持毫秒级检索，必须等待几秒到几分钟才能取回数据」是错误的：S3 Standard-IA 和 One Zone-IA 都支持毫秒级检索，检索延迟与 Standard 存储类基本一致。\n\n**重点考点 / 关键词补充：**\n- Standard-IA：多 AZ，高可用性，适合需要一定冗余的不频繁访问数据\n- One Zone-IA：单 AZ，最低成本 IA，适合可承受 AZ 故障的非关键数据\n- 两者都有最低 30 天存储要求和 128KB 最小对象大小",
        "domain": "Technology and Services",
    },
    {
        "id": "S80",
        "question": "在生产环境中运行 Spot Instance 时，以下哪种做法最能有效降低中断风险并保证工作负载稳定性？",
        "options": [
            "A. 只使用 Spot Instance，不使用其他购买选项，以最大化成本节省",
            "B. 使用 Spot Fleet 或 Auto Scaling Group，并配置 On-Demand 作为基础容量",
            "C. 选择最便宜的 Spot 实例类型，不考虑历史中断率和可用性",
            "D. 关闭 Spot 中断通知处理逻辑以减少系统开销并提升性能",
        ],
        "correct_answers": [
            "B",
        ],
        "explanation": "「使用 Spot Fleet 或 Auto Scaling Group，并配置 On-Demand 作为基础容量」是正确的。\n\n最佳实践是使用混合购买模型：通过 Auto Scaling Group 或 Spot Fleet 设置一定比例的 On-Demand 作为基础容量（保证稳定性），剩余容量使用 Spot 实例降低成本，同时开启容量再平衡（Capacity Rebalancing）来提前应对中断。\n\n其他选项分析：\n\n「只使用 Spot Instance，不使用其他购买选项，以最大化成本节省」是错误的：纯 Spot 模式存在中断风险，不适合对稳定性有要求的生产关键负载。\n\n「选择最便宜的 Spot 实例类型，不考虑历史中断率和可用性」是错误的：价格最低的 Spot 实例通常中断率最高，应同时参考中断率历史和可用区分布。\n\n「关闭 Spot 中断通知处理逻辑以减少系统开销并提升性能」是错误的：中断通知是提前 2 分钟应对的关键机制，关闭它会导致工作负载被无预警中断。\n\n**重点考点 / 关键词补充：**\n- 混合实例策略（On-Demand base + Spot）是生产环境推荐做法\n- 开启 Capacity Rebalancing 可提前 2 分钟前主动替换即将中断的 Spot\n- 适合无状态、可水平扩展的应用",
        "domain": "Technology and Services",
    },
    {
        "id": "S81",
        "question": "在 AWS KMS 中，关于 Customer Managed Key（CMK）的自动密钥轮换，以下哪种说法是正确的？",
        "options": [
            "A. AWS 会自动为所有 CMK 开启并执行密钥轮换",
            "B. 客户必须手动为 CMK 开启自动轮换功能，AWS 才会按年自动轮换",
            "C. CMK 的轮换由 AWS 完全控制，客户无法干预",
            "D. 只有 AWS Managed Key 支持自动轮换",
        ],
        "correct_answers": [
            "B",
        ],
        "explanation": "「客户必须手动为 CMK 开启自动轮换功能，AWS 才会按年自动轮换」是正确的。\n\n对于 Customer Managed Key，自动轮换默认是关闭的。客户需要主动在 KMS 控制台或 API 中开启自动轮换（通常为每年一次），开启后 AWS 会自动处理新密钥的生成和旧密钥的轮换，而客户仍保留对密钥的完全控制权。\n\n其他选项分析：\n\n「AWS 会自动为所有 CMK 开启」是错误的：CMK 的轮换需要客户手动启用。\n\n「CMK 的轮换由 AWS 完全控制」是错误的：客户拥有开启/关闭轮换的控制权。\n\n「只有 AWS Managed Key 支持自动轮换」是错误的：AWS Managed Key 由 AWS 管理轮换，CMK 则由客户决定是否开启。\n\n**重点考点 / 关键词补充：**\n- CMK 自动轮换：需手动开启（每年一次）\n- 轮换后旧密钥仍可用于解密，但新加密操作使用新密钥\n- AWS Managed Key：轮换由 AWS 自动管理，客户无感知",
        "domain": "Security and Compliance",
    },
    {
        "id": "S82",
        "question": "在 S3 存储桶策略（Bucket Policy）中，以下哪个元素最常用于限制只有特定 VPC 内的资源才能访问该存储桶？",
        "options": [
            "A. 在 Principal 字段中直接指定 VPC ID 或 VPC Endpoint ID",
            "B. 在 Action 中使用 vpc:RestrictAccess 这样的条件操作",
            "C. Condition（配合 aws:SourceVpc 或 aws:SourceVpce）",
            "D. 在 Resource ARN 中添加 vpc 标签作为访问控制条件",
        ],
        "correct_answers": [
            "C",
        ],
        "explanation": "「Condition（配合 aws:SourceVpc 或 aws:SourceVpce）」是正确的。\n\n在 S3 Bucket Policy 中，通过 Condition 块使用 aws:SourceVpc 或 aws:SourceVpce 条件键，可以精确限制只有来自特定 VPC 或 VPC Endpoint 的请求才能访问存储桶。这是实现 VPC 级私有访问控制的常用且强大的方式。\n\n其他选项分析：\n\n「在 Principal 字段中直接指定 VPC ID 或 VPC Endpoint ID」是错误的：Principal 用于指定允许访问的身份（IAM 用户、角色、AWS 服务等），不能用来限制请求来源的 VPC。\n\n「在 Action 中使用 vpc:RestrictAccess 这样的条件操作」是错误的：Action 字段只定义允许或拒绝哪些 S3 操作，不支持用 VPC 相关的条件键。\n\n「在 Resource ARN 中添加 vpc 标签作为访问控制条件」是错误的：Resource 字段用于指定策略适用的 S3 资源，VPC 限制必须通过 Condition 块实现，而非在 ARN 中硬编码。\n\n**重点考点 / 关键词补充：**\n- aws:SourceVpc：限制特定 VPC\n- aws:SourceVpce：限制特定 VPC Endpoint（更常用）\n- 常与 VPC Endpoint Policy 配合使用，实现端到端私有访问",
        "domain": "Security and Compliance",
    },
    {
        "id": "S83",
        "question": "AWS 客户希望为组织内所有账户统一设置成本分配标签（Cost Allocation Tags），以便在 AWS Cost Explorer 和 Billing 中按业务部门进行成本分析。最佳做法是什么？",
        "options": [
            "A. 在每个成员账户中分别手动激活相同的成本分配标签键",
            "B. 在 AWS Organizations 管理账户中激活标签键，所有成员账户自动继承",
            "C. 只在 Organizations 的根账户（Root Account）中激活一次标签键即可",
            "D. 标签激活后立即在 Cost Explorer 和 Billing 报表中实时显示，无需任何等待时间",
        ],
        "correct_answers": [
            "B",
        ],
        "explanation": "「在 AWS Organizations 管理账户中激活标签键，所有成员账户自动继承」是正确的。\n\n对于使用 AWS Organizations 的企业，应在管理账户（Management Account）中激活成本分配标签键，这样所有成员账户都会自动继承这些标签设置，便于在整个组织范围内统一进行成本归属和分析。\n\n其他选项分析：\n\n「在每个成员账户中分别手动激活相同的成本分配标签键」是错误的：这种方式效率极低，且容易出现各账户标签键不一致的问题，难以实现全组织统一成本分析。\n\n「只在 Organizations 的根账户（Root Account）中激活一次标签键即可」是错误的：成本分配标签必须在 Organizations 的管理账户（Management Account）中激活，而非根账户（Root）。\n\n「标签激活后立即在 Cost Explorer 和 Billing 报表中实时显示，无需任何等待时间」是错误的：成本分配标签激活后通常需要 24 小时左右的延迟才能在 Cost Explorer 和 Billing 中生效显示。\n\n**重点考点 / 关键词补充：**\n- 成本分配标签需先在 Organizations 管理账户激活\n- 激活后有延迟（通常 24 小时）\n- 推荐为业务部门、项目、环境等定义标准化标签键",
        "domain": "Billing, Pricing, and Support",
    },
    {
        "id": "S84",
        "question": "在 VPC 中部署 NAT Gateway 时，为了实现高可用性（High Availability），正确的做法是什么？",
        "options": [
            "A. 在单个可用区（AZ）内部署一个 NAT Gateway 即可",
            "B. 在每个需要的可用区中分别部署一个 NAT Gateway，并配置相应的路由表",
            "C. 使用一个 NAT Gateway 并通过 Route 53 实现故障转移",
            "D. NAT Gateway 天生跨可用区高可用，无需额外配置",
        ],
        "correct_answers": [
            "B",
        ],
        "explanation": "「在每个需要的可用区中分别部署一个 NAT Gateway，并配置相应的路由表」是正确的。\n\nNAT Gateway 是可用区级别的服务（AZ-scoped）。如果一个可用区发生故障，该 AZ 内的 NAT Gateway 也会不可用。为实现高可用，必须在每个需要互联网访问的私有子网所在的可用区中独立部署 NAT Gateway，并为每个 AZ 的私有子网路由表指向本 AZ 的 NAT Gateway。\n\n其他选项分析：\n\n「在单个可用区内部署一个即可」是错误的：单 AZ 部署在该 AZ 故障时会导致整个私有子网失去互联网访问能力。\n\n「使用 Route 53 实现故障转移」是错误的：Route 53 不能直接用于 NAT Gateway 的 HA，NAT Gateway 本身不支持跨 AZ 故障转移。\n\n「NAT Gateway 天生跨可用区高可用」是错误的：NAT Gateway 是 AZ 级资源，不是 Region 级服务。\n\n**重点考点 / 关键词补充：**\n- NAT Gateway 是 AZ-scoped 服务\n- HA 最佳实践：在每个 AZ 独立部署 + 对应路由表指向本 AZ 的 NAT\n- 每个 NAT Gateway 有独立的 EIP 和带宽限制",
        "domain": "Technology and Services",
    },
    {
        "id": "S85",
        "question": "在 S3 Object Lock 中，以下关于 Governance 模式和 Compliance 模式的区别，哪一项是正确的？",
        "options": [
            "A. Governance 模式下，特定权限的用户可以提前删除或缩短保留期；Compliance 模式下任何用户（包括 root）都无法提前删除",
            "B. Governance 模式和 Compliance 模式在保留期内都允许 root 用户提前删除对象，只是审计日志不同",
            "C. Compliance 模式下 root 用户可以随时解除 Object Lock 保护，而 Governance 模式则完全无法解除",
            "D. Governance 模式主要用于防止误删除，Compliance 模式则主要用于防止勒索软件攻击",
        ],
        "correct_answers": [
            "A",
        ],
        "explanation": "「Governance 模式下，特定权限的用户可以提前删除或缩短保留期；Compliance 模式下任何用户（包括 root）都无法提前删除」是正确的。\n\nGovernance 模式相对灵活，拥有 s3:BypassGovernanceRetention 权限的用户可以在保留期内删除对象或缩短保留期；Compliance 模式极其严格，在保留期内任何用户（包括 AWS 账户 root 用户）都无法删除或缩短保留期，满足最严格的监管要求（如 SEC 17a-4）。\n\n其他选项分析：\n\n「Governance 模式和 Compliance 模式在保留期内都允许 root 用户提前删除对象，只是审计日志不同」是错误的：Governance 模式允许拥有特定权限的用户提前删除或缩短保留期，但 Compliance 模式下任何用户（包括 root）都无法提前删除或缩短保留期。\n\n「Compliance 模式下 root 用户可以随时解除 Object Lock 保护，而 Governance 模式则完全无法解除」是错误的：实际情况完全相反，Compliance 模式下 root 用户也无法提前删除，而 Governance 模式下特定权限用户可以绕过。\n\n「Governance 模式主要用于防止误删除，Compliance 模式则主要用于防止勒索软件攻击」是错误的：两者都可以防止误删除和恶意删除，核心区别在于是否允许特定权限用户绕过保留期。\n\n**重点考点 / 关键词补充：**\n- Governance：可由特定权限用户绕过（适合内部治理）\n- Compliance：任何人（含 root）都无法提前删除（适合外部监管）\n- 开启后 Object Lock 版本无法关闭（只能延长保留期）",
        "domain": "Security and Compliance",
    },
    {
        "id": "S86",
        "question": "以下关于 AWS KMS Customer Managed Key（CMK）的说法，哪一项是正确的？",
        "options": [
            "A. CMK 的密钥策略（Key Policy）可以完全替代 IAM Policy 进行访问控制",
            "B. CMK 的密钥策略（Key Policy）是必选的，即使同时使用 IAM Policy 也必须存在",
            "C. CMK 默认允许所有 IAM 用户访问，无需额外配置",
            "D. CMK 的密钥策略只能由 AWS 管理，客户无法修改",
        ],
        "correct_answers": [
            "B",
        ],
        "explanation": "「CMK 的密钥策略（Key Policy）是必选的，即使同时使用 IAM Policy 也必须存在」是正确的。\n\n每个 Customer Managed Key 都必须有一个密钥策略（Key Policy）。密钥策略是 KMS 资源级策略，是控制 CMK 访问的基础。即使你同时使用 IAM Policy，密钥策略也必须存在且至少定义一个管理员或使用者。\n\n其他选项分析：\n\n「CMK 的密钥策略可以完全替代 IAM Policy」是错误的：两者通常配合使用，密钥策略是基础，IAM Policy 提供更细粒度控制。\n\n「CMK 默认允许所有 IAM 用户访问」是错误的：默认情况下 CMK 没有开放访问，必须通过策略显式授权。\n\n「密钥策略只能由 AWS 管理」是错误的：客户完全拥有并管理 CMK 的密钥策略。\n\n**重点考点 / 关键词补充：**\n- 每个 CMK 必须有 Key Policy（资源策略）\n- Key Policy + IAM Policy 共同生效（显式允许）\n- Key Policy 中至少需要定义一个管理员或使用者",
        "domain": "Security and Compliance",
    },
    {
        "id": "S87",
        "question": "在 Amazon EC2 Auto Scaling Group 中使用 Spot Instance 时，以下哪种分配策略（Allocation Strategy）最适合对中断敏感但又希望获得较低价格的工作负载？",
        "options": [
            "A. lowest-price（最低价格）",
            "B. capacity-optimized（容量优化）",
            "C. capacity-optimized-prioritized（容量优化优先）",
            "D. diversified（分散）",
        ],
        "correct_answers": [
            "B",
        ],
        "explanation": "「capacity-optimized（容量优化）」是正确的。\n\ncapacity-optimized 策略会优先从 Spot 容量最充足的实例池中选择 Spot Instance，从而显著降低中断概率，同时仍然能获得比 On-Demand 低很多的价格，适合对中断相对敏感但又希望节省成本的工作负载。\n\n其他选项分析：\n\n「lowest-price」是错误的：它只追求最低价格，容易选中中断率极高的实例池，导致频繁中断。\n\n「capacity-optimized-prioritized」是错误的：这是 capacity-optimized 的变体，允许你指定实例类型优先级，更适合有特定实例类型偏好的场景。\n\n「diversified」是错误的：它会在多个实例池中分散请求，适合极大规模场景，但中断控制不如 capacity-optimized。\n\n**重点考点 / 关键词补充：**\n- lowest-price：价格最低，但中断风险最高\n- capacity-optimized：中断概率最低，推荐用于生产\n- capacity-optimized-prioritized：容量优化 + 实例类型优先级",
        "domain": "Technology and Services",
    },
    {
        "id": "S88",
        "question": "在 AWS IAM 中，以下关于 Permission Boundary（权限边界）的描述，哪一项是正确的？",
        "options": [
            "A. Permission Boundary 可以扩大 IAM 实体的权限范围",
            "B. Permission Boundary 是一种高级功能，用于设置 IAM 实体（用户或角色）可以拥有的最大权限上限",
            "C. Permission Boundary 只能应用于根用户（Root User）",
            "D. 一旦设置 Permission Boundary，IAM Policy 将不再生效",
        ],
        "correct_answers": [
            "B",
        ],
        "explanation": "「Permission Boundary 是一种高级功能，用于设置 IAM 实体（用户或角色）可以拥有的最大权限上限」是正确的。\n\nPermission Boundary 是一种 IAM 策略，用于为 IAM 用户或角色设置权限“天花板”。即使该实体被附加了权限更大的 IAM Policy，其实际生效的权限也不会超过 Permission Boundary 定义的范围，常用于委托管理员场景下的安全边界控制。\n\n其他选项分析：\n\n「可以扩大 IAM 实体的权限范围」是错误的：它只会限制（缩小）权限，不会扩大。\n\n「只能应用于根用户」是错误的：Permission Boundary 应用于 IAM 用户和角色，根用户不受 IAM 策略限制。\n\n「IAM Policy 将不再生效」是错误的：Permission Boundary 和 IAM Policy 是“交集”关系（两者都允许的权限才生效）。\n\n**重点考点 / 关键词补充：**\n- Permission Boundary 设置“最大权限上限”（不能超过）\n- 与 IAM Policy 取交集生效\n- 常见用于限制通过 IAM Roles Anywhere 或委托创建的角色权限",
        "domain": "Security and Compliance",
    },
    {
        "id": "S89",
        "question": "AWS 客户购买了 Compute Savings Plans 后，以下哪种使用方式可以获得最高的折扣？",
        "options": [
            "A. 只在特定 Region 和特定 EC2 实例家族中使用，以锁定最高折扣率",
            "B. 在任何 Region、任何计算服务（EC2、Fargate、Lambda）上使用，只要符合承诺的计算用量",
            "C. 只能用于运行在 EC2 上的工作负载，Fargate 和 Lambda 不支持",
            "D. 必须提前指定具体的实例类型、操作系统和可用区才能生效",
        ],
        "correct_answers": [
            "B",
        ],
        "explanation": "「在任何 Region、任何计算服务（EC2、Fargate、Lambda）上使用，只要符合承诺的计算用量」是正确的。\n\nCompute Savings Plans 提供最高的灵活性：承诺一定的每小时计算用量（以 USD 计算）后，可以在任何 Region、任何 AWS 区域的 EC2、AWS Fargate、AWS Lambda 上使用，折扣通常在 17%~66% 之间，灵活性远高于 EC2 Instance Savings Plans。\n\n其他选项分析：\n\n「只在特定 Region 和特定 EC2 实例家族中使用，以锁定最高折扣率」是错误的：这是 EC2 Instance Savings Plans 的特点，Compute Savings Plans 的优势正是跨 Region 和跨实例家族的灵活性。\n\n「只能用于运行在 EC2 上的工作负载，Fargate 和 Lambda 不支持」是错误的：Compute Savings Plans 最大的卖点之一就是支持 Fargate 和 Lambda 计算用量。\n\n「必须提前指定具体的实例类型、操作系统和可用区才能生效」是错误的：这是 Reserved Instances 或 EC2 Instance Savings Plans 的限制，Compute Savings Plans 不需要这种提前指定。\n\n**重点考点 / 关键词补充：**\n- Compute Savings Plans：最高灵活性，支持 EC2/Fargate/Lambda\n- EC2 Instance Savings Plans：折扣更高，但仅限特定实例家族和 Region\n- 两者都支持 1 年或 3 年承诺（No Upfront / Partial / All Upfront）",
        "domain": "Billing, Pricing, and Support",
    },
    {
        "id": "S90",
        "question": "AWS 客户希望对 S3 对象实现自动存储分层，但又需要偶尔对归档层的数据进行毫秒级快速检索。推荐使用哪种 S3 存储类功能？",
        "options": [
            "A. 使用 S3 Lifecycle 策略将对象手动转移到 Glacier Deep Archive，并在需要时发起恢复请求",
            "B. S3 Intelligent-Tiering 的 Archive Instant Access 层",
            "C. 将对象存储在 S3 Standard-IA 中，并结合 S3 Batch Operations 进行定期分析",
            "D. 使用 S3 One Zone-IA 配合跨 Region 复制来实现低成本和高可用",
        ],
        "correct_answers": [
            "B",
        ],
        "explanation": "「S3 Intelligent-Tiering 的 Archive Instant Access 层」是正确的。\n\nS3 Intelligent-Tiering 支持 Archive Instant Access 层，它会自动将 90 天未访问的对象移动到低成本的归档层，但仍保持毫秒级的检索性能，非常适合访问模式不规律但偶尔需要快速访问的数据。\n\n其他选项分析：\n\n「使用 S3 Lifecycle 策略将对象手动转移到 Glacier Deep Archive，并在需要时发起恢复请求」是错误的：Glacier Deep Archive 的检索时间通常为 12 小时，不支持毫秒级快速访问，且需要手动发起恢复。\n\n「将对象存储在 S3 Standard-IA 中，并结合 S3 Batch Operations 进行定期分析」是错误的：Standard-IA 本身不具备自动分层能力，需要手动管理，且 Batch Operations 主要是批量处理工具，不是自动分层方案。\n\n「使用 S3 One Zone-IA 配合跨 Region 复制来实现低成本和高可用」是错误的：One Zone-IA 的可用性只有 99.5%，且跨 Region 复制会产生额外费用，并不能实现真正的自动智能分层。\n\n**重点考点 / 关键词补充：**\n- Intelligent-Tiering Archive Instant Access：90天自动归档 + 毫秒级检索\n- 适合访问不规律但需快速检索的场景\n- 比手动 Lifecycle 更智能，无需预定义规则",
        "domain": "Technology and Services",
    },
    {
        "id": "S91",
        "question": "在 AWS Organizations 中，当需要同时限制 IAM 角色权限并防止权限边界被绕过时，最佳的组合方式是什么？",
        "options": [
            "A. 只使用 SCP（Service Control Policies）",
            "B. 只使用 IAM Permission Boundary",
            "C. 同时使用 SCP + IAM Permission Boundary",
            "D. 只使用 IAM Policy",
        ],
        "correct_answers": [
            "C",
        ],
        "explanation": "「同时使用 SCP + IAM Permission Boundary」是正确的。\n\nSCP 在 Organizations 级别为账户或 OU 设置硬性权限边界（Deny 优先），而 Permission Boundary 则为特定 IAM 角色/用户设置“最大权限上限”。两者结合使用可以实现多层防御：SCP 防止整个账户越权，Permission Boundary 防止特定角色被授予过多权限，常用于安全委托管理员场景。\n\n其他选项分析：\n\n「只使用 SCP」是错误的：SCP 是账户级，无法针对具体角色做精细上限控制。\n\n「只使用 IAM Permission Boundary」是错误的：它无法防止账户级别的越权行为。\n\n「只使用 IAM Policy」是错误的：IAM Policy 本身无法提供组织级或角色级上限保护。\n\n**重点考点 / 关键词补充：**\n- SCP：组织级硬边界（Deny 优先）\n- Permission Boundary：角色/用户级权限“天花板”\n- 两者结合使用是委托管理员场景的最佳实践",
        "domain": "Security and Compliance",
    },
    {
        "id": "S92",
        "question": "使用 VPC Interface Endpoint 访问 AWS 服务时，以下哪项配置是确保流量不经过公网且 DNS 解析正确的关键？",
        "options": [
            "A. 开启 Private DNS 名称并在安全组中允许 HTTPS 入站",
            "B. 只创建 Endpoint，无需任何额外配置",
            "C. 使用公有 DNS 解析并通过 NAT Gateway 转发",
            "D. 在路由表中添加指向 Endpoint 的路由",
        ],
        "correct_answers": [
            "A",
        ],
        "explanation": "「开启 Private DNS 名称并在安全组中允许 HTTPS 入站」是正确的。\n\n开启 Private DNS 后，AWS 会自动将服务域名解析到 Endpoint 的私有 IP。安全组需要允许来自私有子网的 HTTPS 入站流量（端口 443），才能让私有子网内的资源通过 Endpoint 私密访问服务。\n\n其他选项分析：\n\n「只创建 Endpoint，无需任何额外配置」是错误的：必须开启 Private DNS 并配置安全组规则。\n\n「使用公有 DNS 解析并通过 NAT Gateway」是错误的：这会走公网，违背私有访问的目的。\n\n「在路由表中添加指向 Endpoint 的路由」是错误的：Interface Endpoint 不通过路由表，而是通过 ENI + DNS 解析。\n\n**重点考点 / 关键词补充：**\n- Interface Endpoint 必须开启 Private DNS 才能实现透明访问\n- 安全组规则是必需的（允许 443 入站）\n- Gateway Endpoint 通过路由表，Interface Endpoint 通过 DNS + ENI",
        "domain": "Technology and Services",
    },
    {
        "id": "S93",
        "question": "AWS 客户希望将本地 Oracle 数据库迁移到 AWS，同时尽量减少对现有应用代码的修改，并且希望获得托管数据库的运维优势。最佳方案是什么？",
        "options": [
            "A. 直接在 Amazon EC2 上部署 Oracle 数据库并完全自行负责运维",
            "B. 使用 AWS Database Migration Service (DMS) 迁移到 Amazon RDS for Oracle",
            "C. 将 Oracle 数据文件直接上传到 Amazon S3，然后使用 Amazon RDS Custom 手动恢复",
            "D. 使用 AWS Snowball Edge 将整个 Oracle 数据库服务器进行离线物理迁移",
        ],
        "correct_answers": [
            "B",
        ],
        "explanation": "「使用 AWS Database Migration Service (DMS) 迁移到 Amazon RDS for Oracle」是正确的。\n\nDMS 可以进行同构（Oracle 到 Oracle）或异构迁移，同时 RDS for Oracle 提供托管的运维优势（备份、打补丁、高可用、多可用区等），并且对应用代码的修改最小，是最符合“少改代码 + 托管运维”需求的方案。\n\n其他选项分析：\n\n「直接在 Amazon EC2 上部署 Oracle 数据库并完全自行负责运维」是错误的：虽然技术可行，但需要自己处理备份、补丁、高可用、监控等大量运维工作，完全失去了托管数据库的优势。\n\n「将 Oracle 数据文件直接上传到 Amazon S3，然后使用 Amazon RDS Custom 手动恢复」是错误的：这不是标准做法，且手动恢复复杂，无法获得 RDS 提供的自动化托管运维能力。\n\n「使用 AWS Snowball Edge 将整个 Oracle 数据库服务器进行离线物理迁移」是错误的：Snowball Edge 主要用于大规模离线数据迁移，不适合正在运行的数据库的在线迁移场景。\n\n**重点考点 / 关键词补充：**\n- DMS 支持同构和异构数据库迁移\n- RDS for Oracle 提供托管运维优势\n- 最小化应用代码修改是关键考点",
        "domain": "Technology and Services",
    },
    {
        "id": "S94",
        "question": "以下哪种应用场景最适合使用 AWS Global Accelerator 而不是 Amazon CloudFront？",
        "options": [
            "A. 全球用户访问静态图片和视频内容",
            "B. 全球用户通过 TCP/UDP 协议访问游戏服务器或 VoIP 应用",
            "C. 缓存动态 API 响应以降低延迟",
            "D. 为 S3 存储桶提供全球 CDN 加速",
        ],
        "correct_answers": [
            "B",
        ],
        "explanation": "「全球用户通过 TCP/UDP 协议访问游戏服务器或 VoIP 应用」是正确的。\n\nAWS Global Accelerator 使用 Anycast IP + AWS 全球骨干网，能显著加速非 HTTP/HTTPS 的 TCP/UDP 流量，特别适合对延迟敏感的游戏、VoIP、金融交易等应用。而 CloudFront 主要优化 HTTP/HTTPS 静态和动态内容缓存。\n\n其他选项分析：\n\n「全球用户访问静态图片和视频内容」是错误的：这是 CloudFront 的强项。\n\n「缓存动态 API 响应以降低延迟」是错误的：CloudFront 更适合此场景。\n\n「为 S3 存储桶提供全球 CDN 加速」是错误的：CloudFront + S3 是标准组合。\n\n**重点考点 / 关键词补充：**\n- Global Accelerator：TCP/UDP + Anycast + 全球骨干网\n- CloudFront：HTTP/HTTPS + 边缘缓存\n- 两者经常结合使用（Global Accelerator + CloudFront）",
        "domain": "Cloud Concepts",
    },
    {
        "id": "S95",
        "question": "AWS 客户希望自动检测账户中的异常成本支出，并在发现异常时立即收到告警。推荐使用哪项服务？",
        "options": [
            "A. AWS Budgets",
            "B. AWS Cost Anomaly Detection",
            "C. AWS Cost Explorer",
            "D. AWS Trusted Advisor",
        ],
        "correct_answers": [
            "B",
        ],
        "explanation": "「AWS Cost Anomaly Detection」是正确的。\n\nAWS Cost Anomaly Detection 使用机器学习自动监控成本模式，当检测到异常支出（例如突然的费用激增）时，会自动创建异常告警并通过 SNS 或 Email 通知用户。它比手动设置预算阈值更智能，适合发现未知的成本异常。\n\n其他选项分析：\n\n「AWS Budgets」是错误的：Budgets 需要用户预先定义预算阈值，无法自动发现未知异常。\n\n「AWS Cost Explorer」是错误的：Cost Explorer 用于分析和可视化历史成本，不提供实时异常告警。\n\n「AWS Trusted Advisor」是错误的：Trusted Advisor 提供最佳实践检查，不专注于成本异常检测。\n\n**重点考点 / 关键词补充：**\n- Cost Anomaly Detection 使用 ML 自动发现异常\n- 支持按服务、账户、标签等维度监控\n- 与 SNS 集成实现自动告警",
        "domain": "Billing, Pricing, and Support",
    },
    {
        "id": "S96",
        "question": "AWS 客户希望获得 S3 存储桶的存储使用情况、访问模式和成本优化建议的自动化报告，最推荐使用哪项服务？",
        "options": [
            "A. AWS Cost Explorer",
            "B. S3 Storage Lens",
            "C. AWS Trusted Advisor",
            "D. Amazon CloudWatch",
        ],
        "correct_answers": [
            "B",
        ],
        "explanation": "「S3 Storage Lens」是正确的。\n\nS3 Storage Lens 提供跨账户、跨区域的 S3 存储使用情况和活动指标的聚合视图，并使用机器学习提供成本优化建议（如未使用版本的存储、未加密对象等）。它是目前最全面的 S3 存储分析和优化工具。\n\n其他选项分析：\n\n「AWS Cost Explorer」是错误的：Cost Explorer 主要关注成本趋势，不提供 S3 特定的存储使用和优化建议。\n\n「AWS Trusted Advisor」是错误的：Trusted Advisor 提供有限的 S3 检查，但深度和范围远不如 S3 Storage Lens。\n\n「Amazon CloudWatch」是错误的：CloudWatch 主要用于监控指标和日志，不提供 S3 存储分析和优化建议。\n\n**重点考点 / 关键词补充：**\n- S3 Storage Lens：跨账户/区域聚合 + ML 驱动的优化建议\n- 支持免费层和高级指标（付费）\n- 常见建议包括：未使用版本、未加密对象、冷数据转 IA",
        "domain": "Technology and Services",
    },
    {
        "id": "S97",
        "question": "以下关于 AWS IAM Roles Anywhere 的描述，哪一项是正确的？",
        "options": [
            "A. IAM Roles Anywhere 只能用于 AWS 内部服务",
            "B. IAM Roles Anywhere 允许在本地服务器或容器中使用 IAM 角色，无需长期访问密钥",
            "C. IAM Roles Anywhere 要求必须使用 AWS 管理控制台",
            "D. IAM Roles Anywhere 只能用于 EC2 实例",
        ],
        "correct_answers": [
            "B",
        ],
        "explanation": "「IAM Roles Anywhere 允许在本地服务器或容器中使用 IAM 角色，无需长期访问密钥」是正确的。\n\nIAM Roles Anywhere 让本地服务器、容器或任何支持 X.509 证书的工作负载能够通过短期凭证获取 IAM 角色权限，从而实现“零长期密钥”的安全最佳实践，特别适合混合云或本地工作负载。\n\n其他选项分析：\n\n「只能用于 AWS 内部服务」是错误的：它是专门为本地/外部工作负载设计的。\n\n「要求必须使用 AWS 管理控制台」是错误的：它是 API/CLI 驱动的。\n\n「只能用于 EC2 实例」是错误的：EC2 通常直接使用 IAM 角色，Roles Anywhere 主要用于非 AWS 环境。\n\n**重点考点 / 关键词补充：**\n- Roles Anywhere：基于 X.509 证书的短期凭证\n- 主要用于本地服务器、容器、混合云场景\n- 显著降低长期访问密钥泄露风险",
        "domain": "Security and Compliance",
    },
    {
        "id": "S98",
        "question": "AWS 客户希望将本地 Oracle 数据库迁移到 AWS，同时尽量减少对现有应用代码的修改，并且希望获得托管数据库的运维优势。最佳方案是什么？",
        "options": [
            "A. 直接在 Amazon EC2 上部署 Oracle 数据库并完全自行负责运维",
            "B. 使用 AWS Database Migration Service (DMS) 迁移到 Amazon RDS for Oracle",
            "C. 将 Oracle 数据文件直接上传到 Amazon S3，然后使用 Amazon RDS Custom 手动恢复",
            "D. 使用 AWS Snowball Edge 将整个 Oracle 数据库服务器进行离线物理迁移",
        ],
        "correct_answers": [
            "B",
        ],
        "explanation": "「使用 AWS Database Migration Service (DMS) 迁移到 Amazon RDS for Oracle」是正确的。\n\nDMS 可以进行同构（Oracle 到 Oracle）或异构迁移，同时 RDS for Oracle 提供托管的运维优势（备份、打补丁、高可用、多可用区等），并且对应用代码的修改最小，是最符合“少改代码 + 托管运维”需求的方案。\n\n其他选项分析：\n\n「直接在 Amazon EC2 上部署 Oracle 数据库并完全自行负责运维」是错误的：虽然技术可行，但需要自己处理备份、补丁、高可用、监控等大量运维工作，完全失去了托管数据库的优势。\n\n「将 Oracle 数据文件直接上传到 Amazon S3，然后使用 Amazon RDS Custom 手动恢复」是错误的：这不是标准做法，且手动恢复复杂，无法获得 RDS 提供的自动化托管运维能力。\n\n「使用 AWS Snowball Edge 将整个 Oracle 数据库服务器进行离线物理迁移」是错误的：Snowball Edge 主要用于大规模离线数据迁移，不适合正在运行的数据库的在线迁移场景。\n\n**重点考点 / 关键词补充：**\n- DMS 支持同构和异构数据库迁移\n- RDS for Oracle 提供托管运维优势\n- 最小化应用代码修改是关键考点",
        "domain": "Technology and Services",
    },
    {
        "id": "S99",
        "question": "以下哪种应用场景最适合使用 AWS Global Accelerator 而不是 Amazon CloudFront？",
        "options": [
            "A. 全球用户访问静态图片和视频内容",
            "B. 全球用户通过 TCP/UDP 协议访问游戏服务器或 VoIP 应用",
            "C. 缓存动态 API 响应以降低延迟",
            "D. 为 S3 存储桶提供全球 CDN 加速",
        ],
        "correct_answers": [
            "B",
        ],
        "explanation": "「全球用户通过 TCP/UDP 协议访问游戏服务器或 VoIP 应用」是正确的。\n\nAWS Global Accelerator 使用 Anycast IP + AWS 全球骨干网，能显著加速非 HTTP/HTTPS 的 TCP/UDP 流量，特别适合对延迟敏感的游戏、VoIP、金融交易等应用。而 CloudFront 主要优化 HTTP/HTTPS 静态和动态内容缓存。\n\n其他选项分析：\n\n「全球用户访问静态图片和视频内容」是错误的：这是 CloudFront 的强项。\n\n「缓存动态 API 响应以降低延迟」是错误的：CloudFront 更适合此场景。\n\n「为 S3 存储桶提供全球 CDN 加速」是错误的：CloudFront + S3 是标准组合。\n\n**重点考点 / 关键词补充：**\n- Global Accelerator：TCP/UDP + Anycast + 全球骨干网\n- CloudFront：HTTP/HTTPS + 边缘缓存\n- 两者经常结合使用（Global Accelerator + CloudFront）",
        "domain": "Cloud Concepts",
    },
    {
        "id": "S100",
        "question": "在 Amazon EC2 Auto Scaling Group 中使用 Spot Instance 时，以下哪种分配策略（Allocation Strategy）最适合对中断敏感但又希望获得较低价格的工作负载？",
        "options": [
            "A. lowest-price（最低价格）",
            "B. capacity-optimized（容量优化）",
            "C. capacity-optimized-prioritized（容量优化优先）",
            "D. diversified（分散）",
        ],
        "correct_answers": [
            "B",
        ],
        "explanation": "「capacity-optimized（容量优化）」是正确的。\n\ncapacity-optimized 策略会优先从 Spot 容量最充足的实例池中选择 Spot Instance，从而显著降低中断概率，同时仍然能获得比 On-Demand 低很多的价格，适合对中断相对敏感但又希望节省成本的工作负载。\n\n其他选项分析：\n\n「lowest-price」是错误的：它只追求最低价格，容易选中中断率极高的实例池，导致频繁中断。\n\n「capacity-optimized-prioritized」是错误的：这是 capacity-optimized 的变体，允许你指定实例类型优先级，更适合有特定实例类型偏好的场景。\n\n「diversified」是错误的：它会在多个实例池中分散请求，适合极大规模场景，但中断控制不如 capacity-optimized。\n\n**重点考点 / 关键词补充：**\n- lowest-price：价格最低，但中断风险最高\n- capacity-optimized：中断概率最低，推荐用于生产\n- capacity-optimized-prioritized：容量优化 + 实例类型优先级",
        "domain": "Technology and Services",
    },
    {
        "id": "S101",
        "question": "AWS 客户希望对多个账户的成本进行高级归类和分析，例如按业务部门、项目或环境进行多维度成本分摊。推荐使用哪项服务？",
        "options": [
            "A. AWS Cost Explorer",
            "B. AWS Cost Categories",
            "C. AWS Budgets",
            "D. Amazon CloudWatch",
        ],
        "correct_answers": [
            "B",
        ],
        "explanation": "「AWS Cost Categories」是正确的。\n\nAWS Cost Categories 允许用户定义自定义规则，将成本按业务维度（部门、项目、环境等）进行归类，支持多层级分层，并在 Cost Explorer、Budgets 和 Billing 中使用这些类别进行分析，是高级成本分摊的核心工具。\n\n其他选项分析：\n\n「AWS Cost Explorer」是错误的：Cost Explorer 是分析工具，但本身不提供自定义成本归类功能。\n\n「AWS Budgets」是错误的：Budgets 主要用于预算和告警，不负责成本归类。\n\n「Amazon CloudWatch」是错误的：CloudWatch 用于监控和日志，与成本归类无关。\n\n**重点考点 / 关键词补充：**\n- Cost Categories：自定义多维度成本归类（支持继承规则）\n- 可在 Cost Explorer、Budgets 中使用\n- 适合复杂组织的多维度成本分摊和分析",
        "domain": "Billing, Pricing, and Support",
    },
    {
        "id": "S103",
        "question": "以下关于 Multi-AZ 部署和 Multi-Region 部署的描述，哪一项是正确的？",
        "options": [
            "A. Multi-AZ 部署可以实现跨 Region 的灾难恢复",
            "B. Multi-AZ 部署主要用于消除单点故障和提高可用性，而跨 Region 灾难恢复需要额外架构",
            "C. Multi-Region 部署的延迟通常低于 Multi-AZ 部署",
            "D. 两者效果完全相同，只是名称不同",
        ],
        "correct_answers": [
            "B",
        ],
        "explanation": "「Multi-AZ 部署主要用于消除单点故障和提高可用性，而跨 Region 灾难恢复需要额外架构」是正确的。\n\nMulti-AZ（同一 Region 内多个可用区）主要解决高可用和单点故障问题；真正的跨 Region 灾难恢复（RPO/RTO 要求极高）需要多 Region 架构（如跨 Region 复制、Route 53 故障转移等）。\n\n其他选项分析：\n\n「Multi-AZ 部署可以实现跨 Region 的灾难恢复」是错误的：Multi-AZ 无法跨越 Region 边界。\n\n「Multi-Region 部署的延迟通常低于 Multi-AZ 部署」是错误的：跨 Region 延迟通常更高。\n\n「两者效果完全相同」是错误的：两者解决的问题范围和复杂度差异很大。\n\n**重点考点 / 关键词补充：**\n- Multi-AZ：高可用 + 消除单点故障（同一 Region 内）\n- Multi-Region 灾难恢复：需要额外架构（跨 Region 复制、Route 53 故障转移等）\n- 两者经常结合使用实现不同层级的容灾",
        "domain": "Cloud Concepts",
    },
    {
        "id": "S104",
        "question": "以下关于 AWS Edge Location 和 Local Zones 的描述，哪一项是正确的？",
        "options": [
            "A. Edge Location 可以运行完整的 EC2 实例和 RDS 数据库",
            "B. Local Zones 主要用于全球内容缓存加速，而 Edge Location 用于运行低延迟应用",
            "C. Edge Location 主要用于降低延迟的内容分发，Local Zones 则允许在靠近人口中心的位置运行完整的 AWS 服务",
            "D. 两者是完全相同的概念，只是不同 Region 的叫法不同",
        ],
        "correct_answers": [
            "C",
        ],
        "explanation": "「Edge Location 主要用于降低延迟的内容分发，Local Zones 则允许在靠近人口中心的位置运行完整的 AWS 服务」是正确的。\n\nEdge Location 是 CloudFront 和 Global Accelerator 使用的全球边缘节点，主要功能是内容缓存和加速；Local Zones 是较新的基础设施形式，部署在靠近大城市的位置，让客户能以极低延迟运行完整的 AWS 服务（如 EC2、EBS、RDS 等）。\n\n其他选项分析：\n\n「Edge Location 可以运行完整的 EC2 实例和 RDS 数据库」是错误的：Edge Location 主要提供缓存和加速能力，不支持完整计算服务。\n\n「Local Zones 主要用于全球内容缓存加速」是错误的：这是 Edge Location 的主要用途。\n\n「两者是完全相同的概念」是错误的：两者定位和能力差异很大。\n\n**重点考点 / 关键词补充：**\n- Edge Location：全球内容分发网络节点（CloudFront/Global Accelerator）\n- Local Zones：靠近人口中心，可运行完整 AWS 服务，低延迟计算\n- 两者都属于全球基础设施的补充形式，核心仍是 Region + AZ",
        "domain": "Cloud Concepts",
    },
    {
        "id": "S105",
        "question": "AWS Global Accelerator 特别适合以下哪类应用场景？",
        "options": [
            "A. 全球用户访问静态图片和视频内容，需要极低的首字节延迟和边缘缓存",
            "B. 全球用户通过 TCP/UDP 协议访问对延迟敏感的游戏服务器或 VoIP 应用",
            "C. 仅需要缓存动态 API 响应，并提供边缘函数计算能力",
            "D. 为 S3 存储桶提供全球 CDN 加速，同时支持边缘计算逻辑",
        ],
        "correct_answers": [
            "B",
        ],
        "explanation": "「全球用户通过 TCP/UDP 协议访问对延迟敏感的游戏服务器或 VoIP 应用」是正确的。\n\nGlobal Accelerator 使用 Anycast IP + AWS 全球骨干网，能显著改善非 HTTP/HTTPS 流量（TCP/UDP）的全球延迟，特别适合游戏、VoIP、金融交易等对延迟极度敏感的应用。\n\n其他选项分析：\n\n「全球用户访问静态图片和视频内容，需要极低的首字节延迟和边缘缓存」是错误的：这是 Amazon CloudFront 的核心优势，Global Accelerator 主要针对 TCP/UDP 非 HTTP 流量。\n\n「仅需要缓存动态 API 响应，并提供边缘函数计算能力」是错误的：动态 API 缓存和边缘计算更适合 CloudFront + Lambda@Edge。\n\n「为 S3 存储桶提供全球 CDN 加速，同时支持边缘计算逻辑」是错误的：S3 + CloudFront 是标准组合，Global Accelerator 不直接提供 S3 的 CDN 缓存能力。\n\n**重点考点 / 关键词补充：**\n- Global Accelerator 优势：Anycast + 全球骨干网，适合 TCP/UDP 应用\n- CloudFront 优势：HTTP/HTTPS 内容缓存加速\n- 两者经常结合使用（Global Accelerator 作为入口 + CloudFront 缓存）",
        "domain": "Cloud Concepts",
    },
    {
        "id": "S107",
        "question": "在 AWS 中，Availability（可用性）和 Durability（持久性）的关键区别是什么？",
        "options": [
            "A. Availability 关注数据不丢失，Durability 关注服务可访问",
            "B. Availability 关注服务可访问性，Durability 关注数据不丢失",
            "C. 两者含义完全相同，只是不同服务使用不同术语",
            "D. Availability 只适用于计算服务，Durability 只适用于存储服务",
        ],
        "correct_answers": [
            "B",
        ],
        "explanation": "「Availability 关注服务可访问性，Durability 关注数据不丢失」是正确的。\\n\\nAvailability（可用性）衡量服务在需要时可被使用的程度（通常用百分比表示，如 99.99%）；Durability（持久性）衡量数据在存储期间不丢失的概率（例如 S3 Standard 的持久性为 99.999999999%）。\\n\\n其他选项分析：\\n\\n「Availability 关注数据不丢失，Durability 关注服务可访问」是错误的：两者定义正好相反。\\n\\n「两者含义完全相同」是错误的：这是常见混淆点，考试经常考区分。\\n\\n「Availability 只适用于计算服务」是错误的：两者都适用于存储和计算服务。\\n\\n**重点考点 / 关键词补充：**\\n- Availability：服务可访问性（ uptime 百分比）\\n- Durability：数据持久性（不丢失概率，11 个 9 等）\\n- 常见搭配：S3 Standard 提供极高的 Durability + 高 Availability",
        "domain": "Cloud Concepts",
    },
    {
        "id": "S108",
        "question": "以下关于 Multi-Region 架构的描述，哪一项是正确的？",
        "options": [
            "A. Multi-Region 架构的主要目的是降低成本",
            "B. Multi-Region 架构可以实现更高的可用性、灾难恢复和全球低延迟访问",
            "C. Multi-Region 架构比 Multi-AZ 架构的延迟通常更低",
            "D. Multi-Region 架构只需要在一个 Region 部署资源即可",
        ],
        "correct_answers": [
            "B",
        ],
        "explanation": "「Multi-Region 架构可以实现更高的可用性、灾难恢复和全球低延迟访问」是正确的。\\n\\nMulti-Region 架构通过在多个地理隔离的 Region 部署资源，可以显著提高整体可用性、实现真正的灾难恢复能力，并通过就近部署降低全球用户的访问延迟。\\n\\n其他选项分析：\\n\\n「Multi-Region 架构的主要目的是降低成本」是错误的：多 Region 部署通常会增加成本。\\n\\n「Multi-Region 架构比 Multi-AZ 架构的延迟通常更低」是错误的：跨 Region 延迟通常更高。\\n\\n「Multi-Region 架构只需要在一个 Region 部署资源」是错误的：这与定义矛盾。\\n\\n**重点考点 / 关键词补充：**\\n- Multi-Region 优势：灾难恢复、更高可用性、全球低延迟\\n- 代价：更高成本、更复杂的架构\\n- 常见模式：Active-Active、Active-Passive、Pilot Light、Warm Standby",
        "domain": "Cloud Concepts",
    },
    {
        "id": "S109",
        "question": "AWS Local Zones 相比传统 Region 的主要优势是什么？",
        "options": [
            "A. 提供更低的存储费用",
            "B. 允许在靠近大型人口中心的位置以极低延迟运行完整的 AWS 服务",
            "C. 自动实现跨 Region 的灾难恢复",
            "D. 完全替代 Edge Locations 进行内容分发",
        ],
        "correct_answers": [
            "B",
        ],
        "explanation": "「允许在靠近大型人口中心的位置以极低延迟运行完整的 AWS 服务」是正确的。\\n\\nLocal Zones 是部署在靠近大城市的位置的基础设施，让客户能够以极低的延迟运行完整的 AWS 服务（如 EC2、EBS、RDS、ECS 等），同时仍能利用 AWS 的全球基础设施。\\n\\n其他选项分析：\\n\\n「提供更低的存储费用」是错误的：Local Zones 的费用通常高于标准 Region。\\n\\n「自动实现跨 Region 的灾难恢复」是错误的：Local Zones 仍属于同一 Region，不提供跨 Region 容灾。\\n\\n「完全替代 Edge Locations 进行内容分发」是错误的：Edge Locations 主要用于内容缓存加速，两者定位不同。\\n\\n**重点考点 / 关键词补充：**\\n- Local Zones：靠近人口中心，低延迟运行完整 AWS 服务\\n- 适合场景：游戏、媒体、金融交易、实时应用\\n- 与 Edge Locations 区别：Local Zones 可运行计算/存储服务，Edge Locations 主要用于缓存",
        "domain": "Cloud Concepts",
    },
    {
        "id": "S111",
        "question": "以下关于 AWS Local Zones 和 Edge Locations 的区别，哪一项是正确的？",
        "options": [
            "A. Local Zones 主要用于内容缓存和加速，Edge Locations 可以运行完整的 EC2、RDS 等计算服务",
            "B. Local Zones 允许在靠近人口中心的位置运行完整的 AWS 服务，Edge Locations 主要用于全球内容分发和延迟降低",
            "C. 两者完全相同，只是 AWS 推出的不同产品名称，实际能力没有区别",
            "D. Local Zones 只存在于中国 Region，Edge Locations 则在全球其他地区部署",
        ],
        "correct_answers": [
            "B",
        ],
        "explanation": "「Local Zones 允许在靠近人口中心的位置运行完整的 AWS 服务，Edge Locations 主要用于全球内容分发和延迟降低」是正确的。\n\nLocal Zones 是较新的基础设施形式，部署在靠近大城市的位置，让客户能以极低延迟运行完整的 AWS 服务（如 EC2、EBS、RDS 等）。Edge Locations 是全球内容分发网络节点，主要用于 CloudFront 和 Global Accelerator 的内容缓存和加速。\n\n其他选项分析：\n\n「Local Zones 主要用于内容缓存和加速，Edge Locations 可以运行完整的 EC2、RDS 等计算服务」是错误的：Local Zones 的核心能力是运行完整 AWS 服务（EC2、EBS、RDS 等），而 Edge Locations 主要用于内容缓存和加速，不支持运行通用计算工作负载。\n\n「两者完全相同，只是 AWS 推出的不同产品名称，实际能力没有区别」是错误的：Local Zones 可运行完整 AWS 服务，Edge Locations 主要用于 CDN 缓存和加速，两者在功能定位上差异极大。\n\n「Local Zones 只存在于中国 Region，Edge Locations 则在全球其他地区部署」是错误的：Local Zones 已在全球多个大城市区域部署（包括美国、欧洲、亚洲等），并非仅限于中国 Region。\n\n**重点考点 / 关键词补充：**\n- Local Zones：靠近人口中心，可运行完整 AWS 服务（计算、存储、数据库）\n- Edge Locations：全球内容分发节点，主要用于降低延迟和缓存\n- 两者都属于全球基础设施的补充形式",
        "domain": "Cloud Concepts",
    },
    {
        "id": "S112",
        "question": "在设计多 Region 灾难恢复架构时，以下哪种模式通常恢复时间最快但成本也最高？",
        "options": [
            "A. Backup and Restore",
            "B. Pilot Light",
            "C. Warm Standby",
            "D. Multi-Site Active/Active",
        ],
        "correct_answers": [
            "D",
        ],
        "explanation": "「Multi-Site Active/Active」是正确的。\n\nMulti-Site Active/Active 模式下，多个 Region 同时处理生产流量，故障时可以实现几乎零停机的故障转移，因此恢复时间最快（RTO 接近 0），但需要维护多个完整生产环境的成本也最高。\n\n其他选项分析：\n\n「Backup and Restore」是错误的：这是最便宜但恢复时间最长的模式。\n\n「Pilot Light」是错误的：核心基础设施运行在备用 Region，但应用层需要启动，恢复时间中等。\n\n「Warm Standby」是错误的：备用 Region 运行缩减版的完整系统，恢复时间较快但不如 Active/Active。\n\n**重点考点 / 关键词补充：**\n- Multi-Site Active/Active：RTO/RPO 最低，成本最高\n- Pilot Light：核心服务运行，应用层待命\n- Warm Standby：缩减版完整系统待命\n- Backup and Restore：最便宜，RTO/RPO 最高",
        "domain": "Cloud Concepts",
    },
    {
        "id": "S113",
        "question": "AWS 客户希望在靠近用户的位置以极低延迟运行完整的应用程序（包括计算和数据库），最适合使用以下哪种基础设施？",
        "options": [
            "A. Edge Locations",
            "B. Local Zones",
            "C. Availability Zones",
            "D. AWS Regions",
        ],
        "correct_answers": [
            "B",
        ],
        "explanation": "「Local Zones」是正确的。\n\nLocal Zones 是部署在靠近大型人口中心的位置的基础设施，允许客户以极低的延迟运行完整的 AWS 服务（如 EC2、EBS、RDS、ECS 等），非常适合对延迟敏感的应用。\n\n其他选项分析：\n\n「Edge Locations」是错误的：Edge Locations 主要用于内容缓存和加速，不支持运行完整的计算和数据库服务。\n\n「Availability Zones」是错误的：AZ 是 Region 内的基础设施，延迟相对较高。\n\n「AWS Regions」是错误的：Region 是地理区域，延迟取决于用户位置。\n\n**重点考点 / 关键词补充：**\n- Local Zones：靠近人口中心，低延迟运行完整 AWS 服务\n- 适合场景：游戏、媒体、金融交易、实时应用\n- 与 Edge Locations 区别：Local Zones 可运行完整服务，Edge Locations 主要缓存",
        "domain": "Cloud Concepts",
    },
    {
        "id": "S115",
        "question": "关于 AWS 数据传输费用，以下哪种说法是正确的？",
        "options": [
            "A. 从互联网传入 AWS 的数据通常需要付费",
            "B. 从 AWS 传出到互联网的数据通常需要付费",
            "C. 同一 Region 内不同 AZ 之间的数据传输费用最高",
            "D. 跨 Region 数据传输通常比 Region 内更便宜",
        ],
        "correct_answers": [
            "B",
        ],
        "explanation": "「从 AWS 传出到互联网的数据通常需要付费」是正确的。\n\nAWS 数据传输收费的一般规律是：入方向（互联网 → AWS）大多免费，出方向（AWS → 互联网）通常收费。跨 Region 传输也通常收费，且费用较高。\n\n其他选项分析：\n\n「从互联网传入 AWS 的数据通常需要付费」是错误的：入互联网流量大多免费。\n\n「同一 Region 内不同 AZ 之间的数据传输费用最高」是错误的：同 Region AZ 间传输通常免费或费用极低。\n\n「跨 Region 数据传输通常比 Region 内更便宜」是错误的：跨 Region 传输通常更贵。\n\n**重点考点 / 关键词补充：**\n- 入互联网 → AWS：大多免费\n- AWS → 互联网：收费（出方向）\n- 同 Region AZ 间：通常免费或极低费用\n- 跨 Region：收费，且通常最贵\n- 优化建议：尽量减少跨 Region 流量，善用 CloudFront",
        "domain": "Billing, Pricing, and Support",
    },
    {
        "id": "S116",
        "question": "AWS Cost Anomaly Detection 主要用于什么场景？",
        "options": [
            "A. 手动设置预算阈值并在超支时告警",
            "B. 自动检测账户中的异常成本支出模式并发出告警",
            "C. 分析历史成本趋势并生成可视化报告",
            "D. 帮助客户选择最优的 Reserved Instance 购买策略",
        ],
        "correct_answers": [
            "B",
        ],
        "explanation": "「自动检测账户中的异常成本支出模式并发出告警」是正确的。\n\nAWS Cost Anomaly Detection 使用机器学习自动监控成本模式，当检测到异常支出（如突然的费用激增）时，会自动创建异常并通过 SNS 或 Email 通知用户。它比手动设置预算阈值更智能，适合发现未知的成本异常。\n\n其他选项分析：\n\n「手动设置预算阈值并在超支时告警」是错误的：这是 AWS Budgets 的功能。\n\n「分析历史成本趋势并生成可视化报告」是错误的：这是 AWS Cost Explorer 的主要功能。\n\n「帮助客户选择最优的 Reserved Instance 购买策略」是错误的：这是 AWS Cost Explorer 或 Trusted Advisor 的部分功能。\n\n**重点考点 / 关键词补充：**\n- Cost Anomaly Detection：ML 驱动的自动异常检测\n- 与 Budgets 的区别：Anomaly Detection 是自动发现未知异常，Budgets 是基于预设阈值告警\n- 支持按服务、账户、标签等维度监控",
        "domain": "Billing, Pricing, and Support",
    },
    {
        "id": "S118",
        "question": "以下关于 AWS 不同支持计划的描述，哪一项是正确的？",
        "options": [
            "A. Developer Support 提供 Technical Account Manager (TAM)",
            "B. Business Support 的严重故障响应时间为 < 1 小时",
            "C. Enterprise On-Ramp Support 提供与 Enterprise 完全相同的响应时间",
            "D. 所有支持计划都包含架构审查服务",
        ],
        "correct_answers": [
            "B",
        ],
        "explanation": "「Business Support 的严重故障响应时间为 < 1 小时」是正确的。\n\nBusiness Support 提供 <1 小时的严重故障响应时间，适合大多数生产环境，是性价比最高的生产级支持计划。\n\n其他选项分析：\n\n「Developer Support 提供 Technical Account Manager (TAM)」是错误的：TAM 是 Enterprise Support 专属。\n\n「Enterprise On-Ramp Support 提供与 Enterprise 完全相同的响应时间」是错误的：Enterprise On-Ramp 的响应时间比 Enterprise 慢（严重故障为 < 30 分钟，而非 < 15 分钟）。\n\n「所有支持计划都包含架构审查服务」是错误的：架构审查主要在 Business 及以上计划中提供，Developer 计划不包含。\n\n**重点考点 / 关键词补充：**\n- Developer：适合开发测试，响应时间较慢，无 TAM\n- Business：<1 小时严重故障响应，适合生产环境\n- Enterprise On-Ramp：<30 分钟响应 + 部分架构审查\n- Enterprise：<15 分钟响应 + TAM + 全面架构支持",
        "domain": "Billing, Pricing, and Support",
    },
    {
        "id": "S119",
        "question": "AWS Cost Categories 的主要作用是什么？",
        "options": [
            "A. 自动检测账户中的异常成本支出",
            "B. 将成本按自定义业务维度（如部门、项目、环境）进行归类和分析",
            "C. 设置预算阈值并在超支时发送告警",
            "D. 分析历史成本趋势并生成可视化报告",
        ],
        "correct_answers": [
            "B",
        ],
        "explanation": "「将成本按自定义业务维度（如部门、项目、环境）进行归类和分析」是正确的。\n\nAWS Cost Categories 允许用户定义自定义规则，将成本按业务维度（部门、项目、环境等）进行归类，支持多层级分层，并在 Cost Explorer、Budgets 和 Billing 中使用这些类别进行分析，是高级成本分摊的核心工具。\n\n其他选项分析：\n\n「自动检测账户中的异常成本支出」是错误的：这是 Cost Anomaly Detection 的功能。\n\n「设置预算阈值并在超支时发送告警」是错误的：这是 AWS Budgets 的功能。\n\n「分析历史成本趋势并生成可视化报告」是错误的：这是 AWS Cost Explorer 的主要功能。\n\n**重点考点 / 关键词补充：**\n- Cost Categories：自定义多维度成本归类（支持继承规则）\n- 可在 Cost Explorer、Budgets 中使用\n- 适合复杂组织的多维度成本分摊和分析",
        "domain": "Billing, Pricing, and Support",
    },
    {
        "id": "S120",
        "question": "使用 AWS Direct Connect 相比通过互联网连接 AWS 时，数据传输费用的主要区别是什么？",
        "options": [
            "A. Direct Connect 的出方向数据传输费用通常比互联网更高，因为专线质量更好",
            "B. Direct Connect 可以显著降低跨 Region 或到互联网的数据传输成本",
            "C. Direct Connect 完全免费，不收取任何端口费用或数据传输费用",
            "D. 两者数据传输费用完全相同，只是连接方式不同",
        ],
        "correct_answers": [
            "B",
        ],
        "explanation": "「Direct Connect 可以显著降低跨 Region 或到互联网的数据传输成本」是正确的。\n\nAWS Direct Connect 提供专线连接，通常比通过互联网传输数据更便宜，尤其适合大量跨 Region 或出互联网的流量，是降低数据传输成本的重要方式。\n\n其他选项分析：\n\n「Direct Connect 的出方向数据传输费用通常比互联网更高，因为专线质量更好」是错误的：Direct Connect 的数据传输费用通常比通过互联网更低，尤其在大量流量场景下能显著节省成本。\n\n「Direct Connect 完全免费，不收取任何端口费用或数据传输费用」是错误的：Direct Connect 需要支付端口小时费，但其数据传输费用通常比互联网连接更低。\n\n「两者数据传输费用完全相同，只是连接方式不同」是错误的：Direct Connect 通常能提供比互联网连接更低的数据传输价格，尤其适合高流量跨 Region 或出互联网的场景。\n\n**重点考点 / 关键词补充：**\n- Direct Connect 优势：更低的数据传输成本 + 更稳定低延迟的连接\n- 特别适合大量跨 Region 或出互联网流量\n- 需要考虑端口费用 + 数据传输费用综合成本",
        "domain": "Billing, Pricing, and Support",
    },
    {
        "id": "S121",
        "question": "AWS 客户购买 1 年期 Savings Plans 后，承诺期结束后会发生什么？",
        "options": [
            "A. 自动以相同条款续订 1 年",
            "B. 自动转换为 On-Demand 实例计费，无需额外操作",
            "C. 必须手动选择是否续订，否则资源会被停止",
            "D. 所有资源会自动切换到 Spot 实例",
        ],
        "correct_answers": [
            "B",
        ],
        "explanation": "「自动转换为 On-Demand 实例计费，无需额外操作」是正确的。\n\nSavings Plans 承诺期结束后，资源会自动按照 On-Demand 价格计费，不会中断，也不需要手动操作。客户可以选择是否购买新的 Savings Plans 来继续享受折扣。\n\n其他选项分析：\n\n「自动以相同条款续订 1 年」是错误的：不会自动续订。\n\n「必须手动选择是否续订，否则资源会被停止」是错误的：资源不会被停止，会正常按 On-Demand 计费。\n\n「所有资源会自动切换到 Spot 实例」是错误的：与 Savings Plans 无关。\n\n**重点考点 / 关键词补充：**\n- 承诺期结束后自动按 On-Demand 计费\n- 资源不会中断\n- 客户可随时购买新 Savings Plans 继续享受折扣\n- 建议提前规划续订或新的承诺",
        "domain": "Billing, Pricing, and Support",
    },
    {
        "id": "S122",
        "question": "关于 AWS KMS 中的 Customer Managed Key (CMK) 与 AWS Managed Key，以下哪项说法是正确的？",
        "options": [
            "A. 两者都由 AWS 自动管理密钥轮换，客户无法干预",
            "B. Customer Managed Key 允许客户控制密钥策略、轮换计划和删除操作",
            "C. AWS Managed Key 可以被客户随时禁用或删除",
            "D. CMK 仅用于 S3 服务，AWS Managed Key 用于所有其他服务",
        ],
        "correct_answers": [
            "B",
        ],
        "explanation": "「Customer Managed Key 允许客户控制密钥策略、轮换计划和删除操作」是正确的。\n\nCustomer Managed Key (CMK) 由客户创建和管理，客户可以定义密钥策略、启用/禁用自动轮换（每年一次）、手动轮换、禁用或删除密钥。而 AWS Managed Key 由 AWS 创建和管理，客户对策略和轮换没有控制权。\n\n其他选项分析：\n\n「两者都由 AWS 自动管理密钥轮换」是错误的：只有 CMK 支持客户控制轮换。\n\n「AWS Managed Key 可以被客户随时禁用或删除」是错误的：AWS Managed Key 客户无法删除或永久禁用。\n\n「CMK 仅用于 S3 服务」是错误的：CMK 可用于多种 AWS 服务（S3、EBS、RDS、Lambda 等）。\n\n**重点考点 / 关键词补充：**\n- CMK（客户托管密钥）：客户完全控制策略、轮换、删除\n- AWS Managed Key：AWS 托管，客户无控制权\n- 自动轮换：CMK 支持每年自动轮换，AWS Managed Key 由 AWS 决定\n- Envelope Encryption：KMS 始终使用 envelope 加密模式",
        "domain": "Security and Compliance",
    },
    {
        "id": "S123",
        "question": "在 S3 Object Lock 中，Compliance 模式和 Governance 模式的主要区别是什么？",
        "options": [
            "A. Compliance 模式下 Root 用户可以修改保留期，Governance 模式则完全不可修改",
            "B. Compliance 模式下任何用户（包括 Root）在保留期内都无法删除或覆盖对象，Governance 模式允许特定权限的用户修改保留期或提前删除",
            "C. 两者在保留期设置和权限控制上完全相同，只是命名不同",
            "D. Governance 模式主要用于内部审计和日志保留，Compliance 模式则用于生产数据备份保护",
        ],
        "correct_answers": [
            "B",
        ],
        "explanation": "「Compliance 模式下任何用户（包括 Root）在保留期内都无法删除或覆盖对象，Governance 模式允许特定权限的用户修改保留期或提前删除」是正确的。\n\n这是 S3 Object Lock 两种保留模式的经典区别：Compliance 模式极其严格（满足 SEC、FINRA 等最严监管），连 Root 用户也无法在保留期内删除或缩短保留期；Governance 模式相对灵活，拥有 s3:BypassGovernanceRetention 权限的用户可以修改保留设置或提前删除。\n\n其他选项分析：\n\n「Compliance 模式下 Root 用户可以修改保留期」是错误的：Compliance 模式下 Root 用户也完全无法修改或缩短保留期，这是其最严格的特点。\n\n「两者在保留期设置和权限控制上完全相同，只是命名不同」是错误的：两者在是否允许特定权限用户绕过保留上有本质区别，权限模型完全不同。\n\n「Governance 模式主要用于内部审计和日志保留，Compliance 模式则用于生产数据备份保护」是错误的：Governance 模式更适合需要一定灵活性的内部治理场景，而非仅审计；Compliance 才是最严的生产数据保护模式。\n\n**重点考点 / 关键词补充：**\n- Object Lock 两种模式：Compliance（最严格） vs Governance（可绕过）\n- Compliance：任何人（含 Root）都无法删除/缩短保留期\n- Governance：拥有 s3:BypassGovernanceRetention 权限的用户可修改\n- 常考：Compliance 用于金融、医疗等强监管场景",
        "domain": "Security and Compliance",
    },
    {
        "id": "S124",
        "question": "启用 S3 Block Public Access 后，以下哪种情况仍然可能发生？",
        "options": [
            "A. 存储桶策略允许公共读取某个对象",
            "B. ACL 设置为 public-read 的对象可被匿名访问",
            "C. 存储桶本身对互联网完全不可访问",
            "D. 通过预签名 URL（Presigned URL）临时访问私有对象",
        ],
        "correct_answers": [
            "D",
        ],
        "explanation": "「通过预签名 URL（Presigned URL）临时访问私有对象」是正确的。\n\nS3 Block Public Access 主要阻止通过存储桶策略、ACL 或公开 URL 的公共访问，但不影响合法的预签名 URL（使用签名凭证的临时访问）。预签名 URL 是私有对象授权访问的标准方式，不属于“公共访问”。\n\n其他选项分析：\n\n「存储桶策略允许公共读取」是错误的：Block Public Access 会阻止此类公共访问，即使策略允许。\n\n「ACL 设置为 public-read」是错误的：Block Public Access 会忽略或阻止公共 ACL。\n\n「存储桶本身对互联网完全不可访问」是错误的：Block Public Access 仅阻止公共访问，私有访问和授权访问仍然正常。\n\n**重点考点 / 关键词补充：**\n- Block Public Access：阻止公共访问（存储桶策略 + ACL + 公开 URL）\n- 不影响：预签名 URL、私有访问、授权访问\n- 推荐：对所有存储桶默认开启，尤其是生产环境\n- 四个设置：BlockPublicAcls、IgnorePublicAcls、BlockPublicPolicy、RestrictPublicBuckets",
        "domain": "Security and Compliance",
    },
    {
        "id": "S125",
        "question": "CloudWatch、CloudTrail 和 AWS Config 在监控与审计方面的主要职责区别是什么？",
        "options": [
            "A. 三者功能完全相同，只是名称不同，可以完全互换使用",
            "B. CloudWatch 负责性能指标和告警，CloudTrail 负责记录 API 调用审计日志，Config 负责记录资源配置变更和合规评估",
            "C. CloudTrail 主要负责监控 EC2 实例的 CPU、内存和网络性能指标",
            "D. CloudWatch 仅用于收集和存储日志文件，Config 则专门用于分析账单和成本趋势",
        ],
        "correct_answers": [
            "B",
        ],
        "explanation": "「CloudWatch 负责性能指标和告警，CloudTrail 负责记录 API 调用审计日志，Config 负责记录资源配置变更和合规评估」是正确的。\n\n这是 CLF-C02 最经典的三者对比：\n- CloudWatch：Metrics（性能数据）、Alarms（告警）、Logs（日志收集分析）\n- CloudTrail：记录所有 AWS API 调用（谁、在何时、对什么资源做了什么操作），用于审计和安全分析\n- AWS Config：持续记录资源配置变更历史，并可进行合规规则评估（如“所有 S3 桶是否开启加密”）\n\n其他选项分析：\n\n「三者功能完全相同，只是名称不同，可以完全互换使用」是错误的：三者在职责上差异显著，CloudWatch 关注“资源运行得怎么样”，CloudTrail 关注“谁做了什么操作”，Config 关注“资源配置变成了什么样子”。\n\n「CloudTrail 主要负责监控 EC2 实例的 CPU、内存和网络性能指标」是错误的：这是 CloudWatch Metrics + Alarms 的核心功能，CloudTrail 只记录 API 调用审计日志。\n\n「CloudWatch 仅用于收集和存储日志文件，Config 则专门用于分析账单和成本趋势」是错误的：CloudWatch 不仅收集日志，还负责性能指标和告警；成本分析主要是 Cost Explorer 的职责，Config 关注的是资源配置变更历史和合规性。\n\n**重点考点 / 关键词补充：**\n- CloudWatch：性能指标 + 告警 + 应用/系统日志\n- CloudTrail：API 调用审计日志（Who, What, When）\n- Config：资源配置变更历史 + 合规规则评估\n- 常考组合：CloudTrail + Config 一起用于安全合规审计",
        "domain": "Technology and Services",
    },
    {
        "id": "S126",
        "question": "以下哪些 AWS 服务属于 Global（全球）级别服务？（注意本题为单选，选出最准确的组合）",
        "options": [
            "A. Amazon S3 存储桶和 Amazon EC2 实例",
            "B. AWS IAM、Amazon CloudFront 和 Amazon Route 53",
            "C. Amazon RDS 数据库和 Amazon DynamoDB 表",
            "D. AWS Lambda 函数和 Amazon EBS 卷",
        ],
        "correct_answers": [
            "B",
        ],
        "explanation": "「AWS IAM、Amazon CloudFront 和 Amazon Route 53」是正确的。\n\nIAM（身份与访问管理）、CloudFront（CDN）和 Route 53（DNS 服务）是典型的 Global 级别服务：其配置和资源不绑定到特定 Region，在 AWS 全球范围内生效或可用。绝大多数其他服务（S3 桶、EC2、RDS、Lambda、DynamoDB 等）都是 Region 级别的资源。\n\n其他选项分析：\n\n「Amazon S3 存储桶和 Amazon EC2 实例」是错误的：两者都是 Region 级资源（S3 桶名虽全局唯一，但实际存储位置在特定 Region）。\n\n「Amazon RDS 数据库和 Amazon DynamoDB 表」是错误的：都是 Region 级服务。\n\n「AWS Lambda 函数和 Amazon EBS 卷」是错误的：都是 Region 级资源。\n\n**重点考点 / 关键词补充：**\n- Global 服务典型代表：IAM、CloudFront、Route 53、AWS Organizations、AWS Artifact、AWS Shield (部分)\n- Region 级服务：EC2、S3、RDS、Lambda、DynamoDB、EBS、VPC 等绝大多数\n- 考试常考陷阱：IAM 是 Global 的，但 EC2 实例、S3 桶（数据）是 Region 的\n- S3 桶名全局唯一，但数据和配置位于特定 Region",
        "domain": "Cloud Concepts",
    },
    {
        "id": "S127",
        "question": "当 Spot Instance 被 AWS 中断时，AWS 通常会提前多久发出中断通知？中断后 EBS 根卷的数据默认会如何处理？",
        "options": [
            "A. 提前 5 分钟通知，EBS 根卷数据会立即丢失",
            "B. 提前 2 分钟通知，EBS 根卷数据默认会保留（除非显式设置删除策略）",
            "C. 没有提前通知，实例直接被终止且所有数据丢失",
            "D. 提前 30 分钟通知，EBS 数据会自动备份到 S3",
        ],
        "correct_answers": [
            "B",
        ],
        "explanation": "「提前 2 分钟通知，EBS 根卷数据默认会保留（除非显式设置删除策略）」是正确的。\n\nAWS Spot Instance 中断时通常会提前 2 分钟通过 EC2 实例元数据服务和 EventBridge 发出中断通知。EBS 根卷（以及附加 EBS 卷）数据默认会在实例终止后保留（与 On-Demand 实例行为一致），除非在启动时明确设置了 DeleteOnTermination=true。\n\n其他选项分析：\n\n「提前 5 分钟通知」是错误的：标准通知时间是 2 分钟。\n\n「没有提前通知」是错误的：AWS 会主动提供中断通知以便应用做优雅退出或 Checkpoint。\n\n「EBS 数据会自动备份到 S3」是错误的：不会自动备份，需要客户自己设计备份策略。\n\n**重点考点 / 关键词补充：**\n- Spot 中断通知：提前 2 分钟（instance metadata + EventBridge）\n- EBS 根卷：默认保留（DeleteOnTermination 默认为 false）\n- 实例存储（ephemeral）：中断时数据会永久丢失\n- 最佳实践：使用 Checkpointing、SQS 队列、Auto Scaling 组 + 生命周期钩子处理中断",
        "domain": "Technology and Services",
    },
    {
        "id": "S128",
        "question": "Local Zones、Wavelength Zones 和 Edge Locations 三者的主要区别是什么？",
        "options": [
            "A. 三者都是 AWS 全球内容分发网络 (CDN) 的不同实现，核心功能完全一致，主要用于缓存静态和动态内容",
            "B. Local Zones 靠近人口中心可运行完整 AWS 服务，Wavelength Zones 是 5G 边缘用于超低延迟移动应用，Edge Locations 主要用于 CloudFront/Global Accelerator 内容分发",
            "C. Wavelength Zones 支持运行完整 EC2、RDS 和 EKS，Local Zones 仅用于 5G 网络加速和边缘计算",
            "D. Edge Locations 支持客户部署容器化应用和 Lambda@Edge 计算逻辑，同时提供全球低延迟内容接入和加速",
        ],
        "correct_answers": [
            "B",
        ],
        "explanation": "「Local Zones 靠近人口中心可运行完整 AWS 服务，Wavelength Zones 是 5G 边缘用于超低延迟移动应用，Edge Locations 主要用于 CloudFront/Global Accelerator 内容分发」是正确的。\n\n这是 CLF-C02 重要的三者对比：\n- Local Zones：部署在靠近大型城市的位置，可运行完整的 AWS 服务（EC2、EBS、RDS 等），解决固定用户低延迟问题。\n- Wavelength Zones：与电信运营商合作部署在 5G 网络边缘，适合 AR/VR、自动驾驶、工业 IoT 等超低延迟（<10ms）移动场景。\n- Edge Locations：全球数量最多的内容分发节点，主要服务 CloudFront 和 Global Accelerator，用于缓存和加速，不运行通用计算服务。\n\n其他选项分析：\n\n「三者都是 AWS 全球内容分发网络 (CDN) 的不同实现，核心功能完全一致，主要用于缓存静态和动态内容」是错误的：只有 Edge Locations 主要用于内容分发和加速，Local Zones 和 Wavelength Zones 可以运行完整的计算和数据库服务。\n\n「Wavelength Zones 支持运行完整 EC2、RDS 和 EKS，Local Zones 仅用于 5G 网络加速和边缘计算」是错误的：实际情况完全相反，Local Zones 支持运行较为完整的 AWS 服务，而 Wavelength Zones 受限于 5G 边缘特定场景。\n\n「Edge Locations 支持客户部署容器化应用和 Lambda@Edge 计算逻辑，同时提供全球低延迟内容接入和加速」是错误的：Edge Locations 不支持运行客户自有的通用计算或容器工作负载，Lambda@Edge 功能非常有限。\n\n**重点考点 / 关键词补充：**\n- Local Zones：靠近人口中心，低延迟运行完整服务\n- Wavelength Zones：5G 边缘，超低延迟移动/实时应用\n- Edge Locations：全球 CDN 节点（CloudFront + Global Accelerator）\n- 核心基础设施仍是 Region + AZ，这三者是补充形式",
        "domain": "Cloud Concepts",
    },
    {
        "id": "S129",
        "question": "在设计高可用和灾难恢复架构时，Multi-AZ 和 Multi-Region 的主要适用场景区别是什么？",
        "options": [
            "A. Multi-AZ 主要用于防范整个 Region 级故障，而 Multi-Region 主要用于消除单点故障",
            "B. Multi-AZ 主要用于同一 Region 内的故障隔离和高可用（RTO 较低），Multi-Region 用于满足合规、全球低延迟或真正的灾难恢复（RTO 较高）",
            "C. 两者在技术实现、RTO/RPO 和成本效果上完全一致，只是物理部署位置不同",
            "D. Multi-Region 部署的成本通常更低，因为可以共享更多基础设施和数据",
        ],
        "correct_answers": [
            "B",
        ],
        "explanation": "「Multi-AZ 主要用于同一 Region 内的故障隔离和高可用（RTO 较低），Multi-Region 用于满足合规、全球低延迟或真正的灾难恢复（RTO 较高）」是正确的。\n\nMulti-AZ：在同一个 Region 内跨多个物理隔离的 AZ 部署，网络延迟低，适合大多数生产环境的高可用和消除单点故障，RTO 通常很低（秒到分钟级）。\nMulti-Region：跨地理隔离的 Region 部署，用于满足数据主权、全球用户低延迟、或防范整个 Region 级灾难，RTO/RPO 通常更高，成本和复杂度也更高。\n\n其他选项分析：\n\n「Multi-AZ 主要用于防范整个 Region 级故障，而 Multi-Region 主要用于消除单点故障」是错误的：描述完全反了，Multi-AZ 无法防范 Region 级故障，Multi-Region 才能做到这一点。\n\n「两者在技术实现、RTO/RPO 和成本效果上完全一致，只是物理部署位置不同」是错误的：Multi-AZ 的网络延迟极低、RTO 通常很低，而 Multi-Region 延迟更高、RTO/RPO 通常更高，成本和复杂度也显著增加。\n\n「Multi-Region 部署的成本通常更低，因为可以共享更多基础设施和数据」是错误的：Multi-Region 通常成本更高（跨 Region 数据传输费用、重复部署的基础设施等）。\n\n**重点考点 / 关键词补充：**\n- Multi-AZ：同一 Region 内，RTO 低，适合大多数 HA 场景\n- Multi-Region：跨 Region，适合合规、全球分发、Region 级 DR\n- 常见组合：先做好 Multi-AZ，再根据需要加 Multi-Region\n- RTO/RPO 要求决定选择哪种架构",
        "domain": "Cloud Concepts",
    },
    {
        "id": "S130",
        "question": "AWS IAM Permission Boundary 和 AWS Organizations 的 Service Control Policies (SCP) 主要区别是什么？",
        "options": [
            "A. Permission Boundary 只能限制 Root 用户，SCP 只能限制普通 IAM 用户和角色",
            "B. Permission Boundary 是在单个 AWS 账户内为特定 IAM 用户或角色设置的权限上限；SCP 是在组织层面为整个成员账户设置的权限边界",
            "C. 两者功能完全相同，只是 AWS 推出的不同产品名称和适用范围描述不同",
            "D. SCP 可以为 IAM 实体额外授予某些高级权限，而 Permission Boundary 只能起到限制作用",
        ],
        "correct_answers": [
            "B",
        ],
        "explanation": "「Permission Boundary 是在单个 AWS 账户内为特定 IAM 用户或角色设置的权限上限；SCP 是在组织层面为整个成员账户设置的权限边界」是正确的。\n\nPermission Boundary：账户内机制，作用于具体的 IAM User 或 Role，作为该实体的“权限天花板”（与策略取交集生效）。\nSCP：Organizations 组织级机制，作用于整个成员账户或 OU，即使账户内的 IAM 策略允许，SCP 也会强制 Deny。\n\n其他选项分析：\n\n「Permission Boundary 只能限制 Root 用户，SCP 只能限制普通 IAM 用户和角色」是错误的：Root 用户不受任何 IAM 策略和 Permission Boundary 的限制；SCP 也无法限制管理账户（Management Account）中的 Root 用户。\n\n「两者功能完全相同，只是 AWS 推出的不同产品名称和适用范围描述不同」是错误的：Permission Boundary 是账户内针对具体 IAM 实体的上限机制，而 SCP 是组织级针对整个账户/OU 的边界机制，两者生效层级和范围完全不同。\n\n「SCP 可以为 IAM 实体额外授予某些高级权限，而 Permission Boundary 只能起到限制作用」是错误的：两者都只能限制权限（取交集或强制 Deny），均无法为 IAM 实体授予任何额外权限。\n\n**重点考点 / 关键词补充：**\n- Permission Boundary：账户内，针对具体 IAM 实体（User/Role）的上限\n- SCP：组织级，针对整个账户/OU 的边界\n- 共同点：两者都只能限制权限，不能授予权限\n- 常考：SCP 影响账户内所有 IAM 实体，Permission Boundary 只影响特定实体",
        "domain": "Security and Compliance",
    },
    {
        "id": "S131",
        "question": "AWS CloudFormation 的主要作用是什么？它与手动在控制台创建资源相比有什么核心优势？",
        "options": [
            "A. CloudFormation 主要用于监控资源性能和设置告警",
            "B. CloudFormation 允许使用代码（模板）以可重复、可版本控制的方式自动创建和管理 AWS 资源基础设施",
            "C. CloudFormation 只能用于创建 EC2 实例，不能管理其他服务",
            "D. CloudFormation 主要用于实时成本优化和预算告警",
        ],
        "correct_answers": [
            "B",
        ],
        "explanation": "「CloudFormation 允许使用代码（模板）以可重复、可版本控制的方式自动创建和管理 AWS 资源基础设施」是正确的。\n\nAWS CloudFormation 是基础设施即代码 (IaC) 服务。通过 JSON 或 YAML 模板，你可以定义整个 AWS 架构（VPC、EC2、S3、IAM、RDS 等），然后一键部署。核心优势包括：可重复部署、一致性、版本控制、回滚能力、依赖关系自动处理。\n\n其他选项分析：\n\n「主要用于监控资源性能」是错误的：这是 CloudWatch 的职责。\n\n「只能用于创建 EC2 实例」是错误的：CloudFormation 支持几乎所有 AWS 资源。\n\n「主要用于实时成本优化」是错误的：成本优化主要靠 Cost Explorer、Budgets 和 Trusted Advisor。\n\n**重点考点 / 关键词补充：**\n- CloudFormation = 基础设施即代码 (Infrastructure as Code)\n- 模板格式：JSON / YAML\n- 核心优势：可重复、一致性、版本控制、自动回滚、依赖管理\n- 常考：CloudFormation Stack = 一组相关资源的集合；Change Set 可预览变更",
        "domain": "Technology and Services",
    },
    {
        "id": "S132",
        "question": "AWS Systems Manager (SSM) 的 Parameter Store 主要用于什么场景？它与 AWS Secrets Manager 的典型区别是什么？",
        "options": [
            "A. Parameter Store 主要用于存储高度敏感的数据库密码和 API Key，Secrets Manager 只能存普通配置参数",
            "B. Parameter Store 适合存储配置数据、数据库连接字符串和非敏感参数；Secrets Manager 专为加密存储和管理敏感凭证（自动轮换）设计",
            "C. 两者功能完全相同，只是 AWS 推出的不同产品名称，实际能力没有区别",
            "D. Parameter Store 只能存储简单的字符串值，Secrets Manager 只能存储二进制格式的密钥",
        ],
        "correct_answers": [
            "B",
        ],
        "explanation": "「Parameter Store 适合存储配置数据...；Secrets Manager 专为加密存储和管理敏感凭证（自动轮换）设计」是正确的。\n\nSSM Parameter Store：适合存放应用配置、数据库连接字符串、许可证密钥等（支持明文和加密两种类型）。\nSecrets Manager：专门用于管理敏感凭证（密码、API Key、证书），提供自动轮换、细粒度访问控制和与 KMS 的深度集成。\n\n其他选项分析：\n\n「Parameter Store 主要用于存储高度敏感的数据库密码和 API Key，Secrets Manager 只能存普通配置参数」是错误的：Parameter Store 可以存储配置参数，而 Secrets Manager 是专门为高度敏感凭证设计的工具（支持自动轮换等高级功能）。\n\n「两者功能完全相同，只是 AWS 推出的不同产品名称，实际能力没有区别」是错误的：Parameter Store 更轻量适合配置数据，Secrets Manager 提供更强的加密、轮换和集成能力，两者定位明显不同。\n\n**重点考点 / 关键词补充：**\n- SSM Parameter Store：配置 + 非极敏感参数（支持分层、版本）\n- Secrets Manager：敏感凭证 + 自动轮换（与 RDS 等集成）\n- 考试常考：Parameter Store 更便宜、更轻量；Secrets Manager 功能更强但成本更高",
        "domain": "Security and Compliance",
    },
    {
        "id": "S133",
        "question": "Amazon S3 Access Points 的主要作用是什么？它相比传统存储桶策略有什么优势？",
        "options": [
            "A. Access Points 主要用于加速 S3 数据传输",
            "B. Access Points 允许为不同应用或团队创建独立的访问点，每个访问点可以有自己的权限策略，从而简化大型存储桶的权限管理",
            "C. Access Points 只能用于静态网站托管",
            "D. Access Points 可以让 S3 存储桶变成多 Region 全局存储",
        ],
        "correct_answers": [
            "B",
        ],
        "explanation": "「Access Points 允许为不同应用或团队创建独立的访问点，每个访问点可以有自己的权限策略，从而简化大型存储桶的权限管理」是正确的。\n\nS3 Access Points 为共享存储桶提供了更细粒度、更易管理的访问入口。每个 Access Point 可以有独立的策略、VPC 限制、访问点名称，便于为不同应用、团队或客户设置隔离的访问权限，而不需要在巨大的存储桶策略中维护大量复杂的规则。\n\n其他选项分析：\n\n「主要用于加速 S3 数据传输」是错误的：加速用 Transfer Acceleration 或 CloudFront。\n\n「只能用于静态网站托管」是错误的：Access Points 是通用访问控制机制。\n\n**重点考点 / 关键词补充：**\n- S3 Access Points：为共享桶提供独立访问入口 + 独立策略\n- 优势：权限管理简化、VPC 限制、名称自定义\n- 适合：大型共享桶、多团队/多应用场景",
        "domain": "Technology and Services",
    },
    {
        "id": "S134",
        "question": "AWS Certificate Manager (ACM) 的主要功能是什么？它与手动管理 SSL/TLS 证书相比有什么优势？",
        "options": [
            "A. ACM 主要用于监控和管理 EC2 实例的 CPU、内存使用率，并可自动生成性能报告",
            "B. ACM 提供免费的 SSL/TLS 证书，并自动处理证书的申请、部署、续期和吊销，特别适合与 CloudFront、ALB、API Gateway 集成",
            "C. ACM 只能签发自签名证书，因此不适合面向公众的生产环境使用，需要额外购买商业证书",
            "D. ACM 主要用于对 S3 中的对象进行服务端加密，并支持与 KMS 深度集成管理密钥",
        ],
        "correct_answers": [
            "B",
        ],
        "explanation": "「ACM 提供免费的 SSL/TLS 证书，并自动处理证书的申请、部署、续期和吊销」是正确的。\n\nAWS Certificate Manager 让你可以轻松申请和部署受信任的公共 SSL/TLS 证书（由 Amazon 信任的 CA 签发），并与 CloudFront、Application Load Balancer、API Gateway、Elastic Beanstalk 等服务深度集成。最大优势是自动续期（无需人工干预，避免证书过期导致的服务中断）。\n\n其他选项分析：\n\n「ACM 主要用于监控和管理 EC2 实例的 CPU、内存使用率，并可自动生成性能报告」是错误的：这是 Amazon CloudWatch 的核心功能，ACM 完全不涉及实例性能监控。\n\n「ACM 只能签发自签名证书，因此不适合面向公众的生产环境使用，需要额外购买商业证书」是错误的：ACM 可以直接签发由 Amazon 信任的公共 CA 签发的受信任证书，广泛用于面向公众的生产环境，无需额外购买。\n\n「ACM 主要用于对 S3 中的对象进行服务端加密，并支持与 KMS 深度集成管理密钥」是错误的：S3 对象加密主要使用 SSE-S3、SSE-KMS 或客户端加密，ACM 的主要用途是 SSL/TLS 终端证书管理。\n\n**重点考点 / 关键词补充：**\n- ACM：免费公共证书 + 自动续期\n- 主要集成：CloudFront、ALB、NLB、API Gateway\n- 优势：自动续期、集中管理、与 AWS 服务原生集成\n- 注意：证书必须在与使用服务的同一 Region（CloudFront 除外）",
        "domain": "Security and Compliance",
    },
    {
        "id": "S135",
        "question": "Amazon EC2 Placement Groups 中的 Cluster、Spread 和 Partition 三种类型的核心区别和适用场景是什么？",
        "options": [
            "A. 三种 Placement Group 的功能和适用场景完全相同，只是 AWS 提供的不同命名方式",
            "B. Cluster 适合需要极低延迟和高网络吞吐的紧密耦合应用；Spread 适合需要最大硬件隔离的少量关键实例；Partition 适合需要将实例分成多个隔离组的大型分布式工作负载",
            "C. Spread Placement Group 主要目的是为了降低 EC2 实例的整体运行成本和费用",
            "D. Partition Placement Group 只能在内存优化型或存储优化型实例上创建和使用",
        ],
        "correct_answers": [
            "B",
        ],
        "explanation": "「Cluster 适合需要极低延迟和高网络吞吐...；Spread 适合需要最大硬件隔离...；Partition 适合...大型分布式工作负载」是正确的。\n\n- Cluster：实例放在同一机架/低延迟网络，适合 HPC、紧密耦合应用（高网络性能）。\n- Spread：每个实例放在不同的物理硬件（不同机架、不同电源等），适合少量关键实例需要最高隔离（如主数据库、关键应用）。\n- Partition：将实例分成多个“分区”，每个分区有独立的硬件，适合 Hadoop、Cassandra、Kafka 等大型分布式系统（既隔离又保持组内通信）。\n\n其他选项分析：\n\n「三种 Placement Group 的功能和适用场景完全相同，只是 AWS 提供的不同命名方式」是错误的：三者在网络拓扑、硬件隔离级别和推荐工作负载上差异显著，设计目标完全不同。\n\n「Spread Placement Group 主要目的是为了降低 EC2 实例的整体运行成本和费用」是错误的：Spread 主要是为了实现最大程度的硬件故障隔离（不同机架、电源、冷却等），通常成本更高而非更低。\n\n**重点考点 / 关键词补充：**\n- Cluster：低延迟 + 高吞吐（HPC）\n- Spread：最大硬件隔离（关键少量实例）\n- Partition：大规模分布式工作负载的组级隔离\n- 考试常考：根据应用类型选择正确的 Placement Group 类型",
        "domain": "Technology and Services",
    },
    {
        "id": "S136",
        "question": "在 KMS Envelope Encryption（信封加密）模型中，数据密钥（Data Key）是如何被保护的？",
        "options": [
            "A. 数据密钥会直接使用客户主密钥 (CMK) 进行加密，然后和加密后的数据一起明文存储",
            "B. 数据密钥用 CMK 加密后得到加密的数据密钥（Encrypted Data Key），只有拿到 CMK 才能解密出明文数据密钥用于加解密数据",
            "C. 数据密钥在生成后永远保持明文状态，不进行任何加密保护",
            "D. 数据密钥的生命周期完全由 S3 服务自动管理，KMS 只负责最终的存储加密",
        ],
        "correct_answers": [
            "B",
        ],
        "explanation": "「数据密钥用 CMK 加密后得到加密的数据密钥...只有拿到 CMK 才能解密出明文数据密钥用于加解密数据」是正确的。\n\nEnvelope Encryption（信封加密）是 KMS 的核心加密模式：先用随机生成的数据密钥加密实际数据，然后用 CMK 加密这个数据密钥（得到 Encrypted Data Key）。这样可以高效加密大量数据，同时利用 KMS 的安全性和密钥管理能力。只有拥有 CMK 解密权限的人才能拿到明文数据密钥。\n\n其他选项分析：\n\n「数据密钥会直接使用客户主密钥 (CMK) 进行加密，然后和加密后的数据一起明文存储」是错误的：这描述了 Envelope Encryption 的部分流程，但遗漏了“先用数据密钥加密实际数据”这个关键步骤，且存储方式描述不准确。\n\n「数据密钥在生成后永远保持明文状态，不进行任何加密保护」是错误的：这是非常不安全的做法，KMS Envelope Encryption 的核心正是用 CMK 保护数据密钥。\n\n「数据密钥的生命周期完全由 S3 服务自动管理，KMS 只负责最终的存储加密」是错误的：虽然 S3 可以集成 KMS，但 Envelope Encryption 模型中，数据密钥的生成、加密和使用是由应用或服务明确控制的，KMS 负责保护数据密钥本身。\n\n**重点考点 / 关键词补充：**\n- Envelope Encryption：用数据密钥加密数据 + 用 CMK 加密数据密钥\n- 优势：性能好 + 密钥管理安全\n- 几乎所有使用 KMS 的 AWS 服务（S3、EBS、RDS 等）都采用此模型",
        "domain": "Security and Compliance",
    },
    {
        "id": "S137",
        "question": "AWS Control Tower 的主要作用是什么？它为多账户环境提供了哪些核心治理能力？",
        "options": [
            "A. Control Tower 主要用于监控单个 EC2 实例的 CPU、内存和网络性能指标，并自动生成详细的 CloudWatch 仪表板",
            "B. Control Tower 提供一键式 Landing Zone 设置、Guardrails（防护机制）和 Account Factory，帮助企业快速建立安全、合规的多账户治理架构",
            "C. Control Tower 只能管理单个 AWS 账户的资源，无法跨多个账户进行统一治理和合规检查",
            "D. Control Tower 主要功能是自动分析成本并推荐 Reserved Instances 和 Savings Plans 的购买策略",
        ],
        "correct_answers": [
            "B",
        ],
        "explanation": "「Control Tower 提供一键式 Landing Zone 设置、Guardrails 和 Account Factory...」是正确的。\n\nAWS Control Tower 是用于多账户环境的治理服务。它可以一键部署符合最佳实践的 Landing Zone（着陆区），自动应用 Guardrails（预防性和检测性防护机制），并通过 Account Factory 快速创建和配置新账户，确保所有账户从一开始就遵循企业安全和合规标准。\n\n其他选项分析：\n\n「主要用于监控单个 EC2 实例的 CPU、内存和网络性能指标，并自动生成详细的 CloudWatch 仪表板」是错误的：Control Tower 不提供任何实例级性能监控或 CloudWatch 仪表板功能，这些属于 CloudWatch 和 CloudWatch Dashboards 的职责。\n\n「只能管理单个 AWS 账户的资源，无法跨多个账户进行统一治理和合规检查」是错误的：Control Tower 的核心价值正是跨多个账户（多账户环境）提供统一的 Landing Zone、Guardrails 和 Account Factory 治理能力。\n\n「主要功能是自动分析成本并推荐 Reserved Instances 和 Savings Plans 的购买策略」是错误的：Control Tower 专注于治理和合规结构，不负责成本分析或购买推荐（这些由 Cost Explorer、Compute Optimizer 等服务负责）。\n\n**重点考点 / 关键词补充：**\n- Control Tower = 多账户治理的“着陆区”服务\n- 核心组件：Landing Zone + Guardrails + Account Factory\n- Guardrails：预防性（阻止违规操作）和检测性（发现违规）\n- 非常适合大型企业或需要强治理的多账户场景",
        "domain": "Security and Compliance",
    },
    {
        "id": "S138",
        "question": "AWS Control Tower 与 AWS Organizations 的关系是什么？Control Tower 提供了 Organizations 本身没有的哪些额外治理能力？",
        "options": [
            "A. Control Tower 完全替代了 Organizations，客户可以直接使用 Control Tower 而无需创建 Organizations 结构",
            "B. Control Tower 构建在 Organizations 之上，自动配置 Organizations 结构，并额外提供预设的 Guardrails、蓝图和 Account Factory，使多账户治理更加自动化和标准化",
            "C. Organizations 提供多账户结构管理，Control Tower 则专注于安全组、NACL 和 VPC 配置的集中管控",
            "D. 两者提供完全相同的多账户治理能力，只是 AWS 推出的两个不同产品名称和品牌",
        ],
        "correct_answers": [
            "B",
        ],
        "explanation": "「Control Tower 构建在 Organizations 之上，自动配置 Organizations 结构，并额外提供预设的 Guardrails、蓝图和 Account Factory...」是正确的。\n\nControl Tower 建立在 AWS Organizations 基础之上。它会自动为你创建并配置 Organizations（包括管理账户、日志归档账户和审计账户），并在此基础上叠加更高级的治理功能：预构建的 Guardrails（基于 SCP 和 Config 规则）、账户蓝图（Blueprint）和 Account Factory（自动化账户创建流程）。\n\n其他选项分析：\n\n「Control Tower 完全替代了 Organizations，客户可以直接使用 Control Tower 而无需创建 Organizations 结构」是错误的：Control Tower 必须构建在 AWS Organizations 之上，它会自动帮你创建和配置 Organizations 结构，而非替代它。\n\n「Organizations 提供多账户结构管理，Control Tower 则专注于安全组、NACL 和 VPC 配置的集中管控」是错误的：Control Tower 的核心价值是提供预构建的 Guardrails、Account Factory 和蓝图，而非仅做网络配置的集中管控。\n\n「两者提供完全相同的多账户治理能力，只是 AWS 推出的两个不同产品名称和品牌」是错误的：Organizations 提供基础的多账户结构与 SCP，而 Control Tower 在其上叠加了更高级、更自动化的治理框架，两者功能定位明显不同。\n\n**重点考点 / 关键词补充：**\n- Control Tower 构建于 Organizations 之上\n- 额外价值：预设 Guardrails + Account Factory + 蓝图\n- 常考：Control Tower 让多账户治理“开箱即用”，大幅降低手动配置 Organizations + SCP + Config 的工作量",
        "domain": "Security and Compliance",
    },
    {
        "id": "S139",
        "question": "AWS Service Catalog 的主要作用是什么？它如何帮助企业实现自助服务与治理的平衡？",
        "options": [
            "A. Service Catalog 主要用于监控应用程序性能和自动扩缩容",
            "B. Service Catalog 允许管理员创建经过批准的产品组合（Portfolios），终端用户可以在受控权限下自助式部署标准化资源，同时强制执行治理约束",
            "C. Service Catalog 只能用于部署 EC2 实例和简单的 S3 存储桶",
            "D. Service Catalog 主要功能是自动备份所有 AWS 资源并进行跨区域复制",
        ],
        "correct_answers": [
            "B",
        ],
        "explanation": "「Service Catalog 允许管理员创建经过批准的产品组合（Portfolios），终端用户可以在受控权限下自助式部署标准化资源，同时强制执行治理约束」是正确的。\n\nAWS Service Catalog 让企业可以在保证治理的前提下实现自助服务。管理员可以将经过审批的 CloudFormation 模板、Terraform 配置或 Marketplace 产品打包成“产品”，放入产品组合中，并设置启动约束、模板约束和权限控制。普通用户或团队可以在权限范围内自助部署，而不会违反企业标准。\n\n其他选项分析：\n\n「Service Catalog 主要用于监控应用程序性能和自动扩缩容」是错误的：这是 CloudWatch / Application Auto Scaling 的职责，Service Catalog 专注于资源模板的标准化分发和治理。\n\n「Service Catalog 只能用于部署 EC2 实例和简单的 S3 存储桶」是错误的：Service Catalog 支持 CloudFormation、Terraform、Marketplace 等多种资源类型，远不止 EC2 和 S3。\n\n「Service Catalog 主要功能是自动备份所有 AWS 资源并进行跨区域复制」是错误的：备份和跨区域复制是 AWS Backup、S3 Replication、DMS 等服务的功能。\n\n**重点考点 / 关键词补充：**\n- Service Catalog = 治理下的自助服务 (Self-service with Governance)\n- 核心概念：Product（产品）、Portfolio（产品组合）、Constraint（约束）\n- 优势：标准化 + 合规 + 降低 IT 部门手动审批负担\n- 常考与 CloudFormation 的结合使用",
        "domain": "Technology and Services",
    },
    {
        "id": "S140",
        "question": "AWS Personal Health Dashboard 与 AWS Trusted Advisor 的主要区别是什么？",
        "options": [
            "A. 两者功能完全相同，只是界面和名称不同，实际提供的建议内容一致",
            "B. Personal Health Dashboard 提供针对你账户的个性化健康事件和计划维护通知；Trusted Advisor 提供基于最佳实践的通用优化建议（成本、性能、安全等）",
            "C. Personal Health Dashboard 只关注成本优化，Trusted Advisor 只关注安全和合规检查",
            "D. Trusted Advisor 是免费的，Personal Health Dashboard 只对 Enterprise Support 及以上客户开放",
        ],
        "correct_answers": [
            "B",
        ],
        "explanation": "「Personal Health Dashboard 提供针对你账户的个性化健康事件和计划维护通知；Trusted Advisor 提供基于最佳实践的通用优化建议」是正确的。\n\nPersonal Health Dashboard：显示 AWS 针对你具体账户的个性化事件（如特定服务在你使用区域的计划维护、已知问题影响等），非常及时和相关。\nTrusted Advisor：提供跨成本优化、性能、安全、容错、卓越运营五个类别的通用最佳实践检查和建议（部分检查需要 Business Support 及以上）。\n\n其他选项分析：\n\n「两者功能完全相同，只是界面和名称不同，实际提供的建议内容一致」是错误的：Personal Health Dashboard 提供针对你具体账户的个性化事件通知，Trusted Advisor 提供跨五个类别的通用最佳实践检查，两者用途和信息来源完全不同。\n\n「Personal Health Dashboard 只关注成本优化，Trusted Advisor 只关注安全和合规检查」是错误的：Personal Health Dashboard 关注你账户的个性化服务健康事件和计划维护，Trusted Advisor 提供成本、性能、安全、容错、卓越运营五个类别的通用检查。\n\n**重点考点 / 关键词补充：**\n- Personal Health Dashboard：个性化、及时、针对你的账户的事件通知\n- Trusted Advisor：通用、检查项驱动的优化建议（5 个类别）\n- 考试常考：不要混淆两者用途\n- Personal Health Dashboard 对所有支持计划免费开放",
        "domain": "Security and Compliance",
    },
    {
        "id": "S141",
        "question": "使用 AWS Control Tower 后，企业通常还能从哪些其他 AWS 服务中获得额外治理价值？（本题为单选，选出最准确的描述）",
        "options": [
            "A. 使用 AWS Control Tower 后，企业就不再需要任何其他治理相关的 AWS 服务",
            "B. 结合 AWS Config 进行持续合规监控、AWS CloudTrail 进行 API 审计、AWS Organizations 进行账户管理，形成完整的治理闭环",
            "C. Control Tower 已经完全包含了所有 IAM 权限管理和策略执行功能",
            "D. 主要需要搭配 AWS Marketplace 中购买的第三方治理和合规工具",
        ],
        "correct_answers": [
            "B",
        ],
        "explanation": "「结合 AWS Config 进行持续合规监控、AWS CloudTrail 进行 API 审计、AWS Organizations 进行账户管理，形成完整的治理闭环」是正确的。\n\nControl Tower 虽然强大，但通常与以下服务配合使用效果最佳：\n- AWS Organizations（基础账户管理）\n- AWS Config（资源配置合规规则 + 聚合器）\n- AWS CloudTrail（API 调用审计）\n- IAM + SCP（权限边界）\n形成从账户创建、策略执行、持续检测到审计的完整治理体系。\n\n其他选项分析：\n\n「使用 AWS Control Tower 后，企业就不再需要任何其他治理相关的 AWS 服务」是错误的：Control Tower 是一个强大的治理编排和启动层，但通常需要与 Config、CloudTrail、Organizations 等服务配合才能形成完整的治理体系。\n\n「Control Tower 已经完全包含了所有 IAM 权限管理和策略执行功能」是错误的：IAM 策略、Service Control Policies (SCP) 和权限边界仍需要单独在 IAM 和 Organizations 中设计和维护。\n\n**重点考点 / 关键词补充：**\n- Control Tower 是治理的“指挥中心”\n- 推荐搭配：Organizations + Config + CloudTrail + IAM\n- 常考组合题：这些服务如何共同实现企业级治理",
        "domain": "Security and Compliance",
    },
]
