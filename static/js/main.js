document.addEventListener("DOMContentLoaded", function () {
    const searchInput = document.getElementById("search-input");
    searchInput.addEventListener("focus", function () {
        this.placeholder = "";
    });
    searchInput.addEventListener("blur", function () {
        this.placeholder = "Search for books here:";
    });
});
