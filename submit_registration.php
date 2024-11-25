<?php
if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    $name = htmlspecialchars($_POST['name']);
    $dob = htmlspecialchars($_POST['dob']);
    $email = htmlspecialchars($_POST['email']);
    $phone = htmlspecialchars($_POST['phone']);
    $address = htmlspecialchars($_POST['address']);
    $emergency_contact = htmlspecialchars($_POST['emergency_contact']);
    $date = htmlspecialchars($_POST['date']);

    // Handling file uploads
    $signature_file = $_FILES['signature'];
    $photo_file = $_FILES['photo'];

    // Define the upload directory
    $upload_dir = "uploads/";
    if (!is_dir($upload_dir)) {
        mkdir($upload_dir, 0755, true); // Create if not exists
    }

    // Move uploaded files to the directory
    $signature_path = $upload_dir . basename($signature_file['name']);
    $photo_path = $upload_dir . basename($photo_file['name']);

    move_uploaded_file($signature_file['tmp_name'], $signature_path);
    move_uploaded_file($photo_file['tmp_name'], $photo_path);

    // Send Email Notification (optional)
    $to = "your-email@example.com";
    $subject = "New Registration from $name";
    $message = "Name: $name\nDOB: $dob\nEmail: $email\nPhone: $phone\nAddress: $address\nEmergency Contact: $emergency_contact\nDate: $date\n";
    $headers = "From: no-reply@yourdomain.com";

    mail($to, $subject, $message, $headers);

    // Confirmation message
    echo "Thank you for registering! Your details have been submitted.";
}
?>
