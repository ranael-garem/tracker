(function() {
  var Heatmap;

  Heatmap = (function() {
    function Heatmap(targetId, screenshotUrl, positionData, opts) {
      var background;
      this.positionData = positionData;
      if (opts == null) {
        opts = {};
      }
      this.target = document.getElementById(targetId);
      this.screenshotOpacity = opts.screenshotAlpha === void 0 ? 0.6 : opts.screenshotAlpha;
      this.heatmapOpacity = opts.heatmapAlpha === void 0 ? 0.6 : opts.heatmapAlpha;
      this.calculateColor = opts.colorScheme === 'simple' ? this.simpleRedGradient : this.fiveColorGradient;
      background = new Image();
      background.src = screenshotUrl;
      background.onload = (function(_this) {
        return function() {
          var context, data, i, maxViews, position, value, views, viewsArray, _i, _j, _k, _l, _len, _len1, _m, _n, _ref, _ref1, _ref2, _ref3, _ref4, _ref5, _results, _results1, _results2;
          _this.width = background.width;
          _this.height = background.height;
          _this.target.width = _this.width;
          _this.target.height = _this.height;
          _this.target.style.width = _this.width + 'px';
          _this.target.style.height = _this.height + 'px';
          context = _this.target.getContext('2d');
          context.globalAlpha = _this.screenshotOpacity;
          context.drawImage(background, 0, 0);
          _this.plus = (function() {
            _results = [];
            for (var _i = 0, _ref = parseInt(_this.height); 0 <= _ref ? _i <= _ref : _i >= _ref; 0 <= _ref ? _i++ : _i--){ _results.push(_i); }
            return _results;
          }).apply(this).map(function() {
            return 0;
          });
          _this.minus = (function() {
            _results1 = [];
            for (var _j = 0, _ref1 = parseInt(_this.height); 0 <= _ref1 ? _j <= _ref1 : _j >= _ref1; 0 <= _ref1 ? _j++ : _j--){ _results1.push(_j); }
            return _results1;
          }).apply(this).map(function() {
            return 0;
          });
          _ref2 = _this.positionData;
          for (_k = 0, _len = _ref2.length; _k < _len; _k++) {
            data = _ref2[_k];
            _ref3 = data.positions;
            for (_l = 0, _len1 = _ref3.length; _l < _len1; _l++) {
              position = _ref3[_l];
              ++_this.plus[position];
              ++_this.minus[position + data.height];
            }
          }
          views = 0;
          maxViews = 0;
          viewsArray = [];
          for (i = _m = 0, _ref4 = parseInt(_this.height); 0 <= _ref4 ? _m <= _ref4 : _m >= _ref4; i = 0 <= _ref4 ? ++_m : --_m) {
            views += _this.plus[i];
            views -= _this.minus[i];
            viewsArray[i] = views;
            maxViews = Math.max(maxViews, views);
          }
          context.globalAlpha = 1.0;
          _results2 = [];
          for (i = _n = 0, _ref5 = parseInt(_this.height); 0 <= _ref5 ? _n <= _ref5 : _n >= _ref5; i = 0 <= _ref5 ? ++_n : --_n) {
            value = viewsArray[i] / maxViews;
            context.beginPath();
            context.moveTo(0, i);
            context.lineTo(_this.width, i);
            context.lineWidth = 1;
            context.strokeStyle = _this.calculateColor(value);
            _results2.push(context.stroke());
          }
          return _results2;
        };
      })(this);
    }

    Heatmap.prototype.fiveColorGradient = function(value) {
      var h;
      h = (1.0 - value) * 240;
      return "hsla(" + h + ", 100%, 50%, " + this.heatmapOpacity + ")";
    };

    Heatmap.prototype.simpleRedGradient = function(value) {
      return "rgba(255, 0, 0, " + (value * this.heatmapOpacity) + ")";
    };

    return Heatmap;

  })();

  window.Heatmap = Heatmap;

}).call(this);
