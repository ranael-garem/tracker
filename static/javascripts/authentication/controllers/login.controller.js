(function () {
  'use strict';

  angular
    .module('tracker.authentication.controllers')
    .controller('LoginController', LoginController);

  LoginController.$inject = ['$location', '$scope', 'Authentication'];

  /**
  * @namespace LoginController
  */
  function LoginController($location, $scope, Authentication) {
    var vm = this;

    vm.login = login;

    vm.error = [];
    // activate();


    // function activate() {
      // If the user is authenticated, they should not be here.
      // if (Authentication.isAuthenticated()) {
        // $location.url('/');
      // }
    // }


    function login() {
      var promise = Authentication.login(vm.login_email, vm.password);

      promise.then(
        // OnSuccess function
        function(answer) {
          vm.msg = answer;
          vm.error = true;
        },
        // OnFailure function
        function(error) {
          vm.msg = error;
          vm.error = true;
        }
      )

    }
  }
})();