//import facebook
FACEBOOK_APP_ID = "1362095630475570"
FACEBOOK_APP_SECRET = "6e9760b0cc49fd736a9b36998aad064e" 

// This is called with the results from from FB.getLoginStatus().
function statusChangeCallback(response) {
	console.log('statusChangeCallback');
	console.log(response);
	
	if (response.status === 'connected') {
		connect();
	} else if (response.status === 'not_authorized') {
		login();
		document.getElementById('status').innerHTML = 'Please log '
				+ 'into this app.';
	} else {
		login();
		document.getElementById('status').innerHTML = 'Please log '
				+ 'into Facebook.';
	}
}

function checkLoginState() {
	FB.getLoginStatus(function(response) {
		statusChangeCallback(response);
	});
}

function connect() {
	console.log('Welcome!  Fetching your information.... ');
	console.log(123123);
	window.location = "/main";
}

// Here we run a very simple test of the Graph API after login is
// successful. See statusChangeCallback() for when this call is made.
function login() {
	console.log('Welcome!  Fetching your information.... ');
	FB.login(function(response) {
		if (response.status === 'connected') {
			window.location = "/main";
		} else if (response.status === 'not_authorized') {
			login();
		} else {
			login();
		}
		console.log(response);
		console.log('Successful login for: ' + response.name);
		document.getElementById('status').innerHTML = 'Thanks for logging in, '
				+ response.name + '!';
	});
}

function facebookSetup() {
	window.fbAsyncInit = function() {
		FB.init({
			appId : FACEBOOK_APP_ID,
			cookie : true, // enable cookies to allow the server to access the session
			xfbml : true, // parse social plugins on this page
			version : 'v2.5' // use graph api version 2.5
		});

		FB.getLoginStatus(function(response) {
			statusChangeCallback(response);
		});
	};

	// Load the SDK asynchronously
	(function(d, s, id) {
		var js, fjs = d.getElementsByTagName(s)[0];
		if (d.getElementById(id))
			return;
		js = d.createElement(s);
		js.id = id;
		js.src = "//connect.facebook.net/en_US/sdk.js";
		fjs.parentNode.insertBefore(js, fjs);
	}(document, 'script', 'facebook-jssdk'));
}

$(document).ready(function() {
	facebookSetup();
});