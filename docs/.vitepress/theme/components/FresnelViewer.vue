<template>
  <div class="technical-figure">
    <div class="figure-header">
      <span class="label">SIMULADOR INTERACTIVO</span>
      <span class="desc">Efecto Fresnel (Reflectancia en Ángulos Rasantes)</span>
    </div>
    
    <div class="canvas-wrapper" ref="canvasContainer"></div>

    <div class="controls-panel">
      <div class="control-group">
        <div class="control-label">
          <span>Exponente Fresnel (Potencia):</span>
          <code>{{ fresnelExponent.toFixed(1) }}</code>
        </div>
        <input type="range" min="0.5" max="5.0" step="0.1" v-model.number="fresnelExponent" @input="updateFresnel" />
        <div class="hints">
          <span>0.5 (Brillo ancho en todo el borde)</span>
          <span>5.0 (Brillo filoso en la silueta)</span>
        </div>
      </div>

      <div class="control-group">
        <div class="control-label">
          <span>Tinte del Borde Fresnel:</span>
        </div>
        <div class="color-presets">
          <button v-for="c in colorPresets" :key="c.name" :style="{ background: c.color }" :title="c.name" @click="setFresnelColor(c.color)" class="color-btn"></button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue';

const canvasContainer = ref(null);
const fresnelExponent = ref(2.5);
const fresnelColor = ref('#38bdf8'); // Azulado rim por defecto

const colorPresets = [
  { name: 'Azul Rim', color: '#38bdf8' },
  { name: 'Blanco Puro', color: '#ffffff' },
  { name: 'Dorado Solar', color: '#fbbf24' },
  { name: 'Rojo Alerta', color: '#ef4444' },
  { name: 'Verde', color: '#34d399' }
];

let scene, camera, renderer, customMesh, animId, customMaterial;

// Vertex Shader para Fresnel
const vertexShader = `
  varying vec3 vNormal;
  varying vec3 vViewPosition;
  void main() {
    vNormal = normalize(normalMatrix * normal);
    vec4 mvPosition = modelViewMatrix * vec4(position, 1.0);
    vViewPosition = -mvPosition.xyz;
    gl_Position = projectionMatrix * mvPosition;
  }
`;

// Fragment Shader para Fresnel
const fragmentShader = `
  uniform vec3 uBaseColor;
  uniform vec3 uFresnelColor;
  uniform float uExponent;
  varying vec3 vNormal;
  varying vec3 vViewPosition;

  void main() {
    vec3 normal = normalize(vNormal);
    vec3 viewDir = normalize(vViewPosition);

    // Ecuación de Fresnel: 1.0 - dot(Normal, ViewDir)
    float fresnel = 1.0 - max(dot(normal, viewDir), 0.0);
    fresnel = pow(fresnel, uExponent);

    vec3 finalColor = mix(uBaseColor, uFresnelColor, fresnel);
    gl_FragColor = vec4(finalColor, 1.0);
  }
`;

const initThree = async () => {
  if (typeof window === 'undefined') return;
  const THREE = await import('three');

  const container = canvasContainer.value;
  if (!container) return;

  const width = container.clientWidth || 600;
  const height = 250;

  scene = new THREE.Scene();
  scene.background = new THREE.Color(0x111217);

  camera = new THREE.PerspectiveCamera(40, width / height, 0.1, 100);
  camera.position.set(0, 0, 3.4);

  renderer = new THREE.WebGLRenderer({ antialias: true });
  renderer.setSize(width, height);
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  container.innerHTML = '';
  container.appendChild(renderer.domElement);

  const geo = new THREE.IcosahedronGeometry(1.05, 4);
  customMaterial = new THREE.ShaderMaterial({
    vertexShader,
    fragmentShader,
    uniforms: {
      uBaseColor: { value: new THREE.Color(0x1e293b) },
      uFresnelColor: { value: new THREE.Color(fresnelColor.value) },
      uExponent: { value: fresnelExponent.value }
    }
  });

  customMesh = new THREE.Mesh(geo, customMaterial);
  scene.add(customMesh);

  const animate = () => {
    animId = requestAnimationFrame(animate);
    customMesh.rotation.y += 0.005;
    customMesh.rotation.x += 0.002;
    renderer.render(scene, camera);
  };
  animate();
};

const updateFresnel = () => {
  if (customMaterial) {
    customMaterial.uniforms.uExponent.value = fresnelExponent.value;
  }
};

const setFresnelColor = (hex) => {
  fresnelColor.value = hex;
  if (customMaterial) {
    customMaterial.uniforms.uFresnelColor.value.set(hex);
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
  height: 250px;
}

.controls-panel {
  padding: 12px 16px;
  background: #f9fafb;
  border-top: 1px solid #e5e7eb;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

.control-group {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.control-label {
  display: flex;
  justify-content: space-between;
  font-size: 11.5px;
  font-weight: 600;
  color: #111827;
}

.control-label code {
  color: #111827;
  font-size: 10.5px;
}

input[type="range"] {
  width: 100%;
  accent-color: #111827;
  cursor: pointer;
}

.hints {
  display: flex;
  justify-content: space-between;
  font-size: 9.5px;
  color: #6b7280;
}

.color-presets {
  display: flex;
  gap: 8px;
  align-items: center;
}

.color-btn {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  border: 1px solid #9ca3af;
  cursor: pointer;
}

@media (max-width: 768px) {
  .controls-panel {
    grid-template-columns: 1fr;
  }
}
</style>
