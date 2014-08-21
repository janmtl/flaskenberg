'use strict';

/* Services */
var flaskenbergServices = angular.module('flaskenbergServices', ['ngResource', 'LocalStorageModule']);
 
flaskenbergServices.factory('User', ['$resource', 'Session', function ($resource, Session){
    return $resource(
      'api/user/:userId', 
      {userId: '@id'},
      {
        'query': {
          isArray: true,
          transformResponse: function (data){ return angular.fromJson(data)["objects"]; }
        },
        'get': {
          transformResponse: function (data){
            return {id: angular.fromJson(data).id, tally: angular.fromJson(data).tally, hash_id: Session.get_user().hash_id};
          }
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

flaskenbergServices.factory('Session', ['localStorageService', function(localStorageService){
    return {
      get_user: function(){
        return {
          id:      localStorageService.get('user_id'),
          hash_id: localStorageService.get('user_hash_id')
        };
      },
      set_user: function(user){
        if (user.id){      localStorageService.set('user_id', user.id); }
        if (user.hash_id){ localStorageService.set('user_hash_id', user.hash_id); }
      }
    }
  }]);