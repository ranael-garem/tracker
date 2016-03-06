(function () {
  'use strict';

  angular
    .module('tracker.logger.controllers')
    .controller('TrackerController', TrackerController);

  TrackerController.$inject = ['$location', '$routeParams', 'Trackers'];

  function TrackerController($location, $routeParams, Trackers) {
    var vm = this;

    vm.tracker = undefined;
    vm.update = update;
    vm.destroy = destroy;
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


    function update() {
      Trackers.update(vm.tracker).then(successFn, errorFn);

      function successFn(data, status, headers, config) {
        alert('Your Tracker has been updated.');
        window.location = '/tracker/' + vm.tracker.id
      }


      function errorFn(data, status, headers, config) {
        console.error(data.error);     
      }
    }


    function destroy() {
      Trackers.destroy(vm.tracker).then(successFn, errorFn);

      function successFn(data, status, headers, config) {
        alert('Your Tracker has been deleted');
        window.location = '/trackers/'
      }


      function errorFn(data, status, headers, config) {
        console.error(data.error);
      }
    }
};
})();