<script setup>
import { computed } from 'vue'
import { STATIC_MODE, useApi } from './composables/useApi'
import SiteHeader from './components/SiteHeader.vue'
import HeroSection from './components/HeroSection.vue'
import AboutSection from './components/AboutSection.vue'
import ProgramSection from './components/ProgramSection.vue'
import VenueSection from './components/VenueSection.vue'
import SocialFeed from './components/SocialFeed.vue'
import ContactSection from './components/ContactSection.vue'
import SiteFooter from './components/SiteFooter.vue'

const { data: profil, error: galatProfil, load: muatProfil } = useApi('/profile')
const { data: stats } = useApi('/stats')

const brand = computed(() => profil.value?.brand)
const nilai = computed(() => profil.value?.nilai ?? [])
const program = computed(() => profil.value?.program ?? [])
const venue = computed(() => profil.value?.venue ?? [])
</script>

<template>
  <SiteHeader />

  <main>
    <div v-if="galatProfil" class="boot-error">
      <h1>{{ STATIC_MODE ? 'Data tidak termuat' : 'Backend belum jalan' }}</h1>
      <p>{{ galatProfil }}</p>
      <p v-if="STATIC_MODE" class="boot-error__hint">
        Berkas <code>api/profile.json</code> tidak ditemukan. Bangun ulang:
        <code>python3 tools/buat_static.py &amp;&amp; npm run build:static</code>
      </p>
      <p v-else class="boot-error__hint">
        Jalankan API-nya dulu:
        <code>cd backend &amp;&amp; .venv/bin/uvicorn app.main:app --reload --port 8010</code>
      </p>
      <button class="btn btn--primary btn--sm" @click="muatProfil()">Coba lagi</button>
    </div>

    <template v-else>
      <HeroSection :brand="brand" :stats="stats" />
      <AboutSection :brand="brand" :nilai="nilai" />
      <ProgramSection :program="program" />
      <VenueSection :venue="venue" />
      <SocialFeed />
      <ContactSection :kontak="profil?.kontak" :program="program" />
    </template>
  </main>

  <SiteFooter
    :brand="brand"
    :sosial="profil?.sosial"
    :meta="profil?.meta"
    :kontak="profil?.kontak"
  />
</template>

<style scoped>
.boot-error {
  max-width: 620px;
  margin: 160px auto 120px;
  padding: 0 var(--gutter);
  text-align: center;
  display: grid;
  gap: 14px;
  justify-items: center;
}

.boot-error h1 {
  font-size: 2rem;
}

.boot-error p {
  color: var(--muted);
}

.boot-error__hint code {
  display: inline-block;
  margin-top: 6px;
  background: var(--paper-soft);
  border: 1px solid var(--line);
  padding: 8px 12px;
  border-radius: 8px;
  font-size: 0.85rem;
}
</style>
