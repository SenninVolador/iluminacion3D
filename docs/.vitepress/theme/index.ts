import DefaultTheme from 'vitepress/theme';
import RoughnessViewer from './components/RoughnessViewer.vue';
import ThreePointLightingViewer from './components/ThreePointLightingViewer.vue';
import KelvinViewer from './components/KelvinViewer.vue';
import AttenuationViewer from './components/AttenuationViewer.vue';
import NormalMapViewer from './components/NormalMapViewer.vue';
import SunShadowViewer from './components/SunShadowViewer.vue';
import SpotConeViewer from './components/SpotConeViewer.vue';
import FresnelViewer from './components/FresnelViewer.vue';
import MobilityViewer from './components/MobilityViewer.vue';
import NodeShaderViewer from './components/NodeShaderViewer.vue';
import VolumetricFogViewer from './components/VolumetricFogViewer.vue';
import './custom.css';

export default {
  extends: DefaultTheme,
  enhanceApp({ app }) {
    app.component('RoughnessViewer', RoughnessViewer);
    app.component('ThreePointLightingViewer', ThreePointLightingViewer);
    app.component('KelvinViewer', KelvinViewer);
    app.component('AttenuationViewer', AttenuationViewer);
    app.component('NormalMapViewer', NormalMapViewer);
    app.component('SunShadowViewer', SunShadowViewer);
    app.component('SpotConeViewer', SpotConeViewer);
    app.component('FresnelViewer', FresnelViewer);
    app.component('MobilityViewer', MobilityViewer);
    app.component('NodeShaderViewer', NodeShaderViewer);
    app.component('VolumetricFogViewer', VolumetricFogViewer);
  }
};
