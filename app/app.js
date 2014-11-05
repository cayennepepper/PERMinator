'use strict';

// Declare app level module which depends on views, and components
angular.module('myApp', [
  'ngRoute',
  'myApp.view1',
  'myApp.view2',
  'myApp.version'
]).
config(['$routeProvider', function($routeProvider) {
  $routeProvider.otherwise({redirectTo: '/view1'});
}]);

function TutoCtrl($scope, $http) {

    $scope.send = function() {
        $http.post('/profile', $scope.profile)
             .success(function(){alert('ok')})
             .error(function(){alert('fail')});
    }

}
