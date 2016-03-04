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

    function register() {
      Authentication.register(vm.reg_email, vm.password, vm.username);
    }
  }
})();