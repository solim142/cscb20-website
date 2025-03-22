function switchResponsive() {
    var x = document.getElementById("mainNav"); // Gets the id
    if (x.className === "topnav") {
        x.className += " responsive"; // Basically appending the class that would change the css
    } else {
        x.className = "topnav"; // Removing the extra class
    }
}