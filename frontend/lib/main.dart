import 'package:flutter/material.dart';

// 각 화면 import
import 'screens/kiosk_screen.dart';
import 'screens/quiz_screen.dart';
import 'screens/typing_mode.dart';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: '디지털 소외계층을 위한 디지털 적응 도우미',
      theme: ThemeData(primarySwatch: Colors.blue),
      home: HomeScreen(),
      debugShowCheckedModeBanner: false,
    );
  }
}

class HomeScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('디지털 소외계층을 위한 디지털 적응 도우미')),
      body: Center(
        child: SingleChildScrollView(
          // 버튼이 많아지면 스크롤 되게 함
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              ElevatedButton(
                child: Text('키오스크 연습'),
                onPressed: () {
                  Navigator.push(
                    context,
                    MaterialPageRoute(builder: (context) => KioskScreen()),
                  );
                },
              ),
              ElevatedButton(
                onPressed: () {
                  Navigator.push(
                    context,
                    MaterialPageRoute(
                      builder: (_) => TypingPracticeModeScreen(), // ✅ 타자 연습 화면
                    ),
                  );
                },
                child: Text("타자 연습"),
              ),
              ElevatedButton(
                child: Text('보안 교육'),
                onPressed: () {
                  Navigator.push(
                    context,
                    MaterialPageRoute(
                      builder: (context) => QuizScreen(), // ✅ QuizScreen 사용
                    ),
                  );
                },
              ),
              ElevatedButton(
                child: Text('보안 퀴즈'),
                onPressed: () {
                  Navigator.push(
                    context,
                    MaterialPageRoute(builder: (context) => QuizScreen()),
                  );
                },
              ),
            ],
          ),
        ),
      ),
    );
  }
}
