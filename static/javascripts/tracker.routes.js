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
    }).when('/tracker/+:tracker_id/update', {
      controller: 'TrackerController',
      controllerAs: 'vm',
      templateUrl: '/static/templates/logger/tracker-update.html'
    }).when('/dashboard/+:tracker_id', {
      controller: 'DashboardController',
      controllerAs: 'vm',
      templateUrl: '/static/templates/logger/dashboard.html'
    }).when('/heatmaps/+:tracker_id', {
      controller: 'TrackerController',
      controllerAs: 'vm',
      templateUrl: '/static/templates/logger/heatmaps.html'
    }).when('/sessions/+:tracker_id', {
      controller: 'TrackerController',
      controllerAs: 'vm',
      templateUrl: '/static/templates/logger/sessions.html'
    }).when('/session/+:session_id', {
      controller: 'SessionReplayController',
      controllerAs: 'vm',
      templateUrl: '/static/templates/logger/session-replay.html'
    }).otherwise('/')};
  
})();