<template>
  <div class="home">
    <div class="header">
      <h1>Posts</h1>
      <button 
        v-if="isAuthenticated" 
        @click="$router.push('/create')" 
        class="create-button"
      >
        <font-awesome-icon :icon="['fas', 'plus']" />
        Create Post
      </button>
    </div>

    <div v-if="postsStore.loading" class="loading">
      Loading posts...
    </div>
    <div v-else-if="postsStore.error" class="error">
      {{ postsStore.error }}
      <button @click="fetchPosts" class="retry-button">
        Try Again
      </button>
    </div>
    <div v-else>
      <PostCard
        v-for="post in postsStore.posts"
        :key="post.id"
        :post="post"
        :comments="postComments[post.id]"
        @like="handleLike(post.id)"
        @comment="handleComment(post.id, $event)"
        @fetch-comments="handleFetchComments(post.id)"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, computed, ref, nextTick } from 'vue'
import { usePostsStore } from '@/stores/posts'
import PostCard from '@/components/PostCard.vue'
import type { IComment } from '@/types/post'

const postsStore = usePostsStore()
const postComments = ref<Record<string, IComment[]>>({})

const isAuthenticated = computed(() => {
  return !!localStorage.getItem('token')
})

const handleLike = async (postId: string) => {
  if (!isAuthenticated.value) return
  await postsStore.likePost(postId)
}

const handleComment = async (postId: string, text: string) => {
  if (!isAuthenticated.value) return
  await postsStore.addComment(postId, text)
  const comments = await postsStore.fetchComments(postId)
  postComments.value[postId] = comments
}

const handleFetchComments = async (postId: string) => {
  const comments = await postsStore.fetchComments(postId)
  postComments.value[postId] = comments
}

const fetchPosts = async () => {
  try {
    await postsStore.fetchPosts()
  } catch (err: any) {
    console.error('Failed to fetch posts:', err)
  }
}

onMounted(async () => {
  if (!postsStore.posts.length) {
    await fetchPosts()
  }
})
</script>

<style scoped>
.home {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

h1 {
  margin: 0;
  color: #1a1a1a;
}

.create-button {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  background-color: #1a1a1a;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 500;
  transition: background-color 0.2s;
}

.create-button:hover {
  background-color: #333;
}

.loading,
.error {
  text-align: center;
  padding: 20px;
  color: #666;
}

.error {
  color: #dc3545;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
}

.retry-button {
  padding: 8px 16px;
  background-color: #1a1a1a;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 500;
  transition: background-color 0.2s;
}

.retry-button:hover {
  background-color: #333;
}
</style> 