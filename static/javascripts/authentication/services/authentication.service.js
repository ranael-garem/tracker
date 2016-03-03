(function () {
  'use strict';

  angular
    .module('tracker.authentication.services')
    .factory('Authentication', Authentication);

  Authentication.$inject = ['$http'];


  function Authentication($http) {

    var Authentication = {
      register: register
    };

    return Authentication;

    function register(email, password, username) {
      return $http.post('/api/users/', {
        username: username,
        password: password,
        email: email
      });
    }
  }
})();