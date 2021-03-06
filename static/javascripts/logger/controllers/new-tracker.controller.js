(function () {
  'use strict';

  angular
    .module('tracker.logger.controllers')
    .controller('NewTrackerController', NewTrackerController);

  NewTrackerController.$inject = ['$location', '$scope', 'Trackers'];


  function NewTrackerController($location, $scope, Trackers) {
    var vm = this;

    vm.create = create;

    
    function create() {
      Trackers.create_tracker(vm.title, vm.url).then(successFn, errorFn);

      function successFn(data, status, headers, config) {
        vm.msg = data;
      }

      function errorFn(data, status, headers, config) {
        vm.msg = data.error;
      }

  }
}
})();