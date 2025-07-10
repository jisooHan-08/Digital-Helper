import 'package:flutter/material.dart';
import 'restaurant_kiosk_screen.dart'; // 식당 키오스크 화면
import 'hospital_kiosk_screen.dart'; // 병원 키오스크 화면

class KioskScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('키오스크 연습')),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            ElevatedButton(
              onPressed: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(builder: (_) => RestaurantKioskScreen()),
                );
              },
              child: Text('🍱 식당 키오스크'),
            ),
            SizedBox(height: 20),
            ElevatedButton(
              onPressed: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(builder: (_) => HospitalKioskScreen()),
                );
              },
              child: Text('🏥 병원 키오스크'),
            ),
          ],
        ),
      ),
    );
  }
}
