window.LESSONS_DATA = {
    beginner: [
        {
            id: "beginner-daisy",
            title: "1. The Daisy",
            xp: 50,
            description: "Surround the yellow center with white edges.",
            htmlContent: `
                <div class="space-y-4 text-slate-700">
                    <p>The first step to solving the Rubik's Cube is creating the "Daisy" on the top face. This means placing all four white edge pieces around the yellow center piece.</p>
                    <div class="flex justify-center my-6">
                        <img src="https://visualcube.api.cubing.net/?fmt=svg&bg=t&size=150&pzl=3&view=plan&stage=cross" alt="The Daisy" class="bg-slate-100 rounded-xl p-2 shadow-sm border border-slate-200" />
                    </div>
                    <ul class="list-disc pl-5 space-y-2">
                        <li>Find edge pieces with a white sticker.</li>
                        <li>Rotate the outer layers to move them to the top layer around the yellow center.</li>
                        <li>Don't worry about the other colors matching yet!</li>
                    </ul>
                </div>
            `
        },
        {
            id: "beginner-cross",
            title: "2. White Cross",
            xp: 100,
            description: "Align edges and build the cross on the bottom.",
            htmlContent: `
                <div class="space-y-4 text-slate-700">
                    <p>Now we will convert our Daisy into a proper White Cross on the bottom face, ensuring that the side colors of the edges match the side centers.</p>
                    <div class="flex justify-center my-6">
                        <img src="https://visualcube.api.cubing.net/?fmt=svg&bg=t&size=150&pzl=3&view=trans&stage=cross" alt="White Cross" class="bg-slate-100 rounded-xl p-2 shadow-sm border border-slate-200" />
                    </div>
                    <h4 class="font-bold text-slate-900">How to do it:</h4>
                    <ul class="list-disc pl-5 space-y-2">
                        <li>Look at the side color of one of your white edges in the Daisy.</li>
                        <li>Rotate the top layer (U) until that color matches the center piece of the same color.</li>
                        <li>Rotate that entire face 180 degrees (e.g., F2 or R2) to drop the white edge down to the white center.</li>
                        <li>Repeat for all 4 edges!</li>
                    </ul>
                </div>
            `
        }
    ],
    cfop: [
        {
            id: "cfop-cross",
            title: "Stage 1: White Cross",
            xp: 100,
            description: "Solve 4 white edges on the bottom optimally.",
            htmlContent: `
                <div class="space-y-4 text-slate-700">
                    <p>The CFOP method begins by building a cross on the bottom (usually White). Unlike the beginner method, advanced cubers solve this on the bottom layer directly to save time and moves.</p>
                    
                    <div class="flex justify-center my-6">
                        <img src="https://visualcube.api.cubing.net/?fmt=svg&bg=t&size=150&pzl=3&view=trans&stage=cross" alt="White Cross" class="bg-slate-100 rounded-xl p-2 shadow-sm border border-slate-200" />
                    </div>

                    <h4 class="font-bold text-slate-900 mt-6">Core Strategies for Advanced Cross:</h4>
                    <ul class="list-disc pl-5 space-y-2">
                        <li><strong>Relative Order:</strong> You don't need to match the centers immediately. As long as the edges are placed in the correct relative order (Blue is opposite Green, Red is opposite Orange), you can align them all at the end with a single D move!</li>
                        <li><strong>Plan in Inspection:</strong> You have 15 seconds before the timer starts. Use it to trace exactly where all 4 white edges will go. The cross can always be solved in 8 moves or fewer.</li>
                        <li><strong>Ignore the Top:</strong> Keep the white center on the bottom (D face) the entire time. Do not flip the cube over to look at it. Trust your plan.</li>
                    </ul>
                    
                    <div class="p-4 bg-amber-50 border border-amber-200 rounded-xl mt-4">
                        <h4 class="font-bold text-amber-800 mb-1">💡 Finger Trick Tip</h4>
                        <p class="text-sm text-amber-700">Use your ring finger to perform D and D' moves without regripping your hands.</p>
                    </div>
                </div>
            `
        },
        {
            id: "cfop-f2l",
            title: "Stage 2: First Two Layers (F2L)",
            xp: 250,
            description: "Pair corners and edges and insert them simultaneously.",
            htmlContent: `
                <div class="space-y-4 text-slate-700">
                    <p>F2L is the most important step in CFOP. Instead of solving the white corners first and then the middle edges, you find a corner and its matching edge, pair them up in the top layer, and insert them into their slot simultaneously.</p>
                    
                    <p>There are 41 basic F2L cases, but they all boil down to three main intuitive scenarios:</p>

                    <h4 class="font-bold text-slate-900 mt-6">Case 1: Different Colors on Top</h4>
                    <div class="flex flex-col md:flex-row items-center gap-6 bg-slate-50 p-4 rounded-xl border border-slate-200">
                        <img src="https://visualcube.api.cubing.net/?fmt=svg&bg=t&size=120&pzl=3&stage=f2l&case=R U R'" alt="F2L Insertion" class="shrink-0" />
                        <div>
                            <p class="text-sm mb-2">When the corner and edge are separated in the top layer and have different colors facing up, bring them together by hiding the corner, moving the edge over it, and bringing the corner back up.</p>
                            <p class="font-code-mono font-bold text-blue-600 bg-blue-50 px-3 py-1 rounded inline-block border border-blue-200">R U R'</p>
                        </div>
                    </div>

                    <h4 class="font-bold text-slate-900 mt-6">Case 2: Same Colors on Top</h4>
                    <div class="flex flex-col md:flex-row items-center gap-6 bg-slate-50 p-4 rounded-xl border border-slate-200">
                        <img src="https://visualcube.api.cubing.net/?fmt=svg&bg=t&size=120&pzl=3&stage=f2l&case=R U' R' U2 y' R' U' R" alt="F2L Same Color" class="shrink-0" />
                        <div>
                            <p class="text-sm mb-2">If the top colors match, hide the corner in a safe slot, move the edge so it's directly opposite the corner, and bring the corner back up. They will form a connected block that you can insert.</p>
                        </div>
                    </div>

                    <h4 class="font-bold text-slate-900 mt-6">Case 3: White Facing Up</h4>
                    <div class="flex flex-col md:flex-row items-center gap-6 bg-slate-50 p-4 rounded-xl border border-slate-200">
                        <img src="https://visualcube.api.cubing.net/?fmt=svg&bg=t&size=120&pzl=3&stage=f2l&case=R U2 R' U' R U R'" alt="F2L White Up" class="shrink-0" />
                        <div>
                            <p class="text-sm mb-2">Move the edge piece so its side color matches its center piece. Then perform a face rotation away from the edge to hide it, move the top corner over it, and bring it back up.</p>
                        </div>
                    </div>
                </div>
            `
        },
        {
            id: "cfop-oll",
            title: "Stage 3: Orient Last Layer (OLL)",
            xp: 150,
            description: "Make the entire top face yellow.",
            htmlContent: `
                <div class="space-y-4 text-slate-700">
                    <p>Your goal is to make the entire top face yellow. Do not worry about the side colors matching yet! While 1-look OLL requires learning 57 algorithms, we recommend starting with <strong>2-look OLL</strong> (only 10 algorithms).</p>
                    
                    <h4 class="font-bold text-slate-900 mt-6">Step 1: Make a Yellow Cross</h4>
                    <p>If you have an "L" shape, hold it in the top-left and perform <code>F U R U' R' F'</code>. If you have a horizontal line, hold it horizontally and perform <code>F R U R' U' F'</code>.</p>

                    <h4 class="font-bold text-slate-900 mt-6">Step 2: Orient the Corners</h4>
                    <p>Once you have a yellow cross, you will have one of 7 corner configurations. Here are the most famous:</p>

                    <div class="flex flex-col md:flex-row items-center gap-6 bg-slate-50 p-4 rounded-xl border border-slate-200 mt-4">
                        <img src="https://visualcube.api.cubing.net/?fmt=svg&bg=t&size=120&pzl=3&view=plan&stage=oll&case=R U R' U R U2 R'" alt="OLL Sune" class="shrink-0" />
                        <div>
                            <p class="font-bold mb-1">The "Sune" (One corner up)</p>
                            <p class="text-sm mb-2">Hold the single yellow corner in the bottom-left of the U face.</p>
                            <p class="font-code-mono font-bold text-blue-600 bg-blue-50 px-3 py-1 rounded inline-block border border-blue-200">R U R' U R U2 R'</p>
                        </div>
                    </div>

                    <div class="flex flex-col md:flex-row items-center gap-6 bg-slate-50 p-4 rounded-xl border border-slate-200 mt-4">
                        <img src="https://visualcube.api.cubing.net/?fmt=svg&bg=t&size=120&pzl=3&view=plan&stage=oll&case=R U2 R' U' R U' R'" alt="OLL Anti-Sune" class="shrink-0" />
                        <div>
                            <p class="font-bold mb-1">The "Anti-Sune"</p>
                            <p class="text-sm mb-2">Like Sune, but the yellow sticker on the right face is near the front.</p>
                            <p class="font-code-mono font-bold text-blue-600 bg-blue-50 px-3 py-1 rounded inline-block border border-blue-200">R U2 R' U' R U' R'</p>
                        </div>
                    </div>
                </div>
            `
        },
        {
            id: "cfop-pll",
            title: "Stage 4: Permute Last Layer (PLL)",
            xp: 200,
            description: "Move the yellow pieces to their final positions.",
            htmlContent: `
                <div class="space-y-4 text-slate-700">
                    <p>The top is yellow, but the pieces need to be shuffled into their solved positions. Full PLL requires 21 algorithms, but <strong>2-look PLL</strong> only requires 6!</p>
                    
                    <h4 class="font-bold text-slate-900 mt-6">Step 1: Permute the Corners</h4>
                    <p>Look for "headlights" (two corners of the same color on the same face). Put them on the back (B) face.</p>

                    <div class="flex flex-col md:flex-row items-center gap-6 bg-slate-50 p-4 rounded-xl border border-slate-200 mt-4">
                        <img src="https://visualcube.api.cubing.net/?fmt=svg&bg=t&size=120&pzl=3&view=plan&stage=pll&case=R U R' U' R' F R2 U' R' U' R U R' F'" alt="PLL T-Perm" class="shrink-0" />
                        <div>
                            <p class="font-bold mb-1">The T-Perm</p>
                            <p class="text-sm mb-2">If you have headlights on the back, the T-perm will swap the front-right and front-left corners to solve all corners.</p>
                            <p class="font-code-mono font-bold text-blue-600 bg-blue-50 px-3 py-1 rounded inline-block border border-blue-200 break-words">R U R' U' R' F R2 U' R' U' R U R' F'</p>
                        </div>
                    </div>

                    <h4 class="font-bold text-slate-900 mt-6">Step 2: Permute the Edges</h4>
                    <p>Now the corners are solved, you just need to cycle 3 edges to finish the cube!</p>

                    <div class="flex flex-col md:flex-row items-center gap-6 bg-slate-50 p-4 rounded-xl border border-slate-200 mt-4">
                        <img src="https://visualcube.api.cubing.net/?fmt=svg&bg=t&size=120&pzl=3&view=plan&stage=pll&case=M2 U M U2 M' U M2" alt="PLL Ua-Perm" class="shrink-0" />
                        <div>
                            <p class="font-bold mb-1">The Ua-Perm (Clockwise)</p>
                            <p class="text-sm mb-2">Put the fully solved bar in the back. This algorithm cycles the front, left, and right edges clockwise.</p>
                            <p class="font-code-mono font-bold text-blue-600 bg-blue-50 px-3 py-1 rounded inline-block border border-blue-200 break-words">M2 U M U2 M' U M2</p>
                        </div>
                    </div>
                </div>
            `
        }
    ]
};
