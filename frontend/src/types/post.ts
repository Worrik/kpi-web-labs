export interface IAuthor {
  id: string
  name: string
  email: string
  created_at: string
}

export interface IUser {
  id: string
  username: string
  avatar_url: string
}

export interface IComment {
  id: string
  post_id: string
  user_id: string
  text: string
  created_at: string
  author: IAuthor | null
}

export interface IPost {
  id: string
  created_at: string
  user_id: string
  text: string
  image_url: string | null
  likes_count: number | null
  comments_count: number | null
  author: IAuthor | null
}