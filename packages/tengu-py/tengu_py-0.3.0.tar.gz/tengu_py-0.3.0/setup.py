# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tengu']

package_data = \
{'': ['*']}

install_requires = \
['dataclasses-json>=0.5.7,<0.6.0',
 'datargs>=0.11.0,<0.12.0',
 'gql[requests]>=3.4.0,<4.0.0',
 'rdkit-pypi>=2022.9.5,<2023.0.0']

setup_kwargs = {
    'name': 'tengu-py',
    'version': '0.3.0',
    'description': 'Python SDK for interacting with the QDX Tengu API',
    'long_description': '# Tengu-py: Python SDK for the QDX Tengu API\n\nThis package exposes a simple provider and CLI for the different tools exposed by the QDX Tengu GraphQL API.\n\n## Usage\n\n### As a library\n\n``` python\nimport json\nfrom pathlib import Path\n\nimport tengu\n\nTOKEN = "your qdx access token"\n\n# get our client to talk with the API\nclient = tengu.Provider(access_token=TOKEN)\n\n# get modules that can be run\nclient.modules()\n\n## running convert\n\n# path to protein pdb with correct charges and protonation\nprotein_pdb = Path("./examples/4w9f_prepared_protein.pdb")\n\n# get base64 encoded data\n\nfile_arg = provider.upload_arg(protein_pdb)\n\nres = client.run("github:talo/tengu-prelude/f8e2e55d9bd428aa7f2bbe3f87c24775fa592b10#convert", [ \n{ "value": "PDB" }, file_arg\n])\n\n// res contains "id" - the instance id; and "outs" - the ids of the return values \n\n// we can pass arguments by "id" reference or by value literal\n\nclient.run("github:talo/tengu-prelude/f8e2e55d9bd428aa7f2bbe3f87c24775fa592b10#pick_conformer", [ \n{ "id": res["outs"][0]["id"] }, { "value": 1 }\n])\n\nclient.poll_module_instance(id) \n// status, progress, logs, outs - out values will be null until module_instance is done\n```\n\n## Sample QP Run\n\n``` python\nfrag_keywords = {\n    "dimer_cutoff": 25,\n    "dimer_mp2_cutoff": 25,\n    "fragmentation_level": 2,\n    "method": "MBE",\n    "monomer_cutoff": 30,\n    "monomer_mp2_cutoff": 30,\n    "ngpus_per_node": 4,\n    "reference_fragment": 293,\n    "trimer_cutoff": 10,\n    "trimer_mp2_cutoff": 10,\n    "lattice_energy_calc": True,\n}\n\nscf_keywords = {\n    "convergence_metric": "diis",\n    "dynamic_screening_threshold_exp": 10,\n    "ndiis": 8,\n    "niter": 40,\n    "scf_conv": 0.000001,\n}\n\ndefault_model = {"method": "RIMP2", "basis": "cc-pVDZ", "aux_basis": "cc-pVDZ-RIFIT", "frag_enabled": True}\n\nqp_instances = client.qp_run(\n    "github:talo/tengu-prelude/0986e4b23780d5e976e7938dc02a949185090fa1#qp_gen_inputs",\n    "github:talo/tengu-prelude/0986e4b23780d5e976e7938dc02a949185090fa1#hermes_energy",\n    "github:talo/tengu-prelude/0986e4b23780d5e976e7938dc02a949185090fa1#qp_collate",\n    provider.upload_arg(Path("some.pdb")),\n    provider.upload_arg(Path("some.gro")),\n    provider.upload_arg(Path("some.sdf")),\n    Arg(None, "sdf"),\n    Arg(None, "MOL"),\n    Arg(\n        None,\n        default_model,\n    ),\n    Arg(None, {"frag": frag_keywords, "scf": scf_keywords}),\n    Arg(\n        None,\n        [\n            ("GLY", 993),\n            ("ASP", 994),\n            ("VAL", 863),\n            ("LYS", 882),\n            ("TYR", 931),\n            ("GLY", 935),\n            ("VAL", 911),\n            ("GLU", 930),\n            ("ALA", 880),\n            ("LEU", 983),\n            ("PRO", 933),\n            ("LEU", 855),\n            ("MET", 929),\n            ("SER", 936),\n            ("LEU", 932),\n        ],\n    ),\n    "GADI",\n    {"walltime": 420},\n    autopoll = (10, 100) # optionally configure polling to wait on the final instance, \n                         # and clean up if any of the prior instances fails\n)\n\n# if you set autpoll, you will get the results of the qp_collate instance,\n# otherwise you will get an array with all the spawned instances, and have to poll manually\nclient.poll_module_instance(qp_collate_instance[2]["id"]) \n```\n',
    'author': 'Ryan Swart',
    'author_email': 'ryan@talosystems.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
