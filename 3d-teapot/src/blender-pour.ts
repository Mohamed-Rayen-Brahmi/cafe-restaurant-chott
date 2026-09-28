import * as THREE from 'three';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';
import { RoomEnvironment } from 'three/examples/jsm/environments/RoomEnvironment.js';
import { toCreasedNormals } from 'three/examples/jsm/utils/BufferGeometryUtils.js';

function initPour(container: HTMLElement): void {
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
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  renderer.toneMapping = THREE.ACESFilmicToneMapping;

  const scene = new THREE.Scene();
  const pmrem = new THREE.PMREMGenerator(renderer);
  scene.environment = pmrem.fromScene(new RoomEnvironment(), 0.04).texture;

  const camera = new THREE.PerspectiveCamera(36, 1, 0.01, 10);
  // Frames the whole pour: the teapot lifts to y=0.38 and the glass sits at x=0.28.
  camera.position.set(0.085, 0.3, 0.84);
  camera.lookAt(0.085, 0.18, 0);

  const key = new THREE.DirectionalLight(0xfff4e8, 2.2);
  key.position.set(-0.5, 0.8, 0.6);
  scene.add(key);
  const fill = new THREE.HemisphereLight(0xf2f4ff, 0x2a2318, 0.7);
  scene.add(fill);

  let mixer: THREE.AnimationMixer | null = null;
  let duration = 0;
  let ready = false;

  function resize(): void {
    const w = container.clientWidth;
    const h = container.clientHeight;
    if (w === 0 || h === 0) return;
    renderer.setSize(w, h, false);
    camera.aspect = w / h;
    camera.updateProjectionMatrix();
  }

  function render(): void {
    renderer.render(scene, camera);
  }

  const loader = new GLTFLoader();
  loader.load(
    '/models/teapot-pour.glb',
    (gltf) => {
      scene.add(gltf.scene);
      gltf.scene.traverse((node) => {
        const mesh = node as THREE.Mesh;
        if ((mesh as any).isMesh) {
          mesh.castShadow = false;
          mesh.receiveShadow = false;
          // The export has flat per-face normals, which makes the lathed
          // teapot look faceted. Smooth them, but keep real creases (rims).
          if (mesh.name === 'TeapotBody' || mesh.name === 'TeapotLid') {
            mesh.geometry = toCreasedNormals(mesh.geometry, Math.PI / 3);
          }
        }
      });
      // Play every clip: a Blender export can split the animation into one
      // clip per object, and playing only the first leaves the rest frozen.
      if (gltf.animations.length > 0) {
        mixer = new THREE.AnimationMixer(gltf.scene);
        for (const clip of gltf.animations) {
          const action = mixer.clipAction(clip);
          action.setLoop(THREE.LoopOnce, 1);
          action.clampWhenFinished = true;
          action.play();
          duration = Math.max(duration, clip.duration);
        }
      }
      ready = true;
      resize();
      updateScrub();
      render();
      container.classList.add('is-ready');
    },
    undefined,
    () => {
      // Load failure: leave the poster image showing (container never gets .is-ready).
    }
  );

  let currentT = -1;
  function updateScrub(): void {
    if (!ready || !mixer) return;
    const rect = container.getBoundingClientRect();
    const vh = window.innerHeight || document.documentElement.clientHeight;
    // Run the pour while the stage is fully on screen: start when its centre
    // is at 85% of the viewport height, finish when it reaches 30%.
    const centre = rect.top + rect.height / 2;
    let progress = (vh * 0.85 - centre) / (vh * 0.55);
    progress = Math.max(0, Math.min(1, progress));
    const t = prefersReduced ? duration : progress * duration;
    if (Math.abs(t - currentT) < 0.002) return;
    currentT = t;
    mixer.setTime(t);
    render();
  }

  const resizeObserver = new ResizeObserver(() => {
    resize();
    updateScrub();
  });
  resizeObserver.observe(container);

  if (!prefersReduced) {
    window.addEventListener('scroll', updateScrub, { passive: true });
    window.addEventListener('resize', updateScrub, { passive: true });
  }
}

function boot(): void {
  document.querySelectorAll<HTMLElement>('[data-pour-3d]').forEach((el) => {
    const lazyIo = new IntersectionObserver(
      (entries, obs) => {
        for (const entry of entries) {
          if (entry.isIntersecting) {
            initPour(entry.target as HTMLElement);
            obs.unobserve(entry.target);
          }
        }
      },
      { rootMargin: '200px' }
    );
    lazyIo.observe(el);
  });
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', boot);
} else {
  boot();
}
