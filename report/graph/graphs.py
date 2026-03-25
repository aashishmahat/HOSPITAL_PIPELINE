import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import pandas as pd
import seaborn as sns
from pathlib import Path

GRAPH_DIR = Path("report/graph")

COLORS = [
    "#2E86AB", "#A23B72", "#F18F01", "#C73E1D", "#44BBA4",
    "#E94F37", "#7B2D8B", "#F5A623", "#393E41", "#1B998B",
]

sns.set_theme(style="whitegrid", palette=COLORS)


def save(fig, name):
    GRAPH_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(GRAPH_DIR / f"{name}.png", bbox_inches="tight", dpi=120)
    plt.close(fig)



def plot_patients(df):

    # BAR — Gender
    fig, ax = plt.subplots()
    df["gender"].value_counts().plot(kind="bar", ax=ax, color=COLORS[:3], edgecolor="white")
    ax.set_title("Patients by Gender")
    ax.set_xlabel("Gender")
    ax.set_ylabel("Count")
    ax.tick_params(axis="x", rotation=0)
    ax.spines[["top", "right"]].set_visible(False)
    save(fig, "patients_gender_bar")

    #  HISTOGRAM — Age distribution
    fig, ax = plt.subplots(figsize=(9, 5))
    ages = df["age"].dropna()
    ax.hist(ages, bins=20, color=COLORS[0], edgecolor="white", alpha=0.85)
    ax.axvline(ages.mean(), color="red", linestyle="--", linewidth=1.8,
               label=f"Avg: {ages.mean():.1f} yrs")
    ax.set_title("Patient Age Distribution")
    ax.set_xlabel("Age")
    ax.set_ylabel("Count")
    ax.legend()
    ax.spines[["top", "right"]].set_visible(False)
    save(fig, "patients_age_histogram")


    # BAR — Blood group
    fig, ax = plt.subplots()
    df["blood_group"].value_counts().plot(kind="bar", ax=ax, color=COLORS[1], edgecolor="white")
    ax.set_title("Patients by Blood Group")
    ax.set_xlabel("Blood Group")
    ax.set_ylabel("Count")
    ax.tick_params(axis="x", rotation=0)
    ax.spines[["top", "right"]].set_visible(False)
    save(fig, "patients_blood_group_bar")

    # BOXPLOT — Age by gender
    if "gender" in df.columns:
        fig, ax = plt.subplots(figsize=(7, 5))
        genders = df["gender"].unique()
        groups  = [pd.to_numeric(df[df["gender"] == g]["age"], errors="coerce").dropna().values
                   for g in genders]
        bp = ax.boxplot(groups, labels=genders, patch_artist=True,
                        medianprops={"color": "white", "linewidth": 2})
        for patch, color in zip(bp["boxes"], COLORS):
            patch.set_facecolor(color)
            patch.set_alpha(0.8)
        ax.set_ylabel("Age (years)")
        ax.set_title("Age Distribution by Gender — Boxplot")
        ax.spines[["top", "right"]].set_visible(False)
        save(fig, "patients_age_gender_boxplot")




def plot_appointments(df):

    #  PIE — Status
    fig, ax = plt.subplots()
    df["status"].value_counts().plot(kind="pie", ax=ax, autopct="%1.1f%%",
                                     colors=COLORS[:df["status"].nunique()])
    ax.set_title("Appointment Status")
    ax.set_ylabel("")
    save(fig, "appointments_status_pie")

    #  HORIZONTAL BAR — Top departments
    fig, ax = plt.subplots()
    df["department_name"].value_counts().head(5).plot(kind="barh", ax=ax, color=COLORS[0])
    ax.set_title("Top 5 Departments by Appointments")
    ax.set_xlabel("Count")
    ax.spines[["top", "right"]].set_visible(False)
    save(fig, "appointments_top_departments_hbar")

    # LINE — Monthly appointment trend
    date_col = next((c for c in ["appointment_date", "date", "created_at"]
                     if c in df.columns), None)
    if date_col:
        df2 = df.copy()
        df2["month"] = pd.to_datetime(df2[date_col], errors="coerce").dt.to_period("M")
        monthly = df2.groupby("month").size().reset_index(name="count")
        monthly["month_str"] = monthly["month"].astype(str)
        fig, ax = plt.subplots(figsize=(12, 5))
        ax.plot(monthly["month_str"], monthly["count"],
                marker="o", color=COLORS[0], linewidth=2.2, markersize=6)
        ax.fill_between(monthly["month_str"], monthly["count"],
                        alpha=0.15, color=COLORS[0])
        ax.set_title("Monthly Appointment Trend — Line")
        ax.set_xlabel("Month")
        ax.set_ylabel("Appointments")
        plt.xticks(rotation=45, ha="right")
        ax.spines[["top", "right"]].set_visible(False)
        ax.grid(axis="y", alpha=0.3)
        save(fig, "appointments_monthly_line")


    # HEATMAP — Appointments per department × weekday
    if date_col and "department_name" in df.columns:
        df2 = df.copy()
        df2["weekday"] = pd.to_datetime(df2[date_col], errors="coerce").dt.day_name()
        top_depts = df2["department_name"].value_counts().head(8).index
        df2 = df2[df2["department_name"].isin(top_depts)]
        day_order = ["Monday", "Tuesday", "Wednesday",
                     "Thursday", "Friday", "Saturday", "Sunday"]
        pivot = pd.crosstab(df2["department_name"], df2["weekday"])
        pivot = pivot[[d for d in day_order if d in pivot.columns]]
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.heatmap(pivot, annot=True, fmt="d", cmap="YlOrRd",
                    linewidths=0.4, ax=ax)
        ax.set_title("Appointments: Department × Weekday — Heatmap")
        plt.tight_layout()
        save(fig, "appointments_dept_weekday_heatmap")



