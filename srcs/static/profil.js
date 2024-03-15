window.addEventListener('load', function () {
	document.getElementById('logout-button').onclick = function() {
		document.cookie = "pongtoken" + "=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
		location.reload();
	}
})