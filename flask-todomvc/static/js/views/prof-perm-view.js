/*global Backbone, jQuery, _, ENTER_KEY, ESC_KEY */
var app = app || {};

(function ($) {
	'use strict';

	app.ProfPermView = Backbone.View.extend({
		//... is a list tag.
		tagName:  'li',

		// Cache the template function for a single item.
		template: _.template($('#prof-perm-template').html()),

		// The DOM events specific to an item.
		events: {
			'dblclick expdate': 'edit',
			'keypress .edit': 'updateOnEnter',
			'keydown .edit': 'revertOnEscape',
		},

		// Re-render the titles of the todo item.
		render: function () {
			this.$el.html(this.template(this.model.toJSON()));
			return this;
		},
	});
})(jQuery);

