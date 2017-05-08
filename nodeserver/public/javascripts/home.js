const AUTH_STORAGE_KEY = 'data-daddies-auth';

var app = new Vue({
  el: '#app',
  data: {
    message: 'Hello Vue!'
  },
  methods: {
    getInfo: function () {
      console.log(JSON.stringify(locals));
      //this.$http.get('https://api.spotify.com/v1/me').then(response => {
          // get body data
          //this.someData = response.body;
      //}, response => {
          // error callback
      //});
    }
  },
  beforeMount() {
    if (typeof locals !== 'undefined' && locals !== null) {
      console.log("locals exists! ");
    }
  }
})
