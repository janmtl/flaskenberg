'use strict';

/* Controllers */
var flaskenbergControllers = angular.module('flaskenbergControllers', []);

flaskenbergControllers.controller('UsersCtrl', ['$scope', 'User',
  function($scope, User) {
    $scope.user = User.query();
  }]);

flaskenbergControllers.controller('TasksCtrl', ['$scope', 'Task',
  function($scope, Task) {
    $scope.tasks = Task.query();
  }]);