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
      get: get,
      update: update,
      destroy: destroy,
      popularity: popularity,
      interactivity: interactivity,
      get_pages: get_pages,

    };

    return Trackers;

    function all() {
      return $http.get('/api/trackers/');
    }

    function create_tracker(title, url) {
      return $http.post('/api/trackers/', {
        title: title,
        url: url
      }).then(successFn, errorFn);


      function successFn(data, status, headers, config) {
        var tracker_id = data.data['id'];
        window.location = '/tracker/' + tracker_id + '/';
      }

      function errorFn(data, status, headers, config) {
        return data.data;
      }
    }

    function destroy(tracker) {
      return $http.delete('/api/trackers/' + tracker.id + '/');
    }



    function get(tracker_id) {
      return $http.get('/api/trackers/' + tracker_id + '/').then(successFn, errorFn);


      function successFn(data, status, headers, config) {
        return data.data;
      }

      function errorFn(data, status, headers, config) {
        return data.data;
      }
    }


    function update(tracker) {
      return $http.put('/api/trackers/' + tracker.id + '/', tracker);
    }


    function popularity(tracker_id) {
      return $http.get('/reports/popularity/' + tracker_id + '/').then(successFn, errorFn);


      function successFn(data, status, headers, config) {
        return data.data;
      }

      function errorFn(data, status, headers, config) {
        return data.data;
      }
    }

    function interactivity(tracker_id) {
      return $http.get('/reports/interactivity/' + tracker_id + '/').then(successFn, errorFn);


      function successFn(data, status, headers, config) {
        return data.data;
      }

      function errorFn(data, status, headers, config) {
        return data.data;
      }
    }

    function get_pages(tracker_id) {
      return $http.get('/api/trackers/' + tracker_id + '/pages/').then(successFn, errorFn);


      function successFn(data, status, headers, config) {
        return data.data;
      }

      function errorFn(data, status, headers, config) {
        return data.data;
      }
    }

  }
})();