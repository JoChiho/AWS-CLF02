# -*- coding: utf-8 -*-
"""扫描题库，输出练习模式术语表中尚未覆盖的高频英文术语。"""
from __future__ import annotations

import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from data.multi_choice import MULTI_CHOICE_QUESTIONS
from data.single_choice import SINGLE_CHOICE_QUESTIONS
from gui.term_glossary import TERM_ANNOTATIONS, annotate_text

SKIP_WORDS = {
    "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M",
    "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z",
    "The", "And", "Or", "For", "To", "In", "On", "At", "By", "An", "As",
    "Is", "It", "If", "Of", "No", "Not", "All", "Any", "Can", "Use",
    "May", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight",
    "Nine", "Ten", "True", "False", "Yes", "Best", "Most", "Least",
    "Which", "What", "When", "Where", "How", "Why", "Who", "That", "This",
    "These", "Those", "With", "From", "Into", "Over", "Under", "Between",
    "During", "After", "Before", "While", "Both", "Each", "Every", "Some",
    "Such", "Than", "Then", "There", "Their", "They", "Them", "Its",
    "Your", "You", "We", "Our", "Us", "He", "She", "His", "Her", "Has",
    "Have", "Had", "Are", "Was", "Were", "Be", "Been", "Being", "Do",
    "Does", "Did", "Will", "Would", "Should", "Could", "Must", "Need",
    "Also", "Only", "Just", "More", "Less", "Much", "Many", "Few",
    "New", "Old", "Same", "Other", "Another", "First", "Last", "Next",
    "High", "Low", "Large", "Small", "Long", "Short", "Fast", "Slow",
    "Good", "Bad", "Better", "Worse", "Cost", "Costs", "Free", "Paid",
    "Data", "File", "Files", "User", "Users", "Team", "Teams", "Work",
    "Load", "Loads", "Task", "Tasks", "Job", "Jobs", "Run", "Runs",
    "Set", "Sets", "Get", "Add", "Remove", "Create", "Delete", "Update",
    "Enable", "Disable", "Allow", "Deny", "Grant", "Revoke", "Apply",
    "Store", "Save", "Read", "Write", "Send", "Receive", "Move", "Copy",
    "Share", "Public", "Private", "Local", "Remote", "Global", "Region",
    "Regions", "Zone", "Zones", "Account", "Accounts", "Group",
    "Groups", "Role", "Roles", "Policy", "Policies", "Key", "Keys",
    "Log", "Logs", "Rule", "Rules", "Plan", "Plans", "Type", "Types",
    "Mode", "Model", "Models", "Level", "Levels", "Size", "Sizes",
    "Time", "Times", "Day", "Days", "Month", "Months", "Year", "Years",
    "Hour", "Hours", "Minute", "Minutes", "Second", "Seconds",
    "Percent", "Percentage", "Number", "Amount", "Total", "Average",
    "Maximum", "Minimum", "Example", "Option", "Options", "Answer",
    "Question", "Service", "Services", "Resource", "Resources",
    "Application", "Applications", "System", "Systems", "Network",
    "Networks", "Server", "Servers", "Instance", "Instances", "Volume",
    "Volumes", "Bucket", "Buckets", "Object", "Objects", "Table", "Tables",
    "Database", "Databases", "Storage", "Compute", "Memory", "CPU",
    "RAM", "GB", "TB", "MB", "KB", "PB", "Mbps", "Gbps", "ms", "sec",
    "min", "hr", "USD", "API", "URL", "URI", "JSON", "XML", "HTML",
    "SQL", "NoSQL", "TLS", "SSL", "SSH", "FTP", "IP", "IPv4", "IPv6",
    "OS", "CLI", "SDK", "GUI", "UI", "UX", "ID", "IDs", "ARN", "ARNs",
    "Tag", "Tags", "Name", "Names", "Value", "Values", "State", "States",
    "Status", "Event", "Events", "Action", "Actions", "Request",
    "Requests", "Response", "Responses", "Error", "Errors", "Warning",
    "Info", "Debug", "Test", "Tests", "Case", "Cases", "Step", "Steps",
    "Phase", "Phases", "Stage", "Stages", "Process", "Processes",
    "Method", "Methods", "Function", "Functions", "Feature", "Features",
    "Benefit", "Benefits", "Risk", "Risks", "Issue", "Issues", "Problem",
    "Solution", "Approach", "Strategy", "Requirement", "Requirements",
    "Compliance", "Security", "Performance", "Availability", "Scalability",
    "Reliability", "Durability", "Elasticity", "Agility", "Flexibility",
    "Efficiency", "Optimization", "Management", "Monitoring", "Logging",
    "Auditing", "Backup", "Restore", "Recovery", "Disaster", "Failover",
    "Redundancy", "Replication", "Migration", "Deployment", "Provisioning",
    "Configuration", "Integration", "Automation", "Orchestration",
    "Encryption", "Decryption", "Authentication", "Authorization",
    "Identification", "Verification", "Validation", "Notification",
    "Communication", "Connection", "Connectivity", "Access", "Control",
    "Governance", "Billing", "Pricing", "Payment", "Invoice", "Budget",
    "Report", "Reports", "Dashboard", "Dashboards", "Metric", "Metrics",
    "Alarm", "Alarms", "Alert", "Alerts", "Trigger", "Triggers",
    "Schedule", "Schedules", "Queue", "Queues", "Topic", "Topics",
    "Stream", "Streams", "Batch", "Real", "Near", "Cold", "Hot", "Warm",
    "Active", "Passive", "Primary", "Secondary", "Master", "Slave",
    "Source", "Target", "Destination", "Origin", "Endpoint", "Endpoints",
    "Gateway", "Gateways", "Firewall", "Firewalls", "Router", "Switch",
    "Subnet", "Subnets", "CIDR", "CIDRs", "Port", "Ports", "Protocol",
    "Protocols", "Packet", "Packets", "Traffic", "Bandwidth", "Latency",
    "Throughput", "Capacity", "Utilization", "Consumption", "Usage",
    "Workload", "Workloads", "Traffic", "Session", "Sessions", "Client",
    "Clients", "Customer", "Customers", "Partner", "Partners", "Vendor",
    "Vendors", "Provider", "Providers", "Developer", "Developers",
    "Administrator", "Administrators", "Operator", "Operators",
    "Engineer", "Engineers", "Architect", "Architects", "Manager",
    "Managers", "Owner", "Owners", "Member", "Members", "Organization",
    "Company", "Business", "Enterprise", "Startup", "Industry",
    "Government", "Education", "Healthcare", "Finance", "Retail",
    "Media", "Gaming", "IoT", "AI", "ML", "DL", "NLP", "ETL", "BI",
    "SaaS", "PaaS", "IaaS", "On", "Demand", "Pay", "Per", "Reserved",
    "Spot", "Dedicated", "Shared", "Managed", "Unmanaged", "Standard",
    "Premium", "Basic", "Advanced", "Custom", "Default", "Optional",
    "Required", "Mandatory", "Recommended", "Supported", "Unsupported",
    "Available", "Unavailable", "Enabled", "Disabled", "Running",
    "Stopped", "Pending", "Failed", "Success", "Complete", "Incomplete",
    "Online", "Offline", "Internal", "External", "Inbound", "Outbound",
    "Incoming", "Outgoing", "Upload", "Download", "Import", "Export",
    "Input", "Output", "Inbound", "Cross", "Multi", "Single", "Dual",
    "Triple", "Full", "Partial", "Complete", "Incremental", "Continuous",
    "Periodic", "Scheduled", "Manual", "Automatic", "Automated",
    "Immediate", "Instant", "Delayed", "Synchronous", "Asynchronous",
    "Concurrent", "Parallel", "Sequential", "Distributed", "Centralized",
    "Decentralized", "Federated", "Hybrid", "Native", "Legacy",
    "Modern", "Traditional", "Classic", "Latest", "Current", "Previous",
    "Future", "Existing", "Additional", "Extra", "Main", "Core",
    "Central", "Peripheral", "Edge", "Cloud", "On-premises", "On-premise",
    "Premises", "Premise", "Physical", "Virtual", "Logical", "Abstract",
    "Concrete", "Direct", "Indirect", "Explicit", "Implicit", "Static",
    "Dynamic", "Fixed", "Variable", "Constant", "Temporary", "Permanent",
    "Persistent", "Transient", "Volatile", "Stable", "Unstable",
    "Consistent", "Inconsistent", "Uniform", "Diverse", "Homogeneous",
    "Heterogeneous", "Symmetric", "Asymmetric", "Synchronous",
    "North", "South", "East", "West", "America", "Europe", "Asia",
    "Pacific", "Africa", "China", "Japan", "India", "Korea", "Brazil",
    "Canada", "Australia", "London", "Tokyo", "Singapore", "Frankfurt",
    "Ireland", "Virginia", "Oregon", "California", "Mumbai", "Sydney",
    "Seoul", "Stockholm", "Paris", "Milan", "Spain", "Sweden", "Netherlands",
    "United", "States", "Kingdom", "Republic", "GovCloud", "ISO", "PCI",
    "HIPAA", "GDPR", "SOC", "FedRAMP", "NIST", "CIS", "OWASP",
}


