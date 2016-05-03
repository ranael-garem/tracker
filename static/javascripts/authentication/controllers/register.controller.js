/**
* Register controller
*/
(function () {
  'use strict';

  angular
    .module('tracker.authentication.controllers')
    .controller('RegisterController', RegisterController);

  RegisterController.$inject = ['$location', '$scope', 'Authentication'];


  function RegisterController($location, $scope, Authentication) {
    var vm = this;

    vm.register = register;
    activate();
    function activate() {
      if (Authentication.isAuthenticated()) {
        $location.url('/trackers');
      }
    }
    function register() {
      var promise = Authentication.register(vm.username, vm.reg_email, vm.password);

      promise.then(

        function(data){
          vm.msg = data;
        },
        function(error){
          vm.msg = error
        })
    }
  }
})();