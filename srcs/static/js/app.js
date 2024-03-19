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
	input.style.width = 12 + "ch";
	var isUsernameValid = true;
	var originalUsername = span.textContent;
	var originalBorderColor = span.parentNode.style.borderColor;
	input.className = span.className;

	span.parentNode.replaceChild(input, span);
	input.focus();
	
	input.addEventListener('input', function(e) {
		fetch(`${window.location.origin}/api/check_availability?username=${input.value}`)
		.then(response => {
			if (!response.ok) {
				throw new Error('La requête a échoué.');
			}
			return response.json();
		})
		.then(jsonResponse => {
			isUsernameValid = jsonResponse["username_available"];
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
	
	input.addEventListener('keyup', function(e) {
		if (e.key === 'Enter' || e.key === 'Escape') {
			input.blur();
		}
	});

	input.addEventListener('blur', function() {
		const params = new URLSearchParams();
		params.append('username', input.value);
		const requestOptions = {
			method: 'POST',
			headers: {
				'Authorization': `Bearer ${getCookie('pongtoken')}`,
				'Content-Type': 'application/x-www-form-urlencoded'
			},
			body: params
		};
		
		if (input.parentNode.style.borderColor == originalBorderColor) {
			span.textContent = input.value;
			fetch(`${window.location.origin}/api/users/me/update`, requestOptions)
				.then(response => response.json())
				.then(data => {
					if (!data.updated || !data.updated.includes("username")) {
						span.textContent = originalUsername;
						span.parentNode.style.borderColor = originalBorderColor;
					}
				})
				.catch(error => console.error('Erreur lors de la requête :', error));
		}
		else {
			input.parentNode.style.borderColor = originalBorderColor;
			span.textContent = originalUsername;
		}
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

	
