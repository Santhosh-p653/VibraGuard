// static/js/mockData.js

const mockData = {
    students: [
        { id: 1, name: "Aarav Sharma", rollNo: "CS101", status: "Present", date: "2025-09-20", time: "09:05 AM" },
        { id: 2, name: "Kiara Singh", rollNo: "CS102", status: "Present", date: "2025-09-20", time: "09:07 AM" },
        { id: 3, name: "Rohan Verma", rollNo: "CS103", status: "Absent", date: "2025-09-20", time: "" },
        { id: 4, name: "Ananya Jain", rollNo: "CS104", status: "Present", date: "2025-09-20", time: "09:10 AM" },
        { id: 5, name: "Aditya Patel", rollNo: "CS105", status: "Present", date: "2025-09-20", time: "09:11 AM" },
        { id: 6, name: "Ishita Gupta", rollNo: "CS106", status: "Absent", date: "2025-09-20", time: "" },
        { id: 7, name: "Vikram Reddy", rollNo: "CS107", status: "Present", date: "2025-09-20", time: "09:15 AM" },
        { id: 8, name: "Pooja Kumar", rollNo: "CS108", status: "Present", date: "2025-09-20", time: "09:18 AM" },
    ],
    classes: [
        { id: 1, className: "Mathematics", totalStudents: 30, present: 28, absent: 2, attendanceRate: "93%" },
        { id: 2, className: "Physics", totalStudents: 25, present: 24, absent: 1, attendanceRate: "96%" },
        { id: 3, className: "Computer Science", totalStudents: 28, present: 22, absent: 6, attendanceRate: "78%" },
        { id: 4, className: "Chemistry", totalStudents: 32, present: 31, absent: 1, attendanceRate: "97%" },
    ],
    teachers: [
        { id: 1, name: "Mr. Sharma", subject: "Mathematics", status: "Present", lastLogin: "2025-09-21 08:45 AM" },
        { id: 2, name: "Ms. Desai", subject: "Physics", status: "Present", lastLogin: "2025-09-21 08:50 AM" },
        { id: 3, name: "Dr. Singh", subject: "Computer Science", status: "Absent", lastLogin: "" },
        { id: 4, name: "Mrs. Khan", subject: "Chemistry", status: "Present", lastLogin: "2025-09-21 09:00 AM" },
    ],
};

export default mockData;
