(function () {
  'use strict';

  angular
    .module('tracker.logger.controllers')
    .controller('TrackerController', TrackerController);

  TrackerController.$inject = ['$location', '$routeParams', 'Trackers'];

  function TrackerController($location, $routeParams, Trackers) {
    var vm = this;
    vm.quantity = -10;
    vm.tracker = undefined;
    vm.tracker_pages = undefined;
    vm.update = update;
    vm.destroy = destroy;
    vm.popularity = undefined;
    vm.interactivity = undefined
    activate();
    popularity();
    interactivity();

    function activate() {
      var tracker_id = $routeParams.tracker_id;
      Trackers.get(tracker_id).then(successFn, errorFn);

      function successFn(data, status, headers, config) {
        vm.tracker = data;
      }

      function errorFn(data, status, headers, config) {
        console.error(data.error);
      }

      Trackers.get_pages(tracker_id).then(getPagesSuccessFn, getPagesErrFn);
      
      function getPagesSuccessFn(data, status, headers, config) {
        vm.tracker_pages = data;
      }

      function getPagesErrFn(data, status, headers, config) {
        console.error(data.error);
      }
    }

    function popularity() {
      var tracker_id = $routeParams.tracker_id;
      Trackers.popularity(tracker_id).then(successFn, errorFn);

      function successFn(data, status, headers, config) {
        vm.popularity = data;
      }

      function errorFn(data, status, headers, config) {
        console.error(data.error);
      }

    }

    function interactivity() {
      var tracker_id = $routeParams.tracker_id;
      Trackers.interactivity(tracker_id).then(successFn, errorFn);

      function successFn(data, status, headers, config) {
        vm.interactivity = data;
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