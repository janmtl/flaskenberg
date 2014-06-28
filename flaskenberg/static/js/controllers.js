'use strict';

/* Controllers */
var flaskenbergControllers = angular.module('flaskenbergControllers', []);

flaskenbergControllers.controller('SurveyCtrl', ['$scope', 'User', 'Task', 'Question', 'Answer',
  function($scope, User, Task, Question, Answer) {
    User.get({userId: 1}, function(res){
      $scope.user_id = res.id;
      $scope.tasks   = res.tasks;
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
    $scope.submit = function(answer){
      answer.user_id = $scope.user_id;
      Answer.save(answer);
    };
  }]);