def collect_corpus() -> str:
    parts: list[str] = []
    for q in SINGLE_CHOICE_QUESTIONS + MULTI_CHOICE_QUESTIONS:
        parts.append(q.get("question", ""))
        for opt in q.get("options", []):
            parts.append(opt)
        parts.append(q.get("explanation", ""))
    return "\n".join(parts)


def extract_candidates(corpus: str) -> Counter[str]:
    found: list[str] = []

    patterns = [
        r"\b(?:Amazon|AWS)\s+[A-Z][A-Za-z0-9]+(?:\s+[A-Z][A-Za-z0-9]+)*\b",
        r"\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)+\b",
        r"\b[A-Z][a-z]+(?:-[A-Z][a-z]+)+\b",
        r"\b[A-Z]{2,8}\b",
    ]
    for pat in patterns:
        for m in re.finditer(pat, corpus):
            found.append(m.group())

    return Counter(found)


def is_covered(term: str) -> bool:
    known = {en.lower() for en, _ in TERM_ANNOTATIONS}
    if term.lower() in known:
        return True
    sample = annotate_text(f"Use {term} for this.")
    return "（" in sample and term in sample


def main() -> None:
    corpus = collect_corpus()
    counts = extract_candidates(corpus)
    uncovered: list[tuple[str, int]] = []

    for term, count in counts.most_common():
        if term in SKIP_WORDS or term.lower() in {w.lower() for w in SKIP_WORDS}:
            continue
        if is_covered(term):
            continue
        uncovered.append((term, count))

    print("=== Uncovered terms (freq >= 2) ===")
    for term, count in uncovered:
        if count >= 2:
            print(f"{count:4d}  {term}")
    print(f"\nUnique uncovered (freq>=2): {sum(1 for _, c in uncovered if c >= 2)}")
    print(f"Unique uncovered (all): {len(uncovered)}")


if __name__ == "__main__":
    main()