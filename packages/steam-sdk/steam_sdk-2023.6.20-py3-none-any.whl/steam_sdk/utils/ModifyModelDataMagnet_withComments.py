import os
from pathlib import Path
import ruamel.yaml
from steam_sdk.data.DataModelMagnet import DataModelMagnet
from functools import reduce


if __name__ == "__main__":
    path_to_models = Path.joinpath(
        Path(__file__).parent.parent.parent, "tests/builders/model_library/magnets"
    )

    model_names = [x.parts[-1] for x in Path(path_to_models).iterdir() if x.is_dir()]

    for model_name in model_names:
        yaml_file = Path.joinpath(
            path_to_models, model_name, "input", "modelData_" + model_name + ".yaml"
        )

        # Check if the file exists:
        if os.path.isfile(yaml_file):
            # Read the file:
            with open(yaml_file, "r") as stream:
                # Read the yaml file and store the date inside ruamel_yaml_object:
                # ruamel_yaml_object is a special object that stores both the data and
                # comments. Even though the data might be changed or added, the same
                # object will be used to create the new YAML file to store the comments.
                ruamel_yaml_object = ruamel.yaml.YAML().load(yaml_file)
            print(f"The file has been read: {yaml_file}")

            # Create a DataModelMagnet object from the yaml file's data:
            # Note: Obsolete keys (the keys that are not in DataModelMagnet) will
            # automatically be deleted. Moreover, if new keys are added to
            # DataModelMagnet, they will be added to the YAML file. The new key's values
            # will be DataModelMagnet's default values.
            model_data = DataModelMagnet(**ruamel_yaml_object)

            # Some values of the new and old keys can be changed like this:
            # model_data.Options_LEDET.magnet_inductance.flag_calculate_inductance = True

            # Old values of obsolete keys can be moved to new keys like this:
            # model_data.Options_LEDET.conductor_geometry_used_for_ISCL.mirrorY_ht = (
            #     ruamel_yaml_object["CoilWindings"]["multipole"]["mirrorY_ht"]
            # )

            # Set to True if you wish to test the results of this script, and False if
            # you wish to really update all yaml input files

            # ==========================================================================
            # ==========================================================================
            # Add pydantic descriptions to the yaml file as comments:
            yaml_file_without_comments_output = Path.joinpath(
                path_to_models,
                model_name,
                "input",
                "modelData_" + model_name + "_WITHOUTCOMMENTS.yaml",
            )
            with open(yaml_file_without_comments_output, "w") as stream:
                ruamel.yaml.YAML().dump(model_data.dict(), stream)

            # Read the file:
            with open(yaml_file, "r") as stream:
                # Read the yaml file and store the date inside ruamel_yaml_object:
                # ruamel_yaml_object is a special object that stores both the data and
                # comments. Even though the data might be changed or added, the same
                # object will be used to create the new YAML file to store the comments.
                ruamel_yaml_object = ruamel.yaml.YAML().load(
                    yaml_file_without_comments_output
                )

            os.remove(yaml_file_without_comments_output)            

            def iterate_fields(model, ruamel_yaml_object, parentKey=None):
                for (currentKey, value), (ruamelKey, ruamelValue) in zip(
                    model.__fields__.items(), ruamel_yaml_object.items()
                ):
                    if value.field_info.description:
                        try:
                            ruamel_yaml_object.yaml_add_eol_comment(
                                value.field_info.description,
                                currentKey,
                            )
                        except:
                            print("passed")
                            pass

                    if hasattr(getattr(model, currentKey), "__fields__"):
                        new_ruamel_yaml_object = iterate_fields(
                            getattr(model, currentKey),
                            ruamel_yaml_object[currentKey],
                        )

                        ruamel_yaml_object[currentKey] = new_ruamel_yaml_object

                return ruamel_yaml_object

            for currentKey, value in model_data.__fields__.items():
                if hasattr(getattr(model_data, currentKey), "__fields__"):
                    ruamel_yaml_object[currentKey] = iterate_fields(
                        getattr(model_data, currentKey),
                        ruamel_yaml_object[currentKey],
                    )

            # ==========================================================================
            # ==========================================================================
            test = True
            if test:
                yaml_file_output = Path.joinpath(
                    path_to_models,
                    model_name,
                    "input",
                    "modelData_" + model_name + "_MODIFIED.yaml",
                )
            else:
                yaml_file_output = yaml_file

            # Write the yaml file back to disk with the same comments
            with open(yaml_file_output, "w") as stream:
                ruamel.yaml.YAML().dump(ruamel_yaml_object, stream)

            print(f"The file has been written: {yaml_file_output}")
        else:
            print(f"WARNING: {yaml_file} is not found.")
