(function () {
  'use strict';

  angular
    .module('tracker.routes')
    .config(config);

  config.$inject = ['$routeProvider'];

  /**
  * @name config
  * @desc Define valid application routes
  */
  function config($routeProvider) {
    $routeProvider.when('/register', {
      controller: 'RegisterController', 
      controllerAs: 'vm',
      templateUrl: '/static/templates/authentication/register.html'
    }).when('/login', {
      controller: 'LoginController',
      controllerAs: 'vm',
      templateUrl: '/static/templates/authentication/login.html'
    }).when('/trackers', {
      controller: 'TrackersListController',
      controllerAs: 'vm',
      templateUrl: '/static/templates/logger/trackers.html'
    }).when('/tracker/add', {
      controller: 'NewTrackerController',
      controllerAs: 'vm',
      templateUrl: '/static/templates/logger/new-tracker.html'
    }).when('/tracker/+:tracker_id', {
      controller: 'TrackerController',
      controllerAs: 'vm',
      templateUrl: '/static/templates/logger/tracker.html'
    }).otherwise('/');
  }
})();