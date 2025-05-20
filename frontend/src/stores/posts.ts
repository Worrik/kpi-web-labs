import { defineStore } from 'pinia'
import axios from '@/utils/axios'
import type { IPost } from '@/types/post'

export const usePostsStore = defineStore('posts', {
  state: () => ({
    posts: [] as IPost[],
    loading: false,
    error: null as string | null
  }),

  actions: {
    async fetchPosts() {
      this.loading = true
      this.error = null
      try {
        const response = await axios.get('/posts')
        this.posts = response.data
      } catch (err: any) {
        this.error = err.response?.data?.detail || 'Failed to fetch posts'
      } finally {
        this.loading = false
      }
    },

    async createPost(text: string, imageData: string | null) {
      try {
        const response = await axios.post('/posts', {
          text,
          image_data: imageData
        })
        this.posts.unshift(response.data)
        return response.data
      } catch (err: any) {
        throw new Error(err.response?.data?.detail || 'Failed to create post')
      }
    },

    async likePost(postId: string) {
      try {
        const res = await axios.post(`/posts/${postId}/like`)
        const post = this.posts.find(p => p.id === postId)
        if (res.data && post) {
          post.likes_count = (post.likes_count || 0) + 1
        }
      } catch (err: any) {
        throw new Error(err.response?.data?.detail || 'Failed to like post')
      }
    },

    async addComment(postId: string, text: string) {
      try {
        await axios.post(`/posts/${postId}/comment`, { text })
        const post = this.posts.find(p => p.id === postId)
        if (post) {
          post.comments_count = (post.comments_count || 0) + 1
        }
      } catch (err: any) {
        throw new Error(err.response?.data?.detail || 'Failed to add comment')
      }
    },

    async fetchComments(postId: string) {
      try {
        const response = await axios.get(`/posts/${postId}/comments`)
        return response.data
      } catch (err: any) {
        throw new Error(err.response?.data?.detail || 'Failed to fetch comments')
      }
    }
  }
}) 