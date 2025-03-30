function switchResponsive() {
    var x = document.getElementById("mainNav"); // Gets the id
    if (x.className === "navbar") {
        x.className += " responsive"; // Basically appending the class that would change the css
    } else {
        x.className = "navbar"; // Removing the extra class
    }
}

function toggleDark() {
    var r = document.querySelector('html');
    
    var color = getComputedStyle(r).getPropertyValue('--UofTBlue');
    
    // Checking if the main colour matches the Lightmode one
    if (color == '#1E3765') { 
        r.style.setProperty('--UofTBlue', '#76DAF4');
        r.style.setProperty('--UofTLightBlue', '#1A98BA');
        r.style.setProperty('--navbarLightBlue', '#003F51');
        r.style.setProperty('--UofTGreen', '#00A189');
        r.style.setProperty('--background', '#000000');
        r.style.setProperty('--text', '#FFFFFF');
        r.style.setProperty('--footertext', '#003F51');
    } else {
        r.style.setProperty('--UofTBlue', '#1E3765');
        r.style.setProperty('--UofTLightBlue', '#007FA3');
        r.style.setProperty('--navbarLightBlue', '#B2D8E3');
        r.style.setProperty('--UofTGreen', '#00A189');
        r.style.setProperty('--background', '#FFFFFF');
        r.style.setProperty('--text', '#000000');
        r.style.setProperty('--footertext', '#96A1B7');
    }
}