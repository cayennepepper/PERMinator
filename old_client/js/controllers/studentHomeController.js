// <div ng-app="" ng-controller="studentHomeController">
var myApp = angular.module('permApp', []);
myApp.controller('studentHomeController', ['$scope', function($scope) {
	$scope.firstName = 'placeHolder';
    $scope.john = function(){
    	$scope.firstName = 'John';
    };
    $scope.lastName = 'Doe';
}]);




// First Name: <input type="text" ng-model="firstName"><br>
// Last Name: <input type="text" ng-model="lastName"><br>
// <br>
// Full Name: {{firstName + " " + lastName}}

// </div>

// <script>
// function studentController($scope) {
//     $scope.firstName = "John";
//     $scope.lastName = "Doe";
// }
// </script>