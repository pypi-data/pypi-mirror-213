from .core import ReferenceSubmodel


def _normalize_name(name):
    return name.strip().replace(" ", "_").replace("-", "_")


def to_python_str(model_builder, builder_name: str = None, output_submodels: bool = True):
    sub_uuid_to_names = {}
    lines, submodels_func_def = _to_python_str(
        model_builder, sub_uuid_to_names, builder_name=builder_name, output_submodels=output_submodels
    )

    create_submodels = [
        f'submodels["{submodel_name}"] = create_{_normalize_name(submodel_name)}()'
        for submodel_name, _ in submodels_func_def.items()
    ]

    if output_submodels:
        submodels_func_def = [line for lines in submodels_func_def.values() for line in lines]
        lines = ["submodels = {}"] + submodels_func_def + create_submodels + lines

    return "\n".join(lines)


def _to_python_str(model_builder, sub_uuid_to_names, model_name=None, builder_name=None, output_submodels: bool = True):
    lines = []
    submodels_func_def = {}

    if model_name is None:
        model_name = _normalize_name(model_builder.name)

    if builder_name is None:
        # Append _builder to avoid name conflict with node name
        builder_name = f"{_normalize_name(model_name)}_builder"

    lines.append(f'{builder_name} = ModelBuilder("{model_builder.name}")')

    # Parameters
    lines.extend([f'{builder_name}.add_parameter("{k}", "{v}")' for k, v in model_builder.parameters.items()])

    lines.append("")

    # Groups
    groups = set()
    for node, group in model_builder.groups.items():
        lines.append(f"def create_{node.name}():")
        group_code, other_submodels = _to_python_str(group, sub_uuid_to_names, model_name=node.name)
        submodels_func_def.update(other_submodels)
        group_code += [f"return {node.name}_builder", ""]
        lines.extend(["    " + line for line in group_code])
        groups.add(node.id)

    # Submodels
    for node, submodel in model_builder.submodels.items():
        submodel_code, other_submodels = _to_python_str(submodel, sub_uuid_to_names, model_name=submodel.name)
        submodel_code = "\n".join("    " + line for line in submodel_code)
        submodel_name = _normalize_name(submodel.name)
        submodel_def_str = [
            f"def create_{submodel_name}():",
            submodel_code,
            f"    return {submodel_name}_builder",
            "",
        ]

        submodels_func_def.update(other_submodels)
        submodels_func_def[submodel.name] = submodel_def_str
        sub_uuid_to_names[submodel.uuid] = submodel.name

    # Create nodes
    for node in model_builder.nodes.values():
        node_params = []
        for pname, pvalue in node.params.items():
            if type(pvalue) is str:
                value = pvalue.replace('"', '\\"').replace("'", "\\'").replace("\n", "\\n")
                node_params.append(f'{pname}="{value}"')
            else:
                node_params.append(f"{pname}={pvalue}")
        func_params = [f"{builder_name}", f'name="{node.name}"']
        params = func_params + node_params

        if node.has_dynamic_input_ports:
            inames = [f'"{iname}"' for iname in node.input_names]
            inames = ", ".join(inames)
            if len(inames) > 0:
                params.append(f"input_names=({inames},)")
            else:
                params.append("input_names=()")
        if node.has_dynamic_output_ports:
            onames = [f'"{oname}"' for oname in node.output_names]
            onames = ", ".join(onames)
            if len(onames) > 0:
                params.append(f"output_names=({onames},)")
            else:
                params.append("output_names=()")

        if node.schema._get("modes", "time") != node.time_mode and node.time_mode is not None:
            params.append(f'time_mode="{node.time_mode}"')

        params_str = ", ".join(params)
        lines.append(f"{node.name} = core.{node.__class__.__name__}({params_str})")

        if type(node) is ReferenceSubmodel:
            submodel_name = model_builder.submodels[node].name
            if output_submodels:
                lines.append(f'{builder_name}.add_reference_submodel({node.name}, submodels["{submodel_name}"])')

        if node.id in groups:
            lines.append(f"{builder_name}.add_group({node.name}, create_{node.name}())")

    lines.append("")

    # Connect nodes
    for link in model_builder.links.values():
        src = f"{link.src.node.name}.{link.src.name}"
        dst = f"{link.dst.node.name}.{link.dst.name}"
        lines.append(f"{builder_name}.add_link({src}, {dst})")

    return lines, submodels_func_def
