import { createApp } from 'vue'
import { createPinia } from 'pinia'
import './style.css'
import App from './App.vue'
import router from './router'
import axios from '@/utils/axios'

// Import Font Awesome
import { library } from '@fortawesome/fontawesome-svg-core'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { faHeart, faComment, faPaperPlane, faPlus, faTimes } from '@fortawesome/free-solid-svg-icons'

// Add icons to library
library.add(faHeart, faComment, faPaperPlane, faPlus, faTimes)

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.component('font-awesome-icon', FontAwesomeIcon)

app.mount('#app')
