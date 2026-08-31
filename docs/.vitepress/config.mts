import { defineConfig } from 'vitepress';

export default defineConfig({
  title: "Iluminación 3D",
  description: "Programa académico y repositorio técnico - Profesor Daniel Rojas (UNIACC)",
  base: "/iluminacion3D/",
  cleanUrls: true,
  themeConfig: {
    siteTitle: "Iluminación 3D",
    nav: [
      { text: "Índice", link: "/" },
      { text: "Clases", link: "/clases/clase-01" },
      { text: "Rúbrica Entrega 1", link: "/clases/rubrica-entrega-01" },
      { text: "Shaders PBR", link: "/shaders/01-fundamentos-pbr" },
      { text: "Glosario", link: "/glosario" },
      { text: "Documentos PDF", link: "/recursos/material-visual" }
    ],
    sidebar: {
      '/clases/': [
        {
          text: 'Unidad 1: Iluminación y Composición',
          items: [
            { text: 'Clase 01: Fundamentos y Esquema de 3 Puntos', link: '/clases/clase-01' },
            { text: 'Clase 02: Taller de 3 Puntos, Sol, Cielo y Movilidad', link: '/clases/clase-02' },
            { text: 'Clase 03: Shaders PBR en el Busto, Sol y Fuentes Locales', link: '/clases/clase-03' },
            { text: 'Lectura: Lenguaje Visual y Guía al Jugador', link: '/clases/lenguaje-visual' },
            { text: '📋 Rúbrica: Entrega N°1 (3-Point & Shaders)', link: '/clases/rubrica-entrega-01' }
          ]
        }
      ],
      '/shaders/': [
        {
          text: 'Unidad 2: Shaders y Materiales PBR',
          items: [
            { text: '01. Fundamentos PBR y Mapas de Textura', link: '/shaders/01-fundamentos-pbr' },
            { text: '02. Master Materials e Instancias en Unreal', link: '/shaders/02-master-materials' },
            { text: '03. Modelos de Sombreado (Shading Models)', link: '/shaders/03-shading-models' },
            { text: '04. Matemáticas de Shaders (Fresnel, Lerp, Normales)', link: '/shaders/04-matematicas-shaders' }
          ]
        }
      ],
      '/': [
        {
          text: 'Documentación General',
          items: [
            { text: 'Glosario Técnico (Clase a Clase)', link: '/glosario' },
            { text: '📋 Rúbrica: Entrega N°1 (3-Point & Shaders)', link: '/clases/rubrica-entrega-01' },
            { text: 'Mapa de Contenidos', link: '/moc' },
            { text: 'Fichas Técnicas y Descargas', link: '/recursos/material-visual' }
          ]
        }
      ]
    },
    search: {
      provider: 'local'
    },
    footer: {
      message: 'Cátedra de Iluminación 3D',
      copyright: 'Profesor Daniel Rojas · UNIACC'
    }
  }
});
