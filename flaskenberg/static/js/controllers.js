'use strict';

/* Controllers */
var flaskenbergControllers = angular.module('flaskenbergControllers', []);

flaskenbergControllers.controller('SurveyCtrl', ['$scope', 'User', 'Task', 'Question', 'Answer',
  function($scope, User, Task, Question, Answer) {
    
    
    var next_question = function(){
      //Get the next question
      User.next({userId: 1}, function(res){
        $scope.answer   = Answer.get({answerId: res.answer_id});
        $scope.task     = Task.get({taskId: res.task_id});
        $scope.question = Question.get({questionId: res.question_id});
      });
      $scope.$emit('next_question');
    };
    
    //Submit
    $scope.submit = function(){
      Answer.save($scope.answer);
      next_question();
    };

    //Controller startup
    var init = function(){
      next_question();
    };
    $scope.$on('$routeChangeSuccess', function(){ init(); });


  }]);

flaskenbergControllers.controller('UserCtrl', ['$scope', 'User',
  function($scope, User) {


    //Listen to question progression
    $scope.$on('next_question', function() {
      $scope.user = User.get({userId: 1});
    });

    //Controller startup
    var init = function(){
      $scope.user = User.get({userId: 1});
    };
    $scope.$on('$routeChangeSuccess', function(){ init(); });


  }]);