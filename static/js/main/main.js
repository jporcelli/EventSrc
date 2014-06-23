/**
 * @author james porcelli
 */

// Globals
var map, geocoder, wpid, csrftoken;
var marker_index = {};

var fb_dev = '1446696428905632';

/**
 * 
 */
function initFiltersWindow(){
	
  	// Type select for filters
  	$('#filter_type_select').chosen();
  	$('#filter_radius_select').chosen();
}

/**
 * 
 */
function initCreatedEvents(){
  	
  	// By using jQuery `on` and delegated event handling we can assign handlers
  	// to nodes that exist onload, and in the future
  	
   $('#my_events_list').on('mouseenter', '.event_owner', function(){  	
   		$(this).css('cursor', 'pointer');
   });
	
   $('#my_events_list').on('mouseleave', '.event_owner', function(){
   		$(this).css('cursor', '');
   });
	   
   $('#my_events_list').on('click', '.event_owner', goToOwnedEvent);
}

/**
 * 
 */
function initNewEventWindow(){
  	
  	// Type select for new event form
	$('#event_type_select').chosen();
	
	$('#datetimepicker').datetimepicker({
		closeOnDateSelect : true,
		lazyInit : true,
		format:'Y-m-d H:i',
	});
	
	// Datetime picker for new event form
	$('#datetime_calndr-icon').hover(function() {
		$(this).css('cursor', 'pointer');
	}, function() {
		$(this).css('cursor', '');
	});

	$('#datetime_calndr-icon').click(function(e) {
		$('#datetimepicker').focus().click();
	});
	
	// Validate the new event form
	$('#neweventform').validate({
		errorPlacement : function(error, element) {
			error.css('color', '#f00');
			error.appendTo(element.parent('div'));
		},
	});
	
	$('#neweventform').on('submit', function(e){
		var form = $(this);
		var valid = form.valid();
        
        if(valid)
        {
            e.preventDefault();
            processNewEvent(form);
        }
	});

}

/**
 * Initialize the GeoLocation API
 */
