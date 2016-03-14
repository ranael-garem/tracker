(function () {
  'use strict';

  angular
    .module('tracker.logger.controllers')
    .controller('DashboardController', DashboardController);

  DashboardController.$inject = ['$location', '$routeParams', 'Dashboard'];


  function DashboardController($location, $routeParams, Dashboard) {
    var vm = this;



    vm.visits_labels = [];
    vm.visit_series = ['Series A'];
    vm.visits_data = [];
    vm.visits_date = moment().subtract(15, 'days').format('MMMM D, YYYY') + ' - ' + moment().format('MMMM D, YYYY');
    vm.visits_date_change = visits_date_change;
    
    activate();

    function activate() {
      var tracker_id = $routeParams.tracker_id;
      
      Dashboard.visits_over_time(tracker_id).then(successFn, errorFn);

      function successFn(data, status, headers, config) {
        vm.visits_labels = data.labels;
        vm.visits_data = [data.values,];
      }

      function errorFn(data, status, headers, config) {
        console.log(data.data);
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
}
})();