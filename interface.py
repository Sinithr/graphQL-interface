#!/usr/bin/env python3.4

import graphene
from flask import Flask, jsonify, request, abort
import math

STORES = (
((38.923476, -77.043093), '1827 Adams Mill Rd, DC'),
((38.874674, -77.001121), '1331 4th St, DC'),
((34.046645, -118.259129), '801 S Hope St, LA'),
((33.655242, -117.998635), '21016 Pacific Coast, Huntington Beach'),
((34.143154, -118.131758), 'Shops on Lake Av, Pasadena'),
((34.142889, -118.254599), '252 S Brand Blvd, Glendale'),
((34.097690, -118.330020), '6430 Sunset Blvd, LA'),
((34.017950, -118.493557), '525 Santa Monica Blvd, LA'),
((37.566991, -122.323638), '113 S B St, San Mateo'),
((37.577947, -122.348523), '305 Primrose Rd, Burlingame'),
((37.775523, -122.393391), '201 Berry St, SF'),
((37.760096, -122.434625), '549 Castro St, SF'),
((37.782402, -122.420482), '748 Van Ness Ave, SF'),
((37.788778, -122.393232), '300 Folsom St, SF')
)

app = Flask(__name__)

query = '''{ storeByLocation(criteria: {location: {latitude: 37.760503, longitude: -122.433883}, kmRadius:2.0}){
        distance
        store {
            name
        }
    }
}
'''
### searching stores around location with input radius
@app.route('/interface', methods=['PUT'])
def search():
    # checking request
    if not request.json or not 'query' in request.json:
        abort(400)

    result = schema.execute(request.json['query'])
    if not 'reverse' in request.json:
        shops = sorted([{'distance': shop['distance'], 'name': shop['store']['name']} for shop in result.data['storeByLocation']], key=lambda k: k['distance'])
    else:
        if request.json['reverse'] == 'True':
            shops = sorted([{'distance': shop['distance'], 'name': shop['store']['name']} for shop in result.data['storeByLocation']], key=lambda k: k['distance'], reverse=True)
        else:
            shops = sorted([{'distance': shop['distance'], 'name': shop['store']['name']} for shop in result.data['storeByLocation']], key=lambda k: k['distance'])
    return jsonify(shops)

def distance(locationA, locationB): # distance between 2 points
    R = 6371.0 # km 
    lon1, lat1, lon2, lat2 = map(math.radians, [locationA[0], locationA[1], locationB[0], locationB[1]])

    # haversine formula 
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    r = 6371 # Radius of earth in kilometers
    return c * r

class Location(graphene.InputObjectType):
    latitude = graphene.Float()
    longitude = graphene.Float()

class Store(graphene.ObjectType):
    id = graphene.String()
    name = graphene.String()
    latitude = graphene.Float()
    longitude = graphene.Float()

class LocationSearchCriteria(graphene.InputObjectType):
    location = graphene.Field(Location)
    kmRadius = graphene.Float()

class LocationSearchEntry(graphene.ObjectType):
    store = graphene.Field(Store)
    distance = graphene.Float()
    def resolve_distance(self, args, context, info):
        return self.distance

class Query(graphene.ObjectType):
    storeByLocation = graphene.List(LocationSearchEntry, criteria=LocationSearchCriteria())
    def resolve_storeByLocation(self, args, context, info):
        criteria = args.get('criteria')
        locationB = []
        locationB.append(criteria.get('location')['latitude'])
        locationB.append(criteria.get('location')['longitude'])
        shops = [] #graphene.List(LocationSearchEntry)
        it = 0
        for store in STORES:
            if distance(store[0], locationB) <= criteria.get('kmRadius'):
                location_input = Location(latitude=store[0][0], longitude=store[0][1])
                store_input = Store(id=it, name=store[1], latitude=store[0][0], longitude=store[0][1])
                shop = LocationSearchEntry(distance=distance(store[0], locationB), store=store_input)
                shops.append(shop)
                it = it + 1
        return shops
        
schema = graphene.Schema(query=Query)
if __name__ == "__main__":
    #result = schema.execute(query)
    app.run(debug=True)
