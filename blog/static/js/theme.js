document.addEventListener("DOMContentLoaded", function() {
    const themeSwitch = document.getElementById("theme-switch");
    const currentTheme = localStorage.getItem("theme") || "auto";

    function applyTheme(theme) {
        const themeLink = document.getElementById("theme-style");
        if (theme === "dark") {
            themeLink.href = "/static/css/dark-theme.css";
        } else if (theme === "light") {
            themeLink.href = "/static/css/light-theme.css";
        } else if (theme === "auto") {
            if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
                themeLink.href = "/static/css/dark-theme.css";
            } else {
                themeLink.href = "/static/css/light-theme.css";
            }
        }
    }

    applyTheme(currentTheme);

    themeSwitch.addEventListener("change", function() {
        let selectedTheme = "auto";
        if (this.value === "dark") {
            selectedTheme = "dark";
        } else if (this.value === "light") {
            selectedTheme = "light";
        }

        localStorage.setItem("theme", selectedTheme);
        applyTheme(selectedTheme);
    });

    // Listen for changes to the system theme preference
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', event => {
        if (localStorage.getItem("theme") === "auto") {
            applyTheme("auto");
        }
    });
});
