<template>
  <div class="create-post">
    <h2>Create New Post</h2>
    <form @submit.prevent="handleSubmit" class="post-form">
      <div class="form-group">
        <textarea
          id="text"
          v-model="text"
          placeholder="Post text"
          required
        ></textarea>
      </div>

      <div class="form-group">
        <input
          type="file"
          id="image"
          accept="image/*"
          @change="handleImageChange"
        />
        <div v-if="imagePreview" class="image-preview">
          <img :src="imagePreview" alt="Preview" />
        </div>
      </div>

      <div class="form-actions">
        <button type="submit" :disabled="isSubmitting" class="submit-button">
          {{ isSubmitting ? 'Creating...' : 'Create Post' }}
        </button>
        <button type="button" @click="$router.push('/')" class="cancel-button">
          Cancel
        </button>
      </div>
    </form>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { usePostsStore } from '@/stores/posts'

const router = useRouter()
const postsStore = usePostsStore()

const text = ref('')
const imageFile = ref<File | null>(null)
const imagePreview = ref<string | null>(null)
const isSubmitting = ref(false)

const handleImageChange = (event: Event) => {
  const target = event.target as HTMLInputElement
  if (target.files && target.files[0]) {
    imageFile.value = target.files[0]
    imagePreview.value = URL.createObjectURL(target.files[0])
  }
}

const handleSubmit = async () => {
  if (!text.value.trim()) return

  isSubmitting.value = true
  try {
    let imageData = null
    if (imageFile.value) {
      const reader = new FileReader()
      imageData = await new Promise<string>((resolve) => {
        reader.onload = (e) => {
          const base64 = e.target?.result as string
          const base64Data = base64.split(',')[1]
          resolve(base64Data)
        }
        reader.readAsDataURL(imageFile.value!)
      })
    }

    await postsStore.createPost(text.value, imageData)
    router.push('/')
  } catch (error) {
    console.error('Failed to create post:', error)
  } finally {
    isSubmitting.value = false
  }
}
</script>

<style scoped>
.create-post {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
}

h2 {
  margin-bottom: 20px;
  color: #1a1a1a;
}

.post-form {
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.form-group {
  text-align: left;
  margin-bottom: 20px;
}

label {
  display: block;
  margin-bottom: 8px;
  color: #333;
  font-weight: 500;
}

textarea {
  width: calc(100% - 20px);
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  resize: vertical;
  font-family: inherit;
  font-size: 1rem;
}

textarea:focus {
  outline: none;
  border-color: #1a1a1a;
}

input[type="file"] {
  width: calc(100% - 20px);
  padding: 8px;
  border: 1px dashed #ddd;
  border-radius: 4px;
  cursor: pointer;
}

.image-preview {
  margin-top: 10px;
  position: relative;
  display: inline-block;
}

.image-preview img {
  max-width: 200px;
  max-height: 200px;
  border-radius: 4px;
}

.form-actions {
  display: flex;
  gap: 10px;
  margin-top: 20px;
}

.submit-button,
.cancel-button {
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 500;
  transition: background-color 0.2s;
}

.submit-button {
  background-color: #1a1a1a;
  color: white;
}

.submit-button:hover:not(:disabled) {
  background-color: #333;
}

.submit-button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.cancel-button {
  background-color: #f8f9fa;
  color: #1a1a1a;
}

.cancel-button:hover {
  background-color: #e9ecef;
}
</style> 