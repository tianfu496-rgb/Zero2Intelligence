# -*- coding: utf-8 -*-
"""
基金数据抓取脚本
=================
功能:
    1. 抓取基金基本信息(名称/类型/公司/经理/成立日期/规模等)
    2. 抓取基金历史净值(单位净值 + 累计净值 + 日增长率)
    3. 抓取基金季度持仓(重仓股)
    4. 将以上数据存储到本地 SQLite 数据库

数据来源: akshare (封装了天天基金/雪球等公开接口)
存储方式: SQLite (单文件数据库 fund_data.db)

使用前提:
    pip install -r requirements.txt
    (akshare 内部会请求 fund.eastmoney.com / xueqiu.com 等站点,
     请确保运行环境可以正常访问外网)
"""

import sqlite3
import time
import logging
from datetime import datetime
from pathlib import Path

import akshare as ak
import pandas as pd

# ============ 配置区 ============

DB_PATH = "fund_data.db"

# 采集完成后的 Excel 文件和图表均存放在脚本同目录的 output 文件夹中。
OUTPUT_DIR = Path(__file__).resolve().parent / "output"
EXCEL_FILE_NAME = "fund_data.xlsx"

# 测试用的 10 只基金代码(可自行替换成你关心的基金)
TEST_FUND_CODES = [
    "000001",  # 华夏成长混合
    "110022",  # 易方达消费行业股票
    "161725",  # 招商中证白酒指数(LOF)A
    "005827",  # 易方达蓝筹精选混合
    "003095",  # 中欧医疗健康混合A
    "519674",  # 银河创新成长混合
    "163406",  # 兴全合润混合(LOF)
    "270042",  # 广发纳斯达克100指数(QDII)
    "001631",  # 天弘中证银行指数A
    "000961",  # 天弘沪深300ETF联接A
]

# 每次请求之间的间隔秒数,避免抓取过快被限流/封IP
SLEEP_SECONDS = 1.5

# 每个接口的最大重试次数
MAX_RETRIES = 3
RETRY_DELAY = 3

# ============ 日志配置 ============

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("fund_scraper.log", encoding="utf-8"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)


# ============ 数据库初始化 ============

