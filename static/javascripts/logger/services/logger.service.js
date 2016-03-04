(function () {
  'use strict';

  angular
    .module('tracker.logger.services')
    .factory('Trackers', Trackers);

  Trackers.$inject = ['$http'];


  function Trackers($http) {

    var Trackers = {
      all: all,

    };

    return Trackers;

    function all() {
      return $http.get('/api/trackers/');
    }


  }
})();