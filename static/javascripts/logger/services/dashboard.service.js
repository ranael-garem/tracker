(function () {
  'use strict';

  angular
    .module('tracker.logger.services')
    .factory('Dashboard', Dashboard);

  Dashboard.$inject = ['$http'];


  function Dashboard($http) {

    var Dashboard = {
      visits_over_time: visits_over_time,
      visits_with_date: visits_with_date,
      new_users: new_users,
      new_users_with_date: new_users_with_date,
      bounce_rate: bounce_rate,
      bounce_rate_with_date: bounce_rate_with_date,
    };

    return Dashboard;

    function visits_over_time(tracker_id) {
      return $http.get('/reports/visits/' + tracker_id + '/').then(successFn, errorFn);


      function successFn(data, status, headers, config) {
        return data.data;
      }

      function errorFn(data, status, headers, config) {
        return data.data;
      }
    }


    function visits_with_date(tracker_id, date){
      console.log(date)
      var from_date = new Date(date[0]);
      var to_date = new Date(date[1]);

      var from_date_string = from_date.getFullYear() + '/' + (from_date.getMonth() + 1) + '/' + from_date.getDate() + '/';
      var to_date_string = to_date.getFullYear() + '/' + (to_date.getMonth() + 1) + '/' + to_date.getDate() + '/';

      return $http.get('/reports/visits/' + tracker_id + '/' + from_date_string + to_date_string).then(successFn, errorFn);


      function successFn(data, status, headers, config) {
        return data.data;
      }

      function errorFn(data, status, headers, config) {
        return data.data;
      }
    }


    function new_users(tracker_id) {
      return $http.get('/reports/new-users/' + tracker_id + '/').then(successFn, errorFn);


      function successFn(data, status, headers, config) {
        return data.data;
      }

      function errorFn(data, status, headers, config) {
        return data.data;
      }
    }


    function new_users_with_date(tracker_id, date){
      console.log(date)
      var from_date = new Date(date[0]);
      var to_date = new Date(date[1]);

      var from_date_string = from_date.getFullYear() + '/' + (from_date.getMonth() + 1) + '/' + from_date.getDate() + '/';
      var to_date_string = to_date.getFullYear() + '/' + (to_date.getMonth() + 1) + '/' + to_date.getDate() + '/';

      return $http.get('/reports/new-users/' + tracker_id + '/' + from_date_string + to_date_string).then(successFn, errorFn);


      function successFn(data, status, headers, config) {
        return data.data;
      }

      function errorFn(data, status, headers, config) {
        return data.data;
      }
    }

    function bounce_rate(tracker_id) {
      return $http.get('/reports/bounce/' + tracker_id + '/').then(successFn, errorFn);


      function successFn(data, status, headers, config) {
        return data.data;
      }

      function errorFn(data, status, headers, config) {
        return data.data;
      }
    }


    function bounce_rate_with_date(tracker_id, date){
      var from_date = new Date(date[0]);
      var to_date = new Date(date[1]);

      var from_date_string = from_date.getFullYear() + '/' + (from_date.getMonth() + 1) + '/' + from_date.getDate() + '/';
      var to_date_string = to_date.getFullYear() + '/' + (to_date.getMonth() + 1) + '/' + to_date.getDate() + '/';

      return $http.get('/reports/bounce/' + tracker_id + '/' + from_date_string + to_date_string).then(successFn, errorFn);


      function successFn(data, status, headers, config) {
        return data.data;
      }

      function errorFn(data, status, headers, config) {
        return data.data;
      }
    }

  }

})();