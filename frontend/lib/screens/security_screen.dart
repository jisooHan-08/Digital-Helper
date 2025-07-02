import 'package:flutter/material.dart';

class SecurityScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('보안 교육')),
      body: ListView(
        children: [
          ListTile(
            title: Text('[문자] 택배가 도착했습니다. 링크를 눌러 확인하세요.'),
            onTap: () {
              showDialog(
                context: context,
                builder: (_) => AlertDialog(
                  title: Text('⚠️ 경고'),
                  content: Text('이 링크는 피싱일 수 있습니다! 절대 누르지 마세요.'),
                  actions: [
                    TextButton(
                      onPressed: () => Navigator.pop(context),
                      child: Text('확인'),
                    ),
                  ],
                ),
              );
            },
          ),
          ListTile(
            title: Text('[전화] 금감원입니다. 보안카드 번호를 알려주세요.'),
            onTap: () {
              showDialog(
                context: context,
                builder: (_) => AlertDialog(
                  title: Text('⚠️ 경고'),
                  content: Text('이 전화는 사기일 가능성이 높습니다.'),
                  actions: [
                    TextButton(
                      onPressed: () => Navigator.pop(context),
                      child: Text('확인'),
                    ),
                  ],
                ),
              );
            },
          ),
        ],
      ),
    );
  }
}
