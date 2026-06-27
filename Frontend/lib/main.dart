import 'package:flutter/material.dart';
import 'screens/signup_screen.dart';
import 'package:supabase_flutter/supabase_flutter.dart';

void main() async{

  WidgetsFlutterBinding.ensureInitialized();
  await Supabase.initialize(
    url: 'https://supabase.co',
    publishableKey: 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InNlaHBzc2dveXR1amZ4a2tnbXV1Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODI1NzQwNDMsImV4cCI6MjA5ODE1MDA0M30.dNA8X6vSY-CYWWPQLeRZvvudv0hWpi_qilEt-o804Zk',
  );
  runApp(const MyApp());

}
class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Studysense',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: const MyHomePage(),
    );
  }
}
class MyHomePage extends StatelessWidget {
  const MyHomePage({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
        title: 'Studysense',
        debugShowCheckedModeBanner: false,
        theme: ThemeData(
          colorScheme: ColorScheme.dark(
            primary: Colors.blue,
          ),
          useMaterial3: true,
        ),
        home:const SignupScreen());
  }
}