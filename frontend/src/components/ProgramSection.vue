<script setup>
defineProps({
  program: { type: Array, default: () => [] },
})
</script>

<template>
  <section id="program" class="section section--dark">
    <div class="wrap">
      <div class="prog__head">
        <div>
          <span class="eyebrow">Program &amp; Biaya</span>
          <h2 class="section-title">Pilih sesi yang cocok</h2>
        </div>
        <p class="section-lead">
          Semua kelas terbuka untuk pemula. Perlengkapan dasar sudah termasuk,
          jadi tidak perlu beli raket dulu untuk mencoba.
        </p>
      </div>

      <div class="prog__grid">
        <article
          v-for="p in program"
          :key="p.nama"
          class="prog__card"
          :class="{ 'prog__card--unggulan': p.nama === 'Tennis Malam Minggu' }"
        >
          <span v-if="p.nama === 'Tennis Malam Minggu'" class="prog__tag">
            Paling Ramai
          </span>

          <h3 class="prog__name">{{ p.nama }}</h3>
          <p v-if="p.level" class="prog__level">{{ p.level }}</p>

          <p class="prog__price">{{ p.harga }}</p>

          <dl class="prog__meta">
            <div v-if="p.jadwal">
              <dt>Jadwal</dt>
              <dd>{{ p.jadwal }}</dd>
            </div>
            <div v-if="p.durasi">
              <dt>Durasi</dt>
              <dd>{{ p.durasi }}</dd>
            </div>
            <div v-if="p.kapasitas">
              <dt>Kuota</dt>
              <dd>{{ p.kapasitas }}</dd>
            </div>
            <div v-if="p.lokasi">
              <dt>Lokasi</dt>
              <dd>{{ p.lokasi }}</dd>
            </div>
          </dl>

          <ul v-if="p.termasuk?.length" class="prog__incl">
            <li v-for="t in p.termasuk" :key="t">{{ t }}</li>
          </ul>

          <a href="#gabung" class="btn btn--primary btn--sm prog__cta">Daftar</a>
        </article>
      </div>

      <p class="prog__note">
        Harga dan jadwal di atas mengikuti pengumuman terakhir di kanal sosial
        Gow! Tennis. Konfirmasi ulang lewat DM sebelum datang, karena agenda bisa
        berubah mengikuti ketersediaan lapangan.
      </p>
    </div>
  </section>
</template>

<style scoped>
.prog__head {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 32px;
  align-items: end;
  margin-bottom: 46px;
}

.prog__grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(276px, 1fr));
  gap: 20px;
}

.prog__card {
  position: relative;
  display: flex;
  flex-direction: column;
  padding: 30px 26px 28px;
  border: 1px solid var(--line-dark);
  border-radius: var(--radius-lg);
  background: rgba(255, 255, 255, 0.035);
  transition: transform 0.2s ease, border-color 0.2s ease, background 0.2s ease;
}

.prog__card:hover {
  transform: translateY(-5px);
  border-color: rgba(215, 232, 75, 0.45);
  background: rgba(255, 255, 255, 0.06);
}

.prog__card--unggulan {
  border-color: var(--lime-400);
  background: rgba(215, 232, 75, 0.07);
}

.prog__tag {
  position: absolute;
  top: -11px;
  left: 26px;
  background: var(--lime-400);
  color: var(--navy-900);
  font-size: 0.68rem;
  font-weight: 800;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  padding: 4px 11px;
  border-radius: 999px;
}

.prog__name {
  font-size: 1.62rem;
  margin-bottom: 5px;
}

.prog__level {
  font-size: 0.78rem;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--lime-400);
  margin-bottom: 18px;
}

.prog__price {
  font-family: var(--font-display);
  font-size: 2.15rem;
  font-weight: 700;
  line-height: 1;
  margin-bottom: 22px;
}

.prog__meta {
  margin: 0 0 20px;
  display: grid;
  gap: 11px;
}

.prog__meta > div {
  display: grid;
  grid-template-columns: 74px 1fr;
  gap: 10px;
  align-items: baseline;
}

.prog__meta dt {
  font-size: 0.68rem;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: rgba(255, 255, 255, 0.45);
}

.prog__meta dd {
  margin: 0;
  font-size: 0.9rem;
  color: rgba(255, 255, 255, 0.86);
}

.prog__incl {
  list-style: none;
  margin: 0 0 24px;
  padding: 18px 0 0;
  border-top: 1px solid var(--line-dark);
  display: grid;
  gap: 8px;
}

.prog__incl li {
  position: relative;
  padding-left: 22px;
  font-size: 0.89rem;
  color: rgba(255, 255, 255, 0.78);
}

.prog__incl li::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0.48em;
  width: 9px;
  height: 9px;
  border-radius: 50%;
  background: var(--lime-400);
}

.prog__cta {
  margin-top: auto;
  align-self: flex-start;
}

.prog__note {
  margin-top: 34px;
  font-size: 0.86rem;
  color: rgba(255, 255, 255, 0.5);
  max-width: 76ch;
}

@media (max-width: 820px) {
  .prog__head {
    grid-template-columns: 1fr;
    gap: 16px;
    align-items: start;
  }
}
</style>
