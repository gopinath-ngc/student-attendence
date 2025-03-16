import pandas as pd
import os
DATA_FILE = "student_attendance.csv"
if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE)
else:
    df = pd.DataFrame(columns=[
        'Roll No', 
        'Student Name', 
        'Month', 
        'Classes Present', 
        'Classes Absent', 
        'Working Days', 
        'Attendance Percentage'
    ]).astype({
        'Roll No': 'int64',
        'Classes Present': 'int64',
        'Classes Absent': 'int64',
        'Working Days': 'int64'
    })

def calculate_percentage(present, working_days):
    """Calculate the attendance percentage."""
    if working_days == 0:
        return 0.0
    return round((present / working_days) * 100, 2)

def validate_attendance(present, absent, working_days):
    """Validate attendance input values."""
    if present + absent > working_days:
        raise ValueError("Present + Absent days cannot exceed working days")
    if present < 0 or absent < 0:
        raise ValueError("Days cannot be negative")

def add_student():
    """Add a new student record."""
    global df  
    print("\nAdd New Student Record:")
    try:
        roll_no = int(input("Enter Roll Number: "))
        name = input("Enter Student Name: ").strip().title()
        month = input("Enter Month: ").strip().title()
        
        present = int(input("Enter classes present: "))
        absent = int(input("Enter classes absent: "))
        working_days = int(input("Enter working days: "))
        
        validate_attendance(present, absent, working_days)
        
        existing = df[(df['Roll No'] == roll_no) & (df['Month'] == month)]
        if not existing.empty:
            print("Record exists! Use the update feature instead.")
            return
        
        attendance_percentage = calculate_percentage(present, working_days)
        
        new_record = {
            'Roll No': roll_no,
            'Student Name': name,
            'Month': month,
            'Classes Present': present,
            'Classes Absent': absent,
            'Working Days': working_days,
            'Attendance Percentage': attendance_percentage
        }
        
        df = pd.concat([df, pd.DataFrame([new_record])], ignore_index=True)
        df.to_csv(DATA_FILE, index=False)
        print("Record added successfully!")
        
    except ValueError as e:
        print(f"Error: {e}")

def update_attendance():
    """Update attendance for an existing student."""
    global df  
    print("\nUpdate Attendance:")
    try:
        roll_no = int(input("Enter Roll Number: "))
        month = input("Enter Month: ").title()
        
        record = df[(df['Roll No'] == roll_no) & (df['Month'] == month)]
        if record.empty:
            print("No record found!")
            return
            
        idx = record.index[0]
        working_days = df.at[idx, 'Working Days']
        
        print(f"\nCurrent Attendance (Working Days: {working_days})")
        print(f"Present: {df.at[idx, 'Classes Present']}")
        print(f"Absent: {df.at[idx, 'Classes Absent']}")
        
        choice = input("\nUpdate:\n1. Add Present\n2. Add Absent\nChoice: ")
        days = int(input("Days to add: "))
        
        if days < 0:
            raise ValueError("Negative days not allowed")
            
        if choice == '1':
            new_present = df.at[idx, 'Classes Present'] + days
            new_absent = df.at[idx, 'Classes Absent']
        elif choice == '2':
            new_absent = df.at[idx, 'Classes Absent'] + days
            new_present = df.at[idx, 'Classes Present']
        else:
            print("Invalid choice!")
            return
            
        validate_attendance(new_present, new_absent, working_days)
        
        df.at[idx, 'Classes Present'] = new_present
        df.at[idx, 'Classes Absent'] = new_absent
        df.at[idx, 'Attendance Percentage'] = calculate_percentage(new_present, working_days)
        
        df.to_csv(DATA_FILE, index=False)
        print("Attendance updated successfully!")
        
    except ValueError as e:
        print(f"Error: {e}")

def generate_report():
    """Generate attendance reports."""
    global df 
    print("\nAttendance Report:")
    if df.empty:
        print("No records available!")
        return
        
    choice = input("1. Full Report\n2. Individual Report\nChoice: ")
    
    if choice == '1':
        print(df.to_string(index=False))
    elif choice == '2':
        try:
            roll_no = int(input("Enter Roll Number: "))
            student_df = df[df['Roll No'] == roll_no]
            if student_df.empty:
                print("No records found for this Roll Number!")
                return
            print(student_df.to_string(index=False))
        except ValueError:
            print("Invalid Roll Number!")
    else:
        print("Invalid choice!")

def main_menu():
    """Display the main menu and handle user choices."""
    while True:
        print("\nStudent Attendance System")
        print("1. Add Record")
        print("2. Update Attendance")
        print("3. Generate Report")
        print("4. Exit")
        
        choice = input("Choose an option: ")
        
        if choice == '1':
            add_student()
        elif choice == '2':
            update_attendance()
        elif choice == '3':
            generate_report()
        elif choice == '4':
            print("Exiting the system... Goodbye!")
            break
        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main_menu()