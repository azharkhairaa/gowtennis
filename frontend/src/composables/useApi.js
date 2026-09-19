import { ref } from 'vue'

/**
 * Mode statis: dipakai saat situs di-host di static hosting (Surge, Netlify,
 * GitHub Pages) tanpa backend. Data diambil dari berkas .json hasil
 * `tools/buat_static.py`, bukan dari FastAPI.
 */
export const STATIC_MODE = import.meta.env.VITE_STATIC === '1'

// BASE_URL ikut nilai `base` Vite ('/' atau '/<repo>/'), jadi pemanggilan tetap
// benar baik di root domain maupun di sub-path GitHub Pages.
const BASE =
  import.meta.env.VITE_API_BASE || `${import.meta.env.BASE_URL}api`.replace(/\/{2,}/g, '/')
const SUFFIX = STATIC_MODE ? '.json' : ''

/**
 * Pembungkus fetch dengan state loading/error, supaya tiap komponen tidak
 * mengulang pola yang sama.
 */
export function useApi(path, { immediate = true } = {}) {
  const data = ref(null)
  const error = ref(null)
  const loading = ref(false)

  async function load(query = '') {
    loading.value = true
    error.value = null
    try {
      // Berkas statis tidak mengenal query string seperti ?refresh=true.
      const q = STATIC_MODE ? '' : query
      const res = await fetch(`${BASE}${path}${SUFFIX}${q}`)
      if (!res.ok) throw new Error(`HTTP ${res.status}`)
      data.value = await res.json()
    } catch (e) {
      error.value = e.message || 'Gagal memuat data'
    } finally {
      loading.value = false
    }
  }

  if (immediate) load()

  return { data, error, loading, load }
}

export async function postApi(path, body) {
  const res = await fetch(`${BASE}${path}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  })
  const payload = await res.json().catch(() => ({}))
  if (!res.ok) {
    const detail = Array.isArray(payload.detail)
      ? payload.detail.map((d) => d.msg).join(', ')
      : payload.detail || `HTTP ${res.status}`
    throw new Error(detail)
  }
  return payload
}
