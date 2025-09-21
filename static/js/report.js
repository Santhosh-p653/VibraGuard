// static/js/report.js

import mockData from './mockData.js';

export function renderReportTable(type) {
    const reportContainer = document.getElementById('report-content');
    if (!reportContainer) return;

    let data;
    let headers;
    let title;

    switch (type) {
        case 'student':
            data = mockData.students;
            headers = ["ID", "Name", "Roll No", "Status", "Date", "Time"];
            title = "Individual Student Report";
            break;
        case 'class':
            data = mockData.classes;
            headers = ["ID", "Class Name", "Total Students", "Present", "Absent", "Attendance Rate"];
            title = "Class Attendance Report";
            break;
        case 'teacher':
            data = mockData.teachers;
            headers = ["ID", "Name", "Subject", "Status", "Last Login"];
            title = "Teacher Attendance Report";
            break;
        default:
            reportContainer.innerHTML = `<p class="alert alert-warning">No report data found.</p>`;
            return;
    }

    // Set the page title
    document.getElementById('report-title').textContent = title;

    // Create the table structure
    let tableHtml = `<div class="table-responsive"><table class="table table-hover table-striped"><thead><tr>`;
    headers.forEach(header => {
        tableHtml += `<th scope="col">${header}</th>`;
    });
    tableHtml += `</tr></thead><tbody>`;

    // Populate the table with data
    data.forEach(item => {
        tableHtml += `<tr>`;
        Object.values(item).forEach(value => {
            tableHtml += `<td>${value}</td>`;
        });
        tableHtml += `</tr>`;
    });

    tableHtml += `</tbody></table></div>`;
    reportContainer.innerHTML = tableHtml;
}
