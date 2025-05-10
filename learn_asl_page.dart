import 'package:flutter/material.dart';

class LearnASLPage extends StatelessWidget {
  final List<Map<String, dynamic>> signs = const [
    {"name": "A", "image": "assets/asl_images/A.jpg"},
    {"name": "B", "image": "assets/asl_images/B.jpg"},
    {"name": "C", "image": "assets/asl_images/C.jpg"},
    {"name": "D", "image": "assets/asl_images/D.jpg"},
    {"name": "E", "image": "assets/asl_images/E.jpg"},
    {"name": "F", "image": "assets/asl_images/F.jpg"},
    {"name": "G", "image": "assets/asl_images/G.jpg"},
    {"name": "H", "image": "assets/asl_images/H.jpg"},
    {"name": "I", "image": "assets/asl_images/I.jpg"},
    {"name": "J", "image": "assets/asl_images/J.jpg"},
    {"name": "K", "image": "assets/asl_images/K.jpg"},
    {"name": "L", "image": "assets/asl_images/L.jpg"},
    {"name": "M", "image": "assets/asl_images/M.jpg"},
    {"name": "N", "image": "assets/asl_images/N.jpg"},
    {"name": "O", "image": "assets/asl_images/O.jpg"},
    {"name": "P", "image": "assets/asl_images/P.jpg"},
    {"name": "Q", "image": "assets/asl_images/Q.jpg"},
    {"name": "R", "image": "assets/asl_images/R.jpg"},
    {"name": "S", "image": "assets/asl_images/S.jpg"},
    {"name": "T", "image": "assets/asl_images/T.jpg"},
    {"name": "U", "image": "assets/asl_images/U.jpg"},
    {"name": "V", "image": "assets/asl_images/V.jpg"},
    {"name": "W", "image": "assets/asl_images/W.jpg"},
    {"name": "X", "image": "assets/asl_images/X.jpg"},
    {"name": "Y", "image": "assets/asl_images/Y.jpg"},
    {"name": "Z", "image": "assets/asl_images/Z.jpg"},
  ];

  const LearnASLPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.grey[200],
      appBar: AppBar(
        leading: IconButton(
          icon: const Icon(Icons.arrow_back),
          onPressed: Navigator.of(context).pop,
        ),
        title: const Text("Learn ASL Signs"),
      ),
      body: ListView.builder(
        itemCount: signs.length,
        itemBuilder: (context, index) {
          var sign = signs[index];
          return ListTile(
            title: Text(sign['name']),
            subtitle: Image.asset(
              sign['image'],
              height: 200,
              fit: BoxFit.contain,
            ),
            // onTap behavior can be added later if needed
          );
        },
      ),
    );
  }
}
