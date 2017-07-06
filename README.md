# GraphQL interface
Plik interface.py uruchomić za pomocą python3.4.

Przykładowe żądanie:
curl -i -H "Content-Type: application/json" -X PUT -d '{"query": "{ storeByLocation(criteria: {location: {latitude: 37.760503, longitude: -122.433883}, kmRadius:2.0}){distance store {name}}}", "reverse": "True"}' http://localhost:5000/interface

W przypadku braku flagi sortowania ("reverse") lub wartości innej niż "True" zostanie zwrócona lista posortowana od najbliższego sklepu. 
Z wartością "True" lista będzie posortowana od najdalszego.
