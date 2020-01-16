import hashlib

string = ""
string += "b"

a = hashlib.md5(string.encode()).hexdigest()