function initGeoLocationApi(){
	
	// Initialize the html5 geocoding api
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
function initFacebookApi(){
	
	window.fbAsyncInit = function() {
		FB.init({
			appId : fb_dev,
			cookie : true, // enable cookies to allow the server to access the session
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
 * Initialize the navigation bar items
 */
function initNavBarItems(){
	
	//Handle a navigation to the event content window
	$('#event_content_window').click(function(e){
		var current_window = window.location.hash;		
		
		switch(current_window){
			
			case '#new_event' : {
				$('#new_event').hide();
				window.location.hash = '#event_content_tabs';
				break;
			}
			
			case '#filters_container' : {	
				$('#filters_container').hide();
				window.location.hash = '#event_content_tabs';
				break;
			}
			
			case '#event_content_tabs' : {
				// Do nothing already in this window
				break;
			}
		}
		
		//@TODO Make an XHR request to check for new events e.g 'load' new events, if available
		$('#event_content_tabs').show();
	});
	
	// Handle a navigation to the new event creation window
	$('#new_event_window').click(function(e){	
		var current_window = window.location.hash;		
		
		switch(current_window){
			
			case '#event_content_tabs' : {
				$('#event_content_tabs').hide();
				window.location.hash = '#new_event';
				break;
			}
			
			case '#filters_container' : {	
				$('#filters_container').hide();
				window.location.hash = '#new_event';
				break;
			}
			
			case '#new_event' : {
				// Do nothing already in this window
				break;
			}
		}
		
		// Show the new event creation window
		$('#new_event').show();
	});
	
	// Handle a navigaton to the filters window
	$('#filters_window').click(function(e){
		var current_window = window.location.hash;		

		switch(current_window){
			
			case '#event_content_tabs' : {
				$('#event_content_tabs').hide();
				window.location.hash = '#filters_container';
				break;
			}
			
			case '#new_event' : {				
				$('#new_event').hide();
				window.location.hash = '#filters_container';
				break;
			}
			
			case '#filters_container' : {
				// Do nothing already in this window
				break;
			}
		}
		
		// Show the filters window
		$('#filters_container').show();
	});
}

/**
 * Routine for initializing the window
 */
function initWindow(){
	
	// Hide all the windows that are not the initial state window
	$('#new_event').hide();
	$('#filters_container').hide();
	
	// Set the initia; window hash tag
	window.location.hash = 'event_content_tabs';
	
	// Initialize and setup the event content window tabs
	$('#event_content_tabs').tabs({
		
		// Routine to call during the creating of the event content tabs panel
		create: function( event, ui ) {
			var panel_id = $(ui.panel).prop('id'); 
			// Do something with the initial event content panel
		},
		
		// Routine to call when a new tab is activated (invoked) on the event content tabs
		activate: function( event, ui ) {			
			var new_panel_id = $(ui.newPanel).prop('id');
			var old_panel_id = $(ui.oldPanel).prop('id');
			
			console.log('New event content panel id : ' + old_panel_id);
			console.log('Old event content panel id : ' + new_panel_id);
			
			var x = events_lkuptbl[old_panel_id];
			hideEventMarkers(event_markers[x], x);
			
			var y = events_lkuptbl[new_panel_id];
			showEventMarkers(event_markers[y], y);
			
			// @TODO Make and XHR request check for new events e.g 'load' new events, if available
		}
	});
	
	// Functionality to give span elements with the span_anchor class the
	// look and feel of anchors, without being an actual anchor element
	$('.span_anchor').hover(
		function(){
			$(this).css('cursor', 'pointer');
			$(this).css('color', 'blue');
		},
		function(){
			$(this).css('cursor', '');
			$(this).css('color', '');
		}
	);
	
    $(document).tooltip();
}

/**
 * Initialize the jQuery fileupload setup for uploading
 * images for new events
 * 
 * Uses https://github.com/blueimp/jQuery-File-Upload/
 */
function initFileUpload(){
    
    // Initializes the file upload widget
    // @see https://github.com/blueimp/jQuery-File-Upload/
    $('#fileupload').fileupload({   	
        
        url: '/NewEvent/EventPhoto/Upload/',
        
        dataType: 'json',
        
        autoUpload: true,
        
        acceptFileTypes: /(\.|\/)(gif|jpe?g|png)$/i,
        
        maxFileSize: 5000000, // 5 MB
        
        // Enable image resizing, except for Android and Opera,
        // which actually support image resizing, but fail to
        // send Blob objects via XHR requests:
        disableImageResize: /Android(?!.*Chrome)|Opera/
            .test(window.navigator.userAgent),
        
        previewMaxWidth: 100,
        
        previewMaxHeight: 100,
        
        previewCrop: true
        
    }).on('fileuploadadd', function (e, data) {
    	// Callback for a new upload request added to the work queue
    	console.log('fileupload add');
    	console.log(data);
    	
    	// @NOTE Files available (including preview canvas) in data.originalFiles array
        
    }).on('fileuploadprocessalways', function (e, data) {   	
		// Callback for completed, whether success, failure, or aborted, upload request
		console.log('fileupload process always');
		console.log(data);
        
        var index = data.index;
        var file = data.files[index];
        
        if (file.preview) {
        	// @TODO Move to file upload add?
                $('<div class="upload_preview">').html(
                		'<div class="preview_con">').html(file.preview)
	                		.append('<div class="file_meta_con">\
	                			<span class="upload_preview_name">' + file.name + '</span>\
	                			<span class="upload_preview_size">' + formatFileSize(file.size) + '</span>\
	                		</div>\
	                	</div>').prependTo('#files');    
                
        }
        
        if (file.error) {
			console.log('file has error property');
			// @TODO Implement error handling
        }
        
        /*
         @TODO Delete once verified its not required for this implementation
         
        if (index + 1 === data.files.length) {
            data.context.find('button')
                .text('Upload')
                .prop('disabled', !!data.files.error);
        }
        */
        
    }).on('fileuploadprogressall', function (e, data) {
    	// Callback for 'global' file upload progress events
    	
        var progress = parseInt(data.loaded / data.total * 100, 10);
        
        $('#progress .progress-bar').css(
            'width',
            progress + '%'
        );
        
    }).on('fileuploaddone', function (e, data) {
    	// Callback for successful upload requests
    	console.log('fileupload done');
    	console.log(data);
    	
    	// The first div in the files container should be the container for the new file upload
    	var upload_con = $('#files').find('.upload_preview').first();
    	
    	// Add the calculated hash to the file upload preview container so we can dafely
    	// delete the file on the server side if desired
    	upload_con.attr('file_hash', data.result.hash);
    	
    	// @TODO Add the hash to a hidden input to be submitted with the form so we can
    	// go through the final list of uploaded hashes and extract the file upload meta 
    	// data stored in the client session and persist those file upload model instances
    	
    	// @NOTE See description in the server side handler
    	
    	upload_con.append('<button class="btn btn-warning" id="remove_photo">Remove Photo</button>')
    					.append('<input type="hidden" name="event_photo_upload" value="' + data.result.hash + '" />');
	       
    }).on('fileuploadfail', function (e, data) {
		// Callback for failed, on aborted, or error, upload requests
		console.log('fileupload fail');
		console.log(data);
	});    	
}

/**
 * 
 */
function formatFileSize(file_size){
	//@TODO Implement function to return well formatted string with relevent
	// file size suffix e.g KB, MB, GB, and integer prefix 
	
	return file_size + ' bytes';
}

/**
 * On load routine for the document
 */
function main_onload() {
	initFiltersWindow();
	initCreatedEvents();
	initNewEventWindow();
	initGeoLocationApi();
	initFacebookApi();
	initNavBarItems();
	initFileUpload();
	initWindow();
}

/**
 * 
 * @param {Object} location
 */
function produceMarker(location){
	return new google.maps.Marker({
			map : map,
			position : location
		});
}

/**
 * 
 * @param {Object} location
 * @param {Object} image_url
 */
function produceMarkerWithImage(location, image_url){
	return new google.maps.Marker({
			map : map,
			position : location,
			icon : image_url
		});
}

/**
 * 
 * @param {Object} fields
 * @param {Object} image_url
 */
function produceEventMarker(fields, image_url){
	var lat = eval(fields.latitude).toFixed(14);
	var lng = eval(fields.longitude).toFixed(14);
		
	var location = new google.maps.LatLng(lat, lng);

	if(image_url){
		return produceMarkerWithImage(location, image_url);	
	}else{	
		return produceMarker(location);	
	}
}

/**
 * 
 * @param {Object} events
 * @param {Object} image_url
 */
function produceEventMarkers(events, image_url){
	console.log('producing event markers');
	
	var event_count = events.length;
	var markers = [];
	
	for(var i = 0; i < event_count; i++){
		
		// Extract the event object and the fields attribute 
		var event = events[i];
		var fields = event.fields;
	
		var event_data = {
			'title' : fields.title,
			'address' : fields.address,
			'datetime' : fields.event_date,
			'description' : fields.description
		};
		
		// Use the default event marker markup factory method
		var windowMarkup = eventMarkerMarkup(event_data);
		
		// Produce a marker for the event with the default icon
		var marker = produceEventMarker(fields);
				
		markers.push( [marker, windowMarkup] );		
		
		// @TODO May want to be able to index the marker and window markup
		// since if we delete the marker, e.g Delete operation on an Event,
		// we will also want to deallocate the memory associated with the marker
		// window markup
		
		// Create an index on the event PK to the marker for later use
		marker_index[event.pk] = marker;
	}
	
	return markers;
}

/**
 * 
 * @param {Object} markers
 * @param {Object} index
 */
function hideEventMarkers(markers, index){
	console.log('Hiding event markers at index: ' + index);
	
	var length = markers.length;
	for(var i = 0; i < length; i++){
		var marker = markers[i][0];
		marker.setVisible(false);
	}
}

/**
 * 
 * @param {Object} markers
 * @param {Object} index
 */
function showEventMarkers(markers, index){
	console.log('Showing event markers at index: ' + index);
	
	var length = markers.length;
	for(var i = 0; i < length; i++){
		var marker = markers[i][0];
		marker.setVisible(true);
	}	
}

/**
 * 
 * @param {Object} markers
 * @param {Object} visible
 */
function renderEventMarkers(markers, visible){	
	console.log('Rendering event markers');
	
	var event_count = markers.length;
	
	for(var i = 0; i < event_count; i++){
		var m = markers[i];
		
		if(visible){
			gmapsSetMarker(m[0], m[1], false);
		}else{
			m[0].setVisible(false);
			gmapsSetMarker(m[0], m[1], false);
		}
	}
}

/**
 * 
 * @param {Object} marker
 * @param {Object} window_markup
 * @param {Object} centerOnMarker
 */
function gmapsSetMarker(marker, window_markup, centerOnMarker){
	console.log('Setting marker');
	
	if(centerOnMarker){
		var location = new google.maps.LatLng(marker.getPosition().lat(), marker.getPosition().lng());
		map.setCenter(location);
	}
	
	var infowindow = new google.maps.InfoWindow({
		content : window_markup
	});
	
	// Add display info window to marker onclick event handler
	google.maps.event.addListener(marker, 'click', function() {
    	infowindow.open(map,marker);
  	});
}

/**
 * 
 * @param {Object} e
 */
function goToOwnedEvent(e){
	console.log('Navigating to client owned event');
}

/**
 * 
 * @param {Object} position
 */
function goHome(position){
	console.log('Navigating to client current location');
	
	var lat = position.coords.latitude;
 	var lng = position.coords.longitude; 
 	
 	// Center the map around the clients current location
 	map.setCenter(new google.maps.LatLng(lat, lng));
}

/**
 * 
 * @param {Object} data
 */
function create_event(data) {
	console.log('Creating new event');
	console.log(data);
	
	var fields = data.fields;
	
	// List item markup
	var markup = 
				'<li class="my_event_li">\
					<div class="event_owner" data-event_id="' + data.pk + '">\
						<span class="event_title">' + fields.title + '</span>\
						<span class="event_date">' + fields.event_date + '</span>\
						<p>' + fields.description + '</p>\
					</div>\
				</li>';
	
	var my_events_list = $('#my_events_list');
	
	var my_events_header = $('#my_events_header');
	var events_list_size = my_events_header.attr('data-events_created_list_length');
	
	my_events_header.text('Events Created ('+ (eval(events_list_size) + 1) +')');
	
	if(eval(events_list_size) === 0){
		// Remove the li for no events currently in my events list
		my_events_list.find('li').remove();
	}
	
	// Prepend the new event markup to the clients list of created events
	my_events_list.prepend( $(markup) );
}

/**
 * 
 * Full docs on the response object can be found in the documentation
 * for FB.getLoginStatus().
 * 
 * @param {Object} response
 */
function fbStatusChangeCallback(response) {
	console.log('FB status change event');
	console.log(response);

	// The response object is returned with a status field that lets the
	// app know the current login status of the person.
	if (response.status === 'connected') {
		// Logged into your app and Facebook.

		var accessToken = response.authResponse.accessToken;
		var userId = response.authResponse.userID;

	} else if (response.status === 'not_authorized') {
		// The person is logged into Facebook, but not your app.
	} else {
		// The person is not logged into Facebook, so we're not sure if
		// they are logged into this app or not.
	}
}

/**
 * 
 * @param {Object} position
 */
function geo_success(position) {
	var lat = position.coords.latitude;
	var lng = position.coords.longitude;
	
	// Need DOM node
	var mapcanvas = document.getElementById('map-canvas');

	// Make sure gmaps not already initialized
	if (mapcanvas.children.length === 0) {
		// Init google maps
		initializeMap(lng, lat);
	} else {
		// Google maps already present in DOM
	}
}

/**
 * 
 * @param {Object} lng
 * @param {Object} lat
 */
function initializeMap(lng, lat) {

	//@TODO - This is Sydney, Australio, update to world view, or maybe educated guess of client pos
	//Maybe use Google service as fallback
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
	
	// Home marker markup
	var gmapsMarkerHomeDisplay = 
		'<div class="event_marker_display">\
			<span class="home_marker_title">You are here</span>\
		</div>';
		
	// Home marker icon	
	var image = 'http://labs.google.com/ridefinder/images/mm_20_blue.png';
	
	var marker = produceMarkerWithImage(new google.maps.LatLng(lat, lng), image);
	
	// No need to center on marker, since map is already centered on client initial location
	gmapsSetMarker(marker, gmapsMarkerHomeDisplay, false);
	
	// Google Maps map object initialized, Create and render all the event markers
	
	// Push to index 0
	event_markers.push( produceEventMarkers(events_in_area) );
				
	// This is the on create event functionality. We render the area events initially so
	// we render them as visible
	renderEventMarkers(event_markers[0], true);
				
	// Push to index 1
	event_markers.push( produceEventMarkers(events_created) );
				
	// We also render the event markers for the other functions but render them as invisible
	// since they are not part of the on create functionality.
	renderEventMarkers(event_markers[1], false);

	// @TODO when planned events is developed, include planned events in the initialization
}

/**
 * Callback routine to invoke when their when a drag event ends (stops)
 * on the map canvas
 * 
 */
function gmapsEvent_DragEnd() {
	var center = map.getBounds().getCenter();
	
	console.log('Drag end: map center: ' + center);
	
	// @TODO Should invoke an XHR request to check for new events in the new 
	// search area, and display the number of possible new results in the #refresh results
	// list item as a notice of possible new events if a refresh is performed
	
	
}

/**
 * 
 */
function gmapsEvent_ZoomChange() {
	// @TODO Ensure the units of the calculated view port radius
	var r = curViewPortRadius(map);

	console.log("Google Maps zoom change event fired");
	console.log("Radius at current zoom level: " + r);
}

/**
 * 
 * @param {Object} event
 */
function gmapsEvent_Click(event) {
	var latlng = event.latLng;

	console.log('Google Maps click even fired');
	console.log('Click event latlng: ' + latlng);
	
	//@Attention : Not using dialog anymore so have to differentiate another way
	//@TODO We can use the current url hash
	if (window.location.hash === '#new_event' && $('#map_click_event_location').is(':checked') === true ) {
		
		// Reverse geocode request to find address	
    		geocoder.geocode({'latLng': latlng}, 
    		function(results, status) {
      			if (status == google.maps.GeocoderStatus.OK) {
        			if (results[0]) {
        				
        				console.log('Google maps geocode results');
        				console.log(results);
				        
				        // Set the address of the event form
				        $('#event_location').val(results[0].formatted_address);
				        
				        // Set the form lat,lng hidden fields to avoid a duplicate geocoding lookup
				        $('#event_lat').val(eval(latlng.lat()).toFixed(14));
				        $('#event_lng').val(eval(latlng.lng()).toFixed(14));
        			}
      			} else {
        			console.log("Geocoder failed due to: " + status);
      			}
    		}); 
	} else {
    	// Map click but new event dialog is not open and map click location specification not checked
	}
}

/**
 * 
 * @param {Object} map
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
 * @param {Object} form
 */
function processNewEvent(form) {
	console.log('Processing new event form submission');
	console.log(form.serialize());
	
	// Extract the form data
	var title = form.find("input[name='title']").val();
	var address = form.find("input[name='address']").val();
	var type = form.find("input[name='type']").val();
	var datetime = form.find("input[name='event_date']").val();
	var description = form.find("textarea[name='description']").val();
	var lat = form.find("input[name='latitude']").val();
	var lng = form.find("input[name='longitude']").val();
	
	// @Note - This feels like duplicate work, 
	// @TODO Eliminate the need to extract all this form data 
	
	// Format the data in object notation format for the event marker markup
	// factory 
	var event_marker_data = {
		'title' : title,
		'address' : address,
		'datetime' : datetime,
		'description' : description
	};
	
	// Use the default event marker markup factory method
	var markerEventDisplay = eventMarkerMarkup(event_marker_data);
	
	if(lat === '' || lng === ''){
		// Obtain lat,lng, conversion from address with geocode api
	
		console.log('Address to obtain from Geocode API');
		console.log(address);
		
		geocoder.geocode({
			'address' : address
			}, 
			
			function(results, status) {
				if (status == google.maps.GeocoderStatus.OK) {
					console.log('Google maps geocoding response');
					console.log(results);
					
					// Set the form lat, and lng, fields since we dont have them
					var lat = eval($('#event_lat').val(results[0].geometry.location.lat())).toFixed(14);
					var lng = eval($('#event_lng').val(results[0].geometry.location.lng())).toFixed(14);
					
					// @TODO Should set the marker to invisible unless the current tab panel is
					// created events
					var marker = produceMarker(new google.maps.LatLng(lat, lng));
					
					// Create the google maps marker window for the event
					gmapsSetMarker(marker, markerEventDisplay, true);
					
					// Add the event to the database
					persistNewEvent(form, marker);
					
					event_markers[CREATED_EVENTS_IDX].push( [marker, markerEventDisplay] );	
					
			} else {
				// Geocode failed, check the status code
				console.log('Geocode request failed');
			}
		});
	
	// @TODO Implement the need for this duplicate code in the two branches of the if/else
	
	}else{
		// No geocode api request needed
		console.log('No geocode api request needed');
		
		// @TODO Should set the marker to invisible unless the current tab panel is
		// created events
		var marker = produceMarker(new google.maps.LatLng(lat, lng));
		
		// Add the event to the database
		persistNewEvent(form, marker);
					
		// Create the google maps marker window for the event
		gmapsSetMarker(marker, markerEventDisplay, true);
		
		event_markers[CREATED_EVENTS_IDX].push( [marker, markerEventDisplay] );	
	}
}

/**
 * 
 * @param {Object} event
 */
function eventMarkerMarkup(event){
	return '<div class="event_marker_display">\
				<h5 class="event_marker_display_title">' + event.title + '</h5>\
				<p class="event_marker_display_address">' + event.address + '</p>\
				<p class="event_marker_display_datetime">' + event.datetime + '</p>\
				<p class="event_marker_display_description">' + event.description + '</p>\
			</div>'; 
}

/**
 * 
 * @param {Object} form
 */
function persistNewEvent(form, marker){
	console.log('Persisting new event');
	
	// XHR setup
	xhrSetup();

	// Persist the new event
	$.ajax({
		dataType : 'json',
		type: 'POST',
		url : '/Event/Submit/',
		data : $(form).serialize(),
		beforeSend : function(jqXHR, settings){
			// show the loading GIF
			loading(true);
			putStatusMessage('Loading');
			showStatusMessage();
			
		},
		success : function(data) {			
			console.log('Response from new event submission');
			console.log(data);
			
			// @TODO Must see what None type over the wire in JSON form looks like
			// to be able to interpret error, or define an Object representing an Error
			// and serialize, and return that

			if(data){				
				// Hide the loading GIF
				clearAndHideStatusMessage();
				loading(false);
				
				// Notice of new event posting to server
				putStatusMessage('You\'re Event Has Posted');
				showStatusMessage();
				
				setTimeout(function(){
					clearAndHideStatusMessage();
				}, 3000);
				
				// Clear the new event form fields
				clearFormFields(form);
				
				marker_index[data.pk] = marker;
				
				// Add the new event to the list of the clients created events
				console.log('Debug: Creating new event element in markup');
				create_event(data);
				
				$('#event_content_window').click();
				
				// Supposed to open the events created window
				// @TODO Make sure this works
				$('#events_created').click();
			}else{
				
				// Return a more descriptive error message from the server to include as the message
				// Add an error message to the form
				$(form).append($('<p style="color: #f00;">An error occured during processing of you\'re event</p>'));
			}
		}
	});	
}

/**
 * 
 */
function checkForNewEvents(positon){
	console.log('Checking for new events');
	
	// XHR setup
	xhrSetup();
}

/**
 * 
 */
function loading(status){
	var loading = $('#loading');
	
	if(status){
		loading.show();
	}else{
		loading.hide();
	}
}

/**
 * 
 */
function putStatusMessage(message){
	var r = $('#status_message').find("span.notification");
	r.text(message);
}

/**
 * 
 */
function showStatusMessage(){
	$('#status_message').show();
}

function clearAndHideStatusMessage(){
	$('#status_message').find(".notification").text('');
	$('#status_message').hide();
}

/**
 * Clear all the form fields im the form
 * 
 * @param {Object} form The form to clear
 */
function clearFormFields(form){
	// Clear the input fields
	$(form).find("input, textarea").val("");	
	
	// Remove any existing photo uploads from the form
	$('#files').empty();
	
	//Reset the file upload progress bar
	$('#progress .progress-bar').css(
            'width',
            0 + '%'
        );
}

/**
 * These HTTP methods do not require CSRF protection
 * 
 * @param {Object} method The HTTP method being used 
 */
function csrfSafeMethod(method) {
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

/**
 * Retrieve the CSRF token cookie and set the X-CSRFToken 
 * HTTP request header prior to any XHR requests
 * 
 */
function xhrSetup(){
	csrftoken = $.cookie('csrftoken');
	
	$.ajaxSetup({
		crossDomain: false, // obviates need for sameOrigin test
		beforeSend: function(xhr, settings) {
			     		if (!csrfSafeMethod(settings.type)) {
			     			xhr.setRequestHeader("X-CSRFToken", csrftoken);
			     		}
			   		}
	});
}

$(document).ready(main_onload);
