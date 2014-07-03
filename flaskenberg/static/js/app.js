'use strict';

/* App Module */

var flaskenberg = angular.module('flaskenberg', [
  'ui.bootstrap',
  'ngRoute',

  'flaskenbergControllers',
  'flaskenbergServices'
]).config(['$routeProvider', function ($routeProvider){
  $routeProvider
    .when('/summary', {
        templateUrl: 'templates/summary.html'
    })
    .when('/survey', {
        templateUrl: 'templates/survey.html',
        controller: 'SurveyCtrl'
    })
    .when('/register', {
        templateUrl: 'templates/register.html',
        controller: 'UserCtrl'
    })
    .otherwise({
      redirectTo: '/register'
    });
}]);