/*global Backbone */
var app = app || {};

(function () {
	'use strict';

	app.Studentperm = Backbone.Model.extend({
		// Default attributes for the section
		defaults: {
			course:'',
			section:'',
			studentID:'',
			blurb:'',
			status:'',
			submissionTime:'',
			expirationTime:'',
			sectionRank:'',
			errorMsg:null
		},

	});
})();