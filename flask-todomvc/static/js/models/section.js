/*global Backbone */
var app = app || {};

(function () {
	'use strict';

	app.Section = Backbone.Model.extend({
		//has attrs sectionID, sectionNum, enrollmentCap, defaultExpiration, courseID
		defaults:  {
			sectionNum: 0
		}
	});
})();
