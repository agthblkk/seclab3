import unittest
from main import PoemCipher

class TestPoemCipher(unittest.TestCase):
    def setUp(self):
        self.poem = (
            "Садок вишневий коло хати,\n"
            "Хрущі над вишнями гудуть,\n"
            "Плугатарі з плугами йдуть,\n"
            "Співають ідучи дівчата,\n"
            "А матері вечерять ждуть."
        )
        self.cipher = PoemCipher(self.poem)

    def test_encrypt(self):
        message = "привіт"
        encrypted = self.cipher.encrypt(message)
        self.assertTrue(all("/" in code for code in encrypted.split(", ")), "Шифрование должно генерировать коды вида CC/SS")

    def test_encrypt_decrypt(self):
        message = "привіт"
        encrypted = self.cipher.encrypt(message)
        decrypted = self.cipher.decrypt(encrypted)
        self.assertEqual(decrypted, message, "Дешифрование зашифрованного сообщения должно совпадать с исходным сообщением")

    def test_missing_character(self):
        message = "-"
        encrypted = self.cipher.encrypt(message)
        self.assertTrue("??" in encrypted, "Для отсутствующих символов шифрование должно возвращать '??'")
