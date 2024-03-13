window.addEventListener('load', function () {
	document.getElementById("logo-name").addEventListener("mouseover", function() {
		this.classList.add("rotateAnimation");
	});
	document.getElementById("logo-name").addEventListener("mouseout", function() {
        this.addEventListener("animationend", () => {
            this.classList.remove("rotateAnimation");
        });
    });
})
