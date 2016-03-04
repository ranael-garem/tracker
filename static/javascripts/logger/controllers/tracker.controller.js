(function () {
  'use strict';

  angular
    .module('tracker.logger.controllers')
    .controller('TrackerController', TrackerController);

  TrackerController.$inject = ['$location', '$scope', 'Trackers'];


  function TrackerController($location, $scope, Trackers) {
    var vm = this;

    vm.trackers = [];

    activate();
    
    function activate() {
      Trackers.all().then(successFn, errorFn);

      function successFn(data, status, headers, config) {
        vm.trackers = data.data;
      }

      function errorFn(data, status, headers, config) {
        console.error(data.error);
      }

  }
}
})();