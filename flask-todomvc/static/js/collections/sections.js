/*global Backbone */
var app = app || {};

(function () {
	'use strict';

	var Sections = Backbone.Collection.extend({
		// Reference to this collection's model.
		model: app.Section,
	});

	// Create our global collection of sections.
	app.prof_sections = new Sections();
})();
