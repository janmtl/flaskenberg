'use strict';

/* Controllers */
var flaskenbergControllers = angular.module('flaskenbergControllers', []);

flaskenbergControllers.controller('SurveyCtrl', ['$scope', 'User', 'Task', 'Question', 'Answer', 'Session',
  function($scope, User, Task, Question, Answer, Session) {
    

    var next_question = function(){
      //Get the next question
      User.next({userId: Session.get_user_id()}, function(res){
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

flaskenbergControllers.controller('UserCtrl', ['$scope', '$location', 'User', 'Session',
  function($scope, $location, User, Session) {


    //Listen to question progression
    $scope.$on('next_question', function() { init(); });

    //Save new users
    $scope.submit = function(){
      var new_user = new User($scope.user)
      new_user.$save(function(u){
        Session.set_user_id(u.id);
        $location.path('/survey');
      });
    }

    //Controller startup
    var init = function(){
      if ($location.path() === '/survey') {
        $scope.user = User.get({userId: Session.get_user_id()});
        $scope.showUser = true;
      } else {
        $scope.showUser = false;
      }
    };
    $scope.$on('$routeChangeSuccess', function(){ init(); });


  }]);