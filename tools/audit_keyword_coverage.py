#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AWS CLF-C02 Keyword Coverage Gap Audit
Compares docs/AWS-CLF-C02_All_Knowledge_Points.md against current question bank corpus.
"""

import ast
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

# Curated comprehensive keyword list extracted from AWS-CLF-C02_All_Knowledge_Points.md
# Grouped by original sections for reporting. Includes main terms + variants + Chinese where relevant.
# Each entry: (display_name, search_variants_list)

KEYWORDS = {
    "1. Cloud Concepts - 全球基础设施": [
        ("Region（区域）", ["region", "区域"]),
        ("Availability Zone (AZ)", ["availability zone", "az", "可用区", "可用区域"]),
        ("Edge Location（边缘站点）", ["edge location", "边缘站点", "边缘位置"]),
        ("Local Zones（本地区域）", ["local zones", "local zone", "本地区域", "本地可用区"]),
        ("Wavelength Zones（5G边缘）", ["wavelength zones", "wavelength zone", "wavelength", "5g边缘"]),
        ("AWS Outposts", ["outposts", "aws outposts"]),
    ],
    "1. Cloud Concepts - 核心云概念": [
        ("High Availability（高可用）", ["high availability", "高可用", "高可用性"]),
        ("Fault Tolerance（容错）", ["fault tolerance", "容错", "容错性"]),
        ("Scalability（可扩展性）", ["scalability", "可扩展性", "扩展性"]),
        ("Elasticity（弹性）", ["elasticity", "弹性"]),
        ("Agility（敏捷性）", ["agility", "敏捷性"]),
        ("Global Reach（全球覆盖）", ["global reach", "全球覆盖"]),
        ("Economies of Scale（规模经济）", ["economies of scale", "规模经济"]),
        ("Loose Coupling（松耦合）", ["loose coupling", "松耦合"]),
        ("Stateless vs Stateful", ["stateless", "stateful", "无状态", "有状态"]),
        ("Event-Driven Architecture", ["event-driven", "事件驱动"]),
        ("Serverless", ["serverless", "无服务器"]),
        ("Microservices", ["microservices", "微服务"]),
        ("CI/CD", ["ci/cd", "cicd", "持续集成", "持续部署"]),
    ],
    "1. Cloud Concepts - 云服务模型 & Well-Architected": [
        ("IaaS", ["iaas", "infrastructure as a service"]),
        ("PaaS", ["paas", "platform as a service"]),
        ("SaaS", ["saas", "software as a service"]),
        ("Shared Responsibility Model", ["shared responsibility model", "责任共担模型", "shared responsibility"]),
        ("Well-Architected Framework", ["well-architected framework", "well-architected", "架构良好框架"]),
        ("Operational Excellence", ["operational excellence", "卓越运营"]),
        ("Security（安全性）", ["security pillar", "安全性支柱"]),
        ("Reliability（可靠性）", ["reliability", "可靠性支柱"]),
        ("Performance Efficiency", ["performance efficiency", "性能效率"]),
        ("Cost Optimization", ["cost optimization", "成本优化"]),
        ("Sustainability（可持续性）", ["sustainability", "可持续性"]),
    ],
    "2. Security - IAM": [
        ("IAM User / Group / Role / Policy", ["iam user", "iam group", "iam role", "iam policy"]),
        ("IAM Roles（最重要）", ["iam role", "iam roles"]),
        ("AssumeRole / STS", ["assumerole", "assume role", "sts", "security token service"]),
        ("IAM Policy（Identity-based vs Resource-based）", ["identity-based policy", "resource-based policy"]),
        ("Permission Boundary（权限边界）", ["permission boundary", "权限边界"]),
        ("Service Control Policies (SCP)", ["scp", "service control policy", "service control policies"]),
        ("IAM Roles Anywhere", ["roles anywhere", "iam roles anywhere"]),
        ("IAM Access Analyzer", ["access analyzer", "iam access analyzer"]),
        ("Multi-Factor Authentication (MFA)", ["mfa", "multi-factor authentication", "多因素认证"]),
    ],
    "2. Security - 数据保护与加密": [
        ("AWS KMS", ["kms", "key management service"]),
        ("Customer Managed Key (CMK)", ["customer managed key", "cmk", "客户托管密钥"]),
        ("AWS Managed Key", ["aws managed key", "aws 托管密钥"]),
        ("Key Policy vs IAM Policy", ["key policy"]),
        ("Automatic Key Rotation", ["key rotation", "自动密钥轮换", "automatic key rotation"]),
        ("Envelope Encryption", ["envelope encryption", "信封加密"]),
        ("SSE-S3", ["sse-s3", "sse_s3"]),
        ("SSE-KMS", ["sse-kms", "sse_kms"]),
        ("SSE-C", ["sse-c", "sse_c"]),
        ("Client-Side Encryption", ["client-side encryption", "客户端加密"]),
        ("AWS CloudHSM", ["cloudhsm", "cloud hsm"]),
        ("AWS Secrets Manager", ["secrets manager"]),
        ("Systems Manager Parameter Store", ["parameter store", "ssm parameter store"]),
    ],
    "2. Security - 网络安全 & 威胁检测": [
        ("Security Group（有状态）", ["security group", "安全组"]),
        ("Network ACL（NACL，无状态）", ["network acl", "nacl", "网络 acl"]),
        ("VPC Flow Logs", ["vpc flow logs", "flow logs"]),
        ("AWS PrivateLink", ["privatelink", "private link"]),
        ("VPC Endpoints", ["vpc endpoint", "vpc endpoints", "接口端点", "网关端点"]),
        ("AWS Shield", ["shield", "aws shield", "shield advanced"]),
        ("AWS WAF", ["waf", "web application firewall"]),
        ("AWS Firewall Manager", ["firewall manager"]),
        ("AWS Network Firewall", ["network firewall"]),
        ("Amazon GuardDuty", ["guardduty", "guard duty"]),
        ("AWS Inspector", ["inspector", "aws inspector"]),
        ("Amazon Macie", ["macie"]),
        ("AWS Security Hub", ["security hub"]),
        ("Amazon Detective", ["detective"]),
        ("AWS CloudTrail", ["cloudtrail"]),
        ("AWS Config", ["aws config", "config"]),
    ],
    "2. Security - 合规": [
        ("AWS Artifact", ["artifact", "aws artifact"]),
        ("SOC 1/2/3", ["soc 1", "soc 2", "soc 3"]),
        ("PCI DSS", ["pci dss", "pci"]),
        ("HIPAA", ["hipaa"]),
        ("ISO 27001", ["iso 27001", "iso27001"]),
        ("FedRAMP", ["fedramp"]),
        ("GDPR", ["gdpr"]),
        ("AWS Certificate Manager (ACM)", ["acm", "certificate manager"]),
        ("AWS Cognito", ["cognito"]),
        ("AWS Signer", ["signer"]),
    ],
    "3. Technology - 计算服务 (EC2 & Serverless)": [
        ("Amazon EC2", ["ec2", "amazon ec2"]),
        ("Instance Types", ["instance types", "实例类型", "通用", "计算优化", "内存优化"]),
        ("On-Demand", ["on-demand", "按需实例"]),
        ("Reserved Instances", ["reserved instances", "预留实例", "ri", "standard reserved", "convertible reserved"]),
        ("Spot Instances", ["spot instances", "spot instance", "竞价实例"]),
        ("Savings Plans", ["savings plans", "节省计划"]),
        ("Compute Savings Plans vs EC2 Instance Savings Plans", ["compute savings plans", "ec2 instance savings plans"]),
        ("Auto Scaling", ["auto scaling", "autoscaling"]),
        ("Placement Groups", ["placement groups", "placement group", "集群放置群组", "分散放置群组"]),
        ("Dedicated Hosts / Dedicated Instances", ["dedicated host", "dedicated instance"]),
        ("Nitro System", ["nitro"]),
        ("AWS Lambda", ["lambda", "aws lambda"]),
        ("Amazon ECS / Fargate", ["ecs", "fargate", "amazon ecs"]),
        ("Amazon EKS", ["eks", "kubernetes"]),
        ("AWS App Runner", ["app runner"]),
        ("AWS Elastic Beanstalk", ["elastic beanstalk", "beanstalk"]),
        ("AWS Lightsail", ["lightsail"]),
    ],
    "3. Technology - 存储服务 (S3 等)": [
        ("Amazon S3", ["s3", "amazon s3"]),
        ("S3 Storage Classes", ["storage class", "storage classes", "s3 standard", "intelligent-tiering", "standard-ia", "one zone-ia", "glacier instant retrieval", "glacier flexible retrieval", "glacier deep archive"]),
        ("S3 Lifecycle Policies", ["lifecycle policy", "lifecycle policies", "生命周期策略"]),
        ("S3 Versioning", ["versioning", "版本控制"]),
        ("S3 Object Lock", ["object lock", "对象锁定"]),
        ("Compliance / Governance 模式", ["compliance mode", "governance mode"]),
        ("S3 Intelligent-Tiering", ["intelligent-tiering"]),
        ("S3 Storage Lens", ["storage lens"]),
        ("S3 Transfer Acceleration", ["transfer acceleration"]),
        ("S3 Select", ["s3 select"]),
        ("S3 Batch Operations", ["batch operations"]),
        ("S3 Access Points", ["access points"]),
        ("S3 Object Ownership", ["object ownership"]),
        ("S3 Requester Pays", ["requester pays"]),
        ("Amazon EBS", ["ebs", "elastic block store", "gp3", "io2", "st1", "sc1"]),
        ("Amazon EFS", ["efs", "elastic file system"]),
        ("Amazon FSx", ["fsx", "fsx windows", "fsx lustre"]),
        ("AWS Storage Gateway", ["storage gateway"]),
        ("AWS Snow Family", ["snow family", "snowcone", "snowball", "snowmobile"]),
        ("AWS DataSync", ["datasync"]),
    ],
    "3. Technology - 数据库服务": [
        ("Amazon RDS", ["rds", "amazon rds"]),
        ("Amazon Aurora", ["aurora", "amazon aurora"]),
        ("Aurora Serverless v2", ["aurora serverless"]),
        ("Amazon DynamoDB", ["dynamodb", "dynamo db"]),
        ("Amazon DocumentDB", ["documentdb"]),
        ("Amazon ElastiCache", ["elasticache", "elasti cache", "redis", "memcached"]),
        ("Amazon Neptune", ["neptune"]),
        ("Amazon Timestream", ["timestream"]),
        ("Amazon Keyspaces", ["keyspaces"]),
        ("QLDB", ["qldb", "quantum ledger"]),
        ("Amazon Redshift", ["redshift"]),
        ("Amazon Athena", ["athena"]),
        ("Amazon EMR", ["emr"]),
    ],
    "3. Technology - 网络服务": [
        ("VPC", ["vpc"]),
        ("Subnets", ["subnet", "subnets"]),
        ("Route Tables", ["route table"]),
        ("Internet Gateway", ["internet gateway", "igw"]),
        ("NAT Gateway", ["nat gateway", "nat 网关"]),
        ("VPC Endpoints（Gateway / Interface）", ["gateway endpoint", "interface endpoint"]),
        ("VPC Peering", ["vpc peering", "对等连接"]),
        ("AWS Transit Gateway", ["transit gateway"]),
        ("AWS Direct Connect", ["direct connect"]),
        ("AWS Site-to-Site VPN", ["site-to-site vpn", "vpn"]),
        ("AWS Client VPN", ["client vpn"]),
        ("Amazon CloudFront", ["cloudfront"]),
        ("AWS Global Accelerator", ["global accelerator"]),
        ("Amazon Route 53", ["route 53", "route53"]),
    ],
    "3. Technology - 监控、管理 & 其他服务": [
        ("Amazon CloudWatch", ["cloudwatch", "cloud watch", "metrics", "alarms", "dashboards"]),
        ("AWS Systems Manager (SSM)", ["systems manager", "ssm", "parameter store"]),
        ("AWS CloudFormation", ["cloudformation"]),
        ("AWS Service Catalog", ["service catalog"]),
        ("AWS Organizations", ["organizations"]),
        ("AWS Control Tower", ["control tower"]),
        ("AWS Trusted Advisor", ["trusted advisor"]),
        ("AWS Personal Health Dashboard", ["personal health dashboard"]),
        ("AWS Well-Architected Tool", ["well-architected tool"]),
        ("AWS Step Functions", ["step functions"]),
        ("Amazon EventBridge", ["eventbridge", "event bridge"]),
        ("Amazon SQS", ["sqs", "simple queue service"]),
        ("Amazon SNS", ["sns", "simple notification service"]),
        ("Amazon Kinesis", ["kinesis"]),
        ("AWS Glue", ["glue"]),
        ("Amazon QuickSight", ["quicksight"]),
        ("Amazon API Gateway", ["api gateway"]),
        ("AWS Amplify", ["amplify"]),
        ("AWS IoT Core", ["iot core"]),
        ("Amazon SageMaker", ["sagemaker"]),
        ("AWS Marketplace", ["marketplace"]),
    ],
    "4. Billing - 定价模型 & 工具": [
        ("AWS Free Tier", ["free tier", "免费套餐", "12个月免费"]),
        ("Pay-as-you-go", ["pay-as-you-go", "按需付费"]),
        ("Consolidated Billing", ["consolidated billing", "合并账单"]),
        ("AWS Pricing Calculator", ["pricing calculator"]),
        ("AWS Cost Explorer", ["cost explorer"]),
        ("AWS Budgets", ["budgets", "aws budgets"]),
        ("AWS Cost Anomaly Detection", ["cost anomaly detection"]),
        ("AWS Cost and Usage Report (CUR)", ["cost and usage report", "cur"]),
        ("AWS Billing Conductor", ["billing conductor"]),
    ],
    "4. Billing - 支持计划": [
        ("Basic Support", ["basic support"]),
        ("Developer Support", ["developer support"]),
        ("Business Support", ["business support"]),
        ("Enterprise On-Ramp Support", ["enterprise on-ramp"]),
        ("Enterprise Support", ["enterprise support"]),
        ("Technical Account Manager (TAM)", ["tam", "technical account manager"]),
    ],
    "4. Billing - 数据传输费用（极高频）": [
        ("数据传输费用 - 入站免费", ["入站", "inbound data transfer", "数据传入免费"]),
        ("数据传输费用 - 出站收费", ["出站", "outbound data transfer", "数据传出收费"]),
        ("跨 Region 数据传输", ["跨 region", "cross-region data transfer"]),
        ("AZ 之间数据传输", ["az 之间", "同一 region az"]),
        ("Direct Connect 费用", ["direct connect pricing"]),
        ("CloudFront / Transfer Acceleration 成本", ["transfer acceleration 成本"]),
    ],
    "5. 边缘/高频/易混淆考点": [
        ("Local Zones vs Edge Locations vs Wavelength Zones", ["local zones vs", "edge location vs"]),
        ("Region 选择影响（合规/延迟/成本）", ["region 选择"]),
        ("哪些服务是 Region 级 / Global 级", ["global service", "region level service"]),
        ("IAM Role vs IAM User", ["role vs user", "iam role vs user"]),
        ("KMS Customer Managed Key vs AWS Managed Key", ["cmk vs aws managed"]),
        ("Security Group vs NACL", ["security group vs nacl", "安全组 vs nacl"]),
        ("S3 Block Public Access", ["block public access"]),
        ("Object Lock Compliance vs Governance", ["compliance mode vs governance"]),
        ("Savings Plans vs Reserved Instances", ["savings plans vs reserved", "节省计划 vs 预留实例"]),
        ("Spot Instance 中断行为", ["spot instance interruption", "竞价实例中断"]),
        ("Free Tier 12个月从激活开始", ["free tier.*激活"]),
        ("Multi-AZ vs Multi-Region", ["multi-az vs multi-region"]),
        ("Active/Active vs Active/Passive vs Pilot Light vs Warm Standby", ["pilot light", "warm standby", "active/active", "active/passive"]),
        ("S3 vs EBS vs EFS vs FSx", ["s3 vs ebs", "s3 vs efs"]),
        ("RDS vs Aurora vs DynamoDB", ["rds vs aurora", "aurora vs dynamodb"]),
        ("CloudFront vs Global Accelerator", ["cloudfront vs global accelerator"]),
        ("GuardDuty vs Inspector vs Macie vs Security Hub", ["guardduty vs inspector"]),
        ("CloudWatch vs CloudTrail vs Config", ["cloudwatch vs cloudtrail", "cloudtrail vs config"]),
    ],
}

def load_corpus():
    corpus_path = ROOT / "docs" / "question_bank_corpus.txt"
    single = load_questions_text(ROOT / "data" / "single_choice.py", "SINGLE_CHOICE_QUESTIONS")
    multi = load_questions_text(ROOT / "data" / "multi_choice.py", "MULTI_CHOICE_QUESTIONS")
    corpus = (single + " " + multi).lower()
    corpus_path.write_text(corpus, encoding="utf-8")
    return corpus

def load_questions_text(filename, varname):
    with open(filename, "r", encoding="utf-8") as f:
        content = f.read()
    tree = ast.parse(content)
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign) and getattr(node.targets[0], "id", "") == varname:
            qs = ast.literal_eval(node.value)
            texts = []
            for q in qs:
                texts.append(q.get("question", ""))
                texts.extend(q.get("options", []))
                texts.append(q.get("explanation", ""))
            return " ".join(texts).lower()
    return ""

def check_coverage(corpus):
    results = {}
    total_keywords = 0
    covered = 0
    missing_by_section = {}

    for section, kws in KEYWORDS.items():
        section_missing = []
        for display, variants in kws:
            total_keywords += 1
            hit = False
            for v in variants:
                # For regex-like (e.g. free tier.*激活)
                if ".*" in v:
                    if re.search(v, corpus):
                        hit = True
                        break
                elif v in corpus:
                    hit = True
                    break
            if not hit:
                section_missing.append(display)
            else:
                covered += 1
        missing_by_section[section] = section_missing
        results[section] = {
            "total": len(kws),
            "missing": len(section_missing),
            "missing_list": section_missing,
        }

    return {
        "total_keywords": total_keywords,
        "covered": covered,
        "coverage_rate": round(covered / total_keywords * 100, 1) if total_keywords else 0,
        "by_section": results,
        "missing_by_section": missing_by_section,
    }

def main():
    # Use UTF-8 for file output; stdout uses safe English only to avoid cp932 issues on Windows
    corpus = load_corpus()

    report = check_coverage(corpus)

    # Write detailed report (primary deliverable, supports full Chinese)
    out_path = ROOT / "docs" / "keyword_coverage_gap_report.txt"
    with out_path.open("w", encoding="utf-8") as f:
        f.write("=" * 70 + "\n")
        f.write("AWS CLF-C02 题库关键词覆盖差距审计报告\n")
        f.write("基于 docs/AWS-CLF-C02_All_Knowledge_Points.md vs 当前题库 (245题: 136单选 + 109多选)\n")
        f.write("=" * 70 + "\n\n")
        f.write(f"题库语料库大小: {len(corpus):,} 字符\n\n")
        f.write(f"总关键词数: {report['total_keywords']}\n")
        f.write(f"已覆盖: {report['covered']}\n")
        f.write(f"未覆盖: {report['total_keywords'] - report['covered']}\n")
        f.write(f"覆盖率: {report['coverage_rate']}%\n\n")

        f.write("-" * 70 + "\n")
        f.write("按领域缺失详情\n")
        f.write("-" * 70 + "\n")

        for section, data in report["by_section"].items():
            miss_count = data["missing"]
            total = data["total"]
            pct = round((total - miss_count) / total * 100, 1) if total else 100
            f.write(f"\n【{section}】  {total - miss_count}/{total} 覆盖 ({pct}%)  | 缺失 {miss_count} 个\n")
            if miss_count > 0:
                for m in data["missing_list"]:
                    f.write(f"  ✗ 未覆盖: {m}\n")
            else:
                f.write("  ✓ 该分组全部关键词均有题目覆盖\n")

        # Critical summary
        f.write("\n" + "=" * 70 + "\n")
        f.write("关键缺失汇总（建议优先补充方向）\n")
        f.write("=" * 70 + "\n")
        critical = [(s, d) for s, d in report["by_section"].items() if d["missing"] > 0]
        if critical:
            for s, d in critical:
                f.write(f"- {s}: {d['missing']} 个关键词未覆盖\n")
        else:
            f.write("✓ 所有分组关键词均已覆盖！\n")

    # Safe English-only console output
    print("=" * 60)
    print("AWS CLF-C02 Keyword Coverage Gap Audit - COMPLETE")
    print("=" * 60)
    print(f"Total keywords analyzed: {report['total_keywords']}")
    print(f"Covered: {report['covered']}")
    print(f"Missing: {report['total_keywords'] - report['covered']}")
    print(f"Overall coverage rate: {report['coverage_rate']}%")
    print()
    print("Full detailed report (Chinese + all missing items) saved to:")
    print(f"  {out_path}")
    print()
    print("Quick summary of sections with gaps (see full report for Chinese names):")
    gap_count = 0
    for s, d in report["by_section"].items():
        if d["missing"] > 0:
            gap_count += 1
            # Fully ASCII-safe for Windows cp932 console
            short = "".join(c for c in (s.split(" - ")[0] if " - " in s else s[:25]) if ord(c) < 128).strip() or "Section"
            print("  - {}: {} missing".format(short, d["missing"]))
    if gap_count == 0:
        print("  (None - full coverage achieved)")

if __name__ == "__main__":
    main()
