import phonenumbers

from phonenumbers import geocoder
phone = phonenumbers.parse("+13108900944")

print(geocoder.description_for_number(phone, "en"))