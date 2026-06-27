// lib/database_service.dart
import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/user.dart'; // Ensure this path matches your user model file location

class DatabaseService {
  // Update with your FastAPI base address.
  // Use 'http://10.0.2.2:8000' if testing on an Android Emulator against a local FastAPI instance
  static const String _baseUrl = 'http://10.0.2';

  /// Sends user profile data to the FastAPI backend to store it in PostgreSQL.
  /// [authToken] is the JWT string obtained from Firebase Auth or Supabase Auth.
  static Future<void> registerUser(User user, String authToken) async {
    final url = Uri.parse('$_baseUrl/users/signup');

    try {
      final response = await http.post(
        url,
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
          'Authorization': 'Bearer $authToken', // Pass token securely in headers
        },
        body: jsonEncode(user.toMap()), // Converts user object to a JSON payload
      );

      // Handle server-side validations or error responses
      if (response.statusCode != 201 && response.statusCode != 200) {
        final errorData = jsonDecode(response.body);
        throw Exception(errorData['detail'] ?? 'Failed to sync account to database.');
      }
    } catch (e) {
      print("Database Service Error: $e");
      rethrow; // Pass error up to the UI loop
    }
  }
}
