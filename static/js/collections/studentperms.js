/*global Backbone */
var app = app || {};

(function () {
	'use strict';

	var Studentperms = Backbone.Collection.extend({
		// Reference to this collection's model.
		model: app.Studentperm,
	});

	// Create our global collection of **Todos**.
	app.studentperms = new Studentperms();
})();
