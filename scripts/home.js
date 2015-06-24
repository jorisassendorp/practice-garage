// define globals used in the file
/* globals _base_ */

// initiate a name space (before using it)
var __garage__ = {};

// standard function example, needs to be defined before used!
function load() {
	/**
	 * execute load for dynamic content
	 */
	// function can be plain or called inside a namespace
	__garage__.load();
}

$(function() {
	/****
	 * $(function() <code>)}
	 * contains code that will be executed when page is loaded
	 */
	load();
});

// namespace can contain functions (i prefer to use namespaces)
__garage__.load = function(){
	/**
	 * Loads the list garages
	 */
	_base_.log("loading garages");
	$.ajax({type: "GET", url:"/garages", success: function(data) {
		$('#garage-list').html(data);
	}});
};

