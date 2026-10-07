window.COURSE_DATA = {
    beginner: {
        title: "Beginner Method",
        modules: [
            {
                id: "daisy",
                title: "1. The Daisy",
                lessons: [
                    {
                        title: "Creating the Daisy",
                        content: `<p>The first step is placing all four white edge pieces around the yellow center piece.</p>
                                  <ul class="list-disc pl-5 space-y-2 mt-4 text-sm">
                                      <li>Find edge pieces with a white sticker.</li>
                                      <li>Rotate the outer layers to move them to the top layer around the yellow center.</li>
                                  </ul>`,
                        setupScramble: "",
                        algorithm: ""
                    }
                ]
            }
        ]
    },
    cfop: {
        title: "CFOP Masterclass",
        modules: [
            {
                id: "cross",
                title: "1. The White Cross",
                lessons: [
                    {
                        title: "Advanced Cross Strategies",
                        content: `<p class="text-sm leading-relaxed mb-4">Unlike the beginner method, advanced cubers solve the cross on the bottom layer directly to save time and moves.</p>
                                  <h4 class="font-bold text-slate-900 text-sm mt-4">Core Strategies:</h4>
                                  <ul class="list-disc pl-5 space-y-2 mt-2 text-sm">
                                      <li><strong>Relative Order:</strong> You don't need to match the centers immediately. As long as the edges are placed in the correct relative order (Blue is opposite Green, Red is opposite Orange), you can align them all at the end with a single D move!</li>
                                      <li><strong>Plan in Inspection:</strong> You have 15 seconds before the timer starts. Use it to trace exactly where all 4 white edges will go. The cross can always be solved in 8 moves or fewer.</li>
                                      <li><strong>Ignore the Top:</strong> Keep the white center on the bottom (D face) the entire time. Do not flip the cube over to look at it.</li>
                                  </ul>`,
                        setupScramble: "",
                        algorithm: ""
                    }
                ]
            },
            {
                id: "f2l",
                title: "2. First Two Layers (F2L)",
                lessons: [
                    {
                        title: "What is F2L?",
                        content: `<p class="text-sm leading-relaxed">F2L is the most important step in CFOP. Instead of solving the white corners first and then the middle edges, you find a corner and its matching edge, pair them up in the top layer, and insert them into their slot simultaneously.</p>
                        <p class="text-sm mt-4">There are 41 basic F2L cases, but they all boil down to three main intuitive scenarios which we will cover next.</p>`,
                        setupScramble: "",
                        algorithm: ""
                    },
                    {
                        title: "Case 1: Different Colors on Top",
                        content: `<p class="text-sm">When the corner and edge are separated in the top layer and have different colors facing up, bring them together by hiding the corner, moving the edge over it, and bringing the corner back up.</p>`,
                        setupScramble: "R U' R'",
                        algorithm: "R U R'"
                    },
                    {
                        title: "Case 2: Same Colors on Top",
                        content: `<p class="text-sm">If the top colors match, hide the corner in a safe slot, move the edge so it's directly opposite the corner, and bring the corner back up. They will form a connected block that you can insert.</p>`,
                        setupScramble: "R U R' U2 R U' R' U",
                        algorithm: "U' R U R' U2 R U' R'"
                    },
                    {
                        title: "Case 3: White Facing Up",
                        content: `<p class="text-sm">Move the edge piece so its side color matches its center piece. Then perform a face rotation away from the edge to hide it, move the top corner over it, and bring it back up.</p>`,
                        setupScramble: "R U' R' U R U' R'",
                        algorithm: "R U R' U' R U R'"
                    }
                ]
            },
            {
                id: "oll",
                title: "3. Orient Last Layer (OLL)",
                lessons: [
                    {
                        title: "The Sune",
                        content: `<p class="text-sm leading-relaxed">Once the first two layers are solved, your goal is to make the entire top face yellow. Do not worry about the side colors matching yet!</p>
                        <p class="text-sm mt-4">If you have a yellow cross and exactly one yellow corner facing up, you have the "Sune". Hold the single yellow corner in the bottom-left of the U face.</p>`,
                        setupScramble: "R U2 R' U' R U' R'",
                        algorithm: "R U R' U R U2 R'"
                    }
                ]
            },
            {
                id: "pll",
                title: "4. Permute Last Layer (PLL)",
                lessons: [
                    {
                        title: "The T-Perm",
                        content: `<p class="text-sm leading-relaxed">The top is yellow, but the pieces need to be shuffled into their solved positions.</p>
                        <p class="text-sm mt-4">Look for "headlights" (two corners of the same color on the same face). Put them on the back (B) face. The T-perm will swap the front-right and front-left corners to solve all corners.</p>`,
                        setupScramble: "F R U' R' U R U R2 F' R U R U' R'",
                        algorithm: "R U R' U' R' F R2 U' R' U' R U R' F'"
                    },
                    {
                        title: "The Ua-Perm",
                        content: `<p class="text-sm">Now that the corners are solved, you just need to cycle 3 edges to finish the cube! Put the fully solved bar in the back. This algorithm cycles the front, left, and right edges clockwise.</p>`,
                        setupScramble: "M2 U' M U2 M' U' M2",
                        algorithm: "M2 U M U2 M' U M2"
                    }
                ]
            }
        ]
    }
};
