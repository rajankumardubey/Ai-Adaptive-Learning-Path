import 'package:flutter/material.dart';
import 'home_screen.dart';
// import 'package:flutter/services.dart';
import '../models/user.dart' as my_models;
import 'package:supabase_flutter/supabase_flutter.dart';
// import '../services/database_service.dart';

class LoginScreen extends StatefulWidget {
  LoginScreen({super.key});

  @override
  State<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  final _formKey = GlobalKey<FormState>();
  final TextEditingController _emailController = TextEditingController();
  final TextEditingController _passwordController = TextEditingController();

  void _login() async {
    if (_formKey.currentState!.validate()) {
      // For demonstration purposes, let's assume the login is successful
      showDialog(
        context: context,
        barrierDismissible: false,
        builder: (context) => const Center(child: CircularProgressIndicator()),
      );
      try {
      // 2. Sign in with Supabase Auth
      final authResponse = await Supabase.instance.client.auth.signInWithPassword(
        email: _emailController.text.trim(),
        password: _passwordController.text.trim(),
      );

      final session = authResponse.session;
      final User? supabaseUser = authResponse.user; // Native Supabase User object

      if (supabaseUser == null || session == null) {
        throw Exception("Login failed. Please verify credentials.");
      }

      // 3. FIX: Pass the 'id' from Supabase into your custom User object
      my_models.User loggedInUser = my_models.User(
        id: supabaseUser.id, // <--- This resolves the 'missing_required_argument' error!
        email: _emailController.text.trim(),
        password: "", // Handled securely by Supabase
        fullName: "", // Optional: Fetch profile data from your API to fill this later
        status: "active",
        dob: DateTime.now(), 
        age: 0,
        address: "",
        phonenumber: "",
      );

      // 4. (Optional) Fetch additional profile fields from your FastAPI backend using the token
      // await DatabaseService.getUserProfile(loggedInUser.id, session.accessToken);

      if (!mounted) return;
      Navigator.pop(context); // Close the loading wheel

      // 5. Navigate to HomeScreen
      Navigator.pushReplacement(
        context,
        MaterialPageRoute(
          builder: (context) => HomeScreen(user: loggedInUser),
        ),
      );

    } catch (error) {
      if (!mounted) return;
      Navigator.pop(context); // Close loading wheel on failure

      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text(error.toString().replaceAll('Exception: ', ''))),
      );
    }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Login Screen'),
      ),
      body: Form(
        key: _formKey,
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(16.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              TextFormField(
                  controller: _emailController,
                  keyboardType: TextInputType.emailAddress,
                decoration: InputDecoration(
                  labelText: 'Email',
                  border: OutlineInputBorder(),
                ),
                  validator: (value) {
                    if (value == null || value.isEmpty) {
                      return 'Please enter your email';
                    }
                    final emailRegex = RegExp(r'^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$');
                    if (!emailRegex.hasMatch(value)) {
                      return 'Please enter a valid email address';
                    }
                    return null;
                  },
              ),
              TextFormField(
                controller: _passwordController,
                obscureText: true,
                decoration: InputDecoration(
                  labelText: 'Password',
                  border: OutlineInputBorder(),
                ),
                  validator: (value) {
                    if (value == null || value.isEmpty) {
                      return 'Please enter your password';
                    }
                    if (value.length < 6) {
                      return 'Password must be at least 6 characters long';
                    }
                    return null;
                  },
              ),
              ElevatedButton(
                onPressed: _login,
                child: const Text('Login'),
                style: ElevatedButton.styleFrom(
                  padding: const EdgeInsets.symmetric(vertical: 16.0),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}