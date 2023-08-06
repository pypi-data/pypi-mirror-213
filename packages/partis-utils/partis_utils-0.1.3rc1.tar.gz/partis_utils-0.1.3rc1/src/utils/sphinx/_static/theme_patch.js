// replaces the furo inlined script for setting initial data-theme
document.body.dataset.theme = localStorage.getItem("theme") || "auto";