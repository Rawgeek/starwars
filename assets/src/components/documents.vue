<template>
  <div class="documents">
    <div v-if="loading" class="loading">
      Loading...
    </div>

    <div v-if="error" class="error">
      {{ error }}
    </div>

    <div v-if="documents" class="content">
      <h2>Documents <a v-on:click="fetchNew" class="btn btn-outline-primary">Fetch new</a></h2>
      <div class="table-responsive">
        <table class="table table-striped table-sm">
          <tr v-for="document in documents" :key="document.id">
            <td><router-link :to="{ name: 'Document', params: { documentId: document.id }}">{{ document.name }}</router-link></td>
            <td><a v-bind:href="document.file" download>Download</a></td>
            <td>{{ document.created_at | formatDate }}</td>
          </tr>
        </table>
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
      documents: [],
      error: null
    }
  },
  created () {
    this.fetchData()
  },
  watch: {
    '$route': 'fetchData'
  },
  methods: {
    fetchData () {
      this.loading = true
      axios
        .get('http://localhost:8000/api/documents/')
        .then(response => {
          this.loading = false
          this.documents = response.data
        })
    },
    fetchNew () {
      this.loading = true
      axios
        .post('http://localhost:8000/api/documents/')
        .then(response => {
          this.fetchData()
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