def init_db(db_path: str = DB_PATH) -> sqlite3.Connection:
    """创建数据库和数据表(若已存在则跳过)"""
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS fund_info (
            code            TEXT PRIMARY KEY,
            name            TEXT,
            fund_type       TEXT,
            company         TEXT,
            manager         TEXT,
            establish_date  TEXT,
            scale           TEXT,
            update_time     TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS fund_nav (
            code                TEXT,
            nav_date            TEXT,
            unit_nav            REAL,
            accum_nav           REAL,
            daily_growth_rate   REAL,
            PRIMARY KEY (code, nav_date)
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS fund_holdings (
            code            TEXT,
            report_period   TEXT,
            stock_code      TEXT,
            stock_name      TEXT,
            ratio           REAL,
            PRIMARY KEY (code, report_period, stock_code)
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS fund_manager (
            code            TEXT,
            manager_name    TEXT,
            PRIMARY KEY (code, manager_name)
        )
    """)

    conn.commit()
    logger.info("数据库初始化完成: %s", db_path)
    return conn


# ============ 带重试的请求封装 ============

def retry_call(func, *args, **kwargs):
    """对 akshare 接口调用做简单重试,应对偶发的网络/接口波动"""
    last_err = None
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            return func(*args, **kwargs)
        except Exception as e:  # noqa: BLE001
            last_err = e
            logger.warning(
                "调用 %s 第 %d/%d 次失败: %s",
                getattr(func, "__name__", str(func)),
                attempt,
                MAX_RETRIES,
                e,
            )
            if attempt < MAX_RETRIES:
                time.sleep(RETRY_DELAY)
    raise last_err


# ============ 各类数据抓取函数 ============

def fetch_basic_info(code: str) -> dict:
    """抓取基金基本信息(雪球接口): 名称/类型/公司/经理/成立日期/规模"""
    df = retry_call(ak.fund_individual_basic_info_xq, symbol=code)
    if df is None or df.empty:
        return {}
    # 接口返回两列: item / value,转成字典方便取值
    df.columns = ["item", "value"]
    info = dict(zip(df["item"], df["value"]))
    return info


def fetch_nav_history(code: str) -> pd.DataFrame:
    """抓取历史净值: 单位净值 + 累计净值 + 日增长率"""
    unit_df = retry_call(
        ak.fund_open_fund_info_em, symbol=code, indicator="单位净值走势"
    )
    time.sleep(SLEEP_SECONDS)
    accum_df = retry_call(
        ak.fund_open_fund_info_em, symbol=code, indicator="累计净值走势"
    )

    if unit_df is None or unit_df.empty:
        return pd.DataFrame()

    unit_df = unit_df.rename(columns={"日增长率": "日增长率"})
    if accum_df is not None and not accum_df.empty:
        merged = pd.merge(unit_df, accum_df, on="净值日期", how="left")
    else:
        merged = unit_df.copy()
        merged["累计净值"] = None

    return merged


def fetch_holdings(code: str) -> pd.DataFrame:
    """抓取季度持仓(重仓股),优先取今年,取不到则回退去年"""
    this_year = datetime.now().year
    df = retry_call(ak.fund_portfolio_hold_em, symbol=code, date=str(this_year))
    if df is None or df.empty:
        time.sleep(SLEEP_SECONDS)
        df = retry_call(
            ak.fund_portfolio_hold_em, symbol=code, date=str(this_year - 1)
        )
    return df if df is not None else pd.DataFrame()


# ============ 存储函数 ============

def save_basic_info(conn: sqlite3.Connection, code: str, info: dict):
    if not info:
        logger.warning("[%s] 未获取到基本信息,跳过存储", code)
        return

    name = info.get("基金简称") or info.get("基金全称")
    fund_type = info.get("基金类型")
    company = info.get("基金公司")
    manager = info.get("基金经理")
    establish_date = info.get("成立时间") or info.get("成立日期")
    scale = info.get("最新规模") or info.get("资产规模")

    conn.execute(
        """
        INSERT OR REPLACE INTO fund_info
        (code, name, fund_type, company, manager, establish_date, scale, update_time)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            code, name, fund_type, company, manager, establish_date, scale,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        ),
    )

    if manager:
        for name_part in str(manager).replace("等", "").split(","):
            name_part = name_part.strip()
            if name_part:
                conn.execute(
                    "INSERT OR IGNORE INTO fund_manager (code, manager_name) VALUES (?, ?)",
                    (code, name_part),
                )

    conn.commit()
    logger.info("[%s] 基本信息已存储: %s", code, name)


def save_nav_history(conn: sqlite3.Connection, code: str, df: pd.DataFrame):
    if df is None or df.empty:
        logger.warning("[%s] 未获取到净值数据,跳过存储", code)
        return

    rows = []
    for _, r in df.iterrows():
        rows.append((
            code,
            str(r.get("净值日期")),
            r.get("单位净值"),
            r.get("累计净值"),
            r.get("日增长率"),
        ))

    conn.executemany(
        """
        INSERT OR REPLACE INTO fund_nav
        (code, nav_date, unit_nav, accum_nav, daily_growth_rate)
        VALUES (?, ?, ?, ?, ?)
        """,
        rows,
    )
    conn.commit()
    logger.info("[%s] 净值数据已存储,共 %d 条", code, len(rows))


def save_holdings(conn: sqlite3.Connection, code: str, df: pd.DataFrame):
    if df is None or df.empty:
        logger.warning("[%s] 未获取到持仓数据,跳过存储", code)
        return

    rows = []
    for _, r in df.iterrows():
        report_period = r.get("季度") or r.get("报告期") or ""
        rows.append((
            code,
            str(report_period),
            str(r.get("股票代码", "")),
            r.get("股票名称"),
            r.get("占净值比例"),
        ))

    conn.executemany(
        """
        INSERT OR REPLACE INTO fund_holdings
        (code, report_period, stock_code, stock_name, ratio)
        VALUES (?, ?, ?, ?, ?)
        """,
        rows,
    )
    conn.commit()
    logger.info("[%s] 持仓数据已存储,共 %d 条", code, len(rows))


# ============ 数据导出与可视化 ============

def export_to_excel(conn: sqlite3.Connection, output_path: Path):
    """将 SQLite 中的全部基金数据导出到一个 Excel 工作簿。"""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    tables = {
        "基金信息": "SELECT * FROM fund_info ORDER BY code",
        "历史净值": "SELECT * FROM fund_nav ORDER BY code, nav_date",
        "季度持仓": "SELECT * FROM fund_holdings ORDER BY code, report_period, ratio DESC",
        "基金经理": "SELECT * FROM fund_manager ORDER BY code, manager_name",
    }

    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        for sheet_name, sql in tables.items():
            df = pd.read_sql_query(sql, conn)
            df.to_excel(writer, sheet_name=sheet_name, index=False)

            worksheet = writer.sheets[sheet_name]
            worksheet.freeze_panes = "A2"
            worksheet.auto_filter.ref = worksheet.dimensions

            # 依据内容调整列宽，保证导出的文件打开后较易阅读。
            for index, column in enumerate(df.columns, start=1):
                max_length = max(
                    len(str(column)),
                    *(len(str(value)) for value in df[column].fillna("")),
                )
                worksheet.column_dimensions[
                    worksheet.cell(row=1, column=index).column_letter
                ].width = min(max_length + 2, 36)

    logger.info("Excel 数据已导出: %s", output_path)


def create_visualizations(conn: sqlite3.Connection, output_dir: Path):
    """为每只基金生成历史净值折线图和最新季度持仓柱状图。"""
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        logger.warning("未安装 matplotlib，已跳过图表生成。请执行 pip install matplotlib")
        return

    chart_dir = output_dir / "charts"
    chart_dir.mkdir(parents=True, exist_ok=True)
    plt.rcParams["font.sans-serif"] = [
        "Microsoft YaHei", "SimHei", "Arial Unicode MS", "DejaVu Sans"
    ]
    plt.rcParams["axes.unicode_minus"] = False

    funds = pd.read_sql_query("SELECT code, name FROM fund_info ORDER BY code", conn)
    chart_count = 0
    for _, fund in funds.iterrows():
        code = fund["code"]
        name = fund["name"] if pd.notna(fund["name"]) else code

        nav_df = pd.read_sql_query(
            """
            SELECT nav_date, unit_nav, accum_nav
            FROM fund_nav WHERE code = ? ORDER BY nav_date
            """,
            conn,
            params=(code,),
        )
        nav_df["nav_date"] = pd.to_datetime(nav_df["nav_date"], errors="coerce")
        nav_df["unit_nav"] = pd.to_numeric(nav_df["unit_nav"], errors="coerce")
        nav_df["accum_nav"] = pd.to_numeric(nav_df["accum_nav"], errors="coerce")
        nav_df = nav_df.dropna(subset=["nav_date"]).sort_values("nav_date")

        if not nav_df.empty and nav_df[["unit_nav", "accum_nav"]].notna().any().any():
            fig, ax = plt.subplots(figsize=(11, 5))
            ax.plot(nav_df["nav_date"], nav_df["unit_nav"], label="单位净值", linewidth=1.2)
            ax.plot(nav_df["nav_date"], nav_df["accum_nav"], label="累计净值", linewidth=1.2)
            ax.set_title(f"{code} {name} - 历史净值走势")
            ax.set_xlabel("日期")
            ax.set_ylabel("净值")
            ax.grid(alpha=0.25)
            ax.legend()
            fig.autofmt_xdate()
            fig.tight_layout()
            fig.savefig(chart_dir / f"{code}_nav.png", dpi=160)
            plt.close(fig)
            chart_count += 1

        holdings_df = pd.read_sql_query(
            """
            SELECT report_period, stock_code, stock_name, ratio
            FROM fund_holdings WHERE code = ? ORDER BY report_period DESC
            """,
            conn,
            params=(code,),
        )
        if holdings_df.empty:
            continue

        latest_period = holdings_df["report_period"].iloc[0]
        holdings_df = holdings_df[holdings_df["report_period"] == latest_period].copy()
        holdings_df["ratio"] = pd.to_numeric(holdings_df["ratio"], errors="coerce")
        holdings_df = holdings_df.dropna(subset=["ratio"]).nlargest(10, "ratio")

        if not holdings_df.empty:
            labels = holdings_df["stock_name"].fillna(holdings_df["stock_code"])
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.barh(labels, holdings_df["ratio"])
            ax.invert_yaxis()
            ax.set_title(f"{code} {name} - {latest_period} 前十持仓")
            ax.set_xlabel("占净值比例")
            ax.set_ylabel("股票")
            ax.grid(axis="x", alpha=0.25)
            fig.tight_layout()
            fig.savefig(chart_dir / f"{code}_holdings.png", dpi=160)
            plt.close(fig)
            chart_count += 1

    logger.info("图表生成完成: %s（共 %d 张）", chart_dir, chart_count)


# ============ 主流程 ============

def run(fund_codes=None, db_path: str = DB_PATH, output_dir: Path = OUTPUT_DIR):
    fund_codes = fund_codes or TEST_FUND_CODES
    conn = init_db(db_path)

    for i, code in enumerate(fund_codes, 1):
        logger.info("===== [%d/%d] 开始处理基金 %s =====", i, len(fund_codes), code)
        try:
            info = fetch_basic_info(code)
            save_basic_info(conn, code, info)
            time.sleep(SLEEP_SECONDS)

            nav_df = fetch_nav_history(code)
            save_nav_history(conn, code, nav_df)
            time.sleep(SLEEP_SECONDS)

            holdings_df = fetch_holdings(code)
            save_holdings(conn, code, holdings_df)
            time.sleep(SLEEP_SECONDS)

        except Exception as e:  # noqa: BLE001
            logger.error("[%s] 处理失败,已跳过: %s", code, e)
            continue

    output_dir = Path(output_dir)
    try:
        export_to_excel(conn, output_dir / EXCEL_FILE_NAME)
        create_visualizations(conn, output_dir)
    except Exception as e:  # noqa: BLE001
        logger.exception("导出 Excel 或生成图表失败: %s", e)

    conn.close()
    logger.info("全部基金处理完成,数据库文件: %s，输出目录: %s", db_path, output_dir)


if __name__ == "__main__":
    run()
