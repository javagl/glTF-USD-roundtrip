# glTF-USD-roundtrip

For **all** tests, the baseline expectation is that the output is visually roughly the same as the input (including possible animations). This is a low bar. It does, for example, not dictate the scene structure. It does also not dictate the material (beyond "looking roughly the same" - this touches the question of whether one should expect "pixel-perfect" output for glTF renderers, or what the "ground truth" is in the first place). But for example: If the input uses no material (causing the "default material" to be used when it is displayed), and the output _does_ use a material, but this material is the same as the "default material", then the output is still _visually the same_. Doing a _structural_ comparison beyond that would require a strict formalization of "structural similiarity". One can go very far here, but probably not in the first iteration of all that.

> Note: The top-level elements of glTF considered here are `accessors`, `animations`, `buffers`, `bufferViews`, `cameras`, `images`, `materials`, `meshes`, `nodes`, `samplers`, `scene`, `scenes`, `skins`, `textures` (excluding `asset`, `extensionsUsed`, `extensionsRequired`, `extensions`, and `extras`).

## Basic geometry

- Covered: `accessors`,  `buffers`, `bufferViews`, `meshes`
- Ignored: `animations`, `cameras`, `images`, `materials`, `nodes`, `samplers`, `scene`, `scenes`, `skins`, `textures`

Test models: `Triangle`, `TriangleWithoutIndices`, `SimpleMeshes`, `SimpleSparseAccessor`

Expected: 
- The structure of the scene graph is ignored.
- The structure of `accessors`/`bufferViews`/`buffers` is ignored
- Whether or not the exported version of `TriangleWithoutIndices` uses indices or not is ignored. 
- Whether or not the exported version of `SimpleSparseAccessor` uses sparse accessors or not is ignored. 

## Basic animation

- Covered:  `accessors`, `animations`, `buffers`, `bufferViews`, `meshes`, `nodes`, `samplers`, 
- Ignored: `cameras`, `images`, `materials`, `scene`, `scenes`, `skins`, `textures`

Test models: `AnimatedTriangle`, `InterpolationTest`

Expected: 
- The structure of the scene graph is ignored (except for the `nodes` that are targeted by the animation samplers)
- The structure of `accessors`/`bufferViews`/`buffers` is ignored
- Whether or not the exported version uses the same interpolation mode is ignored, as long as the animation looks the same

## Complex animation

- Covered:  `accessors`, `animations`, `buffers`, `bufferViews`, `meshes`, `nodes`, `samplers`, `skins`
- Ignored: `cameras`, `images`, `materials`, `scene`, `scenes`, `textures`

Test models: `AnimatedMorphCube`, `SimpleMorph`, `SimpleSkin`

Expected: 
- The structure of the scene graph is ignored (except for the `nodes` that are targeted by the animation samplers)
- The structure of `accessors`/`bufferViews`/`buffers` is ignored
- Whether or not the exported version uses the same interpolation mode or morph target structure is ignored, as long as the animation looks the same


## Scene structure
 
(Cameras, node hierarchy, `scenes` structure...)
...

## Materials 

- Covered:  ... `images`, `materials`, ...,  `samplers`, ...  `textures`

...








