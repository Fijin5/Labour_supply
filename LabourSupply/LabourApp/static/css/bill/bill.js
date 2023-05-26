const switchLight = document.getElementsByClassName("switch-light");
let colorDarkIsActive = true;
switchLight[0].addEventListener("click", () => {
	toggleCssMode();
	colorDarkIsActive = !colorDarkIsActive;
});

function toggleCssMode() {
	const iconSun = switchLight[0].querySelector(".feather-sun");
	const iconMoon = switchLight[0].querySelector(".feather-moon");
	if (colorDarkIsActive) {
		iconSun.classList.add("d-none");
		iconMoon.classList.remove("d-none");
		document.body.classList.add("light-mode");
	} else {
		iconMoon.classList.add("d-none");
		iconSun.classList.remove("d-none");
		document.body.classList.remove("light-mode");
	}
}
