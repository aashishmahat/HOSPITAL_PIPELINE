import matplotlib.pyplot as plt
from pathlib import Path

GRAPH_DIR = Path("report/graph")


def save(fig, name):
    GRAPH_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(GRAPH_DIR / f"{name}.png", bbox_inches="tight")
    plt.close(fig)


# ── Patients ──────────────────────────────────────────────────────────────────
def plot_patients(df):
    # Gender
    fig, ax = plt.subplots()
    df["gender"].value_counts().plot(kind="bar", ax=ax, color="steelblue")
    ax.set_title("Patients by Gender")
    ax.set_xlabel("Gender")
    ax.set_ylabel("Count")
    save(fig, "patients_gender")

    # Age distribution
    fig, ax = plt.subplots()
    df["age"].dropna().plot(kind="hist", ax=ax, bins=20, color="steelblue", edgecolor="white")
    ax.set_title("Patient Age Distribution")
    ax.set_xlabel("Age")
    save(fig, "patients_age")

    # Blood group
    fig, ax = plt.subplots()
    df["blood_group"].value_counts().plot(kind="bar", ax=ax, color="steelblue")
    ax.set_title("Patients by Blood Group")
    ax.set_xlabel("Blood Group")
    ax.set_ylabel("Count")
    save(fig, "patients_blood_group")


# ── Appointments ──────────────────────────────────────────────────────────────
def plot_appointments(df):
    # Status
    fig, ax = plt.subplots()
    df["status"].value_counts().plot(kind="pie", ax=ax, autopct="%1.1f%%")
    ax.set_title("Appointment Status")
    ax.set_ylabel("")
    save(fig, "appointments_status")

    # Top departments
    fig, ax = plt.subplots()
    df["department_name"].value_counts().head(5).plot(kind="barh", ax=ax, color="steelblue")
    ax.set_title("Top 5 Departments by Appointments")
    ax.set_xlabel("Count")
    save(fig, "appointments_top_departments")


# ── Billing ───────────────────────────────────────────────────────────────────
def plot_billing(df):
    # Payment mode
    fig, ax = plt.subplots()
    df["payment_mode"].value_counts().plot(kind="bar", ax=ax, color="steelblue")
    ax.set_title("Billing by Payment Mode")
    ax.set_xlabel("Payment Mode")
    ax.set_ylabel("Count")
    save(fig, "billing_payment_mode")

    # Payment status
    fig, ax = plt.subplots()
    df["payment_status"].value_counts().plot(kind="pie", ax=ax, autopct="%1.1f%%")
    ax.set_title("Payment Status")
    ax.set_ylabel("")
    save(fig, "billing_payment_status")


# ── Lab Tests ─────────────────────────────────────────────────────────────────
def plot_labTests(df):
    # Status
    fig, ax = plt.subplots()
    df["status"].value_counts().plot(kind="pie", ax=ax, autopct="%1.1f%%")
    ax.set_title("Lab Test Status")
    ax.set_ylabel("")
    save(fig, "lab_status")

    # Top tests
    if "test_name" in df.columns:
        fig, ax = plt.subplots()
        df["test_name"].value_counts().head(5).plot(kind="barh", ax=ax, color="steelblue")
        ax.set_title("Top 5 Lab Tests")
        ax.set_xlabel("Count")
        save(fig, "lab_top_tests")


# ── Main entry point ──────────────────────────────────────────────────────────
def generate_graphs(cleaned):
    plot_patients(cleaned["patients"])
    plot_appointments(cleaned["appointments"])
    plot_billing(cleaned["billing"])
    plot_labTests(cleaned["labTests"])
    print(f"Graphs saved to {GRAPH_DIR}/")