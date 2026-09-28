import * as THREE from 'three';
import {
  createMaghrebTeapotModel,
  createMaghrebTeapotLookDevLights,
  createMaghrebTeapotEnvironment,
  frameMaghrebTeapotCamera,
  configureMaghrebTeapotRenderer,
} from './createTeapotModel';

const canvas = document.getElementById('c') as HTMLCanvasElement;
const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true });
renderer.setSize(800, 800);
renderer.setPixelRatio(1);
configureMaghrebTeapotRenderer(renderer);

const scene = new THREE.Scene();
scene.background = null;
scene.environment = createMaghrebTeapotEnvironment(renderer);

const camera = new THREE.PerspectiveCamera(35, 1, 0.1, 100);

const lights = createMaghrebTeapotLookDevLights('reference');
scene.add(lights);

const model = createMaghrebTeapotModel({ castShadow: true, receiveShadow: true });
scene.add(model);

frameMaghrebTeapotCamera(camera, model, { margin: 1.35, azimuthDeg: 25, elevationDeg: 12 });

function render() {
  renderer.render(scene, camera);
}
render();

(window as any).__setYaw = (deg: number) => {
  frameMaghrebTeapotCamera(camera, model, { margin: 1.35, azimuthDeg: deg, elevationDeg: 12 });
  render();
};
(window as any).__ready = true;
