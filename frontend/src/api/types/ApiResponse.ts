export interface ApiResponse<T = void> {
    success: boolean
    data?: T
    error?: unknown
}


