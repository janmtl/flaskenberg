'use strict';

/* Controllers */
var flaskenbergControllers = angular.module('flaskenbergControllers', []);

flaskenbergControllers.controller('SurveyCtrl', ['$scope', 'User', 'Task', 'Question', 'Answer',
  function($scope, User, Task, Question, Answer) {

    //Get the next question
    User.next({userId: 1}, function(res){
      $scope.answer   = Answer.get({answerId: res.answer_id});
      $scope.task     = Task.get({taskId: res.task_id});
      $scope.question = Question.get({questionId: res.question_id});
    });
    
    //Submit
    $scope.submit = function(){
      Answer.save($scope.answer);
    };
  }]);