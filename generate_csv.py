import re
import csv
from pypdf import PdfReader

pdf_path = 'ATTENDANCE 290926.pdf'
csv_path = 'attendance.csv'

reader = PdfReader(pdf_path)
pattern = re.compile(r'^(\d+)\s+(RA\d+)\s+(.+?)\s+(MBG24[A-Z0-9]{4})\s+(.+?)\s*(\d+(?:\.\d+)?)$')

records = []
for page in reader.pages:
    lines = page.extract_text().split('\n')
    for line in lines:
        line = line.strip()
        if not line or 'CONSOLIDATED' in line or 'Course Title' in line:
            continue
        m = pattern.match(line)
        if m:
            sno, reg, name, code, title, pct_str = m.groups()
            pct_val = float(pct_str)
            status = "Shortage" if pct_val < 75.0 else "Eligible"
            records.append({
                'S.No': int(sno),
                'Register_No': reg.strip(),
                'Student_Name': name.strip(),
                'Course_Code': code.strip(),
                'Course_Title': title.strip(),
                'Attendance_Percentage': f"{pct_val:.2f}",
                'Status': status
            })
        else:
            raise ValueError(f"Unmatched line: {line}")

print(f"Total records processed: {len(records)}")

fieldnames = ['S.No', 'Register_No', 'Student_Name', 'Course_Code', 'Course_Title', 'Attendance_Percentage', 'Status']

with open(csv_path, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(records)

print(f"Successfully generated {csv_path}")
