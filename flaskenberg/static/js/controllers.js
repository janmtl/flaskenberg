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

flaskenbergControllers.controller('SurveyCtrl', ['$scope', 'User', 'Task', 'Question', 'Answer',
  function($scope, User, Task, Question, Answer) {
    User.get({userId: 1}, function(res){
      $scope.tasks =  res.tasks;
      angular.forEach($scope.tasks, function(task, index){
        Task.get({taskId: task.id}, function(res){
          this[index].questions = res.questions;
          angular.forEach($scope.tasks[index].questions, function(question, index){
            Question.get({questionId: question.id}, function(res){
              this[index].choices = res.choicesl
            });
          }, this[index].questions);
        });
      }, $scope.tasks);
    });
  }]);