import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart' show rootBundle;

class RestaurantKioskScreen extends StatefulWidget {
  @override
  _RestaurantKioskScreenState createState() => _RestaurantKioskScreenState();
}

class _RestaurantKioskScreenState extends State<RestaurantKioskScreen> {
  List<dynamic> steps = [];
  Map<String, dynamic> uiLayout = {};
  List<dynamic> menuItems = [];
  int currentStepIndex = 0;
  Map<String, int> cart = {};
  String? selectedDiningOption;

  @override
  void initState() {
    super.initState();
    loadLocalJson();
  }

  Future<void> loadLocalJson() async {
    final jsonString = await rootBundle.loadString(
      'assets/data/Restaurant Kiosk.json',
    );
    final data = json.decode(jsonString);

    // ✅ 구조가 List → [0]에 layout/menu_items, 나머지는 steps
    setState(() {
      uiLayout = data[0]['ui_layout'];

      // 🔥 menu_items는 Map<String, List> → 모든 카테고리 항목을 하나의 List로 합쳐야 함
      final menuMap = data[0]['menu_items'] as Map<String, dynamic>;
      menuItems = menuMap.values.expand((list) => list).toList();

      // steps 리스트
      steps = data.sublist(1);
    });
  }

  void onButtonPressed(String buttonText) {
    final currentStep = steps[currentStepIndex];
    final nextMap = currentStep['next'];
    if (nextMap != null && nextMap[buttonText] != null) {
      final nextStep = nextMap[buttonText];
      final newIndex = steps.indexWhere((step) => step['step'] == nextStep);
      if (newIndex != -1) {
        setState(() {
          currentStepIndex = newIndex;
        });
      }
    }
  }

  void addToCart(String menuName) {
    setState(() {
      cart[menuName] = (cart[menuName] ?? 0) + 1;
    });
  }

  void removeFromCart(String menuName) {
    setState(() {
      if (cart.containsKey(menuName)) {
        if (cart[menuName]! > 1) {
          cart[menuName] = cart[menuName]! - 1;
        } else {
          cart.remove(menuName);
        }
      }
    });
  }

  void clearCart() {
    setState(() {
      cart.clear();
      selectedDiningOption = null;
    });
  }

  int getCartTotal() {
    int total = 0;
    cart.forEach((name, count) {
      final menu = menuItems.firstWhere(
        (item) => item['name'] == name,
        orElse: () => {'price': 0},
      );
      total += (int.tryParse(menu['price'].toString()) ?? 0) * count;
    });
    return total;
  }

