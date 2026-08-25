import DefaultTheme from 'vitepress/theme';
import RoughnessViewer from './components/RoughnessViewer.vue';
import ThreePointLightingViewer from './components/ThreePointLightingViewer.vue';

export default {
  extends: DefaultTheme,
  enhanceApp({ app }) {
    app.component('RoughnessViewer', RoughnessViewer);
    app.component('ThreePointLightingViewer', ThreePointLightingViewer);
  }
};
