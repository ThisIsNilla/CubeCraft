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
                        <img src="https://cube.rider.biz/visualcube.php?fmt=svg&bg=t&size=150&pzl=3&view=plan&stage=cross" alt="The Daisy" class="bg-slate-100 rounded-xl p-2 shadow-sm border border-slate-200" />
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
                        <img src="https://cube.rider.biz/visualcube.php?fmt=svg&bg=t&size=150&pzl=3&view=trans&stage=cross" alt="White Cross" class="bg-slate-100 rounded-xl p-2 shadow-sm border border-slate-200" />
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
            description: "Solve 4 white edges on the bottom.",
            htmlContent: `
                <div class="space-y-4 text-slate-700">
                    <p>The CFOP method begins by building a cross on the bottom (usually White). Advanced cubers solve this on the bottom layer directly without making a "Daisy" first to save time.</p>
                    <div class="flex justify-center my-6">
                        <img src="https://cube.rider.biz/visualcube.php?fmt=svg&bg=t&size=150&pzl=3&view=trans&stage=cross" alt="White Cross" class="bg-slate-100 rounded-xl p-2 shadow-sm border border-slate-200" />
                    </div>
                    <div class="p-4 bg-amber-50 border border-amber-200 rounded-xl">
                        <h4 class="font-bold text-amber-800 mb-1">💡 Pro Tip</h4>
                        <p class="text-sm text-amber-700">Try to plan the entire cross during your 15 seconds of inspection time so you can execute it blindfolded!</p>
                    </div>
                </div>
            `
        },
        {
            id: "cfop-f2l",
            title: "Stage 2: First Two Layers (F2L)",
            xp: 250,
            description: "Pair corners and edges and insert them together.",
            htmlContent: `
                <div class="space-y-4 text-slate-700">
                    <p>Instead of solving the corners and then the middle edges (like the beginner method), CFOP combines them! You find a corner and its matching edge, pair them up in the top layer, and insert them into their slot simultaneously.</p>
                    
                    <h4 class="font-bold text-slate-900 mt-6">Basic Insertion Example</h4>
                    <div class="flex flex-col md:flex-row items-center gap-6 bg-slate-50 p-4 rounded-xl border border-slate-200">
                        <img src="https://cube.rider.biz/visualcube.php?fmt=svg&bg=t&size=120&pzl=3&stage=f2l&case=R U R'" alt="F2L Insertion" class="shrink-0" />
                        <div>
                            <p class="text-sm mb-2">When the pair is joined in the top layer, insert it into the front-right slot using this simple 3-move trigger:</p>
                            <p class="font-code-mono font-bold text-blue-600 bg-blue-50 px-3 py-1 rounded inline-block border border-blue-200">R U R'</p>
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
                    <p>Once the first two layers are solved, your goal is to make the entire top face yellow. You do not care if the side colors of the top layer match yet!</p>
                    
                    <h4 class="font-bold text-slate-900 mt-6">Common Case: "Sune"</h4>
                    <div class="flex flex-col md:flex-row items-center gap-6 bg-slate-50 p-4 rounded-xl border border-slate-200">
                        <img src="https://cube.rider.biz/visualcube.php?fmt=svg&bg=t&size=120&pzl=3&view=plan&stage=oll&case=R U R' U R U2 R'" alt="OLL Sune" class="shrink-0" />
                        <div>
                            <p class="text-sm mb-2">If you have one yellow corner facing up, and the others twisted, use the Sune algorithm:</p>
                            <p class="font-code-mono font-bold text-blue-600 bg-blue-50 px-3 py-1 rounded inline-block border border-blue-200">R U R' U R U2 R'</p>
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
                    <p>The final stage! The top is yellow, but the pieces need to be shuffled around into their solved states. There are 21 PLL algorithms to learn for 1-look PLL.</p>
                    
                    <h4 class="font-bold text-slate-900 mt-6">Famous Algorithm: The T-Perm</h4>
                    <div class="flex flex-col md:flex-row items-center gap-6 bg-slate-50 p-4 rounded-xl border border-slate-200">
                        <img src="https://cube.rider.biz/visualcube.php?fmt=svg&bg=t&size=120&pzl=3&view=plan&stage=pll&case=R U R' U' R' F R2 U' R' U' R U R' F'" alt="PLL T-Perm" class="shrink-0" />
                        <div>
                            <p class="text-sm mb-2">Swaps two adjacent corners and two opposite edges. Incredibly fast to execute!</p>
                            <p class="font-code-mono font-bold text-blue-600 bg-blue-50 px-3 py-1 rounded inline-block border border-blue-200 break-words">R U R' U' R' F R2 U' R' U' R U R' F'</p>
                        </div>
                    </div>
                </div>
            `
        }
    ]
};
