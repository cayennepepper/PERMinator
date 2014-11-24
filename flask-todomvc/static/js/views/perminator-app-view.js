/*global Backbone, jQuery, _, ENTER_KEY */
var app = app || {};

(function ($) {
	'use strict';

	// The Application
	// ---------------

	// Our overall **AppView** is the top-level piece of UI.
	app.AppView = Backbone.View.extend({

		// Instead of generating a new element, bind to the existing skeleton of
		// the App already present in the HTML.
		el: '#todoapp',

		// At initialization we bind to the relevant events on the `Todos`
		// collection, when items are added or changed. Kick things off by
		// loading any preexisting todos that might be saved in *localStorage*.
		initialize: function () {
			this.$list = $('#todo-list');

			this.listenTo(app.prof_sections, 'add', this.addOne);
			this.listenTo(app.prof_sections, 'reset', this.addAll);

			// this.listenTo(app.prof_perms, 'add', this.addOne);
			// this.listenTo(app.prof_perms, 'reset', this.addAll);
		},

		// Add a single todo item to the list by creating a view for it, and
		// appending its element to the `<ul>`.
		addOne: function (section) {
			var view = new app.SectionView({ model: section });
			this.$list.append(view.render().el);
		},

		// Add all items in the **Todos** collection at once.
		addAll: function () {
			this.$list.html('');
			app.prof_sections.each(this.addOne, this);
			// app.prof_perms.each(this.addOne, this);
		},


		// addOne: function (prof-perm) {
		// 	var view = new app.ProfPermView({ model: prof-perm });
		// 	this.$list.append(view.render().el);
		// },


	});
})(jQuery);
