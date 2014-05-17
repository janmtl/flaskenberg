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
    .otherwise({
      redirectTo: '/survey'
    });
}]);