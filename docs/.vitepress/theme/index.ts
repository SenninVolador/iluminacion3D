import DefaultTheme from 'vitepress/theme';
import RoughnessViewer from './components/RoughnessViewer.vue';
import ThreePointLightingViewer from './components/ThreePointLightingViewer.vue';
import KelvinViewer from './components/KelvinViewer.vue';
import AttenuationViewer from './components/AttenuationViewer.vue';
import NormalMapViewer from './components/NormalMapViewer.vue';
import './custom.css';

export default {
  extends: DefaultTheme,
  enhanceApp({ app }) {
    app.component('RoughnessViewer', RoughnessViewer);
    app.component('ThreePointLightingViewer', ThreePointLightingViewer);
    app.component('KelvinViewer', KelvinViewer);
    app.component('AttenuationViewer', AttenuationViewer);
    app.component('NormalMapViewer', NormalMapViewer);
  }
};
