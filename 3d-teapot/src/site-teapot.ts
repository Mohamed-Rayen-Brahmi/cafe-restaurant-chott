import * as THREE from 'three';
import {
  createMaghrebTeapotModel,
  createMaghrebTeapotLookDevLights,
  createMaghrebTeapotEnvironment,
  frameMaghrebTeapotCamera,
  configureMaghrebTeapotRenderer,
} from './createTeapotModel';

function initTeapot3D(container: HTMLElement): void {
  const canvas = container.querySelector('canvas') as HTMLCanvasElement | null;
  if (!canvas || !('WebGLRenderingContext' in window)) return;

  const prefersReduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  let renderer: THREE.WebGLRenderer;
  try {
    renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true });
  } catch (e) {
    return;
  }
  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
  configureMaghrebTeapotRenderer(renderer);

  const scene = new THREE.Scene();
  scene.environment = createMaghrebTeapotEnvironment(renderer);

  const camera = new THREE.PerspectiveCamera(35, 1, 0.1, 100);
  const lights = createMaghrebTeapotLookDevLights('reference');
  scene.add(lights);

  const model = createMaghrebTeapotModel({ castShadow: false, receiveShadow: false });
  scene.add(model);

  function resize(): void {
    const w = container.clientWidth;
    const h = container.clientHeight;
    if (w === 0 || h === 0) return;
    renderer.setSize(w, h, false);
    camera.aspect = w / h;
    frameMaghrebTeapotCamera(camera, model, { margin: 1.5, azimuthDeg: currentYaw, elevationDeg: 10 });
  }

  let currentYaw = 25;
  const resizeObserver = new ResizeObserver(resize);
  resizeObserver.observe(container);
  resize();

  let running = false;
  let rafId = 0;
  const ROTATION_SECONDS = 32; // one full turn in 32s, per imagery.md's "slow, 20-40s" rule
  let lastTime = 0;

  function tick(t: number): void {
    if (!running) return;
    if (lastTime) {
      const dt = (t - lastTime) / 1000;
      currentYaw += (360 / ROTATION_SECONDS) * dt;
      frameMaghrebTeapotCamera(camera, model, { margin: 1.5, azimuthDeg: currentYaw, elevationDeg: 10 });
    }
    lastTime = t;
    renderer.render(scene, camera);
    rafId = requestAnimationFrame(tick);
  }

  function start(): void {
    if (running) return;
    running = true;
    lastTime = 0;
    rafId = requestAnimationFrame(tick);
  }

  function stop(): void {
    running = false;
    if (rafId) cancelAnimationFrame(rafId);
  }

  if (prefersReduced) {
    // Static frame only, no rotation loop at all.
    frameMaghrebTeapotCamera(camera, model, { margin: 1.5, azimuthDeg: currentYaw, elevationDeg: 10 });
    renderer.render(scene, camera);
  } else {
    const io = new IntersectionObserver(
      (entries) => {
        for (const entry of entries) {
          if (entry.isIntersecting) start();
          else stop();
        }
      },
      { threshold: 0.1 },
    );
    io.observe(container);
  }

  container.classList.add('is-ready');
}

function boot(): void {
  document.querySelectorAll<HTMLElement>('[data-teapot-3d]').forEach((el) => {
    // Lazy: only build the scene once the element nears the viewport.
    const lazyIo = new IntersectionObserver(
      (entries, obs) => {
        for (const entry of entries) {
          if (entry.isIntersecting) {
            initTeapot3D(entry.target as HTMLElement);
            obs.unobserve(entry.target);
          }
        }
      },
      { rootMargin: '200px' },
    );
    lazyIo.observe(el);
  });
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', boot);
} else {
  boot();
}
