{
    "image": {
        "required": True,
        "type": "string",
        "empty": False,
        "nullable": True,
    },
    "tests": {
        "excludes": "réponse",
        "required": True,
        "type": "list",
        "empty": False,
        "schema": {
            "required": True,
            "type": "dict",
            "schema": {
                "nom": {"required": False, "type": "string"},
                "validation": {
                    "required": True,
                    "type": "string",
                    "empty": False,
                    "nullable": False,
                },
                "sortie": {
                    "required": True,
                    "type": ["string", "integer"],
                    "nullable": False,
                },
                "utilisateur": {
                    "required": False,
                    "type": "string",
                    "regex": "^[a-z][-a-z0-9_]*$",
                    "nullable": False,
                },
                "rétroactions": {
                    "required": False,
                    "type": "dict",
                    "schema": "rétroactions",
                },
            },
        },
    },
    "réponse": {
        "excludes": "tests",
        "required": True,
        "type": "string",
        "empty": False,
        "nullable": False,
    },
    "utilisateur": {
        "required": False,
        "type": "string",
        "regex": "^[a-z][-a-z0-9_]*$",
        "nullable": False,
    },
    "init": {
        "required": False,
        "type": "string",
        "empty": False,
        "nullable": False,
    },
}
