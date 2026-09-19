<script setup>
import logoUrl from '../assets/logo-gowtennis.png'
defineProps({
  brand: { type: Object, default: null },
  stats: { type: Object, default: null },
})

function ringkas(n) {
  if (n == null) return '—'
  return n >= 1000 ? `${(n / 1000).toFixed(1).replace('.0', '')}K` : String(n)
}
</script>

<template>
  <section id="top" class="hero">
    <div class="hero__bg" aria-hidden="true">
      <span class="hero__ball hero__ball--1"></span>
      <span class="hero__ball hero__ball--2"></span>
      <span class="hero__court"></span>
    </div>

    <div class="wrap hero__inner">
      <div class="hero__copy">
        <span class="hero__badge">
          <span class="hero__dot"></span>
          {{ brand?.kategori || 'Community' }} · {{ brand?.kota || 'Bandung' }}
        </span>

        <h1 class="hero__title">
          Gow!<br /><span class="hero__title-accent">Tennis</span>
        </h1>

        <p class="hero__tagline">
          “{{ brand?.tagline || 'Kadang Melesat, Kadang Meleset' }}”
        </p>

        <p class="hero__lead">
          {{
            brand?.deskripsi_singkat ||
            'Komunitas tenis di Bandung untuk pemula sampai upper beginner.'
          }}
        </p>

        <div class="hero__actions">
          <a href="#gabung" class="btn btn--primary">Ikut Sesi Pertama</a>
          <a href="#program" class="btn btn--ghost">Lihat Program</a>
        </div>

        <dl class="hero__stats">
          <div>
            <dt>Instagram</dt>
            <dd>{{ ringkas(stats?.instagram_followers) }}</dd>
          </div>
          <div>
            <dt>TikTok</dt>
            <dd>{{ ringkas(stats?.tiktok_followers) }}</dd>
          </div>
          <div>
            <dt>Total Likes</dt>
            <dd>{{ ringkas(stats?.tiktok_likes) }}</dd>
          </div>
          <div>
            <dt>Program</dt>
            <dd>{{ stats?.jumlah_program ?? '—' }}</dd>
          </div>
        </dl>
      </div>

      <div class="hero__mark">
        <img :src="logoUrl" alt="Logo Gow! Tennis" width="300" height="300" />
      </div>
    </div>
  </section>
</template>

<style scoped>
.hero {
  position: relative;
  background: linear-gradient(165deg, var(--navy-950) 0%, var(--navy-800) 58%, var(--navy-700) 100%);
  color: #fff;
  padding: 150px 0 88px;
  overflow: hidden;
}

.hero__bg {
  position: absolute;
  inset: 0;
  pointer-events: none;
}

.hero__ball {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  opacity: 0.35;
}

.hero__ball--1 {
  width: 380px;
  height: 380px;
  background: var(--lime-400);
  top: -120px;
  right: -60px;
  opacity: 0.18;
}

.hero__ball--2 {
  width: 300px;
  height: 300px;
  background: #2e6bd6;
  bottom: -140px;
  left: -80px;
  opacity: 0.3;
}

/* Garis-garis tipis meniru marka lapangan tenis. */
.hero__court {
  position: absolute;
  inset: 0;
  background-image: linear-gradient(rgba(255, 255, 255, 0.045) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255, 255, 255, 0.045) 1px, transparent 1px);
  background-size: 120px 120px;
  mask-image: radial-gradient(ellipse at 60% 40%, #000 20%, transparent 75%);
  -webkit-mask-image: radial-gradient(ellipse at 60% 40%, #000 20%, transparent 75%);
}

.hero__inner {
  position: relative;
  display: grid;
  grid-template-columns: 1.25fr 0.75fr;
  gap: 48px;
  align-items: center;
}

.hero__badge {
  display: inline-flex;
  align-items: center;
  gap: 9px;
  padding: 7px 15px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 999px;
  font-size: 0.76rem;
  font-weight: 650;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: rgba(255, 255, 255, 0.88);
}

.hero__dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: var(--lime-400);
  box-shadow: 0 0 0 4px rgba(215, 232, 75, 0.2);
}

.hero__title {
  font-size: clamp(3.6rem, 11vw, 7.2rem);
  margin: 20px 0 6px;
  line-height: 0.88;
}

.hero__title-accent {
  color: var(--lime-400);
}

.hero__tagline {
  font-family: var(--font-display);
  font-size: clamp(1.15rem, 2.6vw, 1.6rem);
  font-weight: 600;
  color: rgba(255, 255, 255, 0.92);
  text-transform: uppercase;
  letter-spacing: 0.02em;
  margin-bottom: 16px;
}

.hero__lead {
  color: rgba(255, 255, 255, 0.7);
  max-width: 52ch;
  font-size: 1.03rem;
}

.hero__actions {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin: 30px 0 42px;
}

.hero__stats {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 10px;
  margin: 0;
  padding-top: 28px;
  border-top: 1px solid rgba(255, 255, 255, 0.14);
  max-width: 520px;
}

.hero__stats dt {
  font-size: 0.68rem;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: rgba(255, 255, 255, 0.5);
  margin-bottom: 4px;
}

.hero__stats dd {
  margin: 0;
  font-family: var(--font-display);
  font-size: 1.85rem;
  font-weight: 700;
  color: var(--lime-400);
  line-height: 1;
}

.hero__mark {
  display: flex;
  justify-content: center;
}

.hero__mark img {
  width: min(300px, 78%);
  height: auto;
  border-radius: 50%;
  box-shadow: 0 30px 70px rgba(0, 0, 0, 0.45);
  animation: apung 6s ease-in-out infinite;
}

@keyframes apung {
  0%,
  100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-14px);
  }
}

@media (max-width: 900px) {
  .hero {
    padding: 126px 0 68px;
  }
  .hero__inner {
    grid-template-columns: 1fr;
    gap: 36px;
  }
  .hero__mark {
    order: -1;
  }
  .hero__mark img {
    width: 160px;
  }
  .hero__stats {
    grid-template-columns: repeat(2, 1fr);
    gap: 18px 10px;
  }
}
</style>
