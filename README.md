# Vosca
A VisionOS Coding Assistant built using langchain and a local vectorstore for extra RAG context.
-----

RAG is a powerful method to keep LLM's up to date with relevant, specialised information so that they can be maximally benefecial for your use case. In this project, I'm first scrapinng data from VisionOS' Docs with my data-scraping.py file, which utilises selenium, beautifulsoup and other relevant tools for webscraping. After gathering the data, it's indexed and embeded in a local vectorstore using langchain tools including Chroma and LLamaCPPEmbeddings with nomic 1.5 weights. A proper RAG pipeline is then set up with an appropriate retriever, augmented prompt and suitable inference with a local llm - mistral:instruct. 

-----

The relevance can be shown here with some early prompting:

**Prompt**: Are you familiar with the VisionOS documentation?

**Mistral**:

I am not directly familiar with a specific documentation called "VisionOS". There are several software and operating systems that go by that name, so it would be helpful if you could provide some more context or specify which one you have in mind. If you can give me more information, such as where the documentation is located (e.g., a link to its website), I'll do my best to help you out. In general, I can assist with searching for and interpreting technical documentation, answering questions about concepts or terminology, and providing guidance on how to use various software tools and technologies.

----

Now that that's established, let's see how the base model compares to the RAG-Model Vosca:

**Prompt**: How can I display 3D content in a Volume in my VisionOS App? I want to create a ball that bounces in 3D space.

**Mistral**:

 To display 3D content, including a bouncing ball, in a Volume in your VisionOS app, you will need to use a 3D rendering engine that supports the OpenGL ES 2.0 API or higher, which is typically used in VisionOS apps. Here are some steps to guide you through creating a simple bouncing ball:

1. Choose a 3D library or framework for VisionOS: You may consider using popular open-source libraries like OpenGL ES, OpenGL Scene Graph (Open Scene Graph for VisionOS), or commercial engines like Unity3D or Unreal Engine, which have strong support for creating 3D content in a Volume.

2. Set up the project: Follow the instructions provided by your chosen library to create a new VisionOS project and configure it to work with the 3D library.

3. Create a 3D model or sphere for the ball: Use modeling software like Blender, Maya, or Autodesk 3ds Max, or generate a simple 3D sphere using your 3D engine's built-in tools. Import the sphere into your VisionOS project.

4. Implement the bouncing behavior: Write code to create the physics rules that will make the ball bounce when it collides with the Volume floor or other objects. You may use a collision detection library, like Open Collision Detection Library (OpenCollide), to implement these rules.

...
----
**Prompt**: How can I display 3D content in a Volume in my VisionOS App? I want to create a ball that bounces in 3D space.

**Vosca**:

 To display 3D content in a Volume in your VisionOS app, you can use RealityKit and build your 3D content using Reality Composer Pro. Here's a general outline of the steps you need to take:

1. Create a new RealityKit entity for the ball using a `ModelEntity` or `ModelNode`. You can import the 3D model into Reality Composer Pro and export it as a RealityKit-compatible file, or create a custom geometry using Swift code.
2. Add the entity to a `RealityView`, which is a built-in UIView in SwiftUI for displaying AR/VR content in VisionOS apps.
3. Use ARKit to anchor the entity to a specific location in the user's environment, or keep it static within the Volume using `ARAnchorEntity` or `ARPlaneAnchorEntity`.
4. Add physics properties to the ball entity, such as mass, restitution (bounciness), and friction, using `PhysicsBodyComponent`. This will enable realistic bouncing behavior when the ball collides with other objects.
5. Use SwiftUI gestures or ARKit hand tracking to add user interaction, such as tapping or pinching, to make the ball bounce in response to user input.

Here's an example of creating a simple bouncing ball using RealityKit and SwiftUI:

```swift
import SwiftUI
import RealityKit

struct ContentView: View {
    @State private var isTapped = false

    var body: some View {
        SceneKitView(scene: createBallScene())
            .gesture(
                TapGesture()
                    .onEnded { _ in
                        self.isTapped.toggle()
                }
            )
            .animation(Animation.easeInOut(duration: 0.1))
            .onReceive(Just(self.$isTapped).map{ $0 }) { newValue in
                if newValue {
                    self.isTapped = false
                    self.animateBall()
                }
            }
    }

    func createBallScene() -> SCNScene {
        let ballModel = ModelEntity(modelURL: Bundle.main.url(forResource: "ball", withExtension: "usdz"))!
        let physicsComponent = PhysicsBodyComponent(type: .dynamic)
        let mass = 1.0
        physicsComponent.mass = mass
        ballModel.addComponent(physicsComponent)
        let ballEntity = AnchorEntity(planeAnchor: nil, entity: ballModel)

        return SCNScene(named: "art.scnassets/default.scn")!
            .rootNode.replacingChildNode(withNode: ballEntity, at: 0)
    }

    func animateBall() {
        // Add physics properties to make the ball bounce
        let direction = SIMD3<Float>(0), SIMD3<Float>(1), SIMD3<Float>(0)
        let force = SCNFforce(direction: direction, magnitude: 5.0)
        let ballEntity = self.$scene.map({ $0?.rootNode.childNodes[0] })!
        ballEntity.physicsBody?.applyForce(force: force)
    }
}
```

Replace `"ball"` with the actual name of your 3D model file, and make sure it's in the correct directory within your app bundle.

---

Now, that's more like it. The base model makes an admirable attempt to tackle the prompt, but the performance is well outshowed by Vosca, which even returns viable code examples in the appropriate programming language. 
