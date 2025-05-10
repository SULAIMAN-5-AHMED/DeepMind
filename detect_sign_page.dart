import 'package:flutter/material.dart';
import 'package:camera/camera.dart';
import 'package:permission_handler/permission_handler.dart';

class DetectSignPage extends StatefulWidget {
  const DetectSignPage({super.key});

  @override
  _DetectSignPageState createState() => _DetectSignPageState();
}

class _DetectSignPageState extends State<DetectSignPage> {
  String predictedLabel = "";
  List<String> history = [];
  CameraController? _cameraController;
  List<CameraDescription>? _cameras;
  bool _isCameraInitialized = false;

  @override
  void initState() {
    super.initState();
    _initCamera();
  }

  Future<void> _initCamera() async {
    final status = await Permission.camera.request();
    if (status.isGranted) {
      _cameras = await availableCameras();
      if (_cameras!.isNotEmpty) {
        _cameraController = CameraController(_cameras![0], ResolutionPreset.medium);
        await _cameraController!.initialize();
        setState(() {
          _isCameraInitialized = true;
        });
      }
    } else {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text("Camera permission is required.")),
      );
    }
  }

  void _captureImage() async {
    if (!_isCameraInitialized || _cameraController == null) return;
    try {
      final XFile image = await _cameraController!.takePicture();
      // Send image.path to your model or server
      final label = await _sendToModel(); // Replace with actual API call
      setState(() {
        predictedLabel = label;
        history.add(label);
      });
    } catch (e) {
      print("Error capturing image: \$e");
    }
  }

  Future<String> _sendToModel() async {
    return "A"; // Dummy response
  }

  void _resetHistory() {
    setState(() {
      history.clear();
      predictedLabel = "";
    });
  }

  @override
  void dispose() {
    _cameraController?.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.blueGrey[50],
      appBar: AppBar(
        leading: IconButton(icon: Icon(Icons.arrow_back), onPressed: () => Navigator.of(context).pop()),
        title: Text("Sign Detection"),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: [
            Container(
              height: 200,
              color: Colors.black,
              child: _isCameraInitialized
                  ? CameraPreview(_cameraController!)
                  : const Center(child: CircularProgressIndicator()),
            ),
            const SizedBox(height: 10),
            ElevatedButton(
              onPressed: _captureImage,
              child: const Text("Capture"),
            ),
            const SizedBox(height: 10),
            Text("Predicted Label: \$predictedLabel", style: const TextStyle(fontSize: 20)),
            const Divider(),
            Expanded(
              child: ListView.builder(
                itemCount: history.length,
                itemBuilder: (context, i) {
                  return Text(history[i]);
                },
              ),
            ),
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceEvenly,
              children: [
                ElevatedButton.icon(
                  onPressed: _resetHistory,
                  icon: const Icon(Icons.refresh),
                  label: const Text("Reset"),
                ),
                ElevatedButton.icon(
                  onPressed: null,
                  icon: const Icon(Icons.save),
                  label: const Text("Save"),
                ),
              ],
            )
          ],
        ),
      ),
    );
  }
}
