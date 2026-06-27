// lib/api_service.dart
import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/user.dart';

class ApiService {
  final String _baseUrl = 'https://your-fastapi-backend.com';

  // Pass the verified JWT Auth Token alongside your profile payload
  Future<void> registerUserToPostgres(User user, String authToken) async {
    final url = Uri.parse('$_baseUrl/users/signup');
    
    try {
      final response = await http.post(
        url,
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
          'Authorization': 'Bearer $authToken', // Protects your API endpoint
        },
        body: jsonEncode(user.toMap()),
      );

      if (response.statusCode != 201 && response.statusCode != 200) {
        final errorData = jsonDecode(response.body);
        throw Exception(errorData['detail'] ?? 'Failed to sync user profile.');
      }
    } catch (e) {
      rethrow;
    }
  }
}
