<script setup>
defineProps({
  brand: { type: Object, default: null },
  nilai: { type: Array, default: () => [] },
})
</script>

<template>
  <section id="tentang" class="section">
    <div class="wrap about">
      <div class="about__head">
        <span class="eyebrow">Tentang Kami</span>
        <h2 class="section-title">Tenis yang tidak bikin kapok</h2>
        <p class="about__body">{{ brand?.deskripsi_panjang }}</p>
      </div>

      <ul class="about__grid">
        <li v-for="(n, i) in nilai" :key="n.judul" class="card about__item">
          <span class="about__num">{{ String(i + 1).padStart(2, '0') }}</span>
          <h3>{{ n.judul }}</h3>
          <p>{{ n.isi }}</p>
        </li>
      </ul>
    </div>
  </section>
</template>

<style scoped>
.about__head {
  max-width: 78ch;
  margin-bottom: 52px;
}

.about__body {
  color: var(--muted);
  font-size: 1.04rem;
  margin-top: 18px;
}

.about__grid {
  list-style: none;
  margin: 0;
  padding: 0;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(248px, 1fr));
  gap: 20px;
}

.about__item {
  padding: 28px 24px 26px;
  position: relative;
}

.about__num {
  display: inline-block;
  font-family: var(--font-display);
  font-size: 0.82rem;
  font-weight: 800;
  letter-spacing: 0.1em;
  color: var(--navy-800);
  background: var(--lime-400);
  padding: 3px 9px;
  border-radius: 6px;
  margin-bottom: 14px;
}

.about__item h3 {
  font-size: 1.32rem;
  margin-bottom: 9px;
}

.about__item p {
  color: var(--muted);
  font-size: 0.94rem;
}
</style>
