<template>
  <article class="post-card">
    <header class="post-header">
      <div class="post-author">
        <span class="author-name">{{ post.author?.name || 'Unknown User' }}</span>
        <time class="post-date" :datetime="post.created_at">{{ formatDate(post.created_at) }}</time>
      </div>
    </header>

    <div class="post-content">
      <div v-if="post.image_url" class="image-container">
        <img 
          :src="getImageUrl(post.image_url)" 
          class="post-image"
          loading="lazy"
        >
      </div>
      <p class="post-text">{{ post.text }}</p>
    </div>

    <div class="post-actions">
      <div class="action-buttons">
        <button 
          @click="handleLike" 
          class="action-button"
          :disabled="!isAuthenticated"
        >
          <font-awesome-icon :icon="['fas', 'heart']" />
          <span class="count">{{ post.likes_count || 0 }}</span>
        </button>

        <button 
          @click="toggleComments" 
          class="action-button"
          :disabled="!isAuthenticated"
        >
          <font-awesome-icon :icon="['fas', 'comment']" />
          <span class="count">{{ post.comments_count || 0 }}</span>
        </button>
      </div>

      <div v-if="!isAuthenticated" class="auth-warning">
        <p>Please <router-link to="/login">login</router-link> to interact with posts</p>
      </div>

      <div v-if="showComments" class="comments-section">
        <form 
          v-if="isAuthenticated"
          @submit.prevent="submitComment" 
          class="comment-form"
        >
          <input 
            v-model="newComment" 
            type="text"
            placeholder="Write a comment..." 
            class="comment-input"
          >
          <button 
            type="submit" 
            class="send-button"
            :disabled="!newComment.trim()"
          >
            <font-awesome-icon :icon="['fas', 'paper-plane']" />
          </button>
        </form>

        <div v-if="loading" class="loading">
          Loading comments...
        </div>
        <div v-else-if="error" class="error">
          {{ error }}
        </div>
        <div v-else-if="comments?.length" class="comments-list">
          <div 
            v-for="comment in comments" 
            :key="comment.id" 
            class="comment"
          >
            <div class="comment-header">
              <span class="comment-author">{{ comment.author?.name || 'Unknown User' }}</span>
              <time class="comment-date" :datetime="comment.created_at">
                {{ formatDate(comment.created_at) }}
              </time>
            </div>
            <p class="comment-text">{{ comment.text }}</p>
          </div>
        </div>
        <div v-else class="no-comments">
          No comments yet. Be the first to comment!
        </div>
      </div>
    </div>
  </article>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import type { IPost, IComment } from '@/types/post'

const props = defineProps<{
  post: IPost
  comments?: IComment[]
}>()

const emit = defineEmits<{
  (e: 'like'): void
  (e: 'comment', text: string): void
  (e: 'fetch-comments'): void
}>()

const showComments = ref(false)
const newComment = ref('')
const loading = ref(false)
const error = ref<string | null>(null)

const isAuthenticated = computed(() => {
  return !!localStorage.getItem('token')
})

const getImageUrl = (imageUrl: string) => {
  return `${import.meta.env.VITE_API_URL}/images${imageUrl}`
}

const handleLike = () => {
  if (!isAuthenticated.value) return
  emit('like')
}

const toggleComments = () => {
  if (!isAuthenticated.value) return
  showComments.value = !showComments.value
}

const submitComment = () => {
  if (newComment.value.trim() && isAuthenticated.value) {
    emit('comment', newComment.value)
    newComment.value = ''
  }
}

const formatDate = (date: string) => {
  return new Date(date).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

watch(showComments, async (newValue) => {
  if (newValue && !props.comments) {
    loading.value = true
    error.value = null
    try {
      emit('fetch-comments')
    } catch (err: any) {
      error.value = err.message || 'Failed to load comments'
    } finally {
      loading.value = false
    }
  }
})
</script>

<style scoped>
.post-card {
  background: white;
  border-radius: 12px;
  padding: 16px;
  margin-bottom: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.post-header {
  margin-bottom: 12px;
}

.post-author {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.author-name {
  font-weight: 600;
  color: #1a1a1a;
  font-size: 1.1em;
}

.post-date {
  color: #666;
  font-size: 0.9em;
}

.post-content {
  margin-bottom: 16px;
}

.image-container {
  width: 100%;
  height: 300px;
  overflow: hidden;
  border-radius: 8px;
  margin-bottom: 12px;
}

.post-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center;
}

.post-text {
  margin: 0;
  color: #1a1a1a;
  line-height: 1.5;
  font-size: 1em;
  white-space: pre-wrap;
  text-align: left;
}

.post-actions {
  border-top: 1px solid #eee;
  padding-top: 12px;
}

.action-buttons {
  display: flex;
  gap: 16px;
  margin-bottom: 12px;
}

.action-button {
  display: flex;
  align-items: center;
  gap: 6px;
  background: none;
  border: none;
  color: #666;
  cursor: pointer;
  padding: 6px 10px;
  border-radius: 4px;
  transition: all 0.2s;
  font-size: 0.95em;
}

.action-button:hover:not(:disabled) {
  background-color: #f5f5f5;
  color: #1a1a1a;
}

.action-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.action-button.is-liked {
  color: #e74c3c;
}

.count {
  font-weight: 500;
}

.auth-warning {
  text-align: center;
  padding: 12px;
  background: #fff3cd;
  color: #856404;
  border-radius: 6px;
  margin-bottom: 12px;
  font-size: 0.9em;
}

.auth-warning a {
  color: #1a1a1a;
  text-decoration: none;
  font-weight: 600;
}

.auth-warning a:hover {
  text-decoration: underline;
}

.comments-section {
  margin-top: 12px;
}

.comment-form {
  display: flex;
  gap: 8px;
  margin-bottom: 16px;
}

.comment-input {
  flex: 1;
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 0.95em;
  transition: border-color 0.2s;
}

.comment-input:focus {
  outline: none;
  border-color: #1a1a1a;
}

.send-button {
  background: #1a1a1a;
  color: white;
  border: none;
  border-radius: 4px;
  padding: 8px 12px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.send-button:hover:not(:disabled) {
  background: #333;
}

.send-button:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.loading,
.error {
  text-align: center;
  padding: 12px;
  margin-bottom: 12px;
  border-radius: 4px;
  font-size: 0.9em;
}

.loading {
  background: #f8f9fa;
  color: #666;
}

.error {
  background: #fff3cd;
  color: #856404;
}

.comments-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.comment {
  background: #f8f9fa;
  padding: 12px;
  border-radius: 6px;
}

.comment-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 6px;
}

.comment-author {
  font-weight: 600;
  color: #1a1a1a;
  font-size: 0.95em;
}

.comment-date {
  color: #666;
  font-size: 0.85em;
}

.comment-text {
  color: #1a1a1a;
  line-height: 1.4;
  margin: 0;
  font-size: 0.95em;
  text-align: left;
}

.no-comments {
  text-align: center;
  padding: 16px;
  color: #666;
  background: #f8f9fa;
  border-radius: 6px;
  font-style: italic;
  font-size: 0.9em;
}
</style>
