window.addEventListener('load', function () {
	document.getElementById("logo-name").addEventListener("mouseover", function() {
		this.classList.add("animation-rotate360");
	});
	document.getElementById("logo-name").addEventListener("mouseout", function() {
        this.addEventListener("animationend", () => {
            this.classList.remove("animation-rotate360");
        });
    });
})
