import arcpy
import datetime
def log_error(message):
    """Logs error messages to a file or other logging mechanism."""
    with open("error_log.txt", "a") as log_file:
        log_file.write(f"{datetime.datetime.now()}: {message}\n")
def select_multipart_features(layer):
    """Selects multipart features in the given layer."""
    multipart_features = []
    with arcpy.da.SearchCursor(layer, ["OID@", "SHAPE@"]) as cursor:
        for row in cursor:
            if row[1] is not None and row[1].isMultipart:
                multipart_features.append(row[0])
    return multipart_features
try:
    # Attempt to get the parameter value
    feature_layer = arcpy.GetParameterAsText(0)  # Assuming it's the first parameter
    if not feature_layer:
        raise ValueError("No feature layer provided. Please ensure the parameter is correctly set.")
    
    # Get the current date and time
    current_datetime = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Append the date and time to the layer names
    temp_layer_with_datetime = f"temp_layer_{current_datetime}"
    output_layer_with_datetime = f"output_layer_{current_datetime}"
    
    # Create a feature layer
    arcpy.MakeFeatureLayer_management(feature_layer, temp_layer_with_datetime)
    
    # Select multipart features
    multipart_oids = select_multipart_features(temp_layer_with_datetime)
    if multipart_oids:
        arcpy.SelectLayerByAttribute_management(temp_layer_with_datetime, "NEW_SELECTION", f"OBJECTID IN ({','.join(map(str, multipart_oids))})")
    
    # Save the selected features to a new layer with the datetime appended
    arcpy.CopyFeatures_management(temp_layer_with_datetime, output_layer_with_datetime)
    
    print(f"Temporary layer: {temp_layer_with_datetime}")
    print(f"Output layer: {output_layer_with_datetime}")
except arcpy.ExecuteError:
    # Handle geoprocessing errors
    error_message = arcpy.GetMessages(2)
    print("Geoprocessing error occurred:")
    print(error_message)
    log_error(f"Geoprocessing error: {error_message}")
except ValueError as ve:
    # Handle value errors
    print("Value error occurred:")
    print(ve)
    log_error(f"Value error: {ve}")
except Exception as e:
    # Handle other errors
    print("An error occurred:")
    print(e)
    log_error(f"General error: {e}")
