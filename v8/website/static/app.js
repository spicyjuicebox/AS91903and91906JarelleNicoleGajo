/* For First Version of Header */
const hamburger = document.querySelector('.header .nav-bar .nav-list .hamburger');
const mobile_menu = document.querySelector('.header .nav-bar .nav-list ul');
const menu_item = document.querySelectorAll('.header .nav-bar .nav-list ul li a');
const header = document.querySelector('.header.container');

// When the 'hamburger' element is clicked, it toggles the 'active' class for both the 'hamburger' and 'mobile_menu' elements.
/* This way, the hamburger which is used for the mobile navigation menu will be toggled and opened. */
if (hamburger) {
    hamburger.addEventListener('click', () => {
        hamburger.classList.toggle('active');
        mobile_menu.classList.toggle('active');
    });
}

/* This is the menu that slides from the left when the hamburger is toggled. */
menu_item.forEach((item) => {
    item.addEventListener('click', () => {
        hamburger.classList.toggle('active');
        mobile_menu.classList.toggle('active');
    });
});


/* For Second Version of Header */
const hamburger2 = document.querySelector('.header2 .nav-bar2 .nav-list2 .hamburger2');
const mobile_menu2 = document.querySelector('.header2 .nav-bar2 .nav-list2 ul');
const menu_item2 = document.querySelectorAll('.header2 .nav-bar2 .nav-list2 ul li a');
const header2 = document.querySelector('.header2.container');

/* This works as the same way as it does in the first version of this header. This just toggles specifcally for template2.html. */
if (hamburger2) {
    hamburger2.addEventListener('click', () => {
        hamburger2.classList.toggle('active');
        mobile_menu2.classList.toggle('active');
    });
}

/* Brings in the menu from the left when the hamburger is toggled for template2.html. */
menu_item2.forEach((item) => {
    item.addEventListener('click', () => {
        hamburger2.classList.toggle('active');
        mobile_menu2.classList.toggle('active');
    });
});


/* This is a scroll event listener. This checks where the user is on the page when they scroll. */
/* When the scroll position is greater than 250, the background colour of the navigation bar will change. */
/* When the scroll position is less than 250 (else), the background colour of the navigation bar will be different (transparent for header and blue for header2). */
/* For First and Second Version of Header */
document.addEventListener('scroll', () => {
    var scroll_position = window.scrollY;
    if (scroll_position > 250) {
        header.style.backgroundColor = 'rgb(28, 74, 154)'; /* When scrolling down, navigation bar changes to this colour. */
        if (header2) {
            header2.style.backgroundColor = 'rgb(28, 74, 154)';
        }
    } else {
        header.style.backgroundColor = 'transparent'; /* When scrolling, this will colour the background of the navigation bar. When going to the top of the page, the background will be transparent. */
        if (header2) {
            header2.style.backgroundColor = 'rgb(28, 74, 154)';
        }
    }
});