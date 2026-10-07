const FACE_COLORS = {
  U: 0xFFFFFF, // White
  D: 0xFFFF00, // Yellow
  F: 0x00FF00, // Green
  B: 0x0000FF, // Blue
  L: 0xFFA500, // Orange
  R: 0xFF0000, // Red
  INTERNAL: 0x222222 // Dark grey for inside
};

let scene, camera, renderer, cubeGroup, controls;
let cubies = {}; // Maps 'x,y,z' to the THREE.Mesh

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

  // OrbitControls for mouse interaction
  if (THREE.OrbitControls) {
      controls = new THREE.OrbitControls(camera, renderer.domElement);
      controls.enableDamping = true;
      controls.dampingFactor = 0.05;
      controls.enablePan = false;
      controls.minDistance = 3;
      controls.maxDistance = 15;
  }

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
    
    if (controls) controls.update(); // smoothly updates damping

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
  const offset = 1.0; 

  for (let x = -1; x <= 1; x++) {
    for (let y = -1; y <= 1; y++) {
      for (let z = -1; z <= 1; z++) {
        const materials = [
          new THREE.MeshLambertMaterial({ color: x === 1 ? FACE_COLORS.R : FACE_COLORS.INTERNAL }),  // 0: Right (x+)
          new THREE.MeshLambertMaterial({ color: x === -1 ? FACE_COLORS.L : FACE_COLORS.INTERNAL }), // 1: Left (x-)
          new THREE.MeshLambertMaterial({ color: y === 1 ? FACE_COLORS.U : FACE_COLORS.INTERNAL }),  // 2: Top (y+)
          new THREE.MeshLambertMaterial({ color: y === -1 ? FACE_COLORS.D : FACE_COLORS.INTERNAL }), // 3: Bottom (y-)
          new THREE.MeshLambertMaterial({ color: z === 1 ? FACE_COLORS.F : FACE_COLORS.INTERNAL }),  // 4: Front (z+)
          new THREE.MeshLambertMaterial({ color: z === -1 ? FACE_COLORS.B : FACE_COLORS.INTERNAL })  // 5: Back (z-)
        ];

        const mesh = new THREE.Mesh(geometry, materials);
        mesh.position.set(x * offset, y * offset, z * offset);
        
        // Add thin black border edges
        const edges = new THREE.EdgesGeometry(geometry);
        const line = new THREE.LineSegments(edges, new THREE.LineBasicMaterial({ color: 0x000000, linewidth: 2 }));
        mesh.add(line);

        cubeGroup.add(mesh);
        cubies[`${x},${y},${z}`] = mesh;
      }
    }
  }
}

window.resetCubeRotation = function() {
    if (controls) {
        controls.reset();
    }
    if (camera) {
        camera.position.set(5, 5, 6);
        camera.lookAt(0, 0, 0);
    }
};

window.updateCubeColors = function(faceletString) {
    console.log("updateCubeColors called with string:", faceletString);
    if (!faceletString || faceletString.length !== 54) {
        console.error("Invalid facelet string length:", faceletString);
        return;
    }

    // Facelet Mapping definition
    const FACELET_MAP = [
        // U0..U8 (y=1, top-left to bottom-right looking at top face)
        {p:[-1, 1, -1], f:2}, {p:[0, 1, -1], f:2}, {p:[1, 1, -1], f:2},
        {p:[-1, 1,  0], f:2}, {p:[0, 1,  0], f:2}, {p:[1, 1,  0], f:2},
        {p:[-1, 1,  1], f:2}, {p:[0, 1,  1], f:2}, {p:[1, 1,  1], f:2},
        // R0..R8 (x=1, top-left to bottom-right looking at right face)
        {p:[1, 1,  1], f:0}, {p:[1, 1,  0], f:0}, {p:[1, 1, -1], f:0},
        {p:[1, 0,  1], f:0}, {p:[1, 0,  0], f:0}, {p:[1, 0, -1], f:0},
        {p:[1, -1, 1], f:0}, {p:[1, -1, 0], f:0}, {p:[1, -1,-1], f:0},
        // F0..F8 (z=1, top-left to bottom-right looking at front face)
        {p:[-1, 1, 1], f:4}, {p:[0, 1, 1], f:4}, {p:[1, 1, 1], f:4},
        {p:[-1, 0, 1], f:4}, {p:[0, 0, 1], f:4}, {p:[1, 0, 1], f:4},
        {p:[-1,-1, 1], f:4}, {p:[0,-1, 1], f:4}, {p:[1,-1, 1], f:4},
        // D0..D8 (y=-1, top-left to bottom-right looking at down face)
        {p:[-1,-1, 1], f:3}, {p:[0,-1, 1], f:3}, {p:[1,-1, 1], f:3},
        {p:[-1,-1, 0], f:3}, {p:[0,-1, 0], f:3}, {p:[1,-1, 0], f:3},
        {p:[-1,-1,-1], f:3}, {p:[0,-1,-1], f:3}, {p:[1,-1,-1], f:3},
        // L0..L8 (x=-1, top-left to bottom-right looking at left face)
        {p:[-1, 1,-1], f:1}, {p:[-1, 1, 0], f:1}, {p:[-1, 1, 1], f:1},
        {p:[-1, 0,-1], f:1}, {p:[-1, 0, 0], f:1}, {p:[-1, 0, 1], f:1},
        {p:[-1,-1,-1], f:1}, {p:[-1,-1, 0], f:1}, {p:[-1,-1, 1], f:1},
        // B0..B8 (z=-1, top-left to bottom-right looking at back face)
        {p:[1, 1,-1], f:5}, {p:[0, 1,-1], f:5}, {p:[-1, 1,-1], f:5},
        {p:[1, 0,-1], f:5}, {p:[0, 0,-1], f:5}, {p:[-1, 0,-1], f:5},
        {p:[1,-1,-1], f:5}, {p:[0,-1,-1], f:5}, {p:[-1,-1,-1], f:5},
    ];

    try {
        for (let i = 0; i < 54; i++) {
            const mapping = FACELET_MAP[i];
            const key = `${mapping.p[0]},${mapping.p[1]},${mapping.p[2]}`;
            const char = faceletString[i];
            
            const mesh = cubies[key];
            if (mesh && FACE_COLORS[char] !== undefined) {
                mesh.material[mapping.f].color.setHex(FACE_COLORS[char]);
            }
        }
        console.log("Successfully updated colors.");
    } catch (e) {
        console.error("Error updating colors:", e);
    }
};

window.addEventListener('DOMContentLoaded', init3DCube);
