const AUTH_STORAGE_KEY = 'data-daddies-auth';

var authStorage = {
  fetch: function () {
    return JSON.parse(localStorage.getItem(AUTH_STORAGE_KEY) || '{}');
  },
  save: function (credentials) {
    localStorage.setItem(AUTH_STORAGE_KEY, JSON.stringify(credentials));
  }
}

var app = new Vue({
  el: '#app',
  data: {
    message: 'Hello Vue!',
    user: {},
    playlists: [],
    credentials: authStorage.fetch()
  },
  methods: {
    getInfo: function () {
      //console.log(JSON.stringify(this.credentials));
      this.$http.get('https://api.spotify.com/v1/me',
        { headers: {'Authorization': 'Bearer '+this.credentials.access_token} })
        .then(response => {
          console.log("successfully retrieved info for "+response.body.display_name);
          this.user = response.body;
        }, response => {
          console.log("error: "+JSON.stringify(response));
      });
    },
    getPlaylists: async function () {
      try {
        var list = await this.$http.get('https://api.spotify.com/v1/users/'+this.user.id+'/playlists', {
          headers: {'Authorization': 'Bearer '+this.credentials.access_token},
        });
        this.playlists = list.body.items;
      } catch (error) {
        console.log("ERROR: "+JSON.stringify(error));
      }
    },
    makePlaylistChart: function () {
      return makeBarGraph(this.playlists.map(function(item) {
        return item.tracks.total;
      }));
    },
    logout: function () {
      this.credentials = {};
    }
  },
  mounted() {
    if (typeof locals !== 'undefined' && locals !== null) {
      if (locals.access_token) this.credentials.access_token = locals.access_token;
      if (locals.refresh_token) this.credentials.refresh_token = locals.refresh_token;
      authStorage.save(this.credentials);
    }
    this.getInfo();
  },
  watch: {
    credentials: {
      handler: function (creds) {
        authStorage.save(creds);
      },
      deep: true
    }
  }
})
