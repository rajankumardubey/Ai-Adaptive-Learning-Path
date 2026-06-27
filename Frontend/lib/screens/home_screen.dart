import 'package:flutter/material.dart';
import '../models/user.dart' as my_models;

class HomeScreen extends StatelessWidget {
  const HomeScreen({super.key, required this.user});
  final my_models.User user;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Home Screen'),
      ),
      body: Center(
        child: Text('Welcome, ${user.fullName}!'),
      ),
    );
  }
}