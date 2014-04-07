'use strict';

/* Services */
var flaskenbergServices = angular.module('flaskenbergServices', ['ngResource']);
 
flaskenbergServices.factory('User', ['$resource',
  function($resource){
    return $resource(
      'api/user/:userId', 
      {
        userId: ''
      }, 
      {
        query: {
          method:'GET', 
          isArray:true
        }
      }
    );
  }]);

flaskenbergServices.factory('Task', ['$resource',
  function($resource){
    return $resource('api/task/:taskId', {}, {
      query: {method:'GET', params:{taskId:''}, isArray:true}
    });
  }]);