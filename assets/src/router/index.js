import Vue from 'vue'
import Router from 'vue-router'
import Documents from '@/components/documents'
import DocumentDetails from '@/components/document'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Documents',
      component: Documents
    },
    {
      path: '/:documentId/',
      name: 'Document',
      component: DocumentDetails
    }
  ]
})
