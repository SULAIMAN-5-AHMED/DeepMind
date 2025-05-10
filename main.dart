
import 'package:flutter/material.dart';
import 'intro_page.dart';
import 'home_page.dart';
import 'learn_asl_page.dart';
import 'detect_sign_page.dart';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: "ASL Helper",
      theme: ThemeData(
        primarySwatch: Colors.deepPurple,
        fontFamily: 'Roboto',
      ),
      initialRoute: '/',
      routes: {
        '/': (context) => IntroPage(),
        '/home': (context) => HomePage(),
        '/learn': (context) => LearnASLPage(),
        '/detect': (context) => DetectSignPage(),
      },
    );
  }
}