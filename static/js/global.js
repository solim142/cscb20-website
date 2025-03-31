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

function openForm(button) {
    if (button.textContent === "Remark Request") {
        console.log("a");
        button.textContent = "Close"

        var form = button.nextElementSibling; // https://developer.mozilla.org/en-US/docs/Web/API/Element/nextElementSibling
        form.style.display = "block";

        console.log(form)
    } else {
        console.log("b");
        button.textContent = "Remark Request"

        var form = button.nextElementSibling; // https://developer.mozilla.org/en-US/docs/Web/API/Element/nextElementSibling
        form.style.display = "none";
    }
}

function editGrade(button) {
    if (button.textContent === "Edit") {
        console.log("a");
        button.textContent = "Close Edit"

        var form = button.nextElementSibling; // https://developer.mozilla.org/en-US/docs/Web/API/Element/nextElementSibling
        form.style.display = "block";

        console.log(form)
    } else {
        console.log("b");
        button.textContent = "Edit"

        var form = button.nextElementSibling; // https://developer.mozilla.org/en-US/docs/Web/API/Element/nextElementSibling
        form.style.display = "none";
    }
}

document.addEventListener('DOMContentLoaded', function () {
    const buttons = document.querySelectorAll('.filter-btn');
    const cards = document.querySelectorAll('.feedback-card');
    const msgOpen = document.getElementById('no-open-feedback');
    const msgReviewed = document.getElementById('no-reviewed-feedback');

    function hideMessages() {
        msgOpen.style.display = 'none';
        msgReviewed.style.display = 'none';
    }

    buttons.forEach(btn => {
        btn.addEventListener('click', () => {
            buttons.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            const status = btn.getAttribute('data-status');

            let visibleCount = 0;
            hideMessages();

            cards.forEach(card => {
                if (status === 'all' || card.getAttribute('data-status') === status) {
                    card.style.display = 'block';
                    visibleCount++;
                } else {
                    card.style.display = 'none';
                }
            });

            // Show appropriate message if nothing visible
            if (status === 'open' && visibleCount === 0) {
                msgOpen.style.display = 'block';
            } else if (status === 'reviewed' && visibleCount === 0) {
                msgReviewed.style.display = 'block';
            }
        });
    });
});
