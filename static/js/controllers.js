'use strict';

/* Controllers */
var flaskenbergControllers = angular.module('flaskenbergControllers', []);

flaskenbergControllers.controller('UsersCtrl', ['$scope', 'User',
  function($scope, User) {
    $scope.users = User.query();
  }]);

flaskenbergControllers.controller('TasksCtrl', ['$scope', 'Task',
  function($scope, Task) {
    $scope.tasks = Task.query();
  }]);

flaskenbergControllers.controller('QuestionsCtrl', ['$scope', 'Question',
  function($scope, Question) {
    $scope.questions = Question.query();
  }]);

flaskenbergControllers.controller('AnswersCtrl', ['$scope', 'Answer',
  function($scope, Answer) {
    $scope.answers = Answer.query();
  }]);