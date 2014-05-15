/**
 * @author james porcelli
 */

// @note: DOM not loaded
// Load the SDK asynchronously
( function(d, s, id) {
		var js, fjs = d.getElementsByTagName(s)[0];
		if (d.getElementById(id))
			return;
		js = d.createElement(s);
		js.id = id;
		js.src = "//connect.facebook.net/en_US/sdk.js";
		fjs.parentNode.insertBefore(js, fjs);
	}(document, 'script', 'facebook-jssdk'));

//Globals
var map, geocoder, wpid;

function main_onload() {
	var fb_test1 = '1446699458905329';
	var fb_dev = '1446696428905632';

	$('#type_filter_select').chosen();
	$('#type_newevent_select').chosen();

	$("#login").dialog({
		autoOpen : false,
		modal : true,
		title : "Login",
	});

	$("#launch_loginUI").click(function() {
		$("#login").dialog("open");
	});

	$("#new_event").dialog({
		autoOpen : false,
		modal : true,
		title : "New Event",
		width : 350,
		height : 500,
	});

	$("#launch_newevtUI").click(function() {
		$("#new_event").dialog("open");
	});
	
	var datetime;
	
	$('#datetimepicker').datetimepicker({
		closeOnDateSelect : false,
		lazyInit : true,
	});

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
	
	$('submit_newevent').click(processNewEvent);
}

function create_event(evt) {
	console.log('New event');
}

// Full docs on the response object can be found in the documentation
// for FB.getLoginStatus().
function fbStatusChangeCallback(response) {
	console.log('FB status change event');
	console.log(response);

	$('#logout').click(function(e) {
		$.ajax({
			dataType : 'json',
			url : '/Logout/',
			data : {
			},
			success : function(data) {
				console.log('Logout');
				console.log(data);
			}
		});
	});

	// The response object is returned with a status field that lets the
	// app know the current login status of the person.
	if (response.status === 'connected') {
		// Logged into your app and Facebook.

		var accessToken = response.authResponse.accessToken;
		var userId = response.authResponse.userID;

		$.ajax({
			dataType : 'json',
			url : '/Login/Fb/',
			data : {
				'accessToken' : accessToken,
				'userId' : userId
			},
			success : function(data) {
				console.log('Django response from FB login');
				console.log(data);
			}
		});
	} else if (response.status === 'not_authorized') {
		// The person is logged into Facebook, but not your app.
	} else {
		// The person is not logged into Facebook, so we're not sure if
		// they are logged into this app or not.
	}
}

// This function is called when someone finishes with the Login
// Button.
function fbCheckLoginState() {
	FB.getLoginStatus(function(response) {
		fbStatusChangeCallback(response);
	});
}

function initialize(lng, lat) {

	//@TODO - This is Sydney, Australio, update to world view, or maybe educated guess of client pos
	if (!lng || !lat) {
		lng = -34.397;
		lat = 150.644;
	}

	var mapOptions = {
		center : new google.maps.LatLng(lat, lng),
		zoom : 15
	};

	map = new google.maps.Map(document.getElementById("map-canvas"), mapOptions);
	geocoder = new google.maps.Geocoder();

	google.maps.event.addListener(map, 'click', gmapsEvent_Click);

	google.maps.event.addListener(map, 'zoom_changed', gmapsEvent_ZoomChange);

	google.maps.event.addListener(map, 'dragend', gmapsEvent_DragEnd);

}

function gmapsEvent_DragEnd() {
	var center = map.getBounds();

	console.log('Drag end: map center: ' + center);
}

function gmapsEvent_ZoomChange() {
	//@note - I believe this is in miles
	var r = curViewPortRadius(map);

	console.log("Google Maps zoom change event fired");
	console.log("Radius at current zoom level: " + r);
}

function gmapsEvent_Click(event) {
	var latlng = event.latLng;

	console.log('Google Maps click even fired');
	console.log('Click event latlng: ' + latlng);
}

function geo_success(position) {
	var lat = position.coords.latitude;
	var lng = position.coords.longitude;

	var mapcanvas = document.getElementById('map-canvas');

	//Make sure gmaps not already initialized
	if (mapcanvas.children.length === 0) {
		//Init google maps
		initialize(lng, lat);
	} else {
		//Google maps already present in DOM
	}
}

/**
 *
 * @param {Object} map
 * @return {Double} radius The radius in miles from the center of the map viewport
 *	to the edge of the map
 */
function curViewPortRadius(map) {
	bounds = map.getBounds();

	center = bounds.getCenter();
	ne = bounds.getNorthEast();

	// r = radius of the earth in statute miles
	var r = 3963.0;

	// Convert lat or lng from decimal degrees into radians (divide by 57.2958)
	var lat1 = center.lat() / 57.2958;
	var lon1 = center.lng() / 57.2958;
	var lat2 = ne.lat() / 57.2958;
	var lon2 = ne.lng() / 57.2958;

	// distance = circle radius from center to Northeast corner of bounds
	var dis = r * Math.acos(Math.sin(lat1) * Math.sin(lat2) + Math.cos(lat1) * Math.cos(lat2) * Math.cos(lon2 - lon1));
	return dis;
}

function geo_error() {

}

function geolocationNotAvailable() {

}

function processNewEvent(e){
	
}


$(document).ready(main_onload);
