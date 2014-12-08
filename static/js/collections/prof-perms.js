/*global Backbone */
var app = app || {};

(function () {
	'use strict';

	var ProfPerms = Backbone.Collection.extend({
		// Reference to this collection's model.
		model: app.ProfPerm,
		comparator: function(model){
			return model.get('status');
		}
	});

	// Create our global collection of sections.
	app.prof_perms = new ProfPerms();
})();
