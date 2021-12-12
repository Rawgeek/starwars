export default {
    data () {
      return {
        loading: false,
        post: null,
        error: null
      }
    },
    created () {
      // fetch the data when the view is created and the data is
      // already being observed
      this.fetchData()
    },
    watch: {
      // call again the method if the route changes
      '$route': 'fetchData'
    },
    methods: {
      fetchData () {
        this.error = this.post = null
        this.loading = true
        const fetchedId = this.$route.params.id
        // replace `getPost` with your data fetching util / API wrapper
        getPost(fetchedId, (err, post) => {
          // make sure this request is the last one we did, discard otherwise
          if (this.$route.params.id !== fetchedId) return
          this.loading = false
          if (err) {
            this.error = err.toString()
          } else {
            this.post = post
          }
        })
      }
    }
  }