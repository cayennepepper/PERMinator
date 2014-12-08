/*global Backbone, jQuery, _, ENTER_KEY, ESC_KEY */
var app = app || {};

(function ($) {
	'use strict';

	// Studentperm Item View
	// --------------

	app.StudentpermView = Backbone.View.extend({
		//Each view is a row in the table described in studentHome.html
		tagName:  'tr',

		// Cache the template function for a single item.
		template: _.template($('#studentperm-template').html()),

		// The DOM events specific to an item.
		events: {
			'click #student-perm-display-blurb': 'edit',
			'click #student-perm-display-sectionrank': 'edit',
			'click #perm-cancel-button': 'cancelPerm',
			'dblclick label': 'edit',
			'keypress': 'updateOnEnter',
			// 'click .destroy': 'clear',
			'keydown': 'revertOnEscape',
			'blur .edit': 'close'
		},

		// The TodoView listens for changes to its model, re-rendering. Since there's
		// a one-to-one correspondence between a **Todo** and a **TodoView** in this
		// app, we set a direct reference on the model for convenience.
		initialize: function () {
			this.$blurbEdit = $('#student-perm-display-blurb');
			this.$sectionRankEdit = $('#student-perm-display-sectionrank');

			this.listenTo(this.model, 'change', this.render);
			this.listenTo(this.model, 'destroy', this.remove);
			this.listenTo(this.model, 'visible', this.toggleVisible);


		},

		// Re-render the titles of the todo item.
		render: function () {
			// Backbone LocalStorage is adding `id` attribute instantly after creating a model.
			// This causes our TodoView to render twice. Once after creating a model and once on `id` change.
			// We want to filter out the second redundant render, which is caused by this `id` change.
			// It's known Backbone LocalStorage bug, therefore we've to create a workaround.
			// https://github.com/tastejs/todomvc/issues/469
			// if (this.model.changed.id !== undefined) {
			// 	return;
			// }

			this.$el.html(this.template(this.model.toJSON()));
			return this;
		},


		// If you're pressing `escape` we revert your change by simply leaving
		// the `editing` state.
		revertOnEscape: function (e) {
			if (e.which === ESC_KEY) {
				this.$el.removeClass('editing');
			}
		},

		// Switch this view into `"editing"` mode, displaying the input field.
		edit: function () {
			this.$el.addClass('editing');
		},

		// Close the `"editing"` mode, saving changes to the perm.
		close: function () {
			var untrimmedBlurbValue = this.$('.b_input_class').val();
			var blurbValue = untrimmedBlurbValue.trim();
			var untrimmedRankValue = this.$('.rank_input_class').val()
			var rankValue = untrimmedRankValue.trim();

			// We don't want to handle blur events from an item that is no
			// longer being edited. Relying on the CSS class here has the
			// benefit of us not having to maintain state in the DOM and the
			// JavaScript logic.
			if (!this.$el.hasClass('editing')) {
				return;
			}

			if (blurbValue && rankValue) {
				this.model.save({ sectionRank: rankValue, blurb: blurbValue}, 
					{dataType: 'text',
						error: function(model, response){
						model.set({errorMsg: response.responseText});
						model.trigger('change');
				}, success: function(model, response){
						model.set({errorMsg: null});
						model.trigger('change');
				}})

				if (blurbValue !== untrimmedBlurbValue || rankValue != untrimmedRankValue) {
					this.model.trigger('change');
				}
			} else {
			}

			this.$el.removeClass('editing');
		},

		// If you hit `enter`, we're through editing the item.
		updateOnEnter: function (e) {
			if (e.which === ENTER_KEY) {
				this.close();
			}
		},

		cancelPerm: function (){
			this.model.save({ status: "Cancelled"}, 
				{dataType: 'text',
					error: function(model, response){
						model.set({errorMsg: response.responseText});
						model.trigger('change');
				}, success: function(model, response){
						model.set({errorMsg: null});
						model.trigger('change');
				}})

		}
	});
})(jQuery);
