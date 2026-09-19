<script setup>
import logoUrl from '../assets/logo-gowtennis.png'
defineProps({
  brand: { type: Object, default: null },
  sosial: { type: Object, default: null },
  meta: { type: Object, default: null },
  kontak: { type: Object, default: null },
})
</script>

<template>
  <footer class="ftr">
    <div class="wrap ftr__inner">
      <div class="ftr__brand">
        <img :src="logoUrl" alt="" width="46" height="46" />
        <div>
          <p class="ftr__name">{{ brand?.nama || 'Gow! Tennis' }}</p>
          <p class="ftr__tag">{{ brand?.tagline }}</p>
        </div>
      </div>

      <nav class="ftr__links" aria-label="Kanal sosial">
        <a :href="sosial?.instagram?.url" target="_blank" rel="noopener noreferrer">
          Instagram {{ sosial?.instagram?.handle }}
        </a>
        <a :href="sosial?.tiktok?.url" target="_blank" rel="noopener noreferrer">
          TikTok {{ sosial?.tiktok?.handle }}
        </a>
        <a
          v-if="kontak?.whatsapp_group"
          :href="kontak.whatsapp_group"
          target="_blank"
          rel="noopener noreferrer"
          >Grup WhatsApp</a
        >
      </nav>

      <p class="ftr__note">
        {{ brand?.kota }}, {{ brand?.negara }} ·
        <span v-if="meta?.tanggal_riset">Data profil per {{ meta.tanggal_riset }}</span>
      </p>
    </div>
  </footer>
</template>

<style scoped>
.ftr {
  background: var(--navy-950);
  color: rgba(255, 255, 255, 0.62);
  padding: 44px 0;
  border-top: 1px solid rgba(255, 255, 255, 0.08);
}

.ftr__inner {
  display: flex;
  flex-wrap: wrap;
  gap: 24px;
  align-items: center;
  justify-content: space-between;
}

.ftr__brand {
  display: flex;
  align-items: center;
  gap: 13px;
}

.ftr__brand img {
  border-radius: 50%;
}

.ftr__name {
  font-family: var(--font-display);
  font-size: 1.22rem;
  font-weight: 800;
  text-transform: uppercase;
  color: #fff;
}

.ftr__tag {
  font-size: 0.82rem;
}

.ftr__links {
  display: flex;
  gap: 22px;
  flex-wrap: wrap;
}

.ftr__links a {
  color: rgba(255, 255, 255, 0.78);
  text-decoration: none;
  font-size: 0.88rem;
  transition: color 0.16s ease;
}

.ftr__links a:hover {
  color: var(--lime-400);
}

.ftr__note {
  font-size: 0.79rem;
  color: rgba(255, 255, 255, 0.4);
  width: 100%;
  padding-top: 20px;
  border-top: 1px solid rgba(255, 255, 255, 0.07);
}
</style>
