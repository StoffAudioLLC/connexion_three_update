def mime_type_negotiation(
    python_payload: Any,
    query_string_mime_type: Optional[str],
    build_date: Optional[datetime] = None,
) -> Optional[flask.Response]:
    """Give the client what they want"""
    if query_string_mime_type:
        # handle bare "yaml" without "text/" prefix
        if "/" not in query_string_mime_type:
            query_string_mime_type = "/" + query_string_mime_type
        accepted_string = query_string_mime_type
    else:
        try:
            accepted_string = flask.request.headers.get("Accept")
        except RuntimeError as runtime_error:
            if "Working outside" not in str(runtime_error):
                raise
            accepted_string = "application/json"

    # split up types
    accepted = convert_accepted_string(accepted_string)

    # requested_type = ""
    desired_type = ""
    if is_dataclass(python_payload):
        python_payload = asdict(python_payload)
    # known convert synonyms into one canonical type
    for string in accepted:
        if string.endswith("/json"):
            desired_type = "application/json"
        if (
            string.endswith("/yaml")
            or string.endswith("/x-yaml")
            or string
            in [
                "text/vnd.yaml",
            ]
        ):
            # requested_type = string
            desired_type = "text/yaml"
        if string.endswith("/xml"):
            # requested_type = string
            desired_type = "application/xml"
        if string.endswith("/msgpack") or string.endswith("/x-msgpack"):
            # requested_type = string
            desired_type = "application/msgpack"
        if string.endswith("/toml") or string.endswith("/x-toml"):
            # requested_type = string
            desired_type = "application/toml"
        if string.endswith("/ion") or string.endswith("/x-ion"):
            # requested_type = string
            desired_type = "application/ion"

        # So why these noqa: W504s? Because flake8, in its mastery of the Python
        # language, will either complain about "W504: Line break after binary operator"
        # _or_ "E502: the backslash is redundant between brackets" here because
        # why not?
        if (
            string.endswith("/rss")
            or string.endswith("/x-rss")
            or string.endswith("/rss+xml")  # noqa: W504
        ):
            # requested_type = string
            desired_type = "application/rss+xml"
        if (
            string.endswith("/atom")
            or string.endswith("/x-atom")
            or string.endswith("/atom+xml")  # noqa: W504
        ):
            # requested_type = string
            desired_type = "application/atom+xml"
        if string.endswith("/csv"):
            # requested_type = string
            desired_type = "text/csv"
        if string.endswith("/bibtex") or string.endswith("x-bibtex"):
            # requested_type = string
            desired_type = "application/bibtex"
        if string.endswith("/bson"):
            desired_type = "application/bson"

        if desired_type:
            break

    if desired_type == "application/json":
        # json is the default
        return None

    if not desired_type:
        # unsupported type falling back to json
        return None

    if desired_type == "text/csv":
        csv_payload = generate_csv(python_payload)
        resp = flask.make_response(csv_payload)
        resp.headers["Content-Type"] = desired_type
        resp.headers["content-disposition"] = 'attachment; filename="Results.csv"'
        return resp
    if desired_type == "application/bibtex":
        bibtex_payload = generate_bibtex(python_payload)
        resp = flask.make_response(bibtex_payload)
        resp.headers["Content-Type"] = desired_type
        resp.headers["content-disposition"] = 'attachment; filename="Results.bib"'
        return resp
    # If the user said they wanted text/msgpack then that is the return content type.
    # we normalize here, but return the user's version
    if desired_type == "text/yaml":
        yaml_payload = yaml.dump(python_payload, Dumper=yaml.CSafeDumper)  # noqa
        resp = flask.make_response(yaml_payload)
        resp.headers["Content-Type"] = desired_type
        # resp.headers["content-disposition"] = "attachment; filename=\"Results.yaml\""
        return resp
    if desired_type == "application/xml":
        xml = dicttoxml.dicttoxml(python_payload, root=True, custom_root="records")
        resp = flask.make_response(xml)
        resp.headers["Content-Type"] = desired_type
        return resp
    if desired_type == "application/msgpack":
        message_pack_payload = msgspec.msgpack.encode(python_payload)  # type: ignore
        resp = flask.make_response(message_pack_payload)
        resp.headers["Content-Type"] = desired_type
        resp.headers["content-disposition"] = 'attachment; filename="Results.msgpack"'
        return resp
    if desired_type == "application/toml":
        # TOML can't deal with a root tuple/list or child tuple/lists
        toml_payload: Optional[str] = None
        try:
            toml_payload = rtoml.dumps(python_payload)
        except Exception:  # pylint: disable=broad-except
            LOGGER.warning(
                "Payload failed to serialize with rtoml. Falling back to toml"
            )
            toml_payload = slow_toml.dumps(python_payload)

        resp = flask.make_response(toml_payload)
        resp.headers["Content-Type"] = desired_type
        resp.headers["content-disposition"] = 'attachment; filename="Results.toml"'
        return resp
    if desired_type == "application/ion":
        # This has wheels, suddenly import started
        # failing even thought pipenv install reports no errors
        # fails on windows now?
        import amazon.ion.simpleion as ion

        ion_payload = ion.dumps(python_payload)
        resp = flask.make_response(ion_payload)
        resp.headers["Content-Type"] = desired_type
        resp.headers["content-disposition"] = 'attachment; filename="Results.ion"'
        return resp
    if desired_type == "application/bson":
        bson_payload = bson.dumps(python_payload)
        resp = flask.make_response(bson_payload)
        resp.headers["Content-Type"] = desired_type
        resp.headers["content-disposition"] = 'attachment; filename="Results.bson"'
    if desired_type in ["application/rss+xml", "application/atom+xml"]:
        feed = generate_rss(python_payload, build_date)
        rss_feed = feed.rss_str(pretty=True)
        atom_feed = feed.atom_str(pretty=True)
        if "atom" in desired_type:
            resp = flask.make_response(atom_feed)
            resp.headers["Content-Type"] = desired_type
            resp.headers["content-disposition"] = 'attachment; filename="Results.atom"'
        else:
            resp = flask.make_response(rss_feed)
            resp.headers["Content-Type"] = desired_type
            resp.headers["content-disposition"] = 'attachment; filename="Results.rss"'
        return resp

    return None