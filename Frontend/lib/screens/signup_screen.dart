import 'package:flutter/material.dart';
import 'home_screen.dart';
import 'package:flutter/services.dart';
import '../models/user.dart' as my_models;
import 'package:supabase_flutter/supabase_flutter.dart';
import '../services/database_service.dart';

class SignupScreen extends StatefulWidget {
  const SignupScreen({super.key});

  
  @override
  State<SignupScreen> createState() => _SignupScreenState();
}
class _SignupScreenState extends State<SignupScreen> {
  final _formKey = GlobalKey<FormState>();

  final TextEditingController _fullNameController = TextEditingController();
  final TextEditingController _ageController = TextEditingController();
  final TextEditingController _emailController = TextEditingController();
  final TextEditingController _passwordController = TextEditingController();
  void dispose() {
    _fullNameController.dispose();
    _ageController.dispose();
    _emailController.dispose();
    _passwordController.dispose();
    super.dispose();
  }

  // 1. Add the "async" keyword so you can use "await"
void _signup() async {
  
  // 2. FIXED: Removed the "!" so this runs when validation PASSES
  if (_formKey.currentState!.validate()) {
    
    // Show loading spinner
    showDialog(
      context: context,
      barrierDismissible: false,
      builder: (context) => const Center(child: CircularProgressIndicator()),
    );

    try {
      // 3. Authenticate directly with Supabase Auth
      final authResponse = await Supabase.instance.client.auth.signUp(
        email: _emailController.text.trim(),
        password: _passwordController.text.trim(),
      );

      final session = authResponse.session;
      final supabaseUser = authResponse.user;

      if (supabaseUser == null || session == null) {
        throw Exception("Authentication failed. Please verify credentials.");
      }

      // Calculate the Date of Birth based on age input
      int userAge = int.tryParse(_ageController.text.trim()) ?? 0;
      DateTime calculatedDob = DateTime.now().subtract(Duration(days: userAge * 365));

      // 4. FIXED: Using your complete User model matching PostgreSQL
      my_models.User newUser = my_models.User(
        id: supabaseUser.id, // Secure Unique ID from Supabase Auth
        fullName: _fullNameController.text.trim(),
        status: "active",
        dob: calculatedDob,
        age: userAge,
        address: "Not Provided Yet",
        phonenumber: "Not Provided Yet",
        email: _emailController.text.trim(),
        password: "", // Handled securely by Supabase
      );

      // 5. FIXED: Passing the real Supabase JWT accessToken to your FastAPI database service
      await DatabaseService.registerUser(newUser, session.accessToken); 

      // 6. FIXED: Pop the loading indicator context from screen stack
      if (!mounted) return;
      Navigator.pop(context);

      // 7. FIXED: lowercase "user:" parameter and removed "const"
      Navigator.pushReplacement(
        context,
        MaterialPageRoute(
          builder: (context) => HomeScreen(user: newUser),
        ),
      );

    } catch (error) {
      // Dismiss loading wheel if things fail
      if (!mounted) return;
      Navigator.pop(context);

      // Show the failure message to your user
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
        title: const Text('Signup Screen'),
      ),
      body: Form(
        key: _formKey,
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(16.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              TextFormField(
                  controller: _fullNameController,
                  keyboardType: TextInputType.name,
                  inputFormatters: [
                    FilteringTextInputFormatter.allow(RegExp(r'[a-zA-Z\s]')),
                  ],
                  decoration: const InputDecoration(
                  labelText: 'Full Name',
                  border: OutlineInputBorder(),
                  ),
                  validator: (value) {
                    if (value == null || value.isEmpty) {
                      return 'Please enter your full name';
                    }
                    return null;
                  },
              ),
              TextFormField(
                  controller: _ageController,
                  keyboardType: TextInputType.number,
                  inputFormatters: [FilteringTextInputFormatter.digitsOnly],
                  decoration: InputDecoration(
                    labelText: 'Age',
                    counterText: 'Enter your age (0-120)',
                    border: OutlineInputBorder(),
                  ),
                  maxLength: 3, // Limit the input to 3 digits
                  validator: (value) {
                    if (value == null || value.isEmpty) {
                      return 'Please enter your age';
                    }
                    final age = int.tryParse(value);
                    if (age == null || age < 0 || age > 120) {
                      return 'Please enter a valid age between 0 and 120';
                    }
                    return null;
                  },
              ),
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
                onPressed: _signup,
                child: const Text('Signup'),
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
           