/* For First Version of Header */
const hamburger = document.querySelector('.header .nav-bar .nav-list .hamburger');
const mobile_menu = document.querySelector('.header .nav-bar .nav-list ul');
const menu_item = document.querySelectorAll('.header .nav-bar .nav-list ul li a');
const header = document.querySelector('.header.container');

/* For Second Version of Header */
const hamburger2 = document.querySelector('.header2 .nav-bar .nav-list .hamburger');
const mobile_menu2 = document.querySelector('.header2 .nav-bar .nav-list ul');
const menu_item2 = document.querySelectorAll('.header2 .nav-bar .nav-list ul li a');
const header2 = document.querySelector('.header2.container');

/* For First Version of Header */
hamburger.addEventListener('click', () => {
	hamburger.classList.toggle('active');
	mobile_menu.classList.toggle('active');
});

/* For Second Version of Header */
hamburger2.addEventListener('click', () => {
	hamburger2.classList.toggle('active');
	mobile_menu2.classList.toggle('active');
});

/* For First and Second Version of Header */
document.addEventListener('scroll', () => {
	var scroll_position = window.scrollY;
	if (scroll_position > 250) {
		header.style.backgroundColor = 'rgb(28, 74, 154)'; /* When scrolling down, navigation bar changes to this colour. */
		header2.style.backgroundColor = 'rgb(255, 0, 0)';
	} else {
		header.style.backgroundColor = 'transparent'; /* When scrolling, this will colour the background of the navigation bar. When going to the top of the page, the background will be transparent. */
		header2.style.backgroundColor = 'rgb(28, 74, 154)';
	}
});

/* For First Version of Header */
menu_item.forEach((item) => {
	item.addEventListener('click', () => {
		hamburger.classList.toggle('active');
		mobile_menu.classList.toggle('active');
	});
});

/* For Second Version of Header */
menu_item2.forEach((item) => {
	item.addEventListener('click', () => {
		hamburger2.classList.toggle('active');
		mobile_menu2.classList.toggle('active');
	});
});