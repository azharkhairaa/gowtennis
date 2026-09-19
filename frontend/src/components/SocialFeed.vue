<script setup>
import { computed, ref, watch } from 'vue'
import { useApi } from '../composables/useApi'
import { prosesEmbed } from '../composables/useSocialEmbed'

const { data, error, loading, load } = useApi('/social/feed')

const filter = ref('semua')
const embedPenuh = ref(false)

const items = computed(() => data.value?.items ?? [])

const terfilter = computed(() => {
  if (filter.value === 'semua') return items.value
  return items.value.filter((i) => i.platform === filter.value)
})

const jumlahPer = computed(() => ({
  semua: items.value.length,
  instagram: items.value.filter((i) => i.platform === 'instagram').length,
  tiktok: items.value.filter((i) => i.platform === 'tiktok').length,
}))

/** Sebuah kartu dirender sebagai embed asli bila diminta, atau kalau unggulan. */
function tampilEmbed(item) {
  return Boolean(item.embed_html) && (embedPenuh.value || item.unggulan)
}

function tanggalTampil(iso) {
  if (!iso) return ''
  const d = new Date(iso)
  if (Number.isNaN(d.getTime())) return iso
  return d.toLocaleDateString('id-ID', {
    day: 'numeric',
    month: 'long',
    year: 'numeric',
  })
}

// Setiap kali daftar kartu berubah, script embed perlu diminta memindai ulang.
watch(
  [terfilter, embedPenuh],
  () => {
    if (terfilter.value.some((i) => tampilEmbed(i))) prosesEmbed()
  },
  { flush: 'post' }
)
</script>

<template>
  <section id="sosial" class="section">
    <div class="wrap">
      <div class="feed__head">
        <div>
          <span class="eyebrow">Kegiatan Terbaru</span>
          <h2 class="section-title">Langsung dari lapangan</h2>
          <p class="section-lead">
            Dokumentasi sesi, jadwal, dan keseharian komunitas, ditarik dari
            Instagram dan TikTok Gow! Tennis.
          </p>
        </div>

        <div class="feed__links">
          <a
            class="btn btn--outline btn--sm"
            href="https://www.instagram.com/gowtennis/"
            target="_blank"
            rel="noopener noreferrer"
            >Instagram</a
          >
          <a
            class="btn btn--outline btn--sm"
            href="https://www.tiktok.com/@gowtennis"
            target="_blank"
            rel="noopener noreferrer"
            >TikTok</a
          >
        </div>
      </div>

      <div class="feed__bar">
        <div class="feed__tabs" role="tablist">
          <button
            v-for="k in ['semua', 'instagram', 'tiktok']"
            :key="k"
            role="tab"
            :aria-selected="filter === k"
            class="feed__tab"
            :class="{ 'is-active': filter === k }"
            @click="filter = k"
          >
            {{ k === 'semua' ? 'Semua' : k === 'instagram' ? 'Instagram' : 'TikTok' }}
            <span class="feed__count">{{ jumlahPer[k] }}</span>
          </button>
        </div>

        <label class="feed__toggle">
          <input v-model="embedPenuh" type="checkbox" />
          <span>Muat semua embed</span>
        </label>
      </div>

      <p v-if="loading" class="feed__state">Memuat kegiatan…</p>

      <div v-else-if="error" class="feed__state feed__state--error">
        <p>Gagal memuat feed: {{ error }}</p>
        <button class="btn btn--outline btn--sm" @click="load()">Coba lagi</button>
      </div>

      <template v-else>
        <div class="feed__grid">
          <article
            v-for="item in terfilter"
            :key="`${item.platform}-${item.id}`"
            class="feed__card"
            :class="{ 'feed__card--embed': tampilEmbed(item) }"
          >
            <!-- Embed resmi dari Instagram/TikTok. -->
            <div v-if="tampilEmbed(item)" class="feed__embed" v-html="item.embed_html" />

            <!-- Kartu ringkas: tidak memuat script pihak ketiga sama sekali. -->
            <a
              v-else
              class="feed__preview"
              :href="item.url"
              target="_blank"
              rel="noopener noreferrer"
            >
              <div class="feed__thumb">
                <img v-if="item.thumbnail" :src="item.thumbnail" :alt="item.judul || ''" loading="lazy" />
                <span v-else class="feed__thumb-ph" aria-hidden="true">
                  {{ item.platform === 'tiktok' ? '♪' : '◎' }}
                </span>
                <span class="feed__badge" :class="`feed__badge--${item.platform}`">
                  {{ item.platform === 'tiktok' ? 'TikTok' : item.tipe === 'reel' ? 'Reel' : 'Post' }}
                </span>
              </div>
              <div class="feed__body">
                <h3 class="feed__title">{{ item.judul || 'Lihat postingan' }}</h3>
                <p v-if="item.tanggal" class="feed__date">{{ tanggalTampil(item.tanggal) }}</p>
                <span class="feed__open">Buka di {{ item.platform === 'tiktok' ? 'TikTok' : 'Instagram' }} →</span>
              </div>
            </a>
          </article>
        </div>

        <p v-if="!terfilter.length" class="feed__state">
          Belum ada konten untuk filter ini.
        </p>

        <!-- Transparansi: dari mana data ini datang dan apa yang belum otomatis. -->
        <details v-if="data" class="feed__meta">
          <summary>
            Sumber data: {{ data.sumber }}
            <span v-if="data.peringatan?.length" class="feed__warn-dot" title="Ada catatan"></span>
          </summary>
          <ul>
            <li>Mode: <code>{{ data.mode }}</code></li>
            <li>Jumlah item: {{ data.jumlah }}</li>
            <li>Diperbarui: {{ data.diperbarui }}</li>
            <li v-for="(w, i) in data.peringatan" :key="i" class="feed__warn">{{ w }}</li>
          </ul>
        </details>
      </template>
    </div>
  </section>
