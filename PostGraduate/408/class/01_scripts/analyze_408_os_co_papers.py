from __future__ import annotations

import csv
import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path

import fitz


ROOT = Path(r"D:\Desktop\ArcNote\PostGraduate\408\class")
SOURCES = [
    Path(r"D:\Desktop\ArcNote\PostGraduate\答题卡\计算机408历年真题\2009-2023计算机408统考真题"),
    Path(r"D:\Desktop\ArcNote\PostGraduate\答题卡\计算机408历年真题\2009-2023计算机408真题解析"),
    Path(r"D:\Desktop\ArcNote\PostGraduate\答题卡\计算机408历年真题\2024计算机408真题+解析"),
    Path(r"D:\Desktop\ArcNote\PostGraduate\答题卡\计算机408历年真题\2025计算机408真题+解析"),
]


@dataclass(frozen=True)
class Chapter:
    subject: str
    chapter: str
    title: str
    keywords: tuple[str, ...]


CHAPTERS = [
    Chapter("操作系统", "第1章", "概述、运行机制、中断/异常、系统调用、引导", ("操作系统", "系统调用", "中断", "异常", "内核态", "用户态", "特权指令", "引导", "启动", "批处理", "分时")),
    Chapter("操作系统", "第2章", "进程、线程、处理机调度、同步互斥、死锁", ("进程", "线程", "PCB", "调度", "时间片", "优先级", "信号量", "PV", "互斥", "同步", "临界区", "管程", "死锁", "银行家", "前趋图")),
    Chapter("操作系统", "第3章", "内存管理、页表、虚拟内存、页面置换", ("页表", "分页", "分段", "虚拟地址", "逻辑地址", "物理地址", "地址变换", "TLB", "快表", "缺页", "页面置换", "工作集", "抖动", "驻留集", "内存管理")),
    Chapter("操作系统", "第4章", "文件系统、目录、文件分配、空闲空间管理", ("文件", "目录", "索引", "inode", "FAT", "位示图", "空闲", "磁盘块", "文件控制块", "FCB", "打开文件", "逻辑格式化")),
    Chapter("操作系统", "第5章", "I/O 管理、缓冲、磁盘调度、设备管理", ("I/O", "输入输出", "设备", "缓冲", "DMA", "磁盘调度", "SCAN", "SSTF", "中断驱动", "设备独立性", "通道")),
    Chapter("计算机组成原理", "第1章", "概述、性能指标、层次结构", ("CPI", "主频", "时钟周期", "CPU时间", "MIPS", "FLOPS", "吞吐率", "响应时间", "性能", "冯诺依曼")),
    Chapter("计算机组成原理", "第2章", "数据表示与运算", ("补码", "原码", "反码", "移码", "定点", "浮点", "IEEE", "溢出", "舍入", "移位", "加法器", "ALU", "规格化")),
    Chapter("计算机组成原理", "第3章", "存储系统、Cache、主存、虚拟存储", ("Cache", "缓存", "主存", "存储器", "映射", "组相联", "全相联", "直接映射", "替换", "写回", "写直达", "命中率", "局部性", "SRAM", "DRAM", "存储芯片", "虚拟存储", "TLB")),
    Chapter("计算机组成原理", "第4章", "指令系统、寻址方式、机器级程序", ("指令", "寻址", "操作码", "地址码", "CISC", "RISC", "立即寻址", "间接寻址", "偏移", "机器指令", "汇编")),
    Chapter("计算机组成原理", "第5章", "CPU、数据通路、控制器、流水线、中断异常", ("CPU", "数据通路", "控制信号", "控制器", "微程序", "硬布线", "流水线", "冒险", "阻塞", "转发", "PC", "IR", "MAR", "MDR", "寄存器", "异常", "中断")),
    Chapter("计算机组成原理", "第6章", "总线", ("总线", "仲裁", "同步总线", "异步总线", "带宽", "突发传送", "总线周期")),
    Chapter("计算机组成原理", "第7章", "输入输出系统、DMA、中断、接口", ("I/O", "输入输出", "接口", "程序查询", "中断方式", "DMA", "中断响应", "中断周期", "设备", "磁盘")),
]


def year_of(path: Path) -> str:
    m = re.search(r"(20\d{2})", path.name)
    return m.group(1) if m else "合集"


def kind_of(path: Path) -> str:
    name = path.name
    if "解析" in name or "答案" in name:
        return "解析/答案"
    if "王道" in name or "历年真题" in name:
        return "合集"
    return "真题"


def extract_text(path: Path, max_pages: int | None = None) -> str:
    parts: list[str] = []
    with fitz.open(path) as doc:
        n = len(doc) if max_pages is None else min(max_pages, len(doc))
        for i in range(n):
            try:
                parts.append(doc[i].get_text("text"))
            except Exception:
                continue
    return "\n".join(parts)


def count_hits(text: str, keywords: tuple[str, ...]) -> int:
    total = 0
    for kw in keywords:
        total += text.count(kw)
    return total


def main() -> None:
    pdfs = []
    for src in SOURCES:
        pdfs.extend(sorted(src.glob("*.pdf")))

    rows = []
    yearly = defaultdict(Counter)
    doc_quality = []

    for pdf in pdfs:
        text = extract_text(pdf)
        clean_len = len(re.sub(r"\s+", "", text))
        cjk_len = len(re.findall(r"[\u4e00-\u9fff]", text))
        doc_quality.append((pdf.name, year_of(pdf), kind_of(pdf), len(text), clean_len, cjk_len))
        for chapter in CHAPTERS:
            hits = count_hits(text, chapter.keywords)
            if hits:
                rows.append({
                    "file": pdf.name,
                    "year": year_of(pdf),
                    "kind": kind_of(pdf),
                    "subject": chapter.subject,
                    "chapter": chapter.chapter,
                    "title": chapter.title,
                    "hits": hits,
                })
                # Avoid letting one large Wangdao collection dominate yearly trend.
                if kind_of(pdf) != "合集":
                    yearly[(chapter.subject, chapter.chapter, chapter.title)][year_of(pdf)] += hits

    ROOT.mkdir(parents=True, exist_ok=True)
    with (ROOT / "408_os_co_keyword_hits.csv").open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["file", "year", "kind", "subject", "chapter", "title", "hits"])
        writer.writeheader()
        writer.writerows(rows)

    with (ROOT / "408_pdf_text_quality.csv").open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["file", "year", "kind", "raw_text_len", "non_space_len", "cjk_chars"])
        writer.writerows(doc_quality)

    print(f"PDF files: {len(pdfs)}")
    print("Top keyword chapter hits, excluding the Wangdao collection as a single over-weighted document:")
    totals = Counter()
    years_seen = defaultdict(set)
    for row in rows:
        if row["kind"] == "合集":
            continue
        key = (row["subject"], row["chapter"], row["title"])
        totals[key] += int(row["hits"])
        if int(row["hits"]) >= 3:
            years_seen[key].add(row["year"])
    for (subject, chapter, title), hits in totals.most_common():
        print(f"{subject} {chapter} {title}: hits={hits}, years_with_signal={len(years_seen[(subject, chapter, title)])}")


if __name__ == "__main__":
    main()
