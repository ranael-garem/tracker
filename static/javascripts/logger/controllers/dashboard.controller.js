(function () {
  'use strict';

  angular
    .module('tracker.logger.controllers')
    .controller('DashboardController', DashboardController);

  DashboardController.$inject = ['$location', '$routeParams', 'Dashboard', 'Trackers'];


  function DashboardController($location, $routeParams, Dashboard, Trackers) {
    var vm = this;
    vm.tracker_id = 0;


    vm.visits_labels = [];
    vm.visit_series = ['Series A'];
    vm.visits_data = [];
    vm.visits_date = moment().subtract(15, 'days').format('MMMM D, YYYY') + ' - ' + moment().format('MMMM D, YYYY');
    vm.visits_date_change = visits_date_change;
    
    vm.new_users_labels = [];
    vm.new_users_series = ['Series A'];
    vm.new_users_data = [];
    vm.new_users_date = moment().subtract(15, 'days').format('MMMM D, YYYY') + ' - ' + moment().format('MMMM D, YYYY');
    vm.new_users_date_change = new_users_date_change;
    
    vm.bounce_rate_labels = [];
    vm.bounce_rate_series = ['Series A'];
    vm.bounce_rate_data = [];
    vm.bounce_rate_date = moment().subtract(15, 'days').format('MMMM D, YYYY') + ' - ' + moment().format('MMMM D, YYYY');
    vm.bounce_rate_date_change = bounce_rate_date_change;

    vm.popularity = undefined;
    vm.bounce_rate = undefined;
    activate();

    function activate() {
      vm.tracker_id = $routeParams.tracker_id;
      
      Dashboard.visits_over_time(tracker_id).then(visitsSuccessFn, visitsErrorFn);

      function visitsSuccessFn(data, status, headers, config) {
        vm.visits_labels = data.labels;
        vm.visits_data = [data.values,];
      }

      function visitsErrorFn(data, status, headers, config) {
        console.log(data.data);
      }

      Dashboard.new_users(tracker_id).then(newUsersSuccessFn, newUsersErrorFn);

      function newUsersSuccessFn(data, status, headers, config) {
        vm.new_users_labels = data.labels;
        vm.new_users_data = [data.values,];
      }

      function newUsersErrorFn(data, status, headers, config) {
        console.log(data.data);
      }


      Dashboard.bounce_rate(tracker_id).then(successFn, errorFn);

      function successFn(data, status, headers, config) {
        vm.bounce_rate = data.bounce_rate;
        vm.bounce_rate_labels = data.labels;
        vm.bounce_rate_data = [data.values,];
      }

      function errorFn(data, status, headers, config) {
        console.log(data.data);
      }

      Trackers.popularity(tracker_id).then(popularitySuccessFn, popularityErrorFn);

      function popularitySuccessFn(data, status, headers, config) {
        vm.popularity = data;
      }

      function popularityErrorFn(data, status, headers, config) {
        console.error(data.error);
      }
  }

    function visits_date_change(){
      var tracker_id = $routeParams.tracker_id;
      var date = vm.visits_date.split('-'); 
      
      Dashboard.visits_with_date(tracker_id, date).then(successFn, errorFn);


      function successFn(data, status, headers, config) {
        vm.visits_labels = data.labels;
        vm.visits_data = [data.values,];
      }

      function errorFn(data, status, headers, config) {
        console.log(data.data);
      }
    }


    function new_users_date_change(){
      var tracker_id = $routeParams.tracker_id;
      var date = vm.new_users_date.split('-'); 
      
      Dashboard.new_users_with_date(tracker_id, date).then(successFn, errorFn);


      function successFn(data, status, headers, config) {
        vm.new_users_labels = data.labels;
        vm.new_users_data = [data.values,];
      }

      function errorFn(data, status, headers, config) {
        console.log(data.data);
      }
    }


    function bounce_rate_date_change(){
      var tracker_id = $routeParams.tracker_id;
      var date = vm.bounce_rate_date.split('-'); 
      
      Dashboard.bounce_rate_with_date(tracker_id, date).then(successFn, errorFn);


      function successFn(data, status, headers, config) {
        vm.bounce_rate_labels = data.labels;
        vm.bounce_rate_data = [data.values,];
      }

      function errorFn(data, status, headers, config) {
        console.log(data.data);
      }
    }

}
})();