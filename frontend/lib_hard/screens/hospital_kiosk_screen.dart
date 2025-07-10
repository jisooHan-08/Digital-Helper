import 'package:flutter/material.dart';

class HospitalKioskScreen extends StatefulWidget {
  @override
  _HospitalKioskScreenState createState() => _HospitalKioskScreenState();
}

class _HospitalKioskScreenState extends State<HospitalKioskScreen> {
  int currentStep = 0;

  String name = '';
  String birthDate = '';
  String gender = '';
  String phone = '';
  String selectedRoom = '';

  List<String> rooms = ['1진료실', '2진료실', '3진료실'];

  void nextStep() {
    setState(() {
      currentStep++;
    });
  }

  void prevStep() {
    setState(() {
      if (currentStep > 0) currentStep--;
    });
  }

  @override
  Widget build(BuildContext context) {
    Widget content;

    switch (currentStep) {
      case 0:
        content = Column(
          children: [
            Text('병원 접수를 시작합니다'),
            ElevatedButton(onPressed: nextStep, child: Text('시작하기')),
          ],
        );
        break;

      case 1:
        content = Column(
          children: [
            Text('이름을 입력하세요'),
            TextField(onChanged: (val) => name = val),
            ElevatedButton(onPressed: nextStep, child: Text('다음')),
          ],
        );
        break;

      case 2:
        content = Column(
          children: [
            Text('생년월일을 입력하세요'),
            TextField(onChanged: (val) => birthDate = val),
            ElevatedButton(onPressed: nextStep, child: Text('다음')),
          ],
        );
        break;

      case 3:
        content = Column(
          children: [
            Text('성별을 선택하세요'),
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                ElevatedButton(
                  onPressed: () {
                    gender = '남성';
                    nextStep();
                  },
                  child: Text('남성'),
                ),
                SizedBox(width: 20),
                ElevatedButton(
                  onPressed: () {
                    gender = '여성';
                    nextStep();
                  },
                  child: Text('여성'),
                ),
              ],
            ),
          ],
        );
        break;

      case 4:
        content = Column(
          children: [
            Text('전화번호를 입력하세요'),
            TextField(onChanged: (val) => phone = val),
            ElevatedButton(onPressed: nextStep, child: Text('다음')),
          ],
        );
        break;

      case 5:
        content = Column(
          children: [
            Text('진료실을 선택하세요'),
            ...rooms.map(
              (room) => ElevatedButton(
                onPressed: () {
                  selectedRoom = room;
                  nextStep();
                },
                child: Text(room),
              ),
            ),
          ],
        );
        break;

      case 6:
        content = Column(
          children: [
            Text('접수 정보를 확인하세요'),
            Text('이름: $name'),
            Text('생년월일: $birthDate'),
            Text('성별: $gender'),
            Text('전화번호: $phone'),
            Text('진료실: $selectedRoom'),
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                ElevatedButton(onPressed: prevStep, child: Text('이전')),
                SizedBox(width: 20),
                ElevatedButton(onPressed: nextStep, child: Text('입력완료')),
              ],
            ),
          ],
        );
        break;

      case 7:
        content = Column(
          children: [
            Text('접수가 완료되었습니다.'),
            ElevatedButton(
              onPressed: () {
                setState(() {
                  currentStep = 0;
                  name = '';
                  birthDate = '';
                  gender = '';
                  phone = '';
                  selectedRoom = '';
                });
              },
              child: Text('처음으로'),
            ),
          ],
        );
        break;

      default:
        content = Text('에러: 올바르지 않은 스텝');
    }

    return Scaffold(
      appBar: AppBar(title: Text('병원 키오스크')),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Center(child: SingleChildScrollView(child: content)),
      ),
    );
  }
}
