// static/js/system.js

import { generateAttendanceRecord, clearAttendanceData } from './data.js';

let isSystemActive = false;
let intervalId = null;
const statusMessage = document.getElementById('status-message');
const systemToggleButton = document.getElementById('system-toggle');
const downloadButtonMain = document.getElementById('download-report');
const downloadButtonSidebar = document.getElementById('download-report-sidebar');

export function initSystemToggle() {
    systemToggleButton.addEventListener('click', () => {
        if (isSystemActive) {
            // Stop the system
            isSystemActive = false;
            systemToggleButton.innerHTML = '<i class="bi bi-play-fill me-2"></i>Start System';
            systemToggleButton.classList.remove('btn-danger');
            systemToggleButton.classList.add('btn-success');
            
            statusMessage.innerHTML = 'System is **OFFLINE**. Click "Start System" to begin attendance tracking.';
            statusMessage.classList.remove('alert-success');
            statusMessage.classList.add('alert-danger');
            
            downloadButtonMain.disabled = false;
            downloadButtonSidebar.disabled = false;
            clearInterval(intervalId); // Stop data generation

        } else {
            // Start the system
            isSystemActive = true;
            systemToggleButton.innerHTML = '<i class="bi bi-stop-fill me-2"></i>Stop System';
            systemToggleButton.classList.remove('btn-success');
            systemToggleButton.classList.add('btn-danger');
            
            statusMessage.innerHTML = 'System is **ONLINE**. Attendance tracking is in progress...';
            statusMessage.classList.remove('alert-danger');
            statusMessage.classList.add('alert-success');
            
            downloadButtonMain.disabled = true;
            downloadButtonSidebar.disabled = true;
            clearAttendanceData(); // Clear old data for new session
            
            // Start generating dummy data every 3 seconds
            intervalId = setInterval(generateAttendanceRecord, 3000);
        }
    });
}
