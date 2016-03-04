(function () {
  'use strict';

  angular
    .module('tracker.authentication.services')
    .factory('Authentication', Authentication);

  Authentication.$inject = ['$http'];


  function Authentication($http) {

    var Authentication = {
      login: login,
      register: register,
      logout: logout,
    };

    return Authentication;

  function register(username, email, password) {
    return $http.post('/api/users/', {
      username: username,
      password: password,
      email: email
    }).then(regSuccess, regError);


    function regSuccess(data, status, headers, config) {
      Authentication.login(email, password);
      // window.location = '/';
    }

    function regError(data, status, headers, config) {
      return data['data']
    }
  }

  function login(email, password) {
    return $http.post('/api/auth/login/', {
      email: email, password: password
    }).then(loginSuccess, loginError);


    function loginSuccess(data, status, headers, config) {

      window.location = '/';
    }

    function loginError(data, status, headers, config) {
      return data['data']['message'];
    }
  }



  function logout() {
    return $http.post('/api/auth/logout/')
        .then(logoutSuccess, logoutError);

      function logoutSuccess(data, status, headers, config) {
        // Authentication.unauthenticate();

        window.location = '/';
      }

      function logoutError(data, status, headers, config) {
        console.error(data);
      }
    }

  }
})();