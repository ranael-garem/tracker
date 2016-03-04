(function () {
  'use strict';

  angular
    .module('tracker.logger.controllers')
    .controller('TrackerController', TrackerController);

  TrackerController.$inject = ['$location', '$routeParams', 'Trackers'];

  function TrackerController($location, $routeParams, Trackers) {
    var vm = this;

    vm.tracker = undefined;

    activate();
    
    function activate() {
      var tracker_id = $routeParams.tracker_id;
      Trackers.get(tracker_id).then(successFn, errorFn);

      function successFn(data, status, headers, config) {
        vm.tracker = data;
        console.log(data);
      }

      function errorFn(data, status, headers, config) {
        console.error(data.error);
      }

  }
}
})();