static/js/download.js

export function handleDownload(data) {
    if (data.length === 0) {
        alert('No attendance data to download!');
        return;
    }

    const headers = ["ID", "Student Name", "Roll Number", "Status", "Timestamp"];
    const csvContent = "data:text/csv;charset=utf-8," 
                     + headers.join(',') + '\n'
                     + data.map(e => Object.values(e).join(',')).join('\n');

    const encodedUri = encodeURI(csvContent);
    const link = document.createElement("a");
    link.setAttribute("href", encodedUri);
    link.setAttribute("download", "attendance_report.csv");
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}
