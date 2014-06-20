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
    Task.next({taskId: 1}, function(res){
      console.log(res);
    });
    User.get({userId: 1}, function(res){
      $scope.user_id = res.id;
      $scope.tasks =  res.tasks;
      angular.forEach($scope.tasks, function(task, task_index){
        Task.get({taskId: task.id}, function(res){
          $scope.tasks[task_index].questions = res.questions;
          angular.forEach($scope.tasks[task_index].questions, function(question, question_index){
            Question.get({questionId: question.id}, function(res){
              $scope.tasks[task_index].questions[question_index].choices = res.choices;
            });
          });
        });
      });
    });
  }]);