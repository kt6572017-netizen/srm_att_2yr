# 🎓 MBA 2nd Year 3rd Sem — Attendance Analytics & Recovery Dashboard

An interactive, high-performance web dashboard built with **Streamlit**, **Pandas**, and **Plotly** for monitoring, analyzing, and calculating student attendance records for the **MBA 2nd Year 3rd Semester (Batch 2024–2026)** at SRM.

---

## 📌 Table of Contents
1. [Overview](#overview)
2. [Key Features](#key-features)
3. [Project File Structure](#project-file-structure)
4. [Step-by-Step Setup Guide](#step-by-step-setup-guide)
5. [Attendance Calculation Formulas](#attendance-calculation-formulas)
6. [Academic Regulations](#academic-regulations)

---

## 🌟 Overview
This project extracts raw academic attendance data from official institutional PDFs (`ATTENDANCE 290926.pdf`), transforms it into structured tabular records (`attendance.csv`), and serves an executive-grade dashboard that tracks student eligibility against university attendance benchmarks.

---

## ✨ Key Features

### 1. Executive Dashboard (HR / People Layout)
- **Statistics Donut Chart**: Visual ratio of students who are Eligible ($\ge 75\%$), Defaulters ($< 75\%$), and 100% Achievers, with a centered cohort readout and floating percentage badge.
- **6 Micro-KPI Cards**:
  - 🔵 **Checked In**: Total subject registrations meeting the $\ge 75\%$ threshold.
  - 🔴 **Not Checked In**: Defaulter subject count requiring regularization.
  - 🟢 **100% Achievers**: Perfect attendance records.
  - 🟣 **Total Courses**: Active courses (12 subjects across core and electives).
  - 🟡 **Defaulter Cases**: Count of unique students with at least one shortage course.
  - 🟠 **Total Students**: Total cohort size (29 students).
- **On-Time Check In (Diverging Bar Chart)**: Compares average class attendance against the 75% benchmark with peak subject callouts.
- **Overtime / Conducted Hours**: Bar breakdown of conducted academic sessions and lab practicals.
- **Attendance Sources (2×2 Grid)**: Device Check-Ins, App Check-Ins, Active Devices, and Inactive Devices.
- **Exceptions & Pending Requests**: Automated grouping of critical shortages ($< 50\%$) and borderline warnings ($50\% - 74\%$).

### 2. Interactive Consecutive Class Recovery Calculator
- Select any student and course to compute:
  - Exact number of **upcoming consecutive classes** they must attend without missing to reach the target eligibility percentage (e.g., 75%).
  - Safe miss buffer (how many classes can be skipped while maintaining eligibility).
  - Visual trajectory curve projecting percentage improvements per upcoming class.

### 3. Master Reports & Defaulter Registry
- Search and filter by **Student Name / Register Number** and **Course Title / Code**.
- Interactive dynamic threshold slider ($50\% - 95\%$).
- 1-Click **Download Defaulter Report (CSV)** for academic audit and notification notices.

---

## 📂 Project File Structure

```text
srm attandence/
│
├── app.py                                # Main Streamlit dashboard application
├── attendance.csv                        # Cleaned structured attendance dataset (174 records)
├── ATTENDANCE 290926.pdf                 # Original institutional attendance document
├── requirements.txt                      # Python dependencies list
├── README.md                             # Comprehensive project documentation
└── MBA_2nd_Year_Attendance_Dashboard.zip # Ready-to-share compressed archive
```

---

## 🚀 Step-by-Step Setup Guide

### Prerequisites
- Python 3.9 or higher installed on your computer.
- [Download Python](https://www.python.org/downloads/) (Make sure to check *"Add Python to PATH"* during installation).

### Step 1: Open Terminal / Command Prompt
Open your terminal (PowerShell, Command Prompt, or Terminal) and navigate to the project directory:
```bash
cd "C:\Users\Riya\OneDrive\Desktop\New folder\srm attandence"
```

### Step 2: Install Required Libraries
Run the following command to install dependencies:
```bash
pip install -r requirements.txt
```

*(Alternatively install directly: `pip install streamlit pandas numpy plotly`)*

### Step 3: Launch the Application
Run the Streamlit app:
```bash
streamlit run app.py
```

### Step 4: Open in Your Browser
The app will automatically open. If not, open your browser and navigate to:
```text
http://localhost:8501
```

---

## 📐 Attendance Calculation Formulas

Let:
- $T$ = Total classes conducted so far
- $A$ = Classes attended so far
- $P_{\text{target}}$ = Target threshold (e.g., $75\% = 0.75$)

### 1. Consecutive Classes Needed to Reach Target:
If current percentage $< P_{\text{target}}$, the number of consecutive upcoming classes $x$ required is:
$$x = \left\lceil \frac{P_{\text{target}} \cdot T - A}{1 - P_{\text{target}}} \right\rceil$$

For a 75% target ($P_{\text{target}} = 0.75$):
$$x = \left\lceil \frac{0.75 T - A}{0.25} \right\rceil = \lceil 3T - 4A \rceil$$

### 2. Safe Miss Buffer (Safe Bunks):
If current percentage $\ge P_{\text{target}}$, the number of classes $m$ that can be safely missed:
$$m = \left\lfloor \frac{A}{P_{\text{target}}} - T \right\rfloor$$

For a 75% target:
$$m = \left\lfloor \frac{4A - 3T}{3} \right\rfloor$$

---

## ⚖️ Academic Regulations
- **University Criteria**: A minimum of **75% attendance** in each individual course is mandatory to appear for the End-Semester Examinations.
- **Condonation Range (65% – 74%)**: Permitted only under approved medical or official duty leaves.
- **Critical Shortage (< 65%)**: Mandatory course repetition / detention in the subject.

---

## 👤 Author & Support
- **Project**: MBA 2nd Year 3rd Sem Attendance Portal
- **Institution**: SRM Institute of Science and Technology
- **Batch**: 2024 – 2026
