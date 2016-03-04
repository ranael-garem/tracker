(function () {
  'use strict';

  angular
    .module('tracker.logger.services')
    .factory('Trackers', Trackers);

  Trackers.$inject = ['$http'];


  function Trackers($http) {

    var Trackers = {
      all: all,
      create_tracker: create_tracker,

    };

    return Trackers;

    function all() {
      return $http.get('/api/trackers/');
    }

    function create_tracker(title) {
      return $http.post('/api/trackers/', {
        title: title
      }).then(successFn, errorFn);


      function successFn(data, status, headers, config) {
        window.location = '/trackers';
      }

      function errorFn(data, status, headers, config) {
        return data.data;
      }
    }

  }
})();