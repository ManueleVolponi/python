import phonenumbers

from phonenumbers import geocoder
phone = phonenumbers.parse("phne_number")

print(geocoder.description_for_number(phone, "en"))
