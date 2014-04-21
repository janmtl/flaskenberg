'use strict';

/* Services */
var flaskenbergServices = angular.module('flaskenbergServices', ['ngResource']);
 
flaskenbergServices.factory('User', ['$resource', function ($resource){
    return $resource(
      'api/user/:userId', 
      {},
      {
        query: {
          method: 'GET', 
          params: {userId:''}, 
          isArray: true,
          transformResponse: function (data){
            return angular.fromJson(data)["objects"];
          }
        }
      }
    );
  }]);

flaskenbergServices.factory('Task', ['$resource', function ($resource){
    return $resource(
      'api/task/:taskId', 
      {}, 
      {
        query: {
          method: 'GET', 
          params: {taskId:''}, 
          isArray: true,
          transformResponse: function (data){
            return angular.fromJson(data)["objects"];
          }
        }
      }
    );
  }]);

flaskenbergServices.factory('Question', ['$resource', function ($resource){
    return $resource(
      'api/question/:questionId', 
      {}, 
      {
        query: {
          method: 'GET', 
          params: {questionId:''}, 
          isArray: true,
          transformResponse: function (data){
            return angular.fromJson(data)["objects"];
          }
        }
      }
    );
  }]);

flaskenbergServices.factory('Choice', ['$resource', function ($resource){
    return $resource(
      'api/choice/:choiceId', 
      {}, 
      {
        query: {
          method: 'GET', 
          params: {choiceId:''}, 
          isArray: true,
          transformResponse: function (data){
            return angular.fromJson(data)["objects"];
          }
        }
      }
    );
  }]);

flaskenbergServices.factory('Answer', ['$resource', function ($resource){
    return $resource(
      'api/answer/:answerId', 
      {}, 
      {
        query: {
          method: 'GET', 
          params: {answerId:''}, 
          isArray: true,
          transformResponse: function (data){
            return angular.fromJson(data)["objects"];
          }
        }
      }
    );
  }]);