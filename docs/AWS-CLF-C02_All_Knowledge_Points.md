# AWS CLF-C02 考试完整知识点关键词清单
## 涵盖所有官方考试大纲 + 边缘/高频考点

---

## 1. Cloud Concepts（云概念） - 24%

### 1.1 AWS 全球基础设施
- Region（区域）
- Availability Zone (AZ) - 物理隔离、独立供电/网络
- Edge Location（边缘站点）- CloudFront / Global Accelerator
- Local Zones（本地区域）- 靠近人口密集区，低延迟
- Wavelength Zones（5G边缘）
- AWS Outposts（本地部署AWS硬件）

### 1.2 核心云概念
- High Availability（高可用）
- Fault Tolerance（容错）
- Scalability（可扩展性） vs Elasticity（弹性）
- Agility（敏捷性）
- Global Reach（全球覆盖）
- Economies of Scale（规模经济）

### 1.3 云服务模型
- IaaS（Infrastructure as a Service）
- PaaS（Platform as a Service）
- SaaS（Software as a Service）
- **Shared Responsibility Model**（责任共担模型）- 最重要考点

### 1.4 AWS Well-Architected Framework（六大支柱）
- Operational Excellence（卓越运营）
- Security（安全性）
- Reliability（可靠性）
- Performance Efficiency（性能效率）
- Cost Optimization（成本优化）
- Sustainability（可持续性）

### 1.5 其他重要概念
- Loose Coupling（松耦合）
- Stateless vs Stateful（无状态 vs 有状态）
- Event-Driven Architecture
- Serverless
- Microservices
- CI/CD 基础概念

---

## 2. Security and Compliance（安全与合规） - 30%

### 2.1 Identity and Access Management (IAM)
- IAM User / Group / Role / Policy
- IAM Roles（最重要）
- AssumeRole / STS
- IAM Policy（Identity-based vs Resource-based）
- Permission Boundary（权限边界）
- Service Control Policies (SCP) - Organizations
- IAM Roles Anywhere
- IAM Access Analyzer
- Multi-Factor Authentication (MFA)

### 2.2 数据保护与加密
- AWS KMS（Key Management Service）
  - Customer Managed Key (CMK) vs AWS Managed Key
  - Key Policy vs IAM Policy
  - Automatic Key Rotation
  - Envelope Encryption
- S3 Server-Side Encryption (SSE-S3, SSE-KMS, SSE-C)
- Client-Side Encryption
- AWS CloudHSM
- AWS Secrets Manager vs Systems Manager Parameter Store

### 2.3 网络安全
- Security Group（有状态）
- Network ACL（NACL，无状态）
- VPC Flow Logs
- AWS PrivateLink / VPC Endpoints
- AWS Shield（Standard / Advanced）
- AWS WAF（Web Application Firewall）
- AWS Firewall Manager
- AWS Network Firewall

### 2.4 威胁检测与响应
- Amazon GuardDuty（智能威胁检测）
- AWS Inspector（漏洞评估）
- Amazon Macie（敏感数据发现）
- AWS Security Hub（安全态势管理）
- Amazon Detective（安全调查）
- AWS CloudTrail（日志）
- AWS Config（合规检查）

### 2.5 合规与认证
- AWS Artifact（合规报告中心）
- 主要合规框架：
  - SOC 1/2/3
  - PCI DSS
  - HIPAA
  - ISO 27001/27017/27018
  - FedRAMP
  - GDPR
  - IRAP, MTCS, C5 等
- AWS Compliance Programs

### 2.6 其他安全服务
- AWS Certificate Manager (ACM)
- AWS Directory Service
- AWS Cognito
- AWS Secrets Manager
- AWS Signer
- AWS Verified Access

---

## 3. Technology and Services（技术与服务） - 34%

### 3.1 计算服务
**Amazon EC2**
- Instance Types（通用、计算优化、内存优化、存储优化、加速计算）
- Purchasing Options：
  - On-Demand
  - Reserved Instances（Standard / Convertible）
  - Spot Instances
  - Savings Plans（Compute / EC2 Instance）
- Auto Scaling（动态、预测、计划）
- Placement Groups（Cluster / Spread / Partition）
- Dedicated Hosts / Dedicated Instances
- Nitro System

**Serverless & Containers**
- AWS Lambda（触发器、并发、Layers、Provisioned Concurrency）
- Amazon ECS / Fargate
- Amazon EKS（Kubernetes）
- AWS App Runner
- AWS Elastic Beanstalk

**其他计算**
- AWS Lightsail
- AWS Outposts
- AWS Wavelength
- VMware Cloud on AWS

### 3.2 存储服务

**Amazon S3**
- Storage Classes（Standard, Intelligent-Tiering, Standard-IA, One Zone-IA, Glacier Instant Retrieval, Glacier Flexible Retrieval, Glacier Deep Archive）
- S3 Lifecycle Policies
- S3 Versioning
- S3 Object Lock（Compliance / Governance 模式）
- S3 Intelligent-Tiering
- S3 Storage Lens
- S3 Transfer Acceleration
- S3 Select
- S3 Batch Operations
- S3 Access Points
- S3 Object Ownership
- S3 Requester Pays

**块存储与文件存储**
- Amazon EBS（gp3, io2, st1, sc1）
- Amazon EFS（标准 vs 低频访问）
- Amazon FSx（Windows / Lustre / NetApp ONTAP / OpenZFS）
- Amazon S3 Glacier

**混合与边缘存储**
- AWS Storage Gateway
- AWS Snow Family（Snowcone, Snowball, Snowmobile）
- AWS DataSync

