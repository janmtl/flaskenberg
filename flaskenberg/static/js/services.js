'use strict';

/* Services */
var flaskenbergServices = angular.module('flaskenbergServices', ['ngResource', 'LocalStorageModule']);
 
flaskenbergServices.factory('User', ['$resource', function ($resource){
    return $resource(
      'api/user/:userId', 
      {userId: '@id'},
      {
        'query': {
          isArray: true,
          transformResponse: function (data){ return angular.fromJson(data)["objects"]; }
        },
        'next': {
          method: 'GET',
          isArray: false,
          url: 'api/user/:userId/next'
        }
      }
    );
  }]);

flaskenbergServices.factory('Task', ['$resource', function ($resource){
    return $resource(
      'api/task/:taskId', 
      {taskId: '@id'}, 
      {
        'query': {
          isArray: true,
          transformResponse: function (data){ return angular.fromJson(data)["objects"]; }
        }
      }
    );
  }]);

flaskenbergServices.factory('Question', ['$resource', function ($resource){
    return $resource(
      'api/question/:questionId', 
      {questionId: '@id'}, 
      {
        'query': {
          isArray: true,
          transformResponse: function (data){ return angular.fromJson(data)["objects"]; }
        }
      }
    );
  }]);

flaskenbergServices.factory('Answer', ['$resource', function ($resource){
    return $resource(
      'api/answer/:answerId', 
      {answerId: '@id'}, 
      {
        'query': {
          isArray: true,
          transformResponse: function (data){ return angular.fromJson(data)["objects"]; }
        },
        'save':{
          method: 'PUT'
        }
      }
    );
  }]);

flaskenbergServices.factory('Session', ['User', 'localStorageService', function(User, localStorageService){
    return {
      get_user: function(){
        return {
          id:      localStorageService.get('user_id'),
          hash_id: localStorageService.get('user_hash_id'),
        };
      },
      set_user: function(user){
        if (user.id){      localStorageService.set('user_id', user.id); }
        if (user.hash_id){ localStorageService.set('user_hash_id', user.hash_id); }
      }
    }
  }]);