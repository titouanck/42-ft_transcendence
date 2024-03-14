function getCookie(cname) {
	var cookieArr = document.cookie.split(';');
	for (var i = 0; i < cookieArr.length; i++) {
		var cookiePair = cookieArr[i].split('=');
		if (cname == cookiePair[0].trim()) {
			return decodeURIComponent(cookiePair[1]);
		}
	}
	return null;
}

function deleteCookie(cname) {
    document.cookie = cname + '=; expires=Thu, 01 Jan 1970 00:00:01 GMT; path=/;';
}

window.addEventListener('load', function () {
	document.getElementById("logo").addEventListener("mouseover", function() {
		this.classList.add("animation-rotate360");
	});
	document.getElementById("logo").addEventListener("mouseout", function() {
		this.addEventListener("animationend", () => {
			this.classList.remove("animation-rotate360");
		});
	});

	document.getElementById("button-logout").addEventListener("click", function() {
		deleteCookie("pongtoken")
		location.reload()
	});
})
