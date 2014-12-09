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
			'click .showBlurb': 'showBlurb',
			'click .hideBlurb': 'hideBlurb',
			'click .statusAccept': 'acceptStatus',
			'click .statusDeny': 'denyStatus',
			'change .statusSelect': 'selectStatus',
			'click .expdate': 'edit',
			'keypress': 'updateOnEnter',
			'keydown': 'revertOnEscape',
		},

		initialize: function() {
			this.listenTo(this.model, 'change', this.render);
		},

		// If you hit `enter`, we're through editing the item.
		updateOnEnter: function (e) {
			if (e.which === ENTER_KEY) {
				this.close();
			}
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

		showBlurb: function() {
			this.model.save({ showBlurb: true });
		},

		hideBlurb: function() {
			this.model.save({ showBlurb: false });
		},

		acceptStatus: function() {
			this.close();
			this.changeStatus("Approved");
		},

		denyStatus: function() {
			this.changeStatus("Denied");
		},

		changeStatus: function(newStatus) {
			this.model.save({ status: newStatus }, 
					{dataType: 'text',
						error: function(model, response){
						model.set({errorMsg: response.responseText});
				}, success: function(model, response){
						model.set({errorMsg: null});
				}});
			this.model.trigger('change');
		},

		selectStatus: function() {
			var newSelect = this.$('.statusSelect').val();
			if(newSelect !== "NoVal") {
				this.model.save({ status: newSelect });
				this.model.trigger('change');	
			}
		},

		render: function () {
			this.$el.html(this.template(this.model.toJSON()));
			return this;
		},

		// Close the `"editing"` mode, saving changes to the perm.
		close: function () {
			var value = this.$('.expdate').val();

			// We don't want to handle blur events from an item that is no
			// longer being edited. Relying on the CSS class here has the
			// benefit of us not having to maintain state in the DOM and the
			// JavaScript logic.
			if (!this.$el.hasClass('editing') && this.model.get('status')!="Expired") {
				return;
			}
			var trimmedValue = value.trim();

			if (trimmedValue) {
				this.model.save({ expirationTime: trimmedValue }, 
					{dataType: 'text',
						error: function(model, response){
						model.set({errorMsg: response.responseText});
						model.trigger('change');
				}, success: function(model, response){
						model.set({errorMsg: null});
						model.trigger('change');
				}});

				if (value !== trimmedValue) {
					// Model values changes consisting of whitespaces only are not causing change to be triggered
					// Therefore we've to compare untrimmed version with a trimmed one to chech whether anything changed
					// And if yes, we've to trigger change event ourselves
					this.model.trigger('change');
				}
			} else {
				this.clear();
			}

			this.$el.removeClass('editing');
		},
	});
})(jQuery);

