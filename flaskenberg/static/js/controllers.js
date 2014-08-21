'use strict';

/* Controllers */
var flaskenbergControllers = angular.module('flaskenbergControllers', []);

flaskenbergControllers.controller('SurveyCtrl', ['$scope', 'User', 'Task', 'Question', 'Answer', 'Session',
  function($scope, User, Task, Question, Answer, Session) {
    

    var next_question = function(){
      //Get the next question
      User.next({userId: Session.get_user().id}, function(res){
        $scope.answers  = res.objects;
        $scope.task     = Task.get({taskId: res.task_id}, function(res){
          $scope.questions = [];
          angular.forEach(res.questions, function(question, index){
            $scope.questions[index] = Question.get({questionId: question.id});
          });
        });
      });
      $scope.$emit('next_question');
    };
    
    //Submit
    $scope.submit = function(){
      angular.forEach($scope.answers, function(answer){
        Answer.save(answer);
      });
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
        Session.set_user(u);
        $location.path('/survey');
      });
    }

    //Controller startup
    var init = function(){
      if ($location.path() === '/survey') {
        $scope.user         = User.get({userId: Session.get_user().id});
        $scope.showUser     = true;
      } else {
        $scope.showUser = false;
      }
    };
    $scope.$on('$routeChangeSuccess', function(){ init(); });


  }]);