### 3.3 数据库服务

**关系型数据库**
- Amazon RDS（MySQL, PostgreSQL, MariaDB, Oracle, SQL Server）
- Amazon Aurora（MySQL / PostgreSQL 兼容）
- Amazon Aurora Serverless v2

**NoSQL / 其他数据库**
- Amazon DynamoDB（键值 + 文档）
- Amazon DocumentDB（MongoDB 兼容）
- Amazon ElastiCache（Redis / Memcached）
- Amazon Neptune（图数据库）
- Amazon Timestream（时序数据库）
- Amazon Keyspaces（Cassandra 兼容）
- Amazon Quantum Ledger Database (QLDB)

**数据仓库与分析**
- Amazon Redshift
- Amazon Redshift Serverless
- Amazon Athena
- Amazon EMR

### 3.4 网络服务

**VPC 核心**
- VPC, Subnets, Route Tables, Internet Gateway, NAT Gateway
- VPC Endpoints（Gateway / Interface）
- VPC Peering
- AWS Transit Gateway
- AWS PrivateLink

**连接服务**
- AWS Direct Connect
- AWS Site-to-Site VPN
- AWS Client VPN
- AWS Cloud WAN

**内容分发与 DNS**
- Amazon CloudFront
- AWS Global Accelerator
- Amazon Route 53（各种路由策略）

### 3.5 监控、日志与管理

- Amazon CloudWatch（Metrics, Alarms, Dashboards, Logs, Events）
- AWS CloudTrail
- AWS Config
- AWS Systems Manager（SSM）
- AWS CloudFormation
- AWS Service Catalog
- AWS Organizations + SCPs
- AWS Control Tower
- AWS Trusted Advisor
- AWS Personal Health Dashboard
- AWS Well-Architected Tool

### 3.6 其他重要服务（高频/边缘）

- AWS Step Functions
- Amazon EventBridge
- Amazon SQS / SNS / MQ
- Amazon Kinesis（Data Streams, Firehose, Analytics）
- AWS Glue
- Amazon QuickSight
- AWS AppSync
- Amazon API Gateway
- AWS Amplify
- AWS Device Farm
- AWS IoT Core
- Amazon SageMaker（高层次理解）
- AWS Marketplace

---

## 4. Billing, Pricing, and Support（账单、定价与支持） - 12%

### 4.1 定价模型

**EC2 定价选项**
- On-Demand
- Reserved Instances（Standard vs Convertible, All Upfront / Partial / No Upfront）
- Spot Instances
- Savings Plans（Compute Savings Plans vs EC2 Instance Savings Plans）
- Dedicated Hosts

**其他定价概念**
- AWS Free Tier（12个月免费 + Always Free）
- Pay-as-you-go
- Consolidated Billing
- AWS Pricing Calculator

### 4.2 成本管理工具

- AWS Cost Explorer
- AWS Budgets（预算 + 告警）
- AWS Cost Anomaly Detection
- AWS Cost Categories
- AWS Cost and Usage Report (CUR)
- AWS Billing Conductor

### 4.3 支持计划

- Basic Support（免费）
- Developer Support
- Business Support
- Enterprise On-Ramp Support
- Enterprise Support

**关键区别**：
- Technical Account Manager (TAM)
- 响应时间（严重故障、业务受影响、生产系统受影响）
- 架构审查（Architecture Review）
- 白手套服务（Proactive Guidance）

### 4.4 数据传输费用（极高频考点）

- 入互联网 → AWS：大多免费
- AWS → 互联网：收费
- 同一 Region 内 AZ 之间：通常免费或极低
- 跨 Region：收费（通常最贵）
- Direct Connect vs 公网费用对比
- CloudFront / Transfer Acceleration 对成本的影响

### 4.5 其他重要主题

- AWS Organizations + Consolidated Billing
- AWS Marketplace（购买第三方软件）
- Reserved Instance Marketplace
- Savings Plans 购买建议与灵活性
- 成本优化策略（Right-sizing, Spot, Savings Plans, Storage Classes 等）
- AWS Support Center vs AWS Personal Health Dashboard

---

## 5. 边缘 / 高频 / 容易混淆的考点（必须掌握）

### 基础设施相关
- Local Zones vs Edge Locations vs Wavelength Zones
- Region 选择对合规、延迟、成本的影响
- 哪些服务是 Region 级 / Global 级

### 安全相关
- IAM Role vs IAM User（最常考）
- KMS Customer Managed Key vs AWS Managed Key
- Security Group vs NACL
- S3 Block Public Access
- Object Lock 的两种模式（Compliance vs Governance）

### 计费相关
- Savings Plans vs Reserved Instances 区别（灵活性 vs 折扣）
- Spot Instance 中断行为与通知
- Free Tier 12个月从“激活”开始算
- 数据传输费用最容易被考的几种场景

### 架构相关
- Multi-AZ vs Multi-Region 的适用场景
- Active/Active vs Active/Passive vs Pilot Light vs Warm Standby vs Backup & Restore
- Stateless 架构的重要性

### 服务对比（高频）
- S3 vs EBS vs EFS vs FSx
- RDS vs Aurora vs DynamoDB
- CloudFront vs Global Accelerator
- GuardDuty vs Inspector vs Macie vs Security Hub
- CloudWatch vs CloudTrail vs Config

---

**说明**：
本清单力求覆盖 AWS CLF-C02 官方考试指南所有知识点 + 真实考试中出现过的边缘和高频考点。建议配合官方 Exam Guide + Well-Architected Framework 白皮书使用。

如需进一步细化某个领域或生成对应题目，请随时告诉我。