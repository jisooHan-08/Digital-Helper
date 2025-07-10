import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

class RestaurantKioskScreen extends StatefulWidget {
  @override
  _RestaurantKioskScreenState createState() => _RestaurantKioskScreenState();
}

class _RestaurantKioskScreenState extends State<RestaurantKioskScreen> {
  List<dynamic> steps = [];
  Map<String, dynamic> uiLayout = {};
  Map<String, dynamic> menuItems = {};
  int currentStepIndex = 0;

  List<Map<String, dynamic>> cart = [];
  int totalPrice = 0;

  @override
  void initState() {
    super.initState();
    loadKioskDataFromAPI();
  }

  Future<void> loadKioskDataFromAPI() async {
    try {
      final response = await http.get(
        Uri.parse('http://127.0.0.1:8000/restaurant_kiosk/db_steps'),
      );
      if (response.statusCode == 200) {
        final List<dynamic> data = json.decode(response.body);
        setState(() {
          uiLayout = data[0]['ui_layout'];
          menuItems = data[0]['menu_items'];
          steps = data.sublist(1);
          currentStepIndex = 0;
        });
      } else {
        throw Exception('데이터 로딩 실패');
      }
    } catch (e) {
      print('API 호출 실패: $e');
    }
  }

  void nextStep([int? step]) {
    if (step != null) {
      final index = steps.indexWhere((s) => s['step'] == step);
      if (index != -1) {
        setState(() => currentStepIndex = index);
      }
    } else if (steps[currentStepIndex]['next_step'] != null) {
      final next = steps[currentStepIndex]['next_step'];
      if (next is int) {
        nextStep(next);
      }
    }
  }

  void addToCart(Map<String, dynamic> item) {
    setState(() {
      cart.add(item);
      totalPrice += (item['price'] as int);
    });
  }

  void removeFromCart(int index) {
    setState(() {
      totalPrice -= (cart[index]['price'] as int);
      cart.removeAt(index);
    });
  }

  @override
  Widget build(BuildContext context) {
    if (steps.isEmpty) {
      return Scaffold(
        appBar: AppBar(title: Text('식당 키오스크')),
        body: Center(child: CircularProgressIndicator()),
      );
    }

    final step = steps[currentStepIndex];

    return Scaffold(
      appBar: AppBar(title: Text('식당 키오스크')),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            if (step['instruction'] != null)
              Text(step['instruction'], style: TextStyle(fontSize: 20)),
            if (step['helper_message'] != null)
              Text(
                step['helper_message'],
                style: TextStyle(color: Colors.grey),
              ),
            SizedBox(height: 20),
            if (step['options'] != null)
              ...List<Widget>.from(
                (step['options'] as List).map(
                  (option) => ElevatedButton(
                    onPressed: () => nextStep(step['next_step'][option]),
                    child: Text(option),
                  ),
                ),
              ),
            if (step['buttons'] != null)
              ...List<Widget>.from(
                (step['buttons'] as List).map(
                  (btn) => ElevatedButton(
                    onPressed: () => nextStep(step['next_step'][btn]),
                    child: Text(btn),
                  ),
                ),
              ),
            if (step['step'] == 102 ||
                step['step'] == 121 ||
                step['step'] == 141)
              Expanded(child: buildMenuSelector()),
            if (step['step'] == 105 || step['step'] == 123)
              Expanded(child: buildCartView()),
            if (step['step'] == 107 ||
                step['step'] == 122 ||
                step['step'] == 142)
              buildDineOptionButtons(),
          ],
        ),
      ),
    );
  }

  Widget buildMenuSelector() {
    return DefaultTabController(
      length: menuItems.keys.length,
      child: Column(
        children: [
          TabBar(
            tabs: menuItems.keys
                .map((category) => Tab(text: category))
                .toList(),
          ),
          Expanded(
            child: TabBarView(
              children: menuItems.keys.map((category) {
                final items = menuItems[category];
                return GridView.builder(
                  gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
                    crossAxisCount: 2,
                    childAspectRatio: 3 / 2,
                  ),
                  itemCount: items.length,
                  itemBuilder: (context, index) {
                    final item = items[index];
                    return Card(
                      child: Column(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          Text(item['name'], style: TextStyle(fontSize: 16)),
                          Text('${item['price']}원'),
                          ElevatedButton(
                            onPressed: () => addToCart(item),
                            child: Text('담기'),
                          ),
                        ],
                      ),
                    );
                  },
                );
              }).toList(),
            ),
          ),
        ],
      ),
    );
  }

  Widget buildCartView() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          '장바구니',
          style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
        ),
        Expanded(
          child: ListView.builder(
            itemCount: cart.length,
            itemBuilder: (context, index) {
              final item = cart[index];
              return ListTile(
                title: Text(item['name']),
                subtitle: Text('${item['price']}원'),
                trailing: IconButton(
                  icon: Icon(Icons.delete),
                  onPressed: () => removeFromCart(index),
                ),
              );
            },
          ),
        ),
        Text('총 금액: $totalPrice원'),
        ElevatedButton(onPressed: () => nextStep(), child: Text('결제하기')),
      ],
    );
  }

  Widget buildDineOptionButtons() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text('식사 방법을 선택해주세요:'),
        Row(
          children: [
            ElevatedButton(
              onPressed: () => nextStep(108),
              child: Text('매장 식사'),
            ),
            SizedBox(width: 10),
            ElevatedButton(onPressed: () => nextStep(108), child: Text('포장')),
          ],
        ),
      ],
    );
  }
}
