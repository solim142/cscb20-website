# Problems & Improvements

Problem: Old page had a fixed width, smaller than a landscape screen, but not quite fit for mobile.
Improvement: Made the widths and heighs relative in the page, with some minimums, that adapt to the user's screen.

Problem: No quick access to MarkUs or the Assignment's contents. Can only do so through clicking on the assignments page first, and then the link.
Improvement: The navigation menu has direct links to MarkUs, and directly links to the specific assignments when hovering over the assignments option.

Problem: No dark mode
Improvement: Created a dark mode of the page, along with a way to switch.

# Challenges

1. A large problem was designing the navigation bar to be: useful buttons, stick to the top of the page, and display a dropdown menu from the position it is, at any point from the page, on top of working and looking good on mobile. The way it was solved was by dividing it into 3 parts: navbar, dropdown and mobile.
In the navbar, the best option was just a flex div that sticks to the top of the page, with all the contents in it, links, justified to spread out.
For the dropdown, it would take the position of the navbar and add a dropdown menu div that is absolute (relative to the viewer) below the option, using a div that contains that option for alignment.
The mobile menu was the hardest part, since it involved the use of media query. To switch between, the navbar for desktop is set to display:none to hide it, and a hidden menu, the mobile one, is displayed instead, which is triggered below an aspect ratio and below a width. Both menus do exist, but media query switches which is displayed and which isn't. Given the complexity of the navbar, the mobile menu was just set to be a simpler dropdown that shows when hovering over the menu icon. We were unfortunately unable to find another way that didn't involve JS to do so reliably.

2. Switching between light and dark mode. Given don't have any templates, the simplest way to "switch" between modes was to create a clone of all the pages, but switch the CSS colour variables, then, the button in the footer is a link to that page's other mode.
