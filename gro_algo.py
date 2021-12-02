
def check_duration(origin,destination):
    endpoint = 'https://maps.googleapis.com/maps/api/directions/json?'
    api_key = 'AIzaSyB0t8cqNglZzb8N0rDMvyU2nozCGfrOOwM'
    # Asks the user to input Where they are and where they want to go.
    origin = input('Location: ').replace(' ', '+')
    destination = input('Destination: ').replace(' ', '+')
    # Building the URL for the request
    nav_request = 'origin={}&destination={}&key={}'.format(origin, destination, api_key)
    request = endpoint + nav_request
    # Sends the request and reads the response.
    response = urllib.request.urlopen(request).read()
    # Loads response as JSON
    directions = json.loads(response)
    time = directions.time
    return time


def ind2route(loc_data):
    route = []
    vehicle_capacity = 400 #(cubics)
    # Initialize a sub-route
    sub_route = []
    elapsed_time = 0
    ID = 0
    ID_next =0
    for ID_module in loc_data:
        ID = ID_module
        ID_next = ID_module+1
        # Update elapsed time
        time = check_time
        updated_elapsed_time = elapsed_time + time
        # Validate vehicle load and elapsed time
        if (check_time(origin, ID) < check_time(origin,ID_next)):
            # Add to current sub-route
            sub_route.append(ID)
            elapsed_time = updated_elapsed_time -time
        else:
            # Save current sub-route
            route.append(sub_route)
            # Initialize a new sub-route and add to it
            sub_route = ID
        #update current and next ID_module
        vehicle_capacity-=40
        ID = ID_next
        ID_next = ID_next+1
    if sub_route != []:
        # Save current sub-route before return if not empty
        route.append(sub_route)
    return route


