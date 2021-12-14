<template>
  <div class="document">
    <div v-if="loading" class="loading">
      Loading...
    </div>

    <div v-if="error" class="error">
      {{ error }}
    </div>

    <div v-if="document" class="content">
      <h2>
        <router-link :to="{ name: 'Documents'}">Documents List</router-link> > {{ document.name }}
      </h2>
      <div class="row">
        <div class="col-md-12">
          <a v-bind:href="document.file" download class="btn btn-outline-primary">Download file</a>
          <a v-if="!groupedView && selectedHeaders.length > 0" v-on:click="groupBySelected" class="btn btn-outline-warning">Group and count</a>
          <a v-if="groupedView" v-on:click="fetchData" class="btn btn-outline-danger">Clear selection</a>
        </div>
      </div>
      <div class="table-responsive">
        <table class="table table-hover">
          <thead>
            <tr>
              <th v-for="header in document.header" :key="header">
                <label><input v-if="!groupedView" type="checkbox" v-bind:value="header" v-model="selectedHeaders" class="form-check-input"> {{ header }}</label>
              </th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(data, dindex)  in document.data" :key="dindex">
              <td v-for="(item, index) in data" :key="index">
                <span>{{ item }}</span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <div>
        <a v-if="!groupedView && document.rows_count > document.data.length" v-on:click="fetchMoreData" class="btn btn-outline-primary">Load More</a>
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
      groupedView: false,
      selectedHeaders: [],
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

      const fetchedId = this.$route.params.documentId

      axios
        .get(`http://localhost:8000/api/documents/${fetchedId}`)
        .then(response => {
          if (this.$route.params.documentId !== fetchedId) return
          this.loading = false
          this.document = response.data
          this.groupedView = false
        })
    },
    groupBySelected () {
      this.loading = true

      const fetchedId = this.$route.params.documentId

      const groupByHeaders = this.selectedHeaders.join(',')
      console.log(groupByHeaders)
      axios
        .get(`http://localhost:8000/api/documents/${fetchedId}?group_by=${groupByHeaders}`)
        .then(response => {
          if (this.$route.params.documentId !== fetchedId) return
          this.loading = false
          this.document = response.data
          this.groupedView = true
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
