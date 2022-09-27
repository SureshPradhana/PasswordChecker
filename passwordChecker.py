import requests
import hashlib
import sys



def request_api_data(query_char):
	url='https://api.pwnedpasswords.com/range/'+query_char
	res=requests.get(url)
	if res.status_code!=200:
		raise RuntimeError(f'error fetching {res.status_code},check the api and try again')
	return res

def get_password_leaks_count(hashes,hashtocheck):
	hashes = (line.split(':') for line in hashes.text.splitlines())
	count=0
	for k,v in hashes:
		if k==hashtocheck:
			count=v
	return count
	
def pwned_api_check(password):
	sha1password=hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
	first5_char,last=sha1password[:5],sha1password[5:]
	response=request_api_data(first5_char)
	return get_password_leaks_count(response,last)

def main(file):
	try:
		with open(file) as my_file:
			   list=my_file.read().splitlines()
			   print(list)
	except FileNotFoundError as err:
		print(err)
	for password in list:
		val=pwned_api_check(password)
		if int(val) > 0: 
			print(f'you may get hacked change password , {password} leaked {val} times')
		else:
			print(f'{password} is safe')
main(sys.argv[1])
