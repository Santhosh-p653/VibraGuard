// static/js/theme.js

export function initThemeToggle() {
    const themeToggle = document.getElementById('theme-toggle');

    // Load theme preference from localStorage
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'dark') {
        document.documentElement.setAttribute('data-bs-theme', 'dark');
        themeToggle.checked = true;
    }

    // Theme Toggle Functionality
    themeToggle.addEventListener('change', () => {
        if (themeToggle.checked) {
            document.documentElement.setAttribute('data-bs-theme', 'dark');
            localStorage.setItem('theme', 'dark');
        } else {
            document.documentElement.setAttribute('data-bs-theme', 'light');
            localStorage.setItem('theme', 'light');
        }
    });
}
