
#filename:base64_.py
#folder:backup
import base64
answer= input("give some chars ")
sample_string = answer # '' #  "GeeksForGeeks is the best"
sample_string_bytes = sample_string.encode("ascii")
base64_bytes = base64.b64encode(sample_string_bytes)
base64_string = base64_bytes.decode("ascii")
print(f"Encoded string: {base64_string}")
