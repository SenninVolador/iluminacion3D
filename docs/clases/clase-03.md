# 🎓 Clase 03: Shaders PBR en el Busto 3D, Sol, Cielo y Luces Locales

En esta sesión continuamos directamente con el **busto 3D de la Clase 02**: construimos su primer **Master Material PBR** con texturas empaquetadas (ORM), y estudiamos cómo reaccionan sus propiedades físicas bajo **Directional Light (Sol)**, **Sky Light (Cielo)** y luces de acento local (**Point, Spot y Rect Lights**).

---

## 🕹️ Simulador Interactivo: Respuesta de Rugosidad y Metalicidad

Prueba cómo los reflejos y el brillo especular del busto cambian al alterar el *Roughness* y *Metallic*:

<RoughnessViewer />

---

## 🧱 1. Master Materials y Texturas Empaquetadas (ORM)

En videojuegos optimizados, empaquetamos tres mapas en escala de grises en una sola textura RGB de 8 bits por canal:
* **Canal R (Rojo)**: **A**mbient **O**cclusion (Oclusión en cavidades faciales).
* **Canal G (Verde)**: **R**oughness (Rugosidad y microfacetas).
* **Canal B (Azul)**: **M**etallic (0.0 no metal vs 1.0 metal puro).

### Master Material vs. Instancias en Unreal Engine 5:
* **`M_Master_PBR`**: Contiene la lógica pesada y los slots de textura. Se compila una sola vez.
* **Material Instances (`MI_Busto`)**: Permiten vestir el busto con piel mate (`Roughness = 0.75`), cromo brillante (`Roughness = 0.10`) o bronce al instante sin esperar a compilar shaders.

---

## ☀️ 2. Iluminación Natural sobre el Busto

1. **Directional Light (Sol)**:
   * Al rotar el sol con `Ctrl + L`, la luz rasante resalta los poros y arrugas del **Normal Map**.
   * Buscamos el ángulo **Rembrandt** (45° lateral) para formar el triángulo luminoso en la mejilla opuesta.
2. **Sky Light (Cúpula Celeste)**:
   * Baña el lado en sombra con luz difusa teñida del azul ambiental, respetando el canal R (Ambient Occlusion) del shader para no aplanar las cuencas de los ojos.

---

## 💡 3. Luces Locales de Acento

| Tipo de Luz | Emisión | Aplicación en el Busto | Parámetro Clave |
| :--- | :--- | :--- | :--- |
| **Point Light** | 360° Esfera | Chispa o fuego cercano de apoyo | `Attenuation Radius` |
| **Spot Light** | Cono direccional | Foco de recorte y brillo en la pupila (*Eye Catchlight*) | `IES Profile` |
| **Rect Light** | Área plana | Softbox de estudio fotográfico en pómulos | `Source Width / Height` |

---

## 🎮 4. Casos de Estudio en la Industria

* [God of War Ragnarök (Santa Monica Studio)](https://www.artstation.com/artwork/g8GZ8K): Rostro de Kratos esculpido bajo sol rasante y antorchas mediante Roughness variable.
* [Horizon Forbidden West (Guerrilla Games)](https://www.guerrilla-games.com/read/the-technology-of-horizon-forbidden-west): Piel mate de Aloy combinada con piezas de armadura metálicas reflectantes.
* [Alan Wake 2 (Remedy Entertainment)](https://www.youtube.com/watch?v=k5lO_68b3cQ): Focos Spot con perfiles IES sobre rostros y ropa húmeda con alto Fresnel.
* [Gears 5 (The Coalition)](https://www.youtube.com/watch?v=J3e2Ea7vJ8Q): Luces de acento para siluetear armaduras metálicas sin sobrecoste en GPU.
