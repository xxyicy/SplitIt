//import facebook
FACEBOOK_APP_ID = "1362095630475570"
FACEBOOK_APP_SECRET = "6e9760b0cc49fd736a9b36998aad064e"

function facebookSetup() {
	window.fbAsyncInit = function() {
		FB.init({
			appId : 'FACEBOOK_APP_ID',
			status : true,
			cookie : true,
			xfbml : true
		});
		FB.Event
				.subscribe(
						'auth.logout',
						function(response) {
							window.location.reload();
						});
	};

	(function() {
		var e = document.createElement('script');
		e.type = 'text/javascript';
		e.src = document.location.protocol
				+ '//connect.facebook.net/en_US/all.js';
		e.async = true;
		document.getElementById('fb-root').appendChild(e);
	}());

}

$(document).ready(function() {
	facebookSetup();
});