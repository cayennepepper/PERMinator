'use strict';
angular.module('permApp', [
'ui.router',
'permApp.filters',
'permApp.services',
'permApp.directives',
'permApp.controllers'
]).config(function($stateProvider, $urlRouterProvider) {
$stateProvider
    .state('login', {
        url: "/login",
        templateUrl: "partials/login.html",
        controller : "loginController"
    })
});