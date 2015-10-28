module.exports = {
  keys: {},
  set: function (key, url, preprocessor) {
    if (this.keys[key] != null) {
      return;
    }

    this.keys[key] = window.fetch(url).then(function (response) {
      return response.json();
    });

    if (preprocessor != null) {
      this.keys[key] = this.keys[key].then(function (data) {
        return preprocessor(data);
      });
    };
  },

  get: function (key) {
    if (this.keys[key] == null) {
      throw "Unknown key: " + key;
    }

    return this.keys[key];
  }
};