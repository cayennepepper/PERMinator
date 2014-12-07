/*global Backbone */
var app = app || {};

(function () {
	'use strict';

	app.ProfPerm = Backbone.Model.extend({
		
		defaults:  {
			sectionID: 1,
			showBlurb: false, 
			errorMsg: null,
		}
	});
})();