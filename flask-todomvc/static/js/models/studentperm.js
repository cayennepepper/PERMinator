/*global Backbone */
var app = app || {};

(function () {
	'use strict';

	app.Studentperm = Backbone.Model.extend({
		// Default attributes for the section
		defaults: {
			section:'',
			studentID:'',
			blurb:'',
			status:'',
			submissionTime:'',
			expirationTime:'',
			sectionRank:'',
		},

		// Sample
		changeDefaultExpiration: function (newExpirationDelta) {
			// this.save({
			// 	defaultExpiration: newExpirationDelta
			// });
		}
	});
})();