def _rs_axis(x, _):
    if x >= 100_000: return f"Rs {x/100_000:.0f}L"
    if x >= 1_000:   return f"Rs {x/1_000:.0f}K"
    return f"Rs {x:.0f}"


def plot_billing(df):

    #  HISTOGRAM — Bill amount distribution
    if "total_amount" in df.columns:
        fig, ax = plt.subplots(figsize=(9, 5))
        amounts = pd.to_numeric(df["total_amount"], errors="coerce").dropna()
        ax.hist(amounts, bins=25, color=COLORS[2], edgecolor="white", alpha=0.85)
        ax.axvline(amounts.mean(), color="red", linestyle="--", linewidth=1.8,
                   label=f"Avg: Rs {amounts.mean():,.0f}")
        ax.xaxis.set_major_formatter(mticker.FuncFormatter(_rs_axis))
        ax.set_title("Bill Amount Distribution — Histogram")
        ax.set_xlabel("Total Bill Amount")
        ax.set_ylabel("Number of Bills")
        ax.legend()
        ax.spines[["top", "right"]].set_visible(False)
        save(fig, "billing_amount_histogram")

    # BOXPLOT — Bill amount by payment mode
    if "total_amount" in df.columns and "payment_mode" in df.columns:
        modes  = df["payment_mode"].unique()
        groups = [pd.to_numeric(df[df["payment_mode"] == m]["total_amount"],
                                errors="coerce").dropna().values for m in modes]
        fig, ax = plt.subplots(figsize=(9, 5))
        bp = ax.boxplot(groups, labels=modes, patch_artist=True,
                        medianprops={"color": "white", "linewidth": 2})
        for patch, color in zip(bp["boxes"], COLORS):
            patch.set_facecolor(color)
            patch.set_alpha(0.8)
        ax.yaxis.set_major_formatter(mticker.FuncFormatter(_rs_axis))
        ax.set_title("Bill Amount by Payment Mode — Boxplot")
        ax.set_ylabel("Amount (Rs)")
        ax.tick_params(axis="x", rotation=15)
        ax.spines[["top", "right"]].set_visible(False)
        save(fig, "billing_amount_mode_boxplot")

    # SCATTER — Discount vs Total amount
    if "discount" in df.columns and "total_amount" in df.columns:
        d = df[["discount", "total_amount"]].apply(
            pd.to_numeric, errors="coerce").dropna()
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.scatter(d["discount"], d["total_amount"],
                   alpha=0.4, color=COLORS[4], edgecolor="white", s=30)
        m, b = np.polyfit(d["discount"], d["total_amount"], 1)
        x_line = np.linspace(d["discount"].min(), d["discount"].max(), 200)
        ax.plot(x_line, m * x_line + b, color="red",
                linewidth=1.8, linestyle="--", label="Trend")
        ax.xaxis.set_major_formatter(mticker.FuncFormatter(_rs_axis))
        ax.yaxis.set_major_formatter(mticker.FuncFormatter(_rs_axis))
        ax.set_title("Discount vs Total Bill Amount — Scatter")
        ax.set_xlabel("Discount (Rs)")
        ax.set_ylabel("Total Amount (Rs)")
        ax.legend()
        ax.spines[["top", "right"]].set_visible(False)
        save(fig, "billing_discount_vs_total_scatter")

    #  WATERFALL — Revenue flow
    if "total_amount" in df.columns and "payment_status" in df.columns:
        total    = pd.to_numeric(df["total_amount"], errors="coerce").sum()
        paid     = pd.to_numeric(
            df[df["payment_status"].str.lower() == "paid"]["total_amount"],
            errors="coerce").sum()
        pending  = total - paid
        discount = pd.to_numeric(df.get("discount", pd.Series([0])),
                                 errors="coerce").sum()
        net      = paid - discount

        labels   = ["Total\nBilled", "Paid", "Pending\n(−)", "Discounts\n(−)", "Net\nCollected"]
        values   = [total, paid, -pending, -discount, net]
        wf_colors = [COLORS[0], COLORS[4], COLORS[3], COLORS[2], COLORS[1]]

        running, bottoms, heights = 0, [], []
        for v in values[:-1]:
            bottoms.append(min(running, running + v))
            heights.append(abs(v))
            running += v
        bottoms.append(0)
        heights.append(abs(net))

        fig, ax = plt.subplots(figsize=(10, 6))
        for i, (lbl, bot, ht, col) in enumerate(
                zip(labels, bottoms, heights, wf_colors)):
            ax.bar(lbl, ht, bottom=bot, color=col, edgecolor="white",
                   width=0.55, alpha=0.88)
            ax.text(i, bot + ht + total * 0.005,
                    f"Rs {abs(values[i])/100_000:.1f}L",
                    ha="center", fontsize=9)
        ax.yaxis.set_major_formatter(mticker.FuncFormatter(_rs_axis))
        ax.set_title("Revenue Waterfall: Billed → Net Collected")
        ax.set_ylabel("Amount (Rs)")
        ax.spines[["top", "right"]].set_visible(False)
        save(fig, "billing_revenue_waterfall")



def generate_graphs(cleaned):
    plot_patients(cleaned["patients"])
    plot_appointments(cleaned["appointments"])
    plot_billing(cleaned["billing"])
    print(f"Graphs saved to {GRAPH_DIR}/")