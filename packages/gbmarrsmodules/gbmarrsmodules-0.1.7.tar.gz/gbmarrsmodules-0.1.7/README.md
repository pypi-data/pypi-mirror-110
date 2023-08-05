![Logo](./assets/GB-small-logo.png)   

## GB Python Modules

This repository contains the python modules that have been developed by GB to facilitate our internal scripting and data standardisation.   

Please see the individual sections below for their definitions.

#### common.py

This contains modules that provide the standardised directory paths for a versioned dataset (e.g. PDB for 2021.1) on MARRS workspace. 
This was developed for the gb-marrs user.
There are 4 possible modules, one for each directory type:
 - download
 - work
 - rdf
 - sql
 
This also contains standardised rdf/sparql PREFIXES for some MARRS graphs. 
This set of Graph PREFIXES is incomplete and will be consolidated to one place in the future.

e.g.
 - CHEMBL_DATA = Namespace ("http://generalbioinformatics.com/data/chembl#")
 - CHEMBL_VOC = Namespace ("http://generalbioinformatics.com/ontologies/chembl#")

---------

#### miriamRegex.py
Contains a python dictionary of identifiers.org regular expressions to validate public ids. 
Note: We sometimes apply stronger standards than identifiers.org - for example on case sensitivity. 
These bespoke changes are documented in this module.

e.g. miriamPattern["pdb"] = "\^[0-9][A-Z0-9]{3}$" # changed from \^[0-9][A-Za-z0-9]{3}$, must be caps for integration

This requires regular updates to maintain concordance with the public repository.

--------------

#### namespaces.py
This is a set of shorthands for RDF namespaces for both public datasets and internal datasets.

e.g.
 - idTaxonomy = Namespace("http://identifiers.org/taxonomy/")
 - GBID_CPSD_GENE = Namespace("http://generalbioinformatics.com/identifiers/cpsd/gene/")

-----------------

#### project_graph_modules.py

 - getNamespace (*needs renaming*): This returns a full identifiers.org URI for an Ensembl id given just the base ID as input
 - pdbDirect: (*needs futher description as it does more than currently described*) return direct hit from pdb
 - getTaxon: return the scientific name for a complete gene identifier uri
 - ensemblCheckFailure: For debug purposes - If an ID is not returning values from the Ensembl API, this returns the reason why.
 - golistDm: return list of Dm genes annotated with GO from named list of GOs
 - peptideExtraction (*needs renaming*): extracts all ensembl peptides for an Ensembl taxon that are found in cpsd/ensembl
 - dartGen: Checks is a single human Ensembl gene is in the Dartable list
 - dartable_genome_check: *needs description writing*
 - annotatePDB: *needs clearer description writing*
 - psql_query: connect to and query MARRS PSQL
 - getOrths_ensembl: return Ensembl orthologs from MARRS PSQL for an input list of Ensembl genes and a target cpsd taxon id. 
    Will NOT return paralogs
 - biomartwget: function to convert a list of ids from a biomart query into a set of data for fungal lead gene
 - remove_namespace: remove the namespace from a URI to leave the base ID.
 - check_graphql_config: Submits a simple graphql request to validate that the graphql server
    is up and running and that the configuration is valid.
 - get_graphql_template: Returns a string object containing the templated graphql query.
    Using the input list of identifiers a graphql template is filled in.
 - run_graphql_query: *needs decscription - specifically around authentication*
 - recursive_key_count: Yields the length of all lists in a nested dictionary
    type structure.
 - check_graphql_json: Checks if there could be more results available than the supplied limit
 - flatten_json: Returns a list of dictionaries. This function will recursively
    search through a nested dictionary object flattening out the results
    so that they can be converted into a pandas dataframe.
 - getOrths: retreive homologs from ceres for Ensembl genes and a target species taxon id.
 - pchemblactive: filters a list of genes to have an entry in ChEMBL
    with a pChembl >= 6 
 - df2file: prints a dataframe to a tab seperated text file in folder of choice.


------------

#### rdfstream.py
This module coordinates the writing of an RDF file in nt format. 
It works via a tmp file until complete and will gzip the final output.

This contains basic Quality control functions and will soon be deprecated for 
a module with more vigorous testing functions.

Example usage:

`from rdfstream import NtWriter
with NtWriter (rdf_outfile) as nt:
    nt.printLiteral(subjectURI, Predicate, "A string"
    nt.printStatement(subjectURI, Predicate, objectURI)`



---------------------

#### rdfWriterValidated.py

WIP: this is currently not deployed but will soon be the default.

*This module coordinates the writing of an RDF file in nt format. 
It works via a tmp file until complete and will gzip the final output.*

*By using this module, we are enforcing essential Quality checks. 
In order to achieve this, there are non-optional input variables (outlined below)*

---------------------

#### util.py
Contains functions for the following tasks:
 - checking all URIs are RDF safe and valid
 - checking RDF classes and predicates are defined in shapes
 - checking URI identifiers match the identifiers.org regex for the assigned namespace

-------

### Contributers

See the CODEOWNERS file for a list of code owners who can review and accept a PR.


### Maintainers

- Accept a PR (merge request)
- Pull down the merged code
- Change the version number in setup.py
- Update the CHANGELOG with details of changes
- Tag the commit:
  ```git tag v1.1.4```
- Push these changes back to the repo with a commit message similar to the following:
  ```git commit -m "feat(1.1.4): added FLG method helpers"```
- Add the tagged commmit to git:
  ```git push origin v1.1.4```
- In gitlab CICD/Pipelines find the new commit (should be at the top) and click the play button to push the new version to PYPY. If you go to CICD/Jobs you should find a 'PASSED' status. If you click on this, in the terminal output at the bottom you will find a link to the new version on PYPY:
  ``` View at: https://pypi.org/project/gbmarrsmodules/0.1.5/ Job suceeded```

