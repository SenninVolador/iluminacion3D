import { defineConfig } from 'vitepress';

export default defineConfig({
  title: "Iluminación 3D & Shaders",
  description: "Portal académico interactivo para videojuegos - Profesor Daniel Rojas (UNIACC)",
  base: "/iluminacion3D/", // Nombre exacto del repo en GitHub
  cleanUrls: true,
  themeConfig: {
    logo: { text: "⚡ 3D LIGHTING & SHADERS" },
    siteTitle: "Iluminación 3D & Shaders",
    nav: [
      { text: "Inicio", link: "/" },
      { text: "Clases", link: "/clases/clase-01" },
      { text: "Shaders PBR", link: "/shaders/01-fundamentos-pbr" },
      { text: "Glosario", link: "/glosario" },
      { text: "Material Visual (PDFs)", link: "/recursos/material-visual" }
    ],
    sidebar: {
      '/clases/': [
        {
          text: 'Módulo 1: Fundamentos y Clases',
          items: [
            { text: 'Clase 01: Fundamentos & 3-Point Lighting', link: '/clases/clase-01' },
            { text: 'Clase 02: Taller 3-Point, Sol, Cielo & Movilidad', link: '/clases/clase-02' },
            { text: 'Clase 03: Shaders PBR en el Busto, Sol & Luces', link: '/clases/clase-03' },
            { text: 'Guía Visual al Jugador', link: '/clases/lenguaje-visual' }
          ]
        }
      ],
      '/shaders/': [
        {
          text: 'Módulo 2: Shaders y Materiales PBR',
          items: [
            { text: '01. Fundamentos PBR y Mapas de Textura', link: '/shaders/01-fundamentos-pbr' },
            { text: '02. Master Materials e Instances (UE5)', link: '/shaders/02-master-materials' },
            { text: '03. Modelos de Sombreado (Shading Models)', link: '/shaders/03-shading-models' },
            { text: '04. Matemáticas de Shaders (Fresnel & Lerp)', link: '/shaders/04-matematicas-shaders' }
          ]
        }
      ],
      '/': [
        {
          text: 'Contenido del Curso',
          items: [
            { text: '📖 Glosario de Términos (Clase a Clase)', link: '/glosario' },
            { text: '🗺️ Mapa de Contenidos (MOC)', link: '/moc' },
            { text: '📄 Fichas Técnicas y Descargas', link: '/recursos/material-visual' }
          ]
        }
      ]
    },
    search: {
      provider: 'local'
    },
    footer: {
      message: 'Ramo de Iluminación 3D y Shaders para Videojuegos',
      copyright: 'Profesor Daniel Rojas · UNIACC'
    }
  }
});
