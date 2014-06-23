/**
 * External Java script for login document
 * 
 * @author james porcelli
 */

//Globals
var geocoder, wpid, lat, lng;

//Facebook app id
var fb_dev = '1446696428905632';

/**
 * Initialize the GeoLocation API
 */
function initGeoLocationApi() {
	//Initialize the html5 geocoding api
	if ('geolocation' in navigator) {
		var geo_options = {
			enableHighAccuracy : true,
			maximumAge : 30000,
			timeout : 27000
		};

		wpid = navigator.geolocation.watchPosition(geo_success, geo_error, geo_options);
	} else {
		geolocationNotAvailable();
	}
}

/**
 * Initialize the Facebook API
 */
function initFacebookApi() {
	window.fbAsyncInit = function() {
		FB.init({
			appId : fb_dev,
			cookie : true, // enable cookies to allow the server to access
			// the session
			xfbml : true, // parse social plugins on this page
			version : 'v2.0' // use version 2.0
		});

		FB.getLoginStatus(function(response) {
			fbStatusChangeCallback(response);
		});

		FB.Event.subscribe('auth.authResponseChange', fbStatusChangeCallback);
	};
}

/**
 * 
 * @param {Object} position
 */
function geo_success(position) {
	
	//Set the lat, lng cordinates of the client position
	lat = position.coords.latitude;
	lng = position.coords.longitude;
}

/**
 * 
 */
function geo_error() {

}

/**
 * 
 */
function geolocationNotAvailable() {

}

/**
 * 
 */
function login_onload() {
	initGeoLocationApi();
	initFacebookApi();
}

/**
 * 
 * @param {Object} response Full docs on the response object can be found in 
 * the documentation for FB.getLoginStatus()
 */
function fbStatusChangeCallback(response) {
	console.log('FB status change event');
	console.log(response);

	// The response object is returned with a status field that lets the
	// app know the current login status of the person.
	if (response.status === 'connected') {
		// Logged into your app and Facebook.

	} else if (response.status === 'not_authorized') {
		// The person is logged into Facebook, but not your app.
	} else {
		// The person is not logged into Facebook, so we're not sure if
		// they are logged into this app or not.
	}
}

/**
 * Login using standard Django login
 * 
 * @param {Object} e
 */
function djangoLogin(e) {

	// The login form
	var form = $('#evtsrc_loginform');
	
	// Append the parameters required for login using HTTP GET
	form.attr('action', '/Login/?lat=' + lat + '&lng=' + lng);
	form.submit();
}

// This function is called when someone finishes with the Login
// Button.
function fblogin(response) {

	// Do we need this FB callback or can we just use the resposne param?
	FB.getLoginStatus(function(response) {
	
		// Obtain the Facebook login tokens after the Facebook authentication
		var accessToken = response.authResponse.accessToken;
		var userId = response.authResponse.userID;

		var form = $('#evtsrc_loginform');
		
		// @TODO Consider passing Facebook login credentials via HTTP POST
		// @Attention is passing via HTTP GET insecure?
		
		// Append the parameters required for login using HTTP GET
		form.attr('action', '/Login/Fb/?userId=' + userId + '&accessToken=' + accessToken + '&lat=' + lat + '&lng=' + lng);
		form.submit();
	});
}


$(document).ready(login_onload);