  Widget buildCartView() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          '🛒 장바구니',
          style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
        ),
        ...cart.entries.map((entry) {
          final name = entry.key;
          final count = entry.value;
          final menu = menuItems.firstWhere(
            (item) => item['name'] == name,
            orElse: () => {'price': 0},
          );
          return ListTile(
            title: Text('$name x$count'),
            subtitle: Text('₩${menu['price'] * count}'),
            trailing: IconButton(
              icon: Icon(Icons.delete),
              onPressed: () => removeFromCart(name),
            ),
          );
        }).toList(),
        if (cart.isNotEmpty)
          Padding(
            padding: const EdgeInsets.symmetric(vertical: 8.0),
            child: Text(
              '총합: ₩${getCartTotal()}',
              style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
            ),
          ),
        if (cart.isNotEmpty)
          ElevatedButton(
            onPressed: () {
              final nextStep = steps[currentStepIndex]['next']?['결제하기'];
              if (nextStep != null) {
                final newIndex = steps.indexWhere(
                  (step) => step['step'] == nextStep,
                );
                if (newIndex != -1) {
                  setState(() {
                    currentStepIndex = newIndex;
                  });
                }
              }
            },
            child: Text('결제하기'),
          ),
      ],
    );
  }

  Widget buildMenuSelection() {
    return GridView.count(
      shrinkWrap: true,
      crossAxisCount: 2,
      childAspectRatio: 0.8,
      children: menuItems.map((item) {
        return Card(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              if (item['image'] != null)
                Image.asset(item['image'], height: 80, fit: BoxFit.cover),
              Text(item['name'], style: TextStyle(fontSize: 16)),
              Text('₩${item['price']}'),
              Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  IconButton(
                    icon: Icon(Icons.remove),
                    onPressed: () => removeFromCart(item['name']),
                  ),
                  Text('${cart[item['name']] ?? 0}'),
                  IconButton(
                    icon: Icon(Icons.add),
                    onPressed: () => addToCart(item['name']),
                  ),
                ],
              ),
              ElevatedButton(
                onPressed: () => addToCart(item['name']),
                child: Text('담기'),
              ),
            ],
          ),
        );
      }).toList(),
    );
  }

  Widget buildReceipt() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          '🧾 영수증',
          style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
        ),
        ...cart.entries.map((entry) {
          final name = entry.key;
          final count = entry.value;
          final menu = menuItems.firstWhere(
            (item) => item['name'] == name,
            orElse: () => {'price': 0},
          );
          return Text('$name x$count  ₩${menu['price'] * count}');
        }).toList(),
        SizedBox(height: 10),
        Text('식사 방법: ${selectedDiningOption ?? "미선택"}'),
        Text(
          '총 결제 금액: ₩${getCartTotal()}',
          style: TextStyle(fontWeight: FontWeight.bold),
        ),
        SizedBox(height: 20),
        ElevatedButton(
          onPressed: () {
            final nextStep = steps[currentStepIndex]['next']?['확인'];
            if (nextStep != null) {
              final newIndex = steps.indexWhere(
                (step) => step['step'] == nextStep,
              );
              if (newIndex != -1) {
                setState(() {
                  currentStepIndex = newIndex;
                });
              }
            }
          },
          child: Text('확인'),
        ),
      ],
    );
  }

  Widget buildDiningOptionButtons(List<String> buttons) {
    return Wrap(
      spacing: 10,
      children: buttons.map((btn) {
        return ElevatedButton(
          style: ElevatedButton.styleFrom(
            backgroundColor: selectedDiningOption == btn ? Colors.green : null,
          ),
          onPressed: () {
            setState(() {
              selectedDiningOption = btn;
            });
            onButtonPressed(btn);
          },
          child: Text(btn),
        );
      }).toList(),
    );
  }

  Widget buildStepUI(Map<String, dynamic> step) {
    final ui = step['ui'] ?? {};
    final type = step['type'] ?? '';
    final text = ui['text'] ?? '';
    final buttons = List<String>.from(ui['buttons'] ?? []);
    final helper = ui['helper_message'] ?? '';
    final top = ui['top'] ?? [];
    final info = ui['info'] ?? {};

    List<Widget> content = [];

    // 상단 버튼
    if (top != null)
      content.add(
        Row(
          mainAxisAlignment: MainAxisAlignment.end,
          children: List<Widget>.from(
            (top as List).map((btn) {
              return TextButton(
                onPressed: () {
                  if (btn == '홈버튼') {
                    setState(() {
                      currentStepIndex = 0;
                      cart.clear();
                      selectedDiningOption = null;
                    });
                  }
                },
                child: Text(btn),
              );
            }),
          ),
        ),
      );

    // 기본 안내 텍스트
    if (text.isNotEmpty)
      content.add(
        Padding(
          padding: const EdgeInsets.only(bottom: 8),
          child: Text(text, style: TextStyle(fontSize: 20)),
        ),
      );

    if (helper.isNotEmpty)
      content.add(
        Padding(
          padding: const EdgeInsets.only(bottom: 8),
          child: Text(helper, style: TextStyle(color: Colors.grey)),
        ),
      );

    // 🔄 분기 처리
    if (type == '메뉴 선택') {
      content.add(buildMenuSelection());
    } else if (type == '장바구니') {
      content.add(buildCartView());
    } else if (type == '영수증') {
      content.add(buildReceipt());
    } else if (type == '식사 방법 선택') {
      content.add(buildDiningOptionButtons(buttons));
    } else if (info.isNotEmpty) {
      content.add(
        Card(
          margin: EdgeInsets.symmetric(vertical: 10),
          child: Padding(
            padding: const EdgeInsets.all(12),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: info.entries
                  .map(
                    (e) => Text(
                      '${e.key}: ${e.value}',
                      style: TextStyle(fontSize: 16),
                    ),
                  )
                  .toList(),
            ),
          ),
        ),
      );
    }

    if (buttons.isNotEmpty && type != '식사 방법 선택')
      content.add(
        Wrap(
          spacing: 10,
          children: buttons
              .map(
                (btn) => ElevatedButton(
                  onPressed: () => onButtonPressed(btn),
                  child: Text(btn),
                ),
              )
              .toList(),
        ),
      );

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: content,
    );
  }

  @override
  Widget build(BuildContext context) {
    if (steps.isEmpty) {
      return Scaffold(
        appBar: AppBar(title: Text('식당 키오스크')),
        body: Center(child: CircularProgressIndicator()),
      );
    }

    final currentStep = steps[currentStepIndex];
    return Scaffold(
      appBar: AppBar(title: Text('식당 키오스크')),
      body: SingleChildScrollView(
        padding: EdgeInsets.all(16),
        child: buildStepUI(currentStep),
      ),
    );
  }
}
