import os
import bpy
import csv
from pathlib import Path

""" 
This script plots data points in blender using British National Grid Easting 
and Northings coordinates. The data plots to be plotted should be stored in 
a csv file, with columns named Easting and Northing containing the 
corresponding data values.

To run this script, first review and edit the parameters in __main__.
"""

def create_color_ramp_material(attr_name: str):
    '''
    Creates a material in Blender with a color ramp, which changes color 
    according to some attribute of the object.

    Parameters
    ----------
    attr_name (str): The name of the attribute of each object on which to 
        base the colour.
    '''
    # Create a new material for the color ramp
    material = bpy.data.materials.new(name="Color Ramp Material")
    material.use_nodes=True
    

    # Delete the existing material output node since we'll be adding our own one in
    node_to_delete =  material.node_tree.nodes['Material Output']
    material.node_tree.nodes.remove( node_to_delete )


    # Create a new color ramp node and add it to the active material
    color_ramp = material.node_tree.nodes.new(type="ShaderNodeValToRGB")
    color_ramp.name = "Color Ramp"
    mat_output = material.node_tree.nodes.new(type="ShaderNodeOutputMaterial")

    material.node_tree.links.new(color_ramp.outputs["Color"], 
                                 mat_output.inputs["Surface"])

    # Set the color stops and positions on the color ramp
    # The below defines a colour ramp varying from red to yellow to blue.
    color_ramp.color_ramp.elements[0].position = 0.0
    color_ramp.color_ramp.elements[0].color = (1.0, 0.0, 0.0, 1.0)
    color_ramp.color_ramp.elements.new(.5)
    color_ramp.color_ramp.elements[1].color = (1.0, 1.0, 0.0, 1.0)
    color_ramp.color_ramp.elements.new(1.0)
    color_ramp.color_ramp.elements[2].color = (0.0, 0.0, 1.0, 1.0)

    # Construct and set the attribute node
    attribute_node = material.node_tree.nodes.new(type="ShaderNodeAttribute")
    attribute_node.attribute_type = 'OBJECT'
    attribute_node.attribute_name = attr_name

    # Link attribute node to the color ramp.
    material.node_tree.links.new(attribute_node.outputs["Fac"], color_ramp.inputs['Fac'])

    return material, color_ramp


def create_stick_material(color: tuple = (0, 0, 0, 1)):
    ''' 
    Creates a simple material for the stick under any data points. 
    
    Parameters
    ----------
    color (tuple): Given in rgba values ranging from 0 to 1. Default is black.
    '''
    stick_material = bpy.data.materials.new(name="StickMat")
    stick_material.use_nodes = True
    stick_material.node_tree.nodes["Principled BSDF"].inputs[0].default_value = color
    return stick_material


def add_data_point(
        location: tuple,
        color_ramp_attribute: str, 
        color_ramp_value: float, 
        disk_material: bpy.types.Material, 
        stick_material: bpy.types.Material):
    
    # Create a new cylinder object and set its properties.
    bpy.ops.mesh.primitive_cylinder_add(radius=sphere_size, 
                                        enter_editmode=False, 
                                        location=location, 
                                        scale=(1,1,0))
    
    # Set the newly created cylinder to the active object
    obj = bpy.context.active_object

    # Add the color ramp attribute
    obj[color_ramp_attribute] = color_ramp_value
    
    # Apply disk material
    obj.data.materials.append(disk_material)
    
    # Add a constraint to the disk to track the camera.
    constraint = obj.constraints.new(type='TRACK_TO')
    camera_obj = bpy.data.objects['Camera']
    constraint.target = camera_obj
    
    # Add a lollipop stick to orient the location on the ground.
    lollipop_location = (location[0], location[1], location[2]/2.0 - 10)
    bpy.ops.mesh.primitive_cylinder_add(location=lollipop_location, 
                                        scale=(1,1,z/2.0))
    
    # Set the stick to the active object
    obj = bpy.context.active_object

    # Set the material to stick_material.
    obj.data.materials.append(stick_material)


if __name__=="__main__": 

    ''' 
    SET PARAMETERS
    '''
    # 3D world parameters
    world_origin_bng_eastings = 532000
    world_origin_bng_northings = 181000
    xmin, ymin, xmax, ymax = [532000, 180000, 533000, 181000] # bounding box

    # Data parameters
    csv_file = str(Path.home()) + \
        str(Path("/Code/3dcity-blender/sample_data/FoodHygieneRatings_CityOfLondon_accessed20241028.csv"))
    color_ramp_attribute = "RatingValue"
    color_ramp_max = 5.0
    
    # Visualisation parameters
    sphere_size = 10
    sphere_height = 80.0

    '''
    Preliminaries
    '''
    # Create materials for our data point objects
    disk_material, color_ramp = create_color_ramp_material(color_ramp_attribute)
    stick_material = create_stick_material()

    ''' 
    Data loop
    '''
    # Open the CSV file
    with open(csv_file) as f:
        reader = csv.DictReader(f)
        
        # Loop through each row in the CSV file.
        for row in reader:    
            # Get the x, y, and z coordinates from the row.
            x = float(row['Easting']) - world_origin_bng_eastings
            y = float(row['Northing']) - world_origin_bng_northings
            z = sphere_height
            
            # Only proceed if the row of data falls inside our square.
            if float(row['Easting']) > xmax:
                continue
            if float(row['Easting']) < xmin:
                continue
            if float(row['Northing']) > ymax:
                continue
            if float(row['Northing']) < ymin:
                continue
            
            try:
                # Get the float value for color from the row.
                value = float(row[color_ramp_attribute]) / color_ramp_max - 0.005
                # We take away a small value since blender doesn't seem to do
                # well with color ramp values at 1.
            except ValueError:
                # Some attributes might not have numeric data. 
                continue
            
            add_data_point(location=(x,y,z), 
                           color_ramp_attribute=color_ramp_attribute, 
                           color_ramp_value=value, 
                           disk_material=disk_material, 
                           stick_material=stick_material)