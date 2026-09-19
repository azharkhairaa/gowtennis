<script setup>
import logoUrl from '../assets/logo-gowtennis.png'
import { onMounted, onUnmounted, ref } from 'vue'

const scrolled = ref(false)
const menuTerbuka = ref(false)

const tautan = [
  { href: '#tentang', label: 'Tentang' },
  { href: '#program', label: 'Program' },
  { href: '#lapangan', label: 'Lapangan' },
  { href: '#sosial', label: 'Kegiatan' },
  { href: '#gabung', label: 'Gabung' },
]

function onScroll() {
  scrolled.value = window.scrollY > 24
}

onMounted(() => window.addEventListener('scroll', onScroll, { passive: true }))
onUnmounted(() => window.removeEventListener('scroll', onScroll))
</script>

<template>
  <header class="hdr" :class="{ 'hdr--solid': scrolled }">
    <div class="wrap hdr__inner">
      <a href="#top" class="hdr__brand">
        <img :src="logoUrl" alt="" width="40" height="40" />
        <span>Gow! Tennis</span>
      </a>

      <nav class="hdr__nav" :class="{ 'is-open': menuTerbuka }">
        <a
          v-for="t in tautan"
          :key="t.href"
          :href="t.href"
          @click="menuTerbuka = false"
          >{{ t.label }}</a
        >
      </nav>

      <a href="#gabung" class="btn btn--primary btn--sm hdr__cta">Daftar Sesi</a>

      <button
        class="hdr__burger"
        :aria-expanded="menuTerbuka"
        aria-label="Buka menu"
        @click="menuTerbuka = !menuTerbuka"
      >
        <span></span><span></span><span></span>
      </button>
    </div>
  </header>
</template>

<style scoped>
.hdr {
  position: fixed;
  inset: 0 0 auto 0;
  z-index: 60;
  transition: background 0.25s ease, box-shadow 0.25s ease, backdrop-filter 0.25s ease;
}

.hdr--solid {
  background: rgba(6, 14, 29, 0.9);
  backdrop-filter: blur(12px);
  box-shadow: 0 1px 0 rgba(255, 255, 255, 0.08);
}

.hdr__inner {
  display: flex;
  align-items: center;
  gap: 20px;
  height: 72px;
}

.hdr__brand {
  display: flex;
  align-items: center;
  gap: 10px;
  font-family: var(--font-display);
  font-size: 1.22rem;
  font-weight: 800;
  text-transform: uppercase;
  color: #fff;
  text-decoration: none;
  letter-spacing: 0.01em;
}

.hdr__brand img {
  border-radius: 50%;
}

.hdr__nav {
  display: flex;
  gap: 26px;
  margin-left: auto;
}

.hdr__nav a {
  color: rgba(255, 255, 255, 0.82);
  text-decoration: none;
  font-size: 0.9rem;
  font-weight: 550;
  transition: color 0.16s ease;
}

.hdr__nav a:hover {
  color: var(--lime-400);
}

.hdr__burger {
  display: none;
  flex-direction: column;
  gap: 5px;
  background: none;
  border: 0;
  cursor: pointer;
  padding: 8px;
}

.hdr__burger span {
  width: 22px;
  height: 2px;
  background: #fff;
  border-radius: 2px;
}

@media (max-width: 860px) {
  .hdr__cta {
    display: none;
  }
  .hdr__burger {
    display: flex;
    margin-left: auto;
  }
  .hdr__nav {
    position: absolute;
    top: 72px;
    left: 0;
    right: 0;
    flex-direction: column;
    gap: 0;
    background: rgba(6, 14, 29, 0.98);
    backdrop-filter: blur(12px);
    padding: 0 var(--gutter);
    max-height: 0;
    overflow: hidden;
    transition: max-height 0.28s ease;
  }
  .hdr__nav.is-open {
    max-height: 320px;
    padding: 8px var(--gutter) 20px;
  }
  .hdr__nav a {
    padding: 13px 0;
    border-bottom: 1px solid rgba(255, 255, 255, 0.08);
  }
}
</style>