</template>

<style scoped>
.feed__head {
  display: flex;
  flex-wrap: wrap;
  gap: 24px;
  justify-content: space-between;
  align-items: flex-end;
  margin-bottom: 30px;
}

.feed__links {
  display: flex;
  gap: 10px;
}

.feed__bar {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  justify-content: space-between;
  align-items: center;
  padding-bottom: 18px;
  border-bottom: 1px solid var(--line);
  margin-bottom: 28px;
}

.feed__tabs {
  display: flex;
  gap: 6px;
}

.feed__tab {
  display: inline-flex;
  align-items: center;
  gap: 7px;
  border: 1px solid var(--line);
  background: #fff;
  border-radius: 999px;
  padding: 8px 16px;
  font-family: var(--font-body);
  font-size: 0.87rem;
  font-weight: 600;
  color: var(--muted);
  cursor: pointer;
  transition: all 0.16s ease;
}

.feed__tab:hover {
  border-color: var(--navy-600);
  color: var(--navy-800);
}

.feed__tab.is-active {
  background: var(--navy-800);
  border-color: var(--navy-800);
  color: #fff;
}

.feed__count {
  font-size: 0.72rem;
  background: rgba(0, 0, 0, 0.08);
  padding: 1px 7px;
  border-radius: 999px;
}

.feed__tab.is-active .feed__count {
  background: var(--lime-400);
  color: var(--navy-900);
}

.feed__toggle {
  display: inline-flex;
  align-items: center;
  gap: 9px;
  font-size: 0.86rem;
  color: var(--muted);
  cursor: pointer;
  user-select: none;
}

.feed__toggle input {
  width: 16px;
  height: 16px;
  accent-color: var(--navy-800);
  cursor: pointer;
}

.feed__grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(290px, 1fr));
  gap: 22px;
  align-items: start;
}

.feed__card {
  border-radius: var(--radius);
  overflow: hidden;
}

.feed__card--embed {
  background: transparent;
  border: 0;
  min-height: 120px;
}

.feed__embed :deep(iframe),
.feed__embed :deep(blockquote) {
  max-width: 100% !important;
  min-width: 0 !important;
  margin: 0 !important;
  border-radius: var(--radius) !important;
}

.feed__preview {
  display: flex;
  flex-direction: column;
  height: 100%;
  text-decoration: none;
  color: inherit;
  background: #fff;
  border: 1px solid var(--line);
  border-radius: var(--radius);
  overflow: hidden;
  box-shadow: var(--shadow-sm);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.feed__preview:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow);
}

.feed__thumb {
  position: relative;
  aspect-ratio: 4 / 5;
  background: linear-gradient(150deg, var(--navy-800), var(--navy-600));
  display: grid;
  place-items: center;
  overflow: hidden;
}

.feed__thumb img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.feed__thumb-ph {
  font-size: 3rem;
  color: rgba(215, 232, 75, 0.5);
}

.feed__badge {
  position: absolute;
  top: 12px;
  left: 12px;
  font-size: 0.66rem;
  font-weight: 800;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  padding: 4px 10px;
  border-radius: 999px;
  backdrop-filter: blur(6px);
}

.feed__badge--instagram {
  background: rgba(255, 255, 255, 0.92);
  color: var(--navy-900);
}

.feed__badge--tiktok {
  background: rgba(0, 0, 0, 0.72);
  color: #fff;
}

.feed__body {
  padding: 18px 18px 20px;
  display: flex;
  flex-direction: column;
  gap: 6px;
  flex: 1;
}

.feed__title {
  font-family: var(--font-body);
  font-size: 0.99rem;
  font-weight: 650;
  text-transform: none;
  letter-spacing: 0;
  line-height: 1.35;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.feed__date {
  font-size: 0.79rem;
  color: var(--muted-light);
}

.feed__open {
  margin-top: auto;
  padding-top: 10px;
  font-size: 0.82rem;
  font-weight: 650;
  color: var(--navy-600);
}

.feed__state {
  padding: 44px 0;
  color: var(--muted);
  text-align: center;
}

.feed__state--error {
  display: grid;
  gap: 14px;
  justify-items: center;
  color: #b91c1c;
}

.feed__meta {
  margin-top: 34px;
  font-size: 0.83rem;
  color: var(--muted);
  border-top: 1px solid var(--line);
  padding-top: 18px;
}

.feed__meta summary {
  cursor: pointer;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 8px;
}

.feed__meta ul {
  margin: 12px 0 0;
  padding-left: 18px;
  display: grid;
  gap: 6px;
}

.feed__meta code {
  background: var(--paper-soft);
  padding: 1px 6px;
  border-radius: 4px;
  font-size: 0.86em;
}

.feed__warn {
  color: #92400e;
}

.feed__warn-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #f59e0b;
  display: inline-block;
}
</style>
