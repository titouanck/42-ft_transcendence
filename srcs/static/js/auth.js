window.addEventListener('load', function () {
    const button_signin_42 = document.getElementById('button-signin-42');
    if (button_signin_42) {
        button_signin_42.addEventListener('click', function() {
            const url = 'https://api.intra.42.fr/oauth/authorize';
            const params = {
                FORTYTWO_API_KEY: "u-s4t2ud-12c57e708b315daf0c44bb3ccdacaa14f1d142926cb04721324333e0a4a349c8",
                redirect_uri: window.location.origin + window.location.pathname,
                scope: 'public',
                response_type: 'code'
            };
            const queryString = new URLSearchParams(params).toString();
            const redirectUrl = `${url}?${queryString}`;
            window.location.href = redirectUrl;
        });
    }
});