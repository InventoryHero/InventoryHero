export interface ApiResponse<T = void> {
  success: boolean
  data?: T
  error?: unknown // TODO REMOVE THIS, is not needed anymore
}
