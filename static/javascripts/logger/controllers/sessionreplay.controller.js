(function () {
  'use strict';

  angular
    .module('tracker.logger.controllers')
    .controller('SessionReplayController', SessionReplayController);

  SessionReplayController.$inject = ['$location', '$routeParams', 'Trackers'];

  function SessionReplayController($location, $routeParams, Trackers) {
    var vm = this;
    vm.session_id = 0;
    activate();
    function activate() {
      vm.session_id = $routeParams.session_id;

    }
};
})();