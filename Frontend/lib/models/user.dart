class User {
  final String id;
  final String fullName;
  final String status;
  final DateTime dob;
  final int age;
  final String address;
  final String phonenumber;
  final String email;
  final String password;

  User({
    required this.id,
    required this.fullName,
    required this.status,
    required this.dob,
    required this.age,
    required this.address,
    required this.phonenumber,
    required this.email,
    required this.password,
  });

  //  FIXED: Parse string dates sent by your FastAPI server
  factory User.fromMap(String id, Map<String, dynamic> data) {
    return User(
      id: id,
      fullName: data['fullName'] as String,
      status: data['status'] as String,
      // Converts the ISO-8601 String back into a Flutter DateTime object
      dob: DateTime.parse(data['dob'] as String), 
      age: data['age'] as int,
      address: data['address'] as String,
      phonenumber: data['phonenumber'] as String,
      email: data['email'] as String,
      password: data['password'] as String,
    );
  }

  //  FIXED: Format dates to standard universal string formats for your database
  Map<String, dynamic> toMap() {
    return {
      'id': id,
      'fullName': fullName,
      'status': status,
      // Converts your DateTime object into a standard string like "2026-06-27T23:33:00"
      'dob': dob.toIso8601String(), 
      'age': age,
      'address': address,
      'phonenumber': phonenumber,
      'email': email,
      'password': password,
    };
  }
}
