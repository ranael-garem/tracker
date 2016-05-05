(function () {
  'use strict';

  angular
    .module('tracker.authentication', [
      'tracker.authentication.controllers',
      'tracker.authentication.services'
    ]);

  angular
    .module('tracker.authentication.controllers', ['ngCookies']);

  angular
    .module('tracker.authentication.services', ['ngCookies']);
})();