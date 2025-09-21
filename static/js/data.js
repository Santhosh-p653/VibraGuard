// static/js/data.js

let attendanceData = [];

export function generateAttendanceRecord() {
    const studentNames = ["Aarav Sharma", "Kiara Singh", "Rohan Verma", "Ananya Jain", "Aditya Patel", "Ishita Gupta", "Vikram Reddy", "Pooja Kumar"];
    const statuses = ["Present", "Absent"];
    const rollNumber = Math.floor(Math.random() * 50) + 1;
    const studentName = studentNames[Math.floor(Math.random() * studentNames.length)];
    const status = statuses[Math.floor(Math.random() * statuses.length)];
    const timestamp = new Date().toLocaleString();
    
    const record = {
        id: attendanceData.length + 1,
        studentName,
        rollNumber,
        status,
        timestamp
    };
    
    attendanceData.push(record);
}

export function getAttendanceData() {
    return attendanceData;
}

export function clearAttendanceData() {
    attendanceData = [];
}
