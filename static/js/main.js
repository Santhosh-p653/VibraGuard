// static/js/main.js

import { initThemeToggle } from './theme.js';
import { initSystemToggle } from './system.js';
import { getAttendanceData } from './data.js';
import { handleDownload } from './download.js';
import { initChatbot } from './chatbot.js'; // Import the new chatbot module

document.addEventListener('DOMContentLoaded', () => {
    // Initialize all modules
    initThemeToggle();
    initChatbot(); // Initialize the chatbot

    const systemToggleButton = document.getElementById('system-toggle');
    const downloadButtonMain = document.getElementById('download-report');
    const downloadButtonSidebar = document.getElementById('download-report-sidebar');

    if (systemToggleButton) {
        initSystemToggle();
    }

    if (downloadButtonMain) {
        downloadButtonMain.addEventListener('click', () => {
            const data = getAttendanceData();
            handleDownload(data);
        });
    }

    if (downloadButtonSidebar) {
        downloadButtonSidebar.addEventListener('click', () => {
            const data = getAttendanceData();
            handleDownload(data);
        });
    }
});
