window.Blog = angular.module('Blog', ['ngRoute', 'restangular', 'LocalStorageModule'])

.config(function($routeProvider, RestangularProvider) {
	RestangularProvider.setBaseUrl('http://localhost:5000/');

	$routeProvider
        .when('/', {
            controller: 'studentHomeController',
            templateUrl: partialsDir + '/home/detail.html'
        })
        .when('/sessions/create', {
            controller: 'SessionCreateCtrl',
            templateUrl: partialsDir + '/session/create.html',
            resolve: {
                redirectIfAuthenticated: redirectIfAuthenticated('/posts/create')
            }
        })
        .when('/sessions/destroy', {
            controller: 'SessionDestroyCtrl',
            templateUrl: partialsDir + '/session/destroy.html'
        })
        .when('/users/create', {
            controller: 'UserCreateCtrl',
            templateUrl: partialsDir + '/user/create.html'
        })
        .when('/posts/create', {
            controller: 'PostCreateCtrl',
            templateUrl: partialsDir + '/post/create.html',
            resolve: {
                redirectIfNotAuthenticated: redirectIfNotAuthenticated('/sessions/create')
            }
        });
   }
