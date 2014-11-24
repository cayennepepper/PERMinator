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
			this.$prof_perm_list = $('#prof-perm-list');
			this.$list = $('#todo-list')

			this.listenTo(app.prof_sections, 'add', this.addOneSection);
			this.listenTo(app.prof_sections, 'reset', this.addAllSections);

			this.listenTo(app.prof_perms, 'add', this.addOnePERM);
			this.listenTo(app.prof_perms, 'reset', this.addAllPERMs);
			this.$studentpermList = $('#studentperm-list');

			this.listenTo(app.studentperms, 'add', this.addOneStudentPerm);
			this.listenTo(app.studentperms, 'reset', this.addAllStudentPerms);
		},

		// Add a single todo item to the list by creating a view for it, and
		// appending its element to the `<ul>`.
		addOneSection: function (section) {
			var view = new app.SectionView({ model: section });
			this.$list.append(view.render().el);
		},

		// Add all items in the **Todos** collection at once.
		addAllSections: function () {
			this.$list.html('');
			app.prof_sections.each(this.addOneSection, this);
		},


		addOnePERM: function (prof_perm) {
			var view = new app.ProfPermView({ model: prof_perm });
			this.$prof_perm_list.append(view.render().el);
		},

		// Add all items in the **Todos** collection at once.
		addAllPERMs: function () {
			this.$prof_perm_list.html('');
			app.prof_perms.each(this.addOnePERM, this);
		},

		addOneStudentPerm:  function(studentperm) {
			var view = new app.StudentpermView({model: studentperm});
			this.$studentpermList.append(view.render().el);
		},

		addAllStudentPerms: function () {
			this.$studentpermList.html('');
			app.studentperms.each(this.addOneStudentPerm, this);
		}


	});
})(jQuery);