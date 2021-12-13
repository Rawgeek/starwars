<template>
  <div class="document">
    <div v-if="loading" class="loading">
      Loading...
    </div>

    <div v-if="error" class="error">
      {{ error }}
    </div>

    <div v-if="document" class="content">
      <h2><router-link :to="{ name: 'Documents'}">Documents List</router-link> > {{ document.name }}</h2>
      <div>
        <a v-bind:href="document.file" download class="btn btn-outline-primary">Download</a>
      </div>
      <div class="table-responsive">
        <table class="table table-striped">
          <tr v-for="header in document.header" :key="header">
            <th>{{ header }}</th>
          </tr>
          <tr v-for="data in document.data" :key="data.name">
            <td>{{ data[0] }}</td>
            <td>{{ data[1] }}</td>
            <td>{{ data[2] }}</td>
            <td>{{ data[3] }}</td>
            <td>{{ data[4] }}</td>
            <td>{{ data[5] }}</td>
            <td>{{ data[6] }}</td>
            <td>{{ data[7] }}</td>
            <td>{{ data[8] }}</td>
            <td>{{ data[9] | formatDate}}</td>
          </tr>
        </table>
      </div>
      <div>
        <a v-if="document.rows_count > document.data.length" v-on:click="fetchMoreData" class="btn btn-outline-primary">Load More</a>
      </div>
    </div>
  </div>
</template>

<script>
const axios = require('axios')

export default {
  data () {
    return {
      loading: false,
      document: {},
      header: [],
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
      this.loading = true

      const fetchedId = this.$route.params.documentId

      axios
        .get(`http://localhost:8000/api/documents/${fetchedId}`)
        .then(response => {
          if (this.$route.params.documentId !== fetchedId) return
          this.loading = false
          this.document = response.data
          this.header = response.data[0]
        })
    },
    fetchMoreData () {
      this.loading = true

      const fetchedId = this.$route.params.documentId

      const offset = this.document.data.length
      axios
        .get(`http://localhost:8000/api/documents/${fetchedId}?offset=${offset}`)
        .then(response => {
          if (this.$route.params.documentId !== fetchedId) return
          this.loading = false
          this.document.data = this.document.data.concat(response.data.data)
          window.scrollTo(0, document.body.scrollHeight)
        })
    }
  }
}
</script>

<style scoped>
h1, h2 {
  font-weight: normal;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
