import bpy

def create_material(eastings_wotts: float, 
                    northings_wotts: float, 
                    texture_width: float, 
                    texture_height: float, 
                    texture_file_path: str):
    '''
    Adds a choropleth overlay material 

    e_wotts: Eastings world origin to texture start
    n_wotts: Northings world origin to texture start
    texture_width: Width of the texture in physcial units (usually metres) in the Eastings direction
    texture_height: Height of the texture in physical units (usually metres) in the Northings direction
    '''

    # Create a new material for the color ramp
    material = bpy.data.materials.new(name="Choropleth Overlay")
    material.use_nodes=True
    principled_bsdf = material.node_tree.nodes["Principled BSDF"]

    geometry_node = material.node_tree.nodes.new("ShaderNodeNewGeometry")

    separate_node = material.node_tree.nodes.new("ShaderNodeSeparateXYZ")
    material.node_tree.links.new(geometry_node.outputs["Position"], separate_node.inputs["Vector"])

    subtract_node1 = material.node_tree.nodes.new("ShaderNodeMath")
    subtract_node1.operation="SUBTRACT"
    material.node_tree.links.new(separate_node.outputs["X"], subtract_node1.inputs["Value"])
    subtract_node1_value = material.node_tree.nodes.new("ShaderNodeValue")
    subtract_node1_value.outputs[0].default_value = eastings_wotts
    material.node_tree.links.new(subtract_node1_value.outputs['Value'], subtract_node1.inputs[1])

    subtract_node2 = material.node_tree.nodes.new("ShaderNodeMath")
    subtract_node2.operation="SUBTRACT"
    material.node_tree.links.new(separate_node.outputs["Y"], subtract_node2.inputs["Value"])
    subtract_node2_value = material.node_tree.nodes.new("ShaderNodeValue")
    subtract_node2_value.outputs[0].default_value = northings_wotts
    material.node_tree.links.new(subtract_node2_value.outputs["Value"], subtract_node2.inputs[1])

    divide_node1 = material.node_tree.nodes.new("ShaderNodeMath")
    divide_node1.operation="DIVIDE"
    material.node_tree.links.new(subtract_node1.outputs["Value"], divide_node1.inputs["Value"])
    divide_node1_value = material.node_tree.nodes.new("ShaderNodeValue")
    divide_node1_value.outputs[0].default_value = texture_width
    material.node_tree.links.new(divide_node1_value.outputs["Value"], divide_node1.inputs[1])
    
    divide_node2 = material.node_tree.nodes.new("ShaderNodeMath")
    divide_node2.operation="DIVIDE"
    material.node_tree.links.new(subtract_node2.outputs["Value"], divide_node2.inputs["Value"])
    divide_node2_value = material.node_tree.nodes.new("ShaderNodeValue")
    divide_node2_value.outputs[0].default_value = texture_height
    material.node_tree.links.new(divide_node2_value.outputs["Value"], divide_node2.inputs[1])    

    combine_node = material.node_tree.nodes.new("ShaderNodeCombineXYZ")
    material.node_tree.links.new(divide_node1.outputs["Value"], combine_node.inputs["X"])
    material.node_tree.links.new(divide_node2.outputs["Value"], combine_node.inputs["Y"])

    texture_node = material.node_tree.nodes.new("ShaderNodeTexImage")
    image = bpy.data.images.load(texture_file_path)
    texture_node.image = image
    material.node_tree.links.new(combine_node.outputs["Vector"], texture_node.inputs["Vector"])
    material.node_tree.links.new(texture_node.outputs["Color"], principled_bsdf.inputs["Base Color"])

    return material

if __name__=="__main__":
    
    from pathlib import Path

    Eastings_world_origin_to_texture_start = -1319.90
    Northings_world_origin_to_texture_start = -10755.41
    Texture_width = 6304.83
    Texture_height = 12523.04

    texture_file_path = str(Path.home()) + str(Path("/Code/3dcity-blender/images/popden_texture.png"))

    material = create_material(eastings_wotts=Eastings_world_origin_to_texture_start, 
                               northings_wotts=Northings_world_origin_to_texture_start,                 
                               texture_width=Texture_width, 
                               texture_height=Texture_height, 
                               texture_file_path=texture_file_path)
    
    for o in ("HIGH_DETAIL_BUILDINGS", "UNDER_CONSTRUCTION", "UNDER_SCAFFOLD"):
        obj = bpy.context.scene.objects.get(o)
        if obj: obj.select_set(True)
        # apply material - overwriting if it already exists
        if len(obj.data.materials) > 0:      
            obj.data.materials[0] = material
        else:
            obj.data.materials.append(material)
