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

function changeUsername(span) {
	var input = document.createElement('input');
	input.value = span.textContent;
	input.style.width = 13 + "ch";
	var isUsernameValid = true;
	var originalUsername = span.textContent;
	var originalBorderColor = span.parentNode.style.borderColor;
	input.className = span.className;

	span.parentNode.replaceChild(input, span);
	input.focus();
	
	input.addEventListener('input', function(e) {
		fetch(`${window.location.origin}/api/check-availability?username=${input.value}`)
		.then(response => {
			if (!response.ok) {
				throw new Error('La requête a échoué.');
			}
			return response.json();
		})
		.then(jsonResponse => {
			isUsernameValid = jsonResponse["username-available"];
			if ((isUsernameValid === true || input.value.trim().toLowerCase().localeCompare(originalUsername.toLowerCase()) == 0) && input.value.length > 0) {
				input.parentNode.style.borderColor = originalBorderColor;
			}
			else {
				input.parentNode.style.borderColor = '#dc3545';
			}
		})
		.catch(error => {
			console.error('Erreur:', error);
		});
	});
	
	input.addEventListener('keypress', function(e) {
		if (e.key === 'Enter') {
			input.blur();
		}
	});

	input.addEventListener('blur', function() {
		if (input.parentNode.style.borderColor != originalBorderColor) {
			input.value = originalUsername;
		}
		else {
			const url = 'http://127.0.0.1:8000/api/change-user-info';
			const formData = new FormData();
			formData.append('access_token', getCookie('pongtoken'));
			formData.append('username', input.value);

			fetch(url, {
				method: 'POST',
				body: formData
			})
			.then(response => {
				if (!response.ok) {
					throw new Error('Network response was not ok');
				}
				return response.json();
			})
			.then(jsonResponse => {
				var changed = jsonResponse["changed"];
				if (changed != "username") {
					input.value = originalUsername;
				}
			})
			.catch(error => {
				console.error('There was a problem with your fetch operation:', error);
			});
		}
		input.parentNode.style.borderColor = originalBorderColor;
		span.textContent = input.value;
		input.parentNode.replaceChild(span, input);
	});
}

function handleFileUpload(event) {
	const file = event.target.files[0];
    if (file) {
        console.log("Nom du fichier:", file.name);
        console.log("Type du fichier:", file.type);
        console.log("Taille du fichier:", file.size, "octets");
    }
}

window.addEventListener('load', function () {
	logo = document.getElementById("logo");
	if (logo) {
		logo.addEventListener("mouseover", function() {
			this.classList.add("animation-rotate360");
		});
		logo.addEventListener("mouseout", function() {
			this.addEventListener("animationend", () => {
				this.classList.remove("animation-rotate360");
			});
		});
	}

	button_logout = document.getElementById("button-logout");
	if (button_logout) {
		button_logout.addEventListener("click", function() {
			deleteCookie("pongtoken")
			location.reload()
		});
	}

	user_username = document.getElementById("user-username");
	if (user_username) {
		user_username.addEventListener("click", function() {
			changeUsername(this)
		});
	}

	user_info_pic_img = document.getElementById('user-info-pic-img');
    user_info_pic_input = document.getElementById('user-info-pic-input');
    
	if (user_info_pic_img && user_info_pic_input) {
		user_info_pic_img.addEventListener('click', function() {
			console.log('clicked')
			user_info_pic_input.click();
		});
	}
})
