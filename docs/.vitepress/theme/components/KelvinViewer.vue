<template>
  <div class="technical-figure">
    <div class="figure-header">
      <span class="label">SIMULADOR INTERACTIVO</span>
      <span class="desc">Temperatura de Color en Grados Kelvin (K)</span>
    </div>
    
    <div class="canvas-wrapper" ref="canvasContainer"></div>

    <div class="controls-panel">
      <div class="control-group-full">
        <div class="control-label">
          <span>Temperatura de Color:</span>
          <code>{{ kelvinValue }} K — {{ kelvinDescription }}</code>
        </div>
        <input type="range" min="1800" max="10000" step="100" v-model.number="kelvinValue" @input="updateKelvin" />
        <div class="kelvin-bar">
          <span style="color: #ea580c;">1800K (Vela / Fuego)</span>
          <span style="color: #eab308;">3200K (Tungsteno)</span>
          <span style="color: #94a3b8;">5500K (Sol Mediodía)</span>
          <span style="color: #38bdf8;">10000K (Cielo Azul)</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue';

const canvasContainer = ref(null);
const kelvinValue = ref(5500);

let scene, camera, renderer, sphereMesh, mainLight, animId;

const kelvinDescription = computed(() => {
  const k = kelvinValue.value;
  if (k < 2400) return 'Luz muy cálida (Vela / Fuego)';
  if (k < 3500) return 'Luz cálida (Bombilla de casa / Atardecer)';
  if (k < 4500) return 'Blanco cálido (Luz fluorescente)';
  if (k < 6000) return 'Luz neutra natural (Sol al mediodía)';
  if (k < 7500) return 'Luz fría (Cielo ligeramente nublado)';
  return 'Luz muy fría (Sombras exteriores en día despejado)';
});

// Función física simplificada para convertir Kelvin a RGB
function kelvinToRGB(k) {
  const temp = k / 100;
  let r, g, b;

  if (temp <= 66) {
    r = 255;
    g = 99.4708025861 * Math.log(temp) - 161.1195681661;
    b = temp <= 19 ? 0 : 138.5177312231 * Math.log(temp - 10) - 305.0447927307;
  } else {
    r = 329.698727446 * Math.pow(temp - 60, -0.1332047592);
    g = 288.1221695283 * Math.pow(temp - 60, -0.0755148492);
    b = 255;
  }

  return {
    r: Math.max(0, Math.min(255, r)) / 255,
    g: Math.max(0, Math.min(255, g)) / 255,
    b: Math.max(0, Math.min(255, b)) / 255
  };
}

const initThree = async () => {
  if (typeof window === 'undefined') return;
  const THREE = await import('three');

  const container = canvasContainer.value;
  if (!container) return;

  const width = container.clientWidth || 600;
  const height = 240;

  scene = new THREE.Scene();
  scene.background = new THREE.Color(0x18181b);

  camera = new THREE.PerspectiveCamera(40, width / height, 0.1, 100);
  camera.position.set(0, 0, 3.2);

  renderer = new THREE.WebGLRenderer({ antialias: true });
  renderer.setSize(width, height);
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  container.innerHTML = '';
  container.appendChild(renderer.domElement);

  const geo = new THREE.SphereGeometry(1, 48, 48);
  const mat = new THREE.MeshStandardMaterial({
    color: 0xd4d4d8,
    roughness: 0.35,
    metalness: 0.1
  });
  sphereMesh = new THREE.Mesh(geo, mat);
  scene.add(sphereMesh);

  mainLight = new THREE.DirectionalLight(0xffffff, 2.5);
  mainLight.position.set(2, 1.5, 2);
  scene.add(mainLight);

  const fillLight = new THREE.DirectionalLight(0x27272a, 0.4);
  fillLight.position.set(-2, -1, -1);
  scene.add(fillLight);

  updateKelvin();

  const animate = () => {
    animId = requestAnimationFrame(animate);
    sphereMesh.rotation.y += 0.004;
    renderer.render(scene, camera);
  };
  animate();
};

const updateKelvin = () => {
  if (mainLight) {
    const rgb = kelvinToRGB(kelvinValue.value);
    mainLight.color.setRGB(rgb.r, rgb.g, rgb.b);
  }
};

onMounted(() => {
  initThree();
});

onBeforeUnmount(() => {
  if (animId) cancelAnimationFrame(animId);
  if (renderer) renderer.dispose();
});
</script>

<style scoped>
.technical-figure {
  border: 1px solid #d1d5db;
  border-radius: 4px;
  margin: 16px 0;
  overflow: hidden;
  background: #ffffff;
}

.figure-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 14px;
  background: #f9fafb;
  border-bottom: 1px solid #e5e7eb;
}

.label {
  font-family: 'JetBrains Mono', monospace;
  font-size: 10px;
  font-weight: 700;
  color: #111827;
  letter-spacing: 0.5px;
}

.desc {
  font-size: 11.5px;
  color: #6b7280;
}

.canvas-wrapper {
  width: 100%;
  height: 240px;
}

.controls-panel {
  padding: 12px 16px;
  background: #f9fafb;
  border-top: 1px solid #e5e7eb;
}

.control-group-full {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.control-label {
  display: flex;
  justify-content: space-between;
  font-size: 12px;
  font-weight: 600;
  color: #111827;
}

.control-label code {
  color: #111827;
  font-size: 11px;
}

input[type="range"] {
  width: 100%;
  accent-color: #111827;
  cursor: pointer;
}

.kelvin-bar {
  display: flex;
  justify-content: space-between;
  font-size: 9.5px;
  font-weight: 600;
}
</style>
