const FACE_COLORS = {
  U: 0xFFFFFF, // White
  D: 0xFFFF00, // Yellow
  F: 0x00FF00, // Green
  B: 0x0000FF, // Blue
  L: 0xFFA500, // Orange
  R: 0xFF0000, // Red
  INTERNAL: 0x222222 // Dark grey for inside
};

let scene, camera, renderer, cubeGroup;

function init3DCube() {
  const container = document.getElementById('cube3d-container');
  if (!container) return;

  scene = new THREE.Scene();

  camera = new THREE.PerspectiveCamera(45, container.clientWidth / container.clientHeight, 0.1, 100);
  camera.position.set(5, 5, 6);
  camera.lookAt(0, 0, 0);

  renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });
  renderer.setSize(container.clientWidth, container.clientHeight);
  container.appendChild(renderer.domElement);

  // Lighting
  const ambientLight = new THREE.AmbientLight(0xffffff, 0.7);
  scene.add(ambientLight);
  const directionalLight = new THREE.DirectionalLight(0xffffff, 0.5);
  directionalLight.position.set(5, 10, 7);
  scene.add(directionalLight);

  cubeGroup = new THREE.Group();
  scene.add(cubeGroup);

  createInitialCube();

  // Animation Loop
  function animate() {
    requestAnimationFrame(animate);
    
    // Slow idle rotation
    cubeGroup.rotation.y += 0.005;
    cubeGroup.rotation.x += 0.002;

    renderer.render(scene, camera);
  }
  animate();

  // Handle Resize
  window.addEventListener('resize', () => {
    camera.aspect = container.clientWidth / container.clientHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(container.clientWidth, container.clientHeight);
  });
}

function createInitialCube() {
  const geometry = new THREE.BoxGeometry(0.95, 0.95, 0.95);
  const offset = 1.0; // Distance between cubies

  // Standard Solved Mapping (Up=White, Right=Red, Front=Green, Down=Yellow, Left=Orange, Back=Blue)
  // ThreeJS Material Order: Right(x+), Left(x-), Top(y+), Bottom(y-), Front(z+), Back(z-)
  
  for (let x = -1; x <= 1; x++) {
    for (let y = -1; y <= 1; y++) {
      for (let z = -1; z <= 1; z++) {
        const materials = [
          new THREE.MeshLambertMaterial({ color: x === 1 ? FACE_COLORS.R : FACE_COLORS.INTERNAL }),  // Right
          new THREE.MeshLambertMaterial({ color: x === -1 ? FACE_COLORS.L : FACE_COLORS.INTERNAL }), // Left
          new THREE.MeshLambertMaterial({ color: y === 1 ? FACE_COLORS.U : FACE_COLORS.INTERNAL }),  // Top
          new THREE.MeshLambertMaterial({ color: y === -1 ? FACE_COLORS.D : FACE_COLORS.INTERNAL }), // Bottom
          new THREE.MeshLambertMaterial({ color: z === 1 ? FACE_COLORS.F : FACE_COLORS.INTERNAL }),  // Front
          new THREE.MeshLambertMaterial({ color: z === -1 ? FACE_COLORS.B : FACE_COLORS.INTERNAL })  // Back
        ];

        const mesh = new THREE.Mesh(geometry, materials);
        mesh.position.set(x * offset, y * offset, z * offset);
        
        // Add thin black border edges
        const edges = new THREE.EdgesGeometry(geometry);
        const line = new THREE.LineSegments(edges, new THREE.LineBasicMaterial({ color: 0x000000, linewidth: 2 }));
        mesh.add(line);

        cubeGroup.add(mesh);
      }
    }
  }
}

window.resetCubeRotation = function() {
    if (cubeGroup) {
        cubeGroup.rotation.set(0, 0, 0);
    }
};

window.addEventListener('DOMContentLoaded', init3DCube);
