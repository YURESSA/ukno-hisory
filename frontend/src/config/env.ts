const apiBaseUrl = import.meta.env.VITE_API_URL || '/api/v1'

const backendOrigin =
  import.meta.env.VITE_BACKEND_URL ||
  apiBaseUrl.replace(/\/api\/v1\/?$/, '')

export const env = {
  apiBaseUrl,
  backendOrigin,
}

export const resolveBackendUrl = (path: string): string => {
  if (/^https?:\/\//.test(path)) {
    return path
  }

  return `${backendOrigin}${path}`